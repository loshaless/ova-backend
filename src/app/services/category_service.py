from app.database.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryResponse, SubCategoryResponse

class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def get_all_categories(self) -> list[CategoryResponse]:
        categories = self.category_repository.get_all_categories()

        return [
            CategoryResponse(
                id=category.category_main_id,
                name=str(category.name),
                image_uri=str(category.image_uri),
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