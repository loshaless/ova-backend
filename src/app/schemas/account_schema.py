from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from decimal import Decimal


class AccountBase(BaseModel):
    user_id: int
    currency: str = "IDR"  # Default to IDR (Indonesian Rupiah)
    account_type: str = "Octo Pay"  # Default to Octo Pay as specified


class AccountCreate(AccountBase):
    account_number: str
    status: str = "ACTIVE"
    balance: Decimal = Field(default=0.00, ge=0)


class AccountUpdate(BaseModel):
    balance: Optional[Decimal] = None
    status: Optional[str] = None


class AccountResponse(BaseModel):
    account_id: int
    user_id: int
    balance: Decimal
    currency: str
    status: str
    created_at: datetime
    account_type: str
    account_number: str

    class Config:
        from_attributes = True