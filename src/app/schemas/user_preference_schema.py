# Pydantic models for request/response
from datetime import datetime, date
from typing import Optional, Dict, Any
from pydantic import BaseModel
import datetime


class TransactionLimitation(BaseModel):
    amount: int
    start_date: date
    end_date: date
    
    model_config = {
        "json_encoders": {
            date: lambda v: v.isoformat()
        }
    }

class PersonaModel(BaseModel):
    goals: str
    interest: str
    limitation: TransactionLimitation

class UserPreferenceUpdate(BaseModel):
    full_name: str
    persona: PersonaModel
    pekerjaan: str
    usia: int
    marital_status: str
    penghasilan_perbulan: int

class UserPreferenceResponse(BaseModel):
    user_preference_id: int
    user_id: int
    preferences: Dict[str, Any]
    last_updated: datetime.datetime
    persona: PersonaModel
    pekerjaan: str
    usia: int
    marital_status: str
    penghasilan_perbulan: int

    class Config:
        from_attributes = True