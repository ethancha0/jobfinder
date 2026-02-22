# this file loads in the companies 

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Company

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_companies(db: Session = Depends(get_db)):
    return db.query(Company).all()

from pydantic import BaseModel

class CompanyCreate(BaseModel):
    name: str
    board_token: str

`@router.post`("/bulk")
def add_companies(companies: list[CompanyCreate], db: Session = Depends(get_db)):
    for company in companies:
        existing = db.query(Company).filter(
            Company.board_token == company.board_token
        ).first()

        if not existing:
            db.add(
                Company(
                    name=company.name,
                    board_token=company.board_token
                )
            )
    db.commit()
    return {"status":"ok"}
    return {"status":"ok"}