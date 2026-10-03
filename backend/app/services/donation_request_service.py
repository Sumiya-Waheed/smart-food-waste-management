from datetime import datetime, timezone

from app.data.store import donations, donation_requests, organizations
from app.models import DonationRequest
from app.schemas.donation_request import DonationRequestCreate
from app.utils.id_generator import generate_id
from app.utils.statuses import (
    DONATION_REQUEST_STATUS_TRANSITIONS,
    DONATION_STATUS_TRANSITIONS,
)
from app.utils.validators import (
    is_donation_expired,
    validate_requested_quantity,
    validate_status_transition,
)


class DonationRequestService:
    @staticmethod
    def create_request(
        data: DonationRequestCreate,
    ) -> DonationRequest:
        donation = donations.get(data.donation_id)

        if donation is None:
            raise ValueError("Donation not found.")

        organization = organizations.get(data.organization_id)

        if organization is None:
            raise ValueError("Organization not found.")

        if not organization.is_active:
            raise ValueError("Organization is inactive.")

        if donation.status != "available":
            raise ValueError(
                f"Donation is not available. Current status: "
                f"{donation.status}"
            )

        if is_donation_expired(
            donation.safe_consumption_deadline
        ):
            donation.status = "expired"
            donation.updated_at = datetime.now(timezone.utc)

            raise ValueError(
                "Donation has expired and cannot be requested."
            )

        validate_requested_quantity(
            data.requested_quantity,
            donation.remaining_quantity,
        )

        request_id = generate_id("REQ")

        request = DonationRequest(
            id=request_id,
            donation_id=donation.id,
            organization_id=organization.id,
            donor_id=donation.donor_id,
            requested_quantity=data.requested_quantity,
            expected_collection_time=data.expected_collection_time,
            message=data.message,
            status="pending",
        )

        donation_requests[request_id] = request

        return request

    @staticmethod
    def accept_request(
        request_id: str,
    ) -> DonationRequest:
        request = donation_requests.get(request_id)

        if request is None:
            raise ValueError("Donation request not found.")

        donation = donations.get(request.donation_id)

        if donation is None:
            raise ValueError("Donation not found.")

        if is_donation_expired(
            donation.safe_consumption_deadline
        ):
            donation.status = "expired"
            donation.updated_at = datetime.now(timezone.utc)

            raise ValueError(
                "Donation has expired and cannot be accepted."
            )

        validate_status_transition(
            request.status,
            "accepted",
            DONATION_REQUEST_STATUS_TRANSITIONS,
        )

        if donation.status != "available":
            raise ValueError(
                f"Donation cannot be accepted. Current status: "
                f"{donation.status}"
            )

        validate_requested_quantity(
            request.requested_quantity,
            donation.remaining_quantity,
        )

        donation.remaining_quantity -= request.requested_quantity

        request.status = "accepted"

        if donation.remaining_quantity == 0:
            validate_status_transition(
                donation.status,
                "reserved",
                DONATION_STATUS_TRANSITIONS,
            )

            donation.status = "reserved"

        donation.updated_at = datetime.now(timezone.utc)
        request.updated_at = datetime.now(timezone.utc)

        return request

    @staticmethod
    def reject_request(
        request_id: str,
        reason: str,
    ) -> DonationRequest:
        request = donation_requests.get(request_id)

        if request is None:
            raise ValueError("Donation request not found.")

        if not reason.strip():
            raise ValueError("Rejection reason is required.")

        validate_status_transition(
            request.status,
            "rejected",
            DONATION_REQUEST_STATUS_TRANSITIONS,
        )

        request.status = "rejected"
        request.rejection_reason = reason.strip()
        request.updated_at = datetime.now(timezone.utc)

        return request

    @staticmethod
    def cancel_request(
        request_id: str,
        reason: str,
    ) -> DonationRequest:
        request = donation_requests.get(request_id)

        if request is None:
            raise ValueError("Donation request not found.")

        if not reason.strip():
            raise ValueError("Cancellation reason is required.")

        validate_status_transition(
            request.status,
            "cancelled",
            DONATION_REQUEST_STATUS_TRANSITIONS,
        )

        request.status = "cancelled"
        request.cancellation_reason = reason.strip()
        request.updated_at = datetime.now(timezone.utc)

        return request

    @staticmethod
    def confirm_collection(
        request_id: str,
    ) -> DonationRequest:
        request = donation_requests.get(request_id)

        if request is None:
            raise ValueError("Donation request not found.")

        donation = donations.get(request.donation_id)

        if donation is None:
            raise ValueError("Donation not found.")

        if is_donation_expired(
            donation.safe_consumption_deadline
        ):
            donation.status = "expired"
            donation.updated_at = datetime.now(timezone.utc)

            raise ValueError(
                "Donation has expired and collection cannot be confirmed."
            )

        validate_status_transition(
            request.status,
            "collection_confirmed",
            DONATION_REQUEST_STATUS_TRANSITIONS,
        )

        request.status = "collection_confirmed"
        request.updated_at = datetime.now(timezone.utc)

        if donation.status == "reserved":
            validate_status_transition(
                donation.status,
                "collection_confirmed",
                DONATION_STATUS_TRANSITIONS,
            )

            donation.status = "collection_confirmed"
            donation.updated_at = datetime.now(timezone.utc)

        return request

    @staticmethod
    def confirm_collected(
        request_id: str,
    ) -> DonationRequest:
        request = donation_requests.get(request_id)

        if request is None:
            raise ValueError("Donation request not found.")

        donation = donations.get(request.donation_id)

        if donation is None:
            raise ValueError("Donation not found.")

        validate_status_transition(
            request.status,
            "collected",
            DONATION_REQUEST_STATUS_TRANSITIONS,
        )

        request.status = "collected"
        request.updated_at = datetime.now(timezone.utc)

        if donation.status == "collection_confirmed":
            validate_status_transition(
                donation.status,
                "collected",
                DONATION_STATUS_TRANSITIONS,
            )

            donation.status = "collected"
            donation.updated_at = datetime.now(timezone.utc)

        return request

    @staticmethod
    def confirm_completed(
        request_id: str,
    ) -> DonationRequest:
        request = donation_requests.get(request_id)

        if request is None:
            raise ValueError("Donation request not found.")

        donation = donations.get(request.donation_id)

        if donation is None:
            raise ValueError("Donation not found.")

        validate_status_transition(
            request.status,
            "completed",
            DONATION_REQUEST_STATUS_TRANSITIONS,
        )

        request.status = "completed"
        request.updated_at = datetime.now(timezone.utc)

        if donation.status == "collected":
            validate_status_transition(
                donation.status,
                "completed",
                DONATION_STATUS_TRANSITIONS,
            )

            donation.status = "completed"
            donation.updated_at = datetime.now(timezone.utc)

        return request