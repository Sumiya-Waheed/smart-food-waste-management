from fastapi import APIRouter, HTTPException

from app.schemas.donation_request import (
    DonationRequestCreate,
    DonationRequestResponse,
)
from app.services.donation_request_service import (
    DonationRequestService,
)


router = APIRouter(
    prefix="/donation-requests",
    tags=["Donation Requests"],
)


@router.post(
    "",
    response_model=DonationRequestResponse,
    status_code=201,
)
def create_donation_request(
    data: DonationRequestCreate,
):
    try:
        return DonationRequestService.create_request(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "/{request_id}/accept",
    response_model=DonationRequestResponse,
)
def accept_donation_request(request_id: str):
    try:
        return DonationRequestService.accept_request(
            request_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "/{request_id}/reject",
    response_model=DonationRequestResponse,
)
def reject_donation_request(
    request_id: str,
    reason: str,
):
    try:
        return DonationRequestService.reject_request(
            request_id,
            reason,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "/{request_id}/cancel",
    response_model=DonationRequestResponse,
)
def cancel_donation_request(
    request_id: str,
    reason: str,
):
    try:
        return DonationRequestService.cancel_request(
            request_id,
            reason,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "/{request_id}/confirm-collection",
    response_model=DonationRequestResponse,
)
def confirm_collection(request_id: str):
    try:
        return DonationRequestService.confirm_collection(
            request_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "/{request_id}/confirm-collected",
    response_model=DonationRequestResponse,
)
def confirm_collected(request_id: str):
    try:
        return DonationRequestService.confirm_collected(
            request_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "/{request_id}/complete",
    response_model=DonationRequestResponse,
)
def complete_donation_request(request_id: str):
    try:
        return DonationRequestService.confirm_completed(
            request_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )