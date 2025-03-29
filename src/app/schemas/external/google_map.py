from pydantic import BaseModel

class GoogleMapResponse(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float