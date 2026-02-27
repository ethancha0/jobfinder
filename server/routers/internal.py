# called by github. protected endpoint that seeds new jobs every 
# 30 minutes from 9-5pm 

from fastapi import APIRouter, Depends, HTTPException, Header
import os
import hmac
from datetime import datetime
from zoneinfo import ZoneInfo

from db.seed_jobs import seed_recent_jobs

router = APIRouter()

def _require_seed_token(x_seed_token: str | None) -> None:
    expected = os.getenv("SEED_CRON_TOKEN")
    if not expected:
        raise HTTPException(status_code=500, detail="SEED_CRON_TOKEN not configured")
    
    # hmac used to compare the tokens
    if not x_seed_token or not hmac.compare_digest(x_seed_token, expected):
        raise HTTPException(status_code=401, detail = "Unauthorized")
    
def _within_pacific_window() -> bool:
    now = datetime.now(ZoneInfo("America/Los_Angeles"))
    # 9am to 5pm
    return ( 9 <= now.hour < 17)

@router.post("/seed", include_in_schema=False)
def seed_now(x_seed_token: str | None = Header(default=None)):
    _require_seed_token(x_seed_token) #raises errors if needed

    if not _within_pacific_window():
        return {"skipped": True, "reason": "outside_9_to_5_pst"}
    
    days = int(os.getenv("SEED_JOBS_DAYS", "1")) #reads env var. 1 is the fallback
    result = seed_recent_jobs(days=days)
    return {"skipped": False, "result": result}
