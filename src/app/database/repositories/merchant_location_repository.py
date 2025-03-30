from sqlalchemy.orm import Session

from app.models.merchant_model import MerchantLocationModel


class MerchantLocationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_merchant_location(self, merchant_location: MerchantLocationModel):
        self.db.add(merchant_location)
        self.db.commit()
        self.db.refresh(merchant_location)
        return merchant_location