#Purpose: Create church, Read church, Update church, Delete church, all database operations go here.

from sqlalchemy.orm import Session
from app.models.church import Church
from app.schemas.church_schema import ChurchCreate

class ChurchRepository:
    @staticmethod
    def create(db: Session, church_data: ChurchCreate) -> Church:
        """Saves a new church record to PostgreSQL."""
        db_church = Church(
            name=church_data.name,
            address=church_data.address,
            city=church_data.city,
            province=church_data.province,
            contact_number=church_data.contact_number,
        )
        db.add(db_church)
        db.commit()
        db.refresh(db_church)
        return db_church

    @staticmethod
    def get_all(db: Session) -> list[Church]:
        """Retrieves all church records."""
        return db.query(Church).all()
    
    @staticmethod
    def get_by_id(db: Session, church_id: int) -> Church | None:
        """Retrieves a single church record by its ID. Returns None if not found."""
        return db.query(Church).filter(Church.id == church_id).first()