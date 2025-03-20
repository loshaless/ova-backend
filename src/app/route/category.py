from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.category import CategoryMain, CategorySub
from app.schemas.category import CategoryResponse, SubCategoryResponse

router = APIRouter(
    prefix="/categories",
)


@router.get("/")
def get_all_categories_with_subcategories(db: Session = Depends(get_db)):
    categories = db.query(CategoryMain).all()

    # Using Pydantic's built-in ORM mode conversion
    return [
        CategoryResponse(
            id=category.category_main_id,
            name=category.name,
            image_uri=category.image_uri,
            subcategories=[
                SubCategoryResponse(
                    id=subcategory.category_sub_id,
                    name=subcategory.name,
                    image_uri=subcategory.image_uri
                )
                for subcategory in category.subcategories
            ]
        )
        for category in categories
    ]

