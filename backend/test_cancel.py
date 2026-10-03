from datetime import datetime, timedelta, timezone

from app.data.store import donations, donation_requests, organizations, restaurants
from app.models import DonationRequest
from app.services.donation_request_service import DonationRequestService


# Clean in-memory stores
organizations.clear()
restaurants.clear()
donations.clear()
donation_requests.clear()


# Create test organization
organization_id = "ORG-TEST"

class TestOrganization:
    def __init__(self):
        self.id = organization_id
        self.is_active = True


organizations[organization_id] = TestOrganization()


# Create test donation
class TestDonation:
    def __init__(self):
        self.id = "DON-TEST"
        self.donor_id = "REST-TEST"
        self.status = "available"
        self.remaining_quantity = 30.0
        self.safe_consumption_deadline = (
            datetime.now(timezone.utc) + timedelta(hours=2)
        )
        self.updated_at = datetime.now(timezone.utc)


donations["DON-TEST"] = TestDonation()


# Create pending request directly for this focused test
request = DonationRequest(
    id="REQ-TEST",
    donation_id="DON-TEST",
    organization_id=organization_id,
    donor_id="REST-TEST",
    requested_quantity=20.0,
    expected_collection_time=datetime.now(timezone.utc),
    message="Test cancellation",
    status="pending",
)

donation_requests["REQ-TEST"] = request


# Cancel request
cancelled_request = DonationRequestService.cancel_request(
    "REQ-TEST",
    "Organization no longer needs the food.",
)


print("REQUEST STATUS:", cancelled_request.status)
print("CANCELLATION REASON:", cancelled_request.cancellation_reason)
print("DONATION REMAINING:", donations["DON-TEST"].remaining_quantity)