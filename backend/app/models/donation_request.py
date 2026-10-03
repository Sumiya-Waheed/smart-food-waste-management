from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationRequest(BaseModel):
    id: str

    donation_id: str
    organization_id: str
    donor_id: str

    requested_quantity: float = Field(gt=0)
    expected_collection_time: datetime

    message: Optional[str] = None

    status: str = "pending"

    rejection_reason: Optional[str] = None
    cancellation_reason: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)