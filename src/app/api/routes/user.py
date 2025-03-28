from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.models.user_preference import UserPreference
from app.schemas.user import UserWithAccount, UserResponseJoinAccount
from sqlalchemy.sql import func, text
from sqlalchemy.orm import joinedload

from app.schemas.user_preference import UserPreferenceResponse, UserPreferenceUpdate

router = APIRouter(
    prefix="/users",
)

@router.get("/", response_model=List[UserResponseJoinAccount])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    users = db.query(User).options(joinedload(User.accounts)).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserResponseJoinAccount)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).options(joinedload(User.accounts)).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/by-name/{name}/{similarity_score}", response_model=UserWithAccount)
def get_user_by_name(name: str, similarity_score: float, db: Session = Depends(get_db)):
    sql = text("""
                SELECT
                    u.full_name,
                    u.phone_number,
                    a.account_number,
                    similarity(LOWER(u.full_name), LOWER(:search_name)) AS full_text_similarity_score,
                    word_similarities_array,
                    max_word_similarity_score
                FROM
                    "USER" u
                JOIN account a on u.user_id = a.user_id,
                    LATERAL (
                        SELECT
                            array_agg(similarity_score) AS word_similarities_array,
                            max(similarity_score) AS max_word_similarity_score
                        FROM
                            unnest(string_to_array(u.full_name, ' ')) AS word,
                            LATERAL (SELECT similarity(LOWER(word), LOWER(:search_name)) AS similarity_score) AS ws
                    ) AS word_similarity_results
                ORDER BY full_text_similarity_score DESC
                LIMIT 1;
            """)
    result = db.execute(sql, {"search_name": name})
    results = result.fetchall()

    full_name_similarity_score = float(results[0][3])
    max_similarity_each_word = float(results[0][5])

    if not results or (full_name_similarity_score< similarity_score and max_similarity_each_word < similarity_score):
        raise HTTPException(status_code=404, detail="User not found")

    return UserWithAccount(
        full_name=results[0][0],
        phone_number=results[0][1],
        account_number=results[0][2]
    )

@router.get("/{user_id}/preferences", response_model=UserPreferenceResponse)
def get_user_preferences(user_id: int, db: Session = Depends(get_db)):
    user_preference = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
    if not user_preference:
        raise HTTPException(status_code=404, detail="User preference not found")
    return user_preference

@router.put("/{user_id}/preferences", response_model=UserPreferenceResponse)
def update_user_preferences(
        user_id: int,
        preference_update: UserPreferenceUpdate,
        db: Session = Depends(get_db)
):
    # Check if user exists
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get existing preference or create new one
    user_preference = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()

    # when data user_preference in database exist
    if user_preference:
        # Update existing record
        if preference_update.preferences is not None:
            user_preference.preferences = preference_update.preferences

        if preference_update.persona is not None and preference_update.persona != "":
            user_preference.persona = preference_update.persona

        # Update last_updated timestamp
        user_preference.last_updated = func.timezone('Asia/Jakarta', func.now())
    else:
        # Create new preference record
        # Ensure we have at least one field to save
        if preference_update.preferences is None and (
                preference_update.persona is None or preference_update.persona == ""):
            raise HTTPException(status_code=400, detail="Either preferences or persona must be provided")

        # If preferences is None, initialize with empty dict
        preferences = preference_update.preferences or {}

        user_preference = UserPreference(
            user_id=user_id,
            preferences=preferences,
            persona=preference_update.persona
        )
        db.add(user_preference)

    db.commit()
    db.refresh(user_preference)
    return user_preference