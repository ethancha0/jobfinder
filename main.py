from fastapi import FastAPI

from clients.greenhouse import router as greenhouse_router

app = FastAPI()

app.include_router(greenhouse_router, prefix="/greenhouse", tags=["greenhouse"])


@app.get("/")
def read_root():
    return {"Hello": "World"}



