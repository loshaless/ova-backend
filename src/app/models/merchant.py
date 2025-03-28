from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.database.connection import Base

class MerchantBrand(Base):
    __tablename__ = "merchant_brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    promo_details = Column(JSONB)

    # Relationship to multiple restaurant locations
    locations = relationship("RestaurantLocation", back_populates="brand")


class RestaurantLocation(Base):
    __tablename__ = "restaurant_locations"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey('merchant_brands.id'), nullable=False)

    # Location-specific details
    name = Column(String)
    address = Column(String)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Relationship back to the brand
    brand = relationship("MerchantBrand", back_populates="locations")