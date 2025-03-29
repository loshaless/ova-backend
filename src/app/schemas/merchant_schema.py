from typing import Optional
from pydantic import BaseModel

class MerchantBrandCreate(BaseModel):
    name: str
    description: Optional[str] = None
    promo_details: Optional[dict] = None

class RestaurantLocationCreate(BaseModel):
    name: str
    brand_id: int
    address: str
    latitude: float
    longitude: float

class BulkCreateRestaurantLocation(BaseModel):
    query: str
    brand_id: int

class RestaurantLocationResponse(BaseModel):
    brand_name: str
    brand_description: Optional[str] = None
    brand_promo_details: Optional[dict] = None
    name: str
    address: str
    latitude: float
    longitude: float
    distance: Optional[float] = None  # Distance from search point