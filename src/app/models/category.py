from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.connection import Base
from sqlalchemy.orm import relationship


class CategoryMain(Base):
    __tablename__ = "category_main"

    category_main_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    image_uri = Column(String(255))
    subcategories = relationship("CategorySub", back_populates="parent_category")

class CategorySub(Base):
    __tablename__ = "category_sub"

    category_sub_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    parent_category_id = Column(Integer, ForeignKey("category_main.category_main_id"), nullable=False)
    image_uri = Column(String(255))
    parent_category = relationship("CategoryMain", back_populates="subcategories")