from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Donation(BaseModel):
    id: str

    donor_id: str
    food_name: str
    food_category: str

    quantity: float = Field(gt=0)
    unit: str

    preparation_datetime: datetime
    safe_consumption_deadline: datetime

    pickup_address: str
    storage_instructions: str

    dietary_info: Optional[str] = None
    description: Optional[str] = None

    status: str = "available"

    remaining_quantity: float = Field(gt=0)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)