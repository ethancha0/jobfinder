from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import threading

from clients.greenhouse import router as greenhouse_router
from routers.companies import router as company_router

from db.database import engine
from db.models import Base
from db.seed import seed_companies
from db.seed_jobs import seed_recent_jobs

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
            days = int(os.getenv("SEED_JOBS_DAYS", "14"))
        except ValueError:
            days = 14

        threading.Thread(
            target=seed_recent_jobs,
            kwargs={"days": days},
            daemon=True,
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

@app.get("/")
def read_root():
    return {"Hello": "World"}



