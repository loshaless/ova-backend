from typing import Optional, List
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

class MerchantLocationDetail(BaseModel):
    brand_name: str
    branch_name: Optional[str] = None
    brand_promo_details: str = None
    address: str
    latitude: float
    longitude: float
    distance_meters: Optional[float] = None
    link: str

class MerchantLocationDetailResponse(BaseModel):
    intent: str = "Show Merchant Location By Promo"
    entities: List[MerchantLocationDetail]
    base64: str