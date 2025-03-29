from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "USER"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    pin = Column(String(255), nullable=False)
    registration_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    accounts = relationship("AccountModel", back_populates="user")