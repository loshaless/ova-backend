from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.sql import func
from app.database.connection import Base

class Transaction(Base):
    __tablename__ = "transaction"

    transaction_id = Column(Integer, primary_key=True, index=True)
    reference_number = Column(String(255), nullable=False, unique=True)
    sender_account_id = Column(Integer, ForeignKey("account.account_id"), nullable=False)
    receiver_account_id = Column(Integer, ForeignKey("account.account_id"), nullable=False)
    amount = Column(Numeric(19, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="IDR")
    transaction_time = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    message = Column(Text)
    is_scheduled = Column(Boolean, nullable=False, default=False)
    admin_fee = Column(Numeric(19, 2), nullable=False, default=0.00)
    transaction_type = Column(String(50), nullable=False)
    sender_name = Column(String(255), nullable=False)
    receiver_name = Column(String(255), nullable=False)
    receiver_location = Column(String(255), nullable=True)
    category_main_id = Column(Integer, nullable=True)
    category_sub_id = Column(Integer, nullable=True)