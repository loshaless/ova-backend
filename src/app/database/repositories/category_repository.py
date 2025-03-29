from sqlalchemy.orm import Session
from typing import Type, Optional

from app.models.category_model import CategoryMainModel


class CategoryRepository:
    def __init__(self, db_session: Session):
        self.session = db_session

    def get_all_categories(self) -> list[Type[CategoryMainModel]]:
        return self.session.query(CategoryMainModel).all()

