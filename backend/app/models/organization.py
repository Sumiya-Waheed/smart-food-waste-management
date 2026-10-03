from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


class Organization(BaseModel):
    id: str
    organization_name: str
    contact_person_name: str
    email: str
    phone: str
    organization_type: str
    address: str
    city: str

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    food_collection_capacity: float = Field(gt=0)
    food_preferences: List[str] = Field(default_factory=list)

    operating_availability: str

    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)