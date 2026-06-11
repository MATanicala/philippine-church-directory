from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.schemas.church_schema import ChurchResponse, ChurchCreate
from app.models.church import Church

router = APIRouter(
    prefix="/churches",
    tags=["Churches"]
)

# Dependency to yield a database session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. READ ALL (GET /churches)
@router.get("/", response_model=List[ChurchResponse])
def read_churches(db: Session = Depends(get_db)):
    """Retrieve all churches from the database."""
    return db.query(Church).all()

# 2. CREATE (POST /churches)
@router.post("/", response_model=ChurchResponse, status_code=status.HTTP_201_CREATED)
def create_church(church_data: ChurchCreate, db: Session = Depends(get_db)):
    """Create a new church record in the database."""
    db_church = Church(
        name=church_data.name,
        address=church_data.address,
        city=church_data.city,
        province=church_data.province,
        contact_number=church_data.contact_number
    )
    db.add(db_church)
    db.commit()
    db.refresh(db_church)
    return db_church

# 3. READ SINGLE (GET /churches/{church_id})
@router.get("/{church_id}", response_model=ChurchResponse)
def read_church(church_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific church record by its unique database ID."""
    church = db.query(Church).filter(Church.id == church_id).first()
    if not church:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Church with ID {church_id} not found"
        )
    return church