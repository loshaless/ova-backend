from fastapi import APIRouter, Depends
from typing import List

from app.core.dependencies import get_google_maps_service
from app.database.connection import get_db
from app.database.repositories.merchant_location_repository import MerchantLocationRepository
from app.database.repositories.user_repository import UserRepository
from app.services.external.google_maps_service import GoogleMapsService
from app.schemas.external.google_map_schema import GoogleMapResponse
from app.schemas.merchant_schema import BulkCreateRestaurantLocation
from sqlalchemy.orm import Session

from app.services.merhant_service import MerchantService

router = APIRouter(
    prefix="/merchant",
)

def get_merchant_service(
        db: Session = Depends(get_db),
        google_maps_service: GoogleMapsService = Depends(get_google_maps_service)
) -> MerchantService:
    return MerchantService(
        UserRepository(db),
        MerchantLocationRepository(db),
        google_maps_service
    )

@router.post("/restaurant-locations/bulk")
def create_bulk_merchant_locations(
    body: BulkCreateRestaurantLocation,
    merchant_service: MerchantService = Depends(get_merchant_service)
):
    merchant_service.create_bulk_merchant_location(body)
    return {"status": "success"}

# Find Nearby Restaurant Locations Endpoint
@router.get("/nearby-location/", response_model=List[GoogleMapResponse])
def find_nearby_restaurants(
        latitude: float = -6.2731663,
        longitude: float = 106.7243052,
        max_distance: float = 2000,
        keyword: str = "CIMB Niaga",
        type_name: str = "bank",
        google_maps_service: GoogleMapsService = Depends(get_google_maps_service)
):
    locations = google_maps_service.nearby_search_places(latitude, longitude, type_name, keyword, max_distance)
    return locations