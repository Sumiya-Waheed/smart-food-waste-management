from datetime import datetime, timedelta, timezone

from app.data.store import organizations, restaurants
from app.models import Organization, Restaurant
from app.schemas.donation import DonationCreate
from app.schemas.donation_request import DonationRequestCreate
from app.services.donation_service import DonationService
from app.services.donation_request_service import DonationRequestService


now = datetime.now(timezone.utc)

org = Organization(
    id="ORG-COLLECTED-TEST",
    organization_name="Collected Test Center",
    contact_person_name="Test Person",
    email="collected-org@test.com",
    phone="03001234567",
    organization_type="NGO",
    address="Test Address",
    city="Karachi",
    food_collection_capacity=100,
    food_preferences=["rice"],
    operating_availability="09:00-18:00",
)
organizations[org.id] = org


restaurant = Restaurant(
    id="REST-COLLECTED-TEST",
    business_name="Collected Test Cafeteria",
    contact_person_name="Test Donor",
    email="collected-donor@test.com",
    phone="03001234568",
    business_type="Cafeteria",
    address="Test Pickup Address",
    city="Karachi",
    operating_availability="09:00-18:00",
)
restaurants[restaurant.id] = restaurant


donation = DonationService.create_donation(
    DonationCreate(
        donor_id=restaurant.id,
        food_name="Vegetable Rice",
        food_category="Meals",
        quantity=30,
        unit="meals",
        preparation_datetime=now,
        safe_consumption_deadline=now + timedelta(hours=6),
        pickup_address="Test Pickup Address",
        storage_instructions="Keep refrigerated",
    )
)


request = DonationRequestService.create_request(
    DonationRequestCreate(
        donation_id=donation.id,
        organization_id=org.id,
        requested_quantity=30,
        expected_collection_time=now + timedelta(hours=2),
        message="Please arrange pickup",
    )
)


DonationRequestService.accept_request(request.id)

DonationRequestService.confirm_collection(request.id)

collected = DonationRequestService.confirm_collected(request.id)


print("REQUEST STATUS:", collected.status)
print("DONATION STATUS:", donation.status)
print("DONATION REMAINING:", donation.remaining_quantity)

if collected.status == "collected":
    print("REQUEST COLLECTED TRANSITION: PASS")
else:
    print("REQUEST COLLECTED TRANSITION: FAIL")

if donation.status == "collected":
    print("DONATION COLLECTED TRANSITION: PASS")
else:
    print("DONATION COLLECTED TRANSITION: FAIL")