# this file loads in the companies 

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID

from db.database import SessionLocal
from db.models import Company

router = APIRouter()

class CompanySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    board_token: str
    active: bool
    created_at: datetime | None = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[CompanySchema])
def get_companies(db: Session = Depends(get_db)):
    return db.query(Company).all()

class CompanyCreate(BaseModel):
    name: str
    board_token: str

@router.post("/bulk")
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
