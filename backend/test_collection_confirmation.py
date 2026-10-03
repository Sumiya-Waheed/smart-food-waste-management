from datetime import datetime, timedelta, timezone

from app.data.store import organizations, restaurants
from app.models import Organization, Restaurant
from app.schemas.donation import DonationCreate
from app.schemas.donation_request import DonationRequestCreate
from app.services.donation_service import DonationService
from app.services.donation_request_service import DonationRequestService


now = datetime.now(timezone.utc)


org = Organization(
    id="ORG-COLLECTION-TEST",
    organization_name="Collection Test Center",
    contact_person_name="Test Person",
    email="collection-org@test.com",
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
    id="REST-COLLECTION-TEST",
    business_name="Collection Test Cafeteria",
    contact_person_name="Test Donor",
    email="collection-donor@test.com",
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


accepted = DonationRequestService.accept_request(
    request.id,
)


confirmed = DonationRequestService.confirm_collection(
    request.id,
)


print("REQUEST STATUS:", confirmed.status)
print("DONATION STATUS:", donation.status)
print("DONATION REMAINING:", donation.remaining_quantity)