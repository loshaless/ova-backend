from pydantic import BaseModel
from typing import List


class SubCategoryResponse(BaseModel):
    id: int
    name: str
    image_uri: str | None
    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    id: int
    name: str
    image_uri: str | None
    subcategories: List[SubCategoryResponse]

    class Config:
        from_attributes = True