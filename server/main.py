from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from clients.greenhouse import router as greenhouse_router
from routers.companies import router as company_router

from db.database import engine
from db.models import Base
from db.seed import seed_companies

Base.metadata.create_all(bind=engine) # autocreates table on startup

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Safe to run on every startup: the seeder only inserts missing board_tokens.
    seed_companies()
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



