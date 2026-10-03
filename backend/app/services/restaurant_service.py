from datetime import datetime, timezone

from app.data.store import restaurants
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate
from app.utils.id_generator import generate_id


class RestaurantService:

    @staticmethod
    def create_restaurant(data: RestaurantCreate) -> Restaurant:
        restaurant = Restaurant(
            id=generate_id("REST"),
            **data.model_dump(),
        )

        restaurants[restaurant.id] = restaurant

        return restaurant

    @staticmethod
    def get_restaurant(restaurant_id: str) -> Restaurant:
        restaurant = restaurants.get(restaurant_id)

        if restaurant is None:
            raise ValueError("Restaurant/cafeteria not found.")

        return restaurant

    @staticmethod
    def list_restaurants() -> list[Restaurant]:
        return list(restaurants.values())

    @staticmethod
    def activate_restaurant(
        restaurant_id: str,
    ) -> Restaurant:
        restaurant = RestaurantService.get_restaurant(restaurant_id)

        restaurant.is_active = True
        restaurant.updated_at = datetime.now(timezone.utc)

        return restaurant

    @staticmethod
    def deactivate_restaurant(
        restaurant_id: str,
    ) -> Restaurant:
        restaurant = RestaurantService.get_restaurant(restaurant_id)

        restaurant.is_active = False
        restaurant.updated_at = datetime.now(timezone.utc)

        return restaurant