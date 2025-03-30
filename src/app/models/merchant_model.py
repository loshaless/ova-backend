from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database.connection import Base

class MerchantLocationModel(Base):
    __tablename__ = "merchant_locations"

    id = Column(Integer, primary_key=True, index=True)

    # Location-specific details
    name = Column(String)
    address = Column(String)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('USER.user_id'), nullable=False)