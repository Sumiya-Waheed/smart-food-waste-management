from datetime import datetime, timedelta, timezone 
 
from app.data.store import organizations, restaurants 
from app.models import Organization, Restaurant 
from app.schemas.donation import DonationCreate 
from app.schemas.donation_request import DonationRequestCreate 
from app.services.donation_service import DonationService 
from app.services.donation_request_service import DonationRequestService 
 
 
now = datetime.now(timezone.utc) 
 
 
org = Organization( 
    id="ORG-REJECT-TEST", 
    organization_name="Reject Test Center", 
    contact_person_name="Test Person", 
    email="reject-org@test.com", 
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
    id="REST-REJECT-TEST", 
    business_name="Reject Test Cafeteria", 
    contact_person_name="Test Donor", 
    email="reject-donor@test.com", 
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
        requested_quantity=20, 
        expected_collection_time=now + timedelta(hours=2), 
        message="Please arrange pickup", 
    ) 
) 
 
 
rejected = DonationRequestService.reject_request( 
    request.id, 
    "Pickup time is not available.", 
) 
 
 
print("REQUEST STATUS:", rejected.status) 
print("REJECTION REASON:", rejected.rejection_reason) 
print("DONATION REMAINING:", donation.remaining_quantity) 
print("DONATION STATUS:", donation.status)