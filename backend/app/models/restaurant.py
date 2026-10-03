from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Restaurant(BaseModel):
    id: str
    business_name: str
    contact_person_name: str
    email: str
    phone: str
    business_type: str
    address: str
    city: str

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    operating_availability: str

    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)