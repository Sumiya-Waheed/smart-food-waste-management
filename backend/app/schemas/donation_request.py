from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationRequestCreate(BaseModel):
    donation_id: str = Field(min_length=1)
    organization_id: str = Field(min_length=1)

    requested_quantity: float = Field(gt=0)

    expected_collection_time: datetime

    message: Optional[str] = Field(
        default=None,
        max_length=1000,
    )


class DonationRequestResponse(BaseModel):
    id: str

    donation_id: str
    organization_id: str
    donor_id: str

    requested_quantity: float
    expected_collection_time: datetime

    message: Optional[str]

    status: str

    rejection_reason: Optional[str]
    cancellation_reason: Optional[str]

    created_at: datetime
    updated_at: datetime