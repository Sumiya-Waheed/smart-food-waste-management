from fastapi import APIRouter, HTTPException

from app.schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
)
from app.services.organization_service import OrganizationService


router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=201,
)
def create_organization(data: OrganizationCreate):
    try:
        return OrganizationService.create_organization(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[OrganizationResponse],
)
def list_organizations():
    return OrganizationService.list_organizations()


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def get_organization(organization_id: str):
    try:
        return OrganizationService.get_organization(
            organization_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.post(
    "/{organization_id}/activate",
    response_model=OrganizationResponse,
)
def activate_organization(organization_id: str):
    try:
        return OrganizationService.activate_organization(
            organization_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.post(
    "/{organization_id}/deactivate",
    response_model=OrganizationResponse,
)
def deactivate_organization(organization_id: str):
    try:
        return OrganizationService.deactivate_organization(
            organization_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )