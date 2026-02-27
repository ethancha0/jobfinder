import os
from html import escape
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import resend

router = APIRouter()


class JobEmailItem(BaseModel):
    greenhouse_job_id: int
    title: str
    url: str
    company: str


@router.post("/")
def send_mail():
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="RESEND_API_KEY not configured")

    resend.api_key = api_key

    to_emails = [e.strip() for e in os.getenv("ALERT_EMAIL_TO", "").split(",") if e.strip()]
    if not to_emails:
        raise HTTPException(status_code=500, detail="ALERT_EMAIL_TO not configured")
    from_email = os.getenv("ALERT_EMAIL_FROM", "Rilakkuma <rilakkuma@ethansjobfinder.com>")

    params = {
        "from": from_email,
        "to": to_emails,
        "subject": "Ethan's Email Bot",
        "html": "<strong>YAYY IT WORKS daisuke da yo</strong>",
    }

    return resend.Emails.send(params)


@router.post("/send-jobs")
def send_jobs_email(jobs: list[JobEmailItem]) -> dict:
    if not jobs:
        raise HTTPException(status_code=400, detail="jobs payload is empty")

    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="RESEND_API_KEY not configured")
    
    resend.api_key = api_key

    to_emails = [e.strip() for e in os.getenv("ALERT_EMAIL_TO", "").split(",") if e.strip()]
    if not to_emails:
        raise HTTPException(status_code=500, detail="ALERT_EMAIL_TO not configured")
    from_email = os.getenv("ALERT_EMAIL_FROM", "Rilakkuma <rilakkuma@ethansjobfinder.com>")

    job_items_html = "".join(
        (
            f"<li><strong>{escape(job.title)}</strong> at {escape(job.company)}"
            f" - <a href=\"{escape(job.url, quote=True)}\">View job</a></li>"
        )
        for job in jobs
    )
    html_body = (
        "<h2>New job matches</h2>"
        f"<p>Found {len(jobs)} new job(s).</p>"
        f"<ul>{job_items_html}</ul>"
    )

    params = {
        "from": from_email,
        "to": to_emails,
        "subject": "Ethan's Job List",
        "html": html_body,
    }

    return resend.Emails.send(params)


    