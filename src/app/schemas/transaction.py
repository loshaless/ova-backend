from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from decimal import Decimal
import uuid


class TransactionBase(BaseModel):
    sender_account_id: int
    receiver_account_id: int
    amount: Decimal = Field(..., gt=0)  # Amount must be greater than 0
    currency: str = "IDR"  # Default to IDR (Indonesian Rupiah)
    message: Optional[str] = None
    is_scheduled: bool = False
    transaction_type: str = "TRANSFER"  # Default to transfer


class TransactionCreate(TransactionBase):
    @validator('sender_account_id')
    def sender_receiver_not_same(cls, v, values):
        if 'receiver_account_id' in values and v == values['receiver_account_id']:
            raise ValueError('Sender and receiver accounts cannot be the same')
        return v

    @classmethod
    def generate_reference_number(cls):
        """Generate a unique reference number for the transaction"""
        return f"TRX-{uuid.uuid4().hex[:12].upper()}"


class TransferRequest(BaseModel):
    sender_account_number: str
    receiver_account_number: str
    amount: Decimal = Field(..., gt=0)
    pin: str  # User PIN for authentication
    message: Optional[str] = None


class TransactionResponse(BaseModel):
    transaction_id: int
    reference_number: str
    sender_account_id: int
    receiver_account_id: int
    amount: Decimal
    currency: str
    transaction_time: datetime
    message: Optional[str]
    admin_fee: Decimal
    transaction_type: str
    is_scheduled: bool

    class Config:
        from_attributes = True