# Pydantic models for request/response
from datetime import date
from typing import Dict, Any, List
from pydantic import BaseModel
import datetime
from enum import Enum

class TransactionLimitation(BaseModel):
    amount: int
    start_date: date
    end_date: date

    model_config = {
        "json_encoders": {
            date: lambda v: v.isoformat()
        }
    }

class SavingHabit(str, Enum):
    REGULAR = "rutin"
    SELDOM = "jarang"
    NEVER = "tidak pernah menabung"

class FinancialBehavior(str, Enum):
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    RISK_TAKER = "risk taker"

class UserPersonaProfile(BaseModel):
    transaksi_limitation: TransactionLimitation
    lifestyle: List[str]
    financial_behavior: FinancialBehavior
    financial_goals: List[str]
    preferred_categories: List[str]
    saving_habit: SavingHabit

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "transaksi_limitation": {
                        "amount": 100000,
                        "start_date": "2025-04-03",
                        "end_date": "2025-07-03"
                    },
                    "lifestyle": [
                        "Hemat",
                        "Keluarga",
                        "Traveler"
                    ],
                    "financial_behavior": "balanced",
                    "financial_goals": [
                        "Dana pensiun",
                        "Beli rumah",
                        "Dana darurat"
                    ],
                    "preferred_categories": [
                        "Food & Beverages",
                        "Groceries",
                        "Investasi"
                    ],
                    "saving_habit": "rutin"
                }
            ]
        }
    }

class UserPreferenceUpdate(BaseModel):
    full_name: str
    persona: UserPersonaProfile
    pekerjaan: str
    usia: int
    marital_status: str
    penghasilan_perbulan: int

class UserPreferenceResponse(BaseModel):
    user_preference_id: int
    user_id: int
    preferences: Dict[str, Any]
    last_updated: datetime.datetime
    persona: UserPersonaProfile
    pekerjaan: str
    usia: int
    marital_status: str
    penghasilan_perbulan: int

    class Config:
        from_attributes = True