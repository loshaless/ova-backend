from sqlalchemy.orm import Session
from typing import List
from app.schemas.complaint_schema import ComplaintResponse, ComplaintCreate
from app.database.repositories.complaint_repository import ComplaintRepository

class ComplaintService:
    def list_user_complaints(db: Session, user_id: int) -> List[ComplaintResponse]:
        complaints = ComplaintRepository.get_complaints_by_user_id(db, user_id)
        return [ComplaintResponse.model_validate(c) for c in complaints]

    def insert_complaint(db: Session, complaint_data: ComplaintCreate) -> ComplaintResponse:
        complaint = ComplaintRepository.create_complaint(db, complaint_data)
        return ComplaintResponse.model_validate(complaint)


