from datetime import datetime
from typing import List

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

class AccountJoinuser(BaseModel):
    account_number: str
    balance: float
    status: str
    account_type: str

class UserResponseJoinAccount(BaseModel):
    user_id: int
    full_name: str
    accounts: List[AccountJoinuser]