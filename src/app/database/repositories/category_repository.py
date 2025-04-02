from sqlalchemy.orm import Session
from typing import Type

from app.models.category_model import CategoryMainModel, CategorySubModel


class CategoryRepository:
    def __init__(self, db_session: Session):
        self.session = db_session

    def get_all_categories(self) -> list[Type[CategoryMainModel]]:
        return self.session.query(CategoryMainModel).all()

    def get_category_by_name(self, name: str) -> Type[CategoryMainModel]:
        return self.session.query(CategoryMainModel).filter(CategoryMainModel.name == name).first()

    def get_subcategory_by_name(self, name: str) -> Type[CategorySubModel]:
        return self.session.query(CategorySubModel).filter(CategorySubModel.name == name).first()
