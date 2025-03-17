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