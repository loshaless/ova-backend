from app.database.repositories.merchant_location_repository import MerchantLocationRepository
from app.database.repositories.user_repository import UserRepository
from app.models.merchant_model import MerchantLocationModel
from app.schemas.merchant_schema import BulkCreateRestaurantLocation, MerchantLocationCreate
from fastapi import HTTPException

from app.services.external.dify_service import DifyService
from app.services.external.google_maps_service import GoogleMapsService


class MerchantService:
    def __init__(
        self,
        user_repository: UserRepository,
        merchant_location_repository: MerchantLocationRepository,
        google_maps_service: GoogleMapsService,
        dify_service: DifyService
    ):
        self.user_repository = user_repository
        self.merchant_location_repository = merchant_location_repository
        self.google_maps_service = google_maps_service
        self.dify_service = dify_service

    def validate_merchant_brand(self, user_id: int):
        brand = self.user_repository.get_user_by_id(user_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Merchant brand not found")

    def create_merchant_location(self, merchant_location_create: MerchantLocationCreate):
        try:
            self.merchant_location_repository.create_merchant_location(
                MerchantLocationModel(
                    name=merchant_location_create.name,
                    address=merchant_location_create.address,
                    latitude=merchant_location_create.latitude,
                    longitude=merchant_location_create.longitude,
                    user_id=merchant_location_create.user_id
                )
            )
        except Exception as e:
            print(e)

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

    async def get_distinct_nearby_merchant_locations_by_lat_long(self, latitude: float, longitude: float, max_distance: float):
       # list_of_merchant_in_tuple = self.merchant_location_repository.get_distinct_nearby_merchant_locations_by_lat_long(latitude, longitude, max_distance)
       # for merchant in list_of_merchant_in_tuple:
       #     merchant_name = merchant[0]
       #     print(merchant_name)
       result = await self.dify_service.retrieve(
           dataset_id="3fbd2244-751d-4a8f-adc4-5623375151fc",
           query="apa saja produk cimb niaga?"
       )
       print(result)
