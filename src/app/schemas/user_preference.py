# Pydantic models for request/response
import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel


class UserPreferenceUpdate(BaseModel):
    preferences: Optional[Dict[str, Any]] = None
    persona: Optional[str] = None


class UserPreferenceResponse(BaseModel):
    user_preference_id: int
    user_id: int
    preferences: Dict[str, Any]
    last_updated: datetime.datetime
    persona: Optional[str] = None

    class Config:
        from_attributes = True