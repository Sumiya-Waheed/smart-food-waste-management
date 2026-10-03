from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class RestaurantCreate(BaseModel):
    business_name: str = Field(min_length=2, max_length=150)
    contact_person_name: str = Field(min_length=2, max_length=100)

    email: EmailStr
    phone: str = Field(min_length=7, max_length=20)

    business_type: str = Field(min_length=2, max_length=100)

    address: str = Field(min_length=5, max_length=300)
    city: str = Field(min_length=2, max_length=100)

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    operating_availability: str = Field(min_length=2, max_length=200)


class RestaurantResponse(BaseModel):
    id: str

    business_name: str
    contact_person_name: str

    email: EmailStr
    phone: str

    business_type: str

    address: str
    city: str

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    operating_availability: str

    is_active: bool
    created_at: datetime