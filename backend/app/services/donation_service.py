from datetime import datetime, timezone

from app.data.store import donations, restaurants
from app.models.donation import Donation
from app.schemas.donation import DonationCreate
from app.utils.id_generator import generate_id
from app.utils.statuses import (
    DONATION_STATUS_TRANSITIONS,
)
from app.utils.validators import (
    is_donation_expired,
    validate_status_transition,
)


class DonationService:

    @staticmethod
    def create_donation(data: DonationCreate) -> Donation:
        donor = restaurants.get(data.donor_id)

        if donor is None:
            raise ValueError(
                "Donor restaurant/cafeteria not found."
            )

        if not donor.is_active:
            raise ValueError(
                "Donor restaurant/cafeteria is inactive."
            )

        if data.safe_consumption_deadline <= data.preparation_datetime:
            raise ValueError(
                "Safe-consumption deadline must be after preparation time."
            )

        if is_donation_expired(
            data.safe_consumption_deadline
        ):
            raise ValueError(
                "Cannot create a donation with an expired deadline."
            )

        donation_id = generate_id("DON")

        donation = Donation(
            id=donation_id,
            donor_id=data.donor_id,
            food_name=data.food_name,
            food_category=data.food_category,
            quantity=data.quantity,
            unit=data.unit,
            preparation_datetime=data.preparation_datetime,
            safe_consumption_deadline=data.safe_consumption_deadline,
            pickup_address=data.pickup_address,
            storage_instructions=data.storage_instructions,
            dietary_info=data.dietary_info,
            description=data.description,
            status="available",
            remaining_quantity=data.quantity,
        )

        donations[donation_id] = donation

        return donation

    @staticmethod
    def get_donation(
        donation_id: str,
    ) -> Donation:
        donation = donations.get(donation_id)

        if donation is None:
            raise ValueError("Donation not found.")

        DonationService.expire_if_needed(donation)

        return donation

    @staticmethod
    def list_donations(
        include_expired: bool = False,
    ) -> list[Donation]:
        result = []

        for donation in donations.values():
            DonationService.expire_if_needed(donation)

            if (
                not include_expired
                and donation.status == "expired"
            ):
                continue

            result.append(donation)

        return result

    @staticmethod
    def cancel_donation(
        donation_id: str,
        reason: str,
    ) -> Donation:
        donation = DonationService.get_donation(
            donation_id
        )

        if not reason.strip():
            raise ValueError(
                "Cancellation reason is required."
            )

        validate_status_transition(
            donation.status,
            "cancelled",
            DONATION_STATUS_TRANSITIONS,
        )

        donation.status = "cancelled"
        donation.updated_at = datetime.now(timezone.utc)

        return donation

    @staticmethod
    def expire_if_needed(
        donation: Donation,
    ) -> Donation:
        if donation.status in {
            "completed",
            "cancelled",
            "expired",
        }:
            return donation

        if is_donation_expired(
            donation.safe_consumption_deadline
        ):
            validate_status_transition(
                donation.status,
                "expired",
                DONATION_STATUS_TRANSITIONS,
            )

            donation.status = "expired"
            donation.updated_at = datetime.now(timezone.utc)

        return donation