from app.database.repositories.user_preference_repository import UserPreferenceRepository
from app.database.repositories.user_repository import UserRepository
from app.schemas.user_preference_schema import UserPreferenceUpdate
from app.helper.date_serialize_helper import serialize_dates
from fastapi import HTTPException

class UserPreferenceService:
    def __init__(
        self,
        user_preference_repository: UserPreferenceRepository,
        user_repository: UserRepository
    ):
        self.user_preference_repository = user_preference_repository
        self.user_repository = user_repository

    def get_user_preference_by_user_id(self, user_id: int):
        user_preference = self.user_preference_repository.get_user_preference_by_user_id(user_id)

        if not user_preference:
            raise HTTPException(status_code=404, detail="User preference not found")
        return user_preference
    
    def get_user_preference_by_full_name(self, full_name: str):
        user_preference = self.user_preference_repository.get_user_preference_by_full_name(full_name)

        if not user_preference:
            raise HTTPException(status_code=404, detail="User preference not found")
        return user_preference

    def update_user_preference(self, user_id: int, preference_update: UserPreferenceUpdate):
        user = self.user_repository.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_preference = self.user_preference_repository.get_user_preference_by_user_id(user_id)

        if user_preference:
            self.user_preference_repository.update_user_preference(user_preference, preference_update)
        else:
            self.user_preference_repository.create_user_preference(user_id, preference_update)

        self.user_preference_repository.commit()
        self.user_preference_repository.refresh(user_preference)

        return user_preference
    
    def update_user_preference_by_name(self, full_name: str, preference_update: UserPreferenceUpdate):
        # Check if user exists
        user_id = self.user_preference_repository.get_user_preference_by_full_name(full_name)
        user = self.user_repository.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_preference = self.user_preference_repository.get_user_preference_by_user_id(user_id)

        if user_preference:
            self.user_preference_repository.update_user_preference(user_preference, preference_update)
        else:
            self.user_preference_repository.update_user_preference(user_preference, preference_update)

        self.user_preference_repository.commit()
        self.user_preference_repository.refresh(user_preference)

        return user_preference
