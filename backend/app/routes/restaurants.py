from fastapi import APIRouter, HTTPException

from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse,
)
from app.services.restaurant_service import RestaurantService


router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"],
)


@router.post(
    "",
    response_model=RestaurantResponse,
    status_code=201,
)
def create_restaurant(data: RestaurantCreate):
    try:
        return RestaurantService.create_restaurant(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[RestaurantResponse],
)
def list_restaurants():
    return RestaurantService.list_restaurants()


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def get_restaurant(restaurant_id: str):
    try:
        return RestaurantService.get_restaurant(
            restaurant_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.post(
    "/{restaurant_id}/activate",
    response_model=RestaurantResponse,
)
def activate_restaurant(restaurant_id: str):
    try:
        return RestaurantService.activate_restaurant(
            restaurant_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.post(
    "/{restaurant_id}/deactivate",
    response_model=RestaurantResponse,
)
def deactivate_restaurant(restaurant_id: str):
    try:
        return RestaurantService.deactivate_restaurant(
            restaurant_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )