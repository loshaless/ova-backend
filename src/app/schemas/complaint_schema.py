from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class ComplaintCreate(BaseModel):
    raw_complaint: str
    complaint_summary: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = 'in progress'
    sub_category: Optional[str] = None
    user_id: Optional[int] = None

class ComplaintResponse(BaseModel):
    complaint_id: UUID4
    submitted_at: datetime
    raw_complaint: str
    complaint_summary: str
    category: str
    status: str
    assigned_to: Optional[str]
    resolved_at: Optional[datetime]
    sub_category: Optional[str]
    user_id: int

    class Config:
        from_attributes = True
