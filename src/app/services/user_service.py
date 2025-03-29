from app.database.repositories.user_repository import UserRepository
from fastapi import HTTPException

from app.schemas.user import UserWithAccount


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_all_users(self, skip: int, limit: int):
        return self.user_repository.get_all_users_join_accounts()

    def get_user_by_user_id(self, user_id: int):
        user =  self.user_repository.get_user_by_id_join_accounts(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_user_by_name(self, name: str, similarity_score: float):
        results = self.user_repository.get_user_by_name(name, similarity_score)
        full_name_similarity_score = float(results[0][3])
        max_similarity_each_word = float(results[0][5])

        if not results or (
                full_name_similarity_score < similarity_score and max_similarity_each_word < similarity_score):
            raise HTTPException(status_code=404, detail="User not found")

        return UserWithAccount(
            full_name=results[0][0],
            phone_number=results[0][1],
            account_number=results[0][2]
        )