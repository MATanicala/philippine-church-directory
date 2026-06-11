from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.schemas.church_schema import ChurchResponse
from app.models.church import Church

router = APIRouter(
    prefix="/churches",
    tags=["Churches"]
)

# Dependency to yield a database session per request and close it after
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ChurchResponse])
def read_churches(db: Session = Depends(get_db)):
    """
    Retrieve all registered churches from the PostgreSQL database.
    """
    churches = db.query(Church).all()
    return churches