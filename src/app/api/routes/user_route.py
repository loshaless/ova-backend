from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.repositories.user_preference_repository import UserPreferenceRepository
from app.database.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserWithAccount, UserResponseJoinAccount

from app.schemas.user_preference_schema import UserPreferenceResponse, UserPreferenceUpdate
from app.services.user_preference_service import UserPreferenceService
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
)

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))

def get_user_preference_service(db: Session = Depends(get_db)) -> UserPreferenceService:
    return UserPreferenceService(UserPreferenceRepository(db), UserRepository(db))

@router.get("/", response_model=List[UserResponseJoinAccount])
def get_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service)
):
    return user_service.get_all_users(skip, limit)

@router.get("/{user_id}", response_model=UserResponseJoinAccount)
def get_user_by_id(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    return user_service.get_user_by_user_id(user_id)

@router.get("/by-name/{name}/{similarity_score}", response_model=UserWithAccount)
def get_user_by_name(
    name: str,
    similarity_score: float,
    user_service: UserService = Depends(get_user_service)
):
    return user_service.get_user_by_name(name, similarity_score)

@router.get("/{user_id}/preferences", response_model=UserPreferenceResponse)
def get_user_preferences(
    user_id: int,
    user_preference_service: UserPreferenceService = Depends(get_user_preference_service)
):
    return user_preference_service.get_user_preference_by_user_id(user_id)

@router.get("/{full_name}/preferences/full-name", response_model=UserPreferenceResponse)
def get_user_preferences(
    full_name: str,
    user_preference_service: UserPreferenceService = Depends(get_user_preference_service)
):
    return user_preference_service.get_user_preference_by_full_name(full_name)

@router.put("/{user_id}/preferences", response_model=UserPreferenceResponse)
def update_user_preferences(
    user_id: int,
    preference_update: UserPreferenceUpdate,
    user_preference_service: UserPreferenceService = Depends(get_user_preference_service)
):
    return user_preference_service.update_user_preference(user_id, preference_update)
