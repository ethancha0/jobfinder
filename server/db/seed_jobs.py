import requests
from datetime import datetime, timedelta, timezone

from sqlalchemy import text
from sqlalchemy.orm import Session

from db.database import Base, SessionLocal, engine
from db.models import Company, Jobs

from notifications.emails import JobEmailItem, send_jobs_email_notification


GREENHOUSE_TIMEOUT = (5, 20)  # (connect, read)


def parse_first_published(value: str | None) -> datetime | None:
    """
    Greenhouse often returns ISO strings like '2026-02-22T17:03:11.123Z'
    or '2026-02-22T17:03:11Z'. Convert to aware datetime (UTC).
    """
    if not value:
        return None
    try:
        s = value.replace("Z", "+00:00")
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def seed_recent_jobs(days: int = 14) -> dict:
    # Ensure tables exist when running the seeder directly
    Base.metadata.create_all(bind=engine)
    # Keep schema in sync for local dev (create_all doesn't migrate types)
    try:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE jobs ALTER COLUMN greenhouse_job_id TYPE BIGINT"))
            conn.execute(text("ALTER TABLE jobs ADD COLUMN IF NOT EXISTS content TEXT"))
            conn.execute(text("ALTER TABLE jobs ADD COLUMN IF NOT EXISTS emailed BOOLEAN DEFAULT FALSE"))
    except Exception:
        # Ignore if table/column doesn't exist yet or DB doesn't support it
        pass

    db: Session = SessionLocal()
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        companies = (
            db.query(Company)
            .filter(Company.active.is_(True))
            .all()
        )

        upserted = 0
        skipped_old = 0
        failures: list[dict] = []
        jobs_to_email = []
        jobs_emailed = 0

        for company in companies:
            
            url = f"https://boards-api.greenhouse.io/v1/boards/{company.board_token}/jobs?content=true"

            try:
                res = requests.get(url, timeout=GREENHOUSE_TIMEOUT)
                if res.status_code != 200:
                    failures.append({
                        "company": company.name,
                        "board_token": company.board_token,
                        "status": res.status_code,
                    })
                    continue

                payload = res.json()
                gh_jobs = payload.get("jobs", [])

                for gh_job in gh_jobs:
                    gh_id = gh_job.get("id")
                    title = gh_job.get("title") or ""
                    absolute_url = gh_job.get("absolute_url") or ""
                    first_published = parse_first_published(gh_job.get("first_published"))
                    content = gh_job.get("content")

                    if gh_id is None:
                        continue

                    # Only keep jobs posted in last N days
                    if not first_published or first_published < cutoff:
                        skipped_old += 1
                        continue

                    # Optional: if Greenhouse includes a status field
                    # status = (gh_job.get("status") or "").lower()
                    # if status and status != "open":
                    #     continue

                    location_obj = gh_job.get("location") or {}
                    location_name = location_obj.get("name") if isinstance(location_obj, dict) else str(location_obj)
                    location_name = location_name or ""

                    # UPSERT: find existing by (company_id, greenhouse_job_id)
                    existing = (
                        db.query(Jobs)
                        .filter(Jobs.company_id == company.id, Jobs.greenhouse_job_id == gh_id)
                        .one_or_none()
                    )

                    if existing:
                        # Update fields (keep fresh)
                        existing.title = title
                        existing.location_name = location_name
                        existing.published_at = first_published
                        existing.url = absolute_url
                        existing.is_active = True
                        existing.content = content
                        job_record = existing
                    else:
                        job_record = Jobs(
                            company_id=company.id,
                            greenhouse_job_id=gh_id,
                            title=title,
                            location_name=location_name,
                            published_at=first_published,
                            url=absolute_url,
                            is_active=True,
                            content=content,
                            emailed=False,
                        )
                        db.add(job_record)

                    
                    if not job_record.emailed:
                        jobs_to_email.append({
                            "company_id": company.id,
                            "company": company.name,
                            "greenhouse_job_id": gh_id,
                            "title": title,
                            "url": absolute_url,
                        })
                        


                    upserted += 1

                db.commit()

            except requests.exceptions.Timeout:
                failures.append({
                    "company": company.name,
                    "board_token": company.board_token,
                    "error": "timeout",
                })
                continue
            except requests.exceptions.RequestException as e:
                failures.append({
                    "company": company.name,
                    "board_token": company.board_token,
                    "error": str(e),
                })
                continue


        if jobs_to_email:
            try:
                payload = [
                    JobEmailItem(
                        greenhouse_job_id=job["greenhouse_job_id"],
                        title=job["title"],
                        url=job["url"],
                        company=job["company"],
                    )
                    for job in jobs_to_email
                ]
                send_jobs_email_notification(payload)

                for job in jobs_to_email:
                    (
                        db.query(Jobs)
                        .filter(
                            Jobs.company_id == job["company_id"],
                            Jobs.greenhouse_job_id == job["greenhouse_job_id"],
                        )
                        .update({Jobs.emailed: True}, synchronize_session=False)
                    )
                db.commit()
                jobs_emailed = len(jobs_to_email)

            except Exception as e:
                db.rollback()
                failures.append({
                    "error": f"email_send_failed: {str(e)}",
                })



        return {
            "companies_checked": len(companies),
            "jobs_to_email": len(jobs_to_email),
            "jobs_emailed": jobs_emailed,
            "upserted_recent_jobs": upserted,
            "skipped_old_jobs": skipped_old,
            "failures": failures[:25],
        }

    finally:
        db.close()


if __name__ == "__main__":
    result = seed_recent_jobs(days=14)
    print(result)