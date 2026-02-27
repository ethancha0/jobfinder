import os
from fastapi import APIRouter, HTTPException
import resend

router = APIRouter()

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