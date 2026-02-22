from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from clients.greenhouse import router as greenhouse_router
from routers.companies import router as company_router

from db.database import engine
from db.models import Base

Base.metadata.create_all(bind=engine) # autocreates table on startup

app = FastAPI()

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



