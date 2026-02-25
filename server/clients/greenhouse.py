import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc


from db.database import SessionLocal
from db.models import Company, Jobs

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/queryjobs")
def query_jobs(
    userQuery: str = Query(default="", description="Search query"),
    db: Session = Depends(get_db)
):
    # Normalize DB results to match the shape returned by /alljobs
    # (companies.tsx expects companyName, location.name, published, url).
    rows = (
        db.query(Jobs, Company.name)
        .join(Company, Company.id == Jobs.company_id)
        .filter(Jobs.title.ilike(f"%{userQuery}%"))
        .order_by(desc(Jobs.published_at)) #order by date posted (descending)
        .all()
    )

    parsed_jobs: list[dict] = []
    for job, company_name in rows:
        published = job.published_at.isoformat() if job.published_at else None
        location = {"name": job.location_name} if job.location_name else None
        parsed_jobs.append(
            {
                "title": job.title,
                "companyName": company_name,
                "location": location,
                "published": published,
                "url": job.url,
                "content": job.content,
            }
        )

    return {
        "jobs": parsed_jobs,
        "count": len(parsed_jobs),
    }






@router.get("/alljobs")
def get_all_greenhouse_jobs(db:Session = Depends(get_db)):

    companies = db.query(Company).filter(Company.active.is_(True)).all()

    softwareInternJobs = []
    totalJobsSearched = 0
    totalCompaniesSearched = 0 
    totalJobErrors = 0 # invalid slugs 
    failures: list[dict] = []

    for company in companies:
        url =  f"https://boards-api.greenhouse.io/v1/boards/{company.board_token}/jobs?content=true"
        try:
            response = requests.get(url, timeout=(5,20))
            totalCompaniesSearched += 1

            if response.status_code != 200:
                totalJobErrors += 1
                failures.append(
                    {
                        "companyName": company.name,
                        "boardToken": company.board_token,
                        "status": response.status_code,
                    }
                )
                continue # skip bad jobs for now
            # return {"error": "Failed to fetch every softare intern jobs"}

            allJobs = response.json()
            for job in allJobs.get("jobs", []):
                totalJobsSearched += 1
                if "software" in job["title"].lower() and "intern" in job["title"].lower():
                    softwareInternJobs.append({
                        "title": job["title"],
                        "companyName": company.name,
                        "location": job["location"],    # using [] assumes key must exist, error if missing
                        "published": job.get("first_published"), # using .get() returns none if missing
                        "url": job["absolute_url"]
                    }
                    )
        except requests.exceptions.Timeout:
            print(f"Timeout for {company}")
            failures.append(
                {
                    "companyName": company.name,
                    "boardToken": company.board_token,
                    "error": "timeout",
                }
            )
            continue
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {company}: {e}")
            failures.append(
                {
                    "companyName": company.name,
                    "boardToken": company.board_token,
                    "error": str(e),
                }
            )
            continue

    return {
        "jobs": softwareInternJobs,
        "total": len(softwareInternJobs),
        "totalSearched": totalJobsSearched,
        "companiesSearched": totalCompaniesSearched,
        "jobErrors": totalJobErrors,
        "failures": failures[:25],
    }





@router.get("/{company_slug}")
def get_greenhouse_jobs(company_slug: str):
    url = "https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"
    url = url.format(company_slug=company_slug)
    try:
        response = requests.get(url, timeout=(5,20))
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Greenhouse request timed out")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Greenhouse request failed: {e}")
    
    if response.status_code != 200:
        return {"error": "Failed to fetch jobs"}
    
    try:
        jobs = response.json()
    except ValueError:
        raise HTTPException(status_code=502, detail="Greenhouse returned invalid JSON")

    parsed_jobs = []
    for job in jobs["jobs"]:
        if "software" in job["title"].lower() or "intern" in job["title"].lower():
            parsed_jobs.append({
                "title": job["title"],
                "companyName": job["company_name"],
                "location": job["location"],
                "published": job["first_published"],
                "url": job["absolute_url"]
            })

    return {
        "jobs": parsed_jobs,
        "total": len(parsed_jobs)
    }




