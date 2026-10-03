from fastapi import APIRouter, HTTPException

from app.schemas.donation import DonationCreate, DonationResponse
from app.services.donation_service import DonationService


router = APIRouter(
    prefix="/donations",
    tags=["Donations"],
)


@router.post(
    "",
    response_model=DonationResponse,
    status_code=201,
)
def create_donation(data: DonationCreate):
    try:
        return DonationService.create_donation(data)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/{donation_id}",
    response_model=DonationResponse,
)
def get_donation(donation_id: str):
    try:
        return DonationService.get_donation(donation_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[DonationResponse],
)
def list_donations():
    return DonationService.list_donations()


@router.post(
    "/{donation_id}/cancel",
    response_model=DonationResponse,
)
def cancel_donation(
    donation_id: str,
    reason: str,
):
    try:
        return DonationService.cancel_donation(
            donation_id,
            reason,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )