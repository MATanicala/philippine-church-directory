from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.schemas.church_schema import ChurchResponse, ChurchCreate, ChurchUpdate
from app.models.church import Church

router = APIRouter(
    prefix="/churches",
    tags=["Churches"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET ALL CHURCHES
@router.get("/", response_model=List[ChurchResponse])
def read_churches(db: Session = Depends(get_db)):
    return db.query(Church).all()

# CREATE CHURCH
@router.post("/", response_model=ChurchResponse, status_code=status.HTTP_201_CREATED)
def create_church(church_data: ChurchCreate, db: Session = Depends(get_db)):
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

# GET SINGLE CHURCH
@router.get("/{church_id}", response_model=ChurchResponse)
def read_church(church_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific church record by its unique database ID.
    """
    church = db.query(Church).filter(Church.id == church_id).first()
    if not church:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Church with ID {church_id} not found"
        )
    return church

# UPDATE CHURCH
@router.put("/{church_id}", response_model=ChurchResponse)
def update_church(church_id: int, church_data: ChurchUpdate, db: Session = Depends(get_db)):
    """
    Update an existing church record partially or completely by its unique ID.
    """
    db_church = db.query(Church).filter(Church.id == church_id).first()
    if not db_church:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Church with ID {church_id} not found"
        )
    
    # Convert Pydantic data into a dictionary, skipping fields that were not provided
    update_data = church_data.model_dump(exclude_unset=True)
    
    # Dynamically update only the fields present in the request body
    for key, value in update_data.items():
        setattr(db_church, key, value)
        
    db.commit()
    db.refresh(db_church)
    return db_church

# DELETE CHURCH (The New Endpoint)
@router.delete("/{church_id}", status_code=status.HTTP_200_OK)
def delete_church(church_id: int, db: Session = Depends(get_db)):
    """
    Remove a church record permanently from the database by its unique ID.
    """
    db_church = db.query(Church).filter(Church.id == church_id).first()
    if not db_church:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Church with ID {church_id} not found"
        )
    
    db.delete(db_church)
    db.commit()
    return {"message": "Church deleted successfully"}
