from typing import Dict

from app.models import (
    Donation,
    DonationRequest,
    Organization,
    Restaurant,
)


organizations: Dict[str, Organization] = {}

restaurants: Dict[str, Restaurant] = {}

donations: Dict[str, Donation] = {}

donation_requests: Dict[str, DonationRequest] = {}