from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.connection import Base
from enum import Enum
from sqlalchemy.orm import relationship

class AccountType(str, Enum):
    OCTO_PAY = "Octo Pay"
    CREDIT_CARD = "Credit Card"

class AccountModel(Base):
    __tablename__ = "account"

    account_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("USER.user_id"), nullable=False)
    balance = Column(Numeric(19, 2), nullable=False, default=0.00)
    currency = Column(String(3), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    account_type = Column(String(50), nullable=False)
    account_number = Column(String(100), nullable=False, unique=True)

    user = relationship("UserModel", back_populates="accounts")
