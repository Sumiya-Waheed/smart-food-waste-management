from datetime import datetime, timedelta, timezone

from app.data.store import organizations, restaurants
from app.models import Organization, Restaurant
from app.schemas.donation import DonationCreate
from app.schemas.donation_request import DonationRequestCreate
from app.services.donation_service import DonationService
from app.services.donation_request_service import DonationRequestService


now = datetime.now(timezone.utc)


# Test organization
org = Organization(
    id="ORG-OVERBOOK-TEST",
    organization_name="Overbooking Test Center",
    contact_person_name="Test Person",
    email="overbook-org@test.com",
    phone="03001234567",
    organization_type="NGO",
    address="Test Address",
    city="Karachi",
    food_collection_capacity=100,
    food_preferences=["rice"],
    operating_availability="09:00-18:00",
)

organizations[org.id] = org


# Test restaurant
restaurant = Restaurant(
    id="REST-OVERBOOK-TEST",
    business_name="Overbooking Test Cafeteria",
    contact_person_name="Test Donor",
    email="overbook-donor@test.com",
    phone="03001234568",
    business_type="Cafeteria",
    address="Test Pickup Address",
    city="Karachi",
    operating_availability="09:00-18:00",
)

restaurants[restaurant.id] = restaurant


# Create 30 meals
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


# First request: 20 meals
request_1 = DonationRequestService.create_request(
    DonationRequestCreate(
        donation_id=donation.id,
        organization_id=org.id,
        requested_quantity=20,
        expected_collection_time=now + timedelta(hours=2),
        message="First request",
    )
)


# Accept first request
DonationRequestService.accept_request(request_1.id)


print("AFTER FIRST ACCEPTANCE:")
print("REMAINING:", donation.remaining_quantity)


# Second request: 15 meals
# Only 10 remain, so this must fail.
try:
    DonationRequestService.create_request(
        DonationRequestCreate(
            donation_id=donation.id,
            organization_id=org.id,
            requested_quantity=15,
            expected_collection_time=now + timedelta(hours=3),
            message="Overbooking test",
        )
    )

    print("OVERBOOKING PROTECTION: FAIL")
    print("ERROR: Request of 15 meals was incorrectly allowed.")

except ValueError as error:
    print("OVERBOOKING PROTECTION: PASS")
    print("ERROR:", error)