from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.complaint_schema import ComplaintResponse, ComplaintCreate
from app.services.complaint_service import ComplaintService
from app.database.repositories.complaint_repository import ComplaintRepository
from app.database.connection import get_db  # Fungsi ini harus mengembalikan session SQLAlchemy

router = APIRouter(
    prefix="/complaints"
)

@router.get("/user/{user_id}", response_model=List[ComplaintResponse])
def get_complaints_by_user(user_id: int, db: Session = Depends(get_db)):
    return ComplaintService.list_user_complaints(db, user_id)

@router.post("/complaints", response_model=ComplaintResponse)
def create_complaint_route(
    complaint_data: ComplaintCreate,
    db: Session = Depends(get_db)
):
    return ComplaintService.insert_complaint(db, complaint_data)
