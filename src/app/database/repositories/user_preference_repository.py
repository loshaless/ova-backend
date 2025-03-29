from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user_preference_model import UserPreferenceModel
from app.schemas.user_preference import UserPreferenceUpdate


class UserPreferenceRepository:
    def __init__(self, db_session: Session):
        self.session = db_session

    def get_user_preference_by_user_id(self, user_id: int):
        return self.session.query(UserPreferenceModel).filter(UserPreferenceModel.user_id == user_id).first()

    def create_user_preference(self, user_id: int, preferences: dict, persona: dict):
        user_preference = UserPreferenceModel(
            user_id=user_id,
            preferences=preferences,
            persona=persona
        )
        self.session.add(user_preference)
        return user_preference

    @staticmethod
    def update_user_preference(user_preference: UserPreferenceModel, preference_update: UserPreferenceUpdate):
        if preference_update.preferences is not None:
            user_preference.preferences = preference_update.preferences

        if preference_update.persona is not None:
            user_preference.persona = preference_update.persona

        # Update last_updated timestamp
        user_preference.last_updated = func.timezone('Asia/Jakarta', func.now())

    def commit(self):
        self.session.commit()

    def refresh(self, obj):
        self.session.refresh(obj)


