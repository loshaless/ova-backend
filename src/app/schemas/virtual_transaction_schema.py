from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from decimal import Decimal
import random
import uuid


class VirtualTransactionBase(BaseModel):
    sender_account_id: int
    receiver_account_ids: List[int]  # Bisa memilih dari daftar account
    min_amount: Decimal = Field(..., gt=0)
    max_amount: Decimal = Field(..., gt=0)
    start_date: datetime
    end_date: datetime
    dummy_messages: List[str] = []
    location: List[str] = []
    currency: str = "IDR"
    category_main_id: int

    @classmethod
    def generate_reference_number(cls):
        return f"VTX-{uuid.uuid4().hex[:12].upper()}"

    @classmethod
    def random_amount(cls, min_amount, max_amount):
        return round(random.uniform(float(min_amount), float(max_amount)), 2)


class VirtualTransactionCreate(VirtualTransactionBase):
    pass


class VirtualTransactionResponse(BaseModel):
    transaction_id: int
    reference_number: str
    sender_account_id: int
    receiver_account_id: int
    amount: Decimal
    currency: str
    transaction_time: datetime
    message: Optional[str]
    transaction_type: str
    sender_name: str
    receiver_name: str
    receiver_location: Optional[str]
    category_main_id: int

    class Config:
        from_attributes = True
