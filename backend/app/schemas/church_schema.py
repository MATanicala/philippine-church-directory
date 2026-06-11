from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ChurchBase(BaseModel):
    """
    Shared properties across all schemas.
    Helps avoid repeating code for field definitions.
    """
    name: str = Field(..., example="A-Hill Church of Christ")
    address: str = Field(..., example="98 Parisas St, Camp 7, Baguio City")
    city: str = Field(..., example="Baguio City")
    province: str = Field(..., example="Benguet")
    contact_number: Optional[str] = Field(None, example="+63 2 8527 2746")

class ChurchCreate(ChurchBase):
    """
    Used for incoming POST /churches request bodies.
    Inherits all required fields from ChurchBase.
    """
    pass

class ChurchUpdate(BaseModel):
    """
    Used for PUT /churches/{id} request bodies.
    All fields are completely optional so the user can update partial data.
    """
    name: Optional[str] = Field(None, example="A-Hill Church of Christ")
    address: Optional[str] = Field(None, example="98 Parisas St, Camp 7, Baguio City")
    city: Optional[str] = Field(None, example="Baguio City")
    province: Optional[str] = Field(None, example="Benguet")
    contact_number: Optional[str] = Field(None, example="+63 2 0000 0000")

class ChurchResponse(ChurchBase):
    """
    Used for outgoing database serialization (GET requests).
    Includes system-generated fields like id and created_at.
    """
    id: int
    created_at: datetime

    class Config:
        from_attributes = True