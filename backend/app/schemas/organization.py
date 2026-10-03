from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class OrganizationCreate(BaseModel):
    organization_name: str = Field(min_length=2, max_length=150)
    contact_person_name: str = Field(min_length=2, max_length=100)

    email: EmailStr
    phone: str = Field(min_length=7, max_length=20)

    organization_type: str = Field(min_length=2, max_length=100)

    address: str = Field(min_length=5, max_length=300)
    city: str = Field(min_length=2, max_length=100)

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    food_collection_capacity: float = Field(gt=0)
    food_preferences: List[str] = Field(default_factory=list)

    operating_availability: str = Field(min_length=2, max_length=200)


class OrganizationResponse(BaseModel):
    id: str

    organization_name: str
    contact_person_name: str
    email: EmailStr
    phone: str

    organization_type: str

    address: str
    city: str

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    food_collection_capacity: float
    food_preferences: List[str]

    operating_availability: str

    is_active: bool
    created_at: datetime