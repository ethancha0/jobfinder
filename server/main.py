from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
import threading

from clients.greenhouse import router as greenhouse_router
from routers.companies import router as company_router
from routers.internal import router as internal_router
from notifications.emails import router as emails_router

from db.database import engine
from db.models import Base
from db.seed import seed_companies
from db.seed_jobs import seed_recent_jobs

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine) # autocreates table on startup

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Safe to run on every startup: the seeder only inserts missing board_tokens.
    seed_companies()

    # Seed jobs on deploy/startup so /greenhouse/queryjobs has data.
    # Run in background to avoid delaying app boot (Render health checks).
    seed_jobs = os.getenv("SEED_JOBS_ON_STARTUP", "1").strip().lower() not in {"0", "false", "no", "off"}
    if seed_jobs:
        try:
            days = int(os.getenv("SEED_JOB_DAYS", "14"))
        except ValueError:
            days = 14

        def _seed_recent_jobs_daemon(*, days: int) -> None:
            try:
                seed_recent_jobs(days=days)
            except Exception:
                # Exceptions in daemon threads can be easy to miss in production logs.
                logger.exception("Daemon thread seed_recent_jobs(days=%s) failed", days)

        threading.Thread(
            target=_seed_recent_jobs_daemon,
            kwargs={"days": days},
            daemon=True,
            name="seed_recent_jobs_daemon",
        ).start()
    yield

app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:3000", "https://jobfinder-two-lake.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(greenhouse_router, prefix="/greenhouse", tags=["greenhouse"])
app.include_router(company_router, prefix="/companies", tags=["companies"])
app.include_router(internal_router, prefix="/internal", tags=["internal"])
app.include_router(emails_router, prefix="/emails", tags=["emails"])

@app.get("/")
def read_root():
    return {"Hello": "World"}



