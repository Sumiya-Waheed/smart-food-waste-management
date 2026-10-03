from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class DonationCreate(BaseModel):
    donor_id: str = Field(min_length=1)

    food_name: str = Field(min_length=2, max_length=150)
    food_category: str = Field(min_length=2, max_length=100)

    quantity: float = Field(gt=0)
    unit: str = Field(min_length=1, max_length=50)

    preparation_datetime: datetime
    safe_consumption_deadline: datetime

    pickup_address: str = Field(min_length=5, max_length=300)
    storage_instructions: str = Field(min_length=2, max_length=500)

    dietary_info: Optional[str] = Field(default=None, max_length=300)
    description: Optional[str] = Field(default=None, max_length=1000)

    @field_validator("safe_consumption_deadline")
    @classmethod
    def validate_deadline(
        cls,
        deadline: datetime,
    ) -> datetime:
        return deadline


class DonationResponse(BaseModel):
    id: str

    donor_id: str

    food_name: str
    food_category: str

    quantity: float
    unit: str

    preparation_datetime: datetime
    safe_consumption_deadline: datetime

    pickup_address: str
    storage_instructions: str

    dietary_info: Optional[str]
    description: Optional[str]

    status: str
    remaining_quantity: float

    created_at: datetime
    updated_at: datetime