from app.database.repositories.merchant_location_repository import MerchantLocationRepository
from app.database.repositories.user_repository import UserRepository
from app.models.merchant_model import MerchantLocationModel
from app.schemas.merchant_schema import BulkCreateRestaurantLocation, MerchantLocationCreate
from fastapi import HTTPException

from app.services.external.google_maps_service import GoogleMapsService


class MerchantService:
    def __init__(
        self,
        user_repository: UserRepository,
        merchant_location_repository: MerchantLocationRepository,
        google_maps_service: GoogleMapsService,
    ):
        self.user_repository = user_repository
        self.merchant_location_repository = merchant_location_repository
        self.google_maps_service = google_maps_service
        pass

    def validate_merchant_brand(self, user_id: int):
        brand = self.user_repository.get_user_by_id(user_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Merchant brand not found")

    def create_merchant_location(self, merchant_location_create: MerchantLocationCreate):
        return self.merchant_location_repository.create_merchant_location(
            MerchantLocationModel(
                name=merchant_location_create.name,
                address=merchant_location_create.address,
                latitude=merchant_location_create.latitude,
                longitude=merchant_location_create.longitude,
                user_id=merchant_location_create.user_id
            )
        )

    def create_bulk_merchant_location(self, merchant_location_create: BulkCreateRestaurantLocation):
        self.validate_merchant_brand(merchant_location_create.user_id)
        merchants = self.google_maps_service.search_places_by_query(merchant_location_create.query)

        for merchant in merchants:
            self.create_merchant_location(
                MerchantLocationCreate(
                    name=merchant.name,
                    address=merchant.address,
                    latitude=merchant.latitude,
                    longitude=merchant.longitude,
                    user_id=merchant_location_create.user_id
                )
            )
