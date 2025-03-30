from app.models.merchant_model import MerchantBrandModel
from sqlalchemy.orm import Session

class MerchantRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_merchant(self, merchant: MerchantBrandModel):
        self.db.add(merchant)
        self.db.commit()
        self.db.refresh(merchant)
        return merchant

    def get_merchant_by_id(self, merchant_id: int):
        return self.db.query(MerchantBrandModel).filter(MerchantBrandModel.id == merchant_id).first()
