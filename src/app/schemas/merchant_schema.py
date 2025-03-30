from typing import Optional
from pydantic import BaseModel

class MerchantLocationCreate(BaseModel):
    name: str
    user_id: int
    address: str
    latitude: float
    longitude: float

class BulkCreateRestaurantLocation(BaseModel):
    query: str
    user_id: int

class MerchantLocationResponse(BaseModel):
    brand_name: str
    brand_description: Optional[str] = None
    brand_promo_details: Optional[dict] = None
    name: str
    address: str
    latitude: float
    longitude: float
    distance: Optional[float] = None  # Distance from search point