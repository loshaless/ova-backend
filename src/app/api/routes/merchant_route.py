from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.core.dependencies import get_google_maps_service
from app.database.connection import get_db
from app.services.external.google_maps_service import GoogleMapsService
from app.models.merchant_model import MerchantBrandModel, MerchantLocationModel
from app.schemas.external.google_map import GoogleMapResponse
from app.schemas.merchant import MerchantBrandCreate, RestaurantLocationCreate, BulkCreateRestaurantLocation
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/merchant",
)

@router.post("/merchant-brands/")
def create_merchant_brand(merchant_brand: MerchantBrandCreate, db: Session = Depends(get_db)):
    db_brand = MerchantBrandModel(
        name=merchant_brand.name,
        description=merchant_brand.description,
        promo_details=merchant_brand.promo_details
    )

    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

@router.post("/restaurant-locations/bulk")
def create_bulk_restaurant_locations(
    body: BulkCreateRestaurantLocation,
    db: Session = Depends(get_db),
    google_maps_service: GoogleMapsService = Depends(get_google_maps_service)
):
    restaurants = google_maps_service.search_places_by_query(body.query)
    for restaurant in restaurants:
        create_restaurant_location(
            RestaurantLocationCreate(
                name=restaurant.name,
                address=restaurant.address,
                latitude=restaurant.latitude,
                longitude=restaurant.longitude,
                brand_id=body.brand_id
            ), db)
    return {"status": "success"}

def create_restaurant_location(
    location: RestaurantLocationCreate,
    db: Session
):
    # Verify the brand exists
    brand = db.query(MerchantBrandModel).filter(MerchantBrandModel.id == location.brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Merchant brand not found")

    db_location = MerchantLocationModel(
        name= location.name,
        brand_id=location.brand_id,
        address=location.address,
        latitude=location.latitude,
        longitude=location.longitude,
    )

    db.add(db_location)
    db.commit()
    db.refresh(db_location)

    return {
        "id": db_location.id,
        "brand_id": db_location.brand_id,
        "address": db_location.address,
        "latitude": db_location.latitude,
        "longitude": db_location.longitude
    }

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