from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.database.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryResponse
from app.services.category_service import CategoryService

router = APIRouter(
    prefix="/categories",
)

def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(CategoryRepository(db))

@router.get("/", response_model=List[CategoryResponse])
def get_all_categories_with_subcategories(
    category_service: CategoryService = Depends(get_category_service)
):
    return category_service.get_all_categories()

