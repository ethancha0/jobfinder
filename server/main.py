from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from clients.greenhouse import router as greenhouse_router

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


@app.get("/")
def read_root():
    return {"Hello": "World"}



