from fastapi import APIRouter, Depends
from typing import List

from app.core.dependencies import get_google_maps_service, get_dify_service, get_vertex_ai_service
from app.database.connection import get_db
from app.database.repositories.llm_prompt_repository import LLMPromptRepository
from app.database.repositories.merchant_location_repository import MerchantLocationRepository
from app.database.repositories.user_repository import UserRepository
from app.services.external.dify_service import DifyService
from app.services.external.google_maps_service import GoogleMapsService
from app.schemas.external.google_map_schema import GoogleMapResponse
from app.schemas.merchant_schema import BulkCreateRestaurantLocation
from sqlalchemy.orm import Session

from app.services.external.vertex_ai_service import VertexAIService
from app.services.merhant_service import MerchantService

router = APIRouter(
    prefix="/merchant",
)

def get_merchant_service(
        db: Session = Depends(get_db),
        google_maps_service: GoogleMapsService = Depends(get_google_maps_service),
        dify_service: DifyService = Depends(get_dify_service),
        vertex_ai_service:  VertexAIService = Depends(get_vertex_ai_service),
) -> MerchantService:
    return MerchantService(
        UserRepository(db),
        MerchantLocationRepository(db),
        google_maps_service,
        dify_service,
        vertex_ai_service,
        LLMPromptRepository(db)
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
        max_distance: float = 5000,
        keyword: str = "CIMB Niaga",
        type_name: str = "bank",
        google_maps_service: GoogleMapsService = Depends(get_google_maps_service)
):
    locations = google_maps_service.nearby_search_places(latitude, longitude, type_name, keyword, max_distance)
    return locations

@router.get("/nearby-location/user")
async def find_nearby_restaurants_user(
        latitude: float = -6.2731663,
        longitude: float = 106.7243052,
        max_distance: float = 5000,
        merchant_service: MerchantService = Depends(get_merchant_service)
):
    list_of_merchant = await merchant_service.get_distinct_nearby_merchant_locations_by_lat_long_with_promo(latitude, longitude, max_distance)
    # return result