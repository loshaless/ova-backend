from app.core.dependencies import get_google_maps_service
from app.database.repositories.merchant_location_repository import MerchantLocationRepository
from app.database.repositories.merchant_repository import MerchantRepository
from app.models.merchant_model import MerchantBrandModel, MerchantLocationModel
from app.schemas.merchant_schema import MerchantBrandCreate, BulkCreateRestaurantLocation, MerchantLocationCreate
from fastapi import HTTPException, Depends

from app.services.external.google_maps_service import GoogleMapsService


class MerchantService:
    def __init__(
        self,
        merchant_repository: MerchantRepository,
        merchant_location_repository: MerchantLocationRepository,
        google_maps_service: GoogleMapsService,
    ):
        self.merchant_repository = merchant_repository
        self.merchant_location_repository = merchant_location_repository
        self.google_maps_service = google_maps_service
        pass

    def create_merchant_brand(self, merchant_brand: MerchantBrandCreate):
        merchant = MerchantBrandModel(
            name=merchant_brand.name,
            description=merchant_brand.description,
            promo_details=merchant_brand.promo_details,
        )
        return self.merchant_repository.create_merchant(merchant)

    def validate_merchant_brand(self, merchant_brand_id: int):
        brand = self.merchant_repository.get_merchant_by_id(merchant_brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Merchant brand not found")

    def create_merchant_location(self, merchant_location_create: MerchantLocationCreate):
        return self.merchant_location_repository.create_merchant_location(
            MerchantLocationModel(
                name=merchant_location_create.name,
                address=merchant_location_create.address,
                latitude=merchant_location_create.latitude,
                longitude=merchant_location_create.longitude,
                brand_id=merchant_location_create.brand_id
            )
        )

    def create_bulk_merchant_location(self, merchant_location_create: BulkCreateRestaurantLocation):
        self.validate_merchant_brand(merchant_location_create.brand_id)
        merchants = self.google_maps_service.search_places_by_query(merchant_location_create.query)

        for merchant in merchants:
            self.create_merchant_location(
                MerchantLocationCreate(
                    name=merchant.name,
                    address=merchant.address,
                    latitude=merchant.latitude,
                    longitude=merchant.longitude,
                    brand_id=merchant_location_create.brand_id
                )
            )
