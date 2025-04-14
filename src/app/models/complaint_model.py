from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from app.database.connection import Base
import uuid
from datetime import datetime

class Complaint(Base):
    __tablename__ = "complaint"

    complaint_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submitted_at = Column(DateTime, nullable=True, default=func.now())
    raw_complaint = Column(Text, nullable=False)
    complaint_summary = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    status = Column(String(20), nullable=True, default='in progress')
    assigned_to = Column(UUID(as_uuid=True), nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    sub_category = Column(String(100), nullable=True)
    user_id = Column(Integer, ForeignKey("USER.user_id"), nullable=True)
