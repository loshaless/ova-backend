from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    full_name: str
    phone_number: str

class UserBaseWithPin(UserBase):
    pin: str

class UserResponseNoPin(UserBase):
    user_id: int
    registration_date: datetime
    
    class Config:
        from_attributes = True

class UserWithAccount(UserBase):
    account_number: str

class UserResponseJoinAccount(BaseModel):
    user_id: int
    full_name: str
    account_id: int
    account_number: str
    balance: float
    status: str
    account_type: str