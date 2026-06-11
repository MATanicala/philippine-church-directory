from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ChurchBase(BaseModel):
    name: str = Field(..., example="San Agustin Church")
    address: str = Field(..., example="General Luna St")
    city: str = Field(..., example="Intramuros, Manila")
    province: str = Field(..., example="Metro Manila")
    contact_number: Optional[str] = Field(None, example="+63 2 8527 2746")
    description: Optional[str] = Field(None, example="A historic Roman Catholic church.")

class ChurchCreate(ChurchBase):
    pass

class ChurchResponse(ChurchBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
