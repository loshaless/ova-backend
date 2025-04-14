from sqlalchemy.orm import Session
from app.models.complaint_model import Complaint
from app.schemas.complaint_schema import ComplaintCreate
from typing import List

class ComplaintRepository:
    def get_complaints_by_user_id(db: Session, user_id: int) -> List[Complaint]:
        return db.query(Complaint).filter(Complaint.user_id == user_id).all()
    

    def create_complaint(db: Session, complaint_data: ComplaintCreate):
        complaint = Complaint(
            raw_complaint=complaint_data.raw_complaint,
            complaint_summary=complaint_data.complaint_summary,
            category=complaint_data.category,
            status=complaint_data.status,
            sub_category=complaint_data.sub_category,
            user_id=complaint_data.user_id,
        )
        db.add(complaint)
        db.commit()
        db.refresh(complaint)
        return complaint

