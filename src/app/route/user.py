from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import UserResponseNoPin, UserBase
from sqlalchemy.sql import func, text
router = APIRouter(
    prefix="/users",
)

@router.get("/", response_model=List[UserResponseNoPin])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/by-phone/{phone_number}", response_model=UserResponseNoPin)
def get_user_by_phone(phone_number: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/by-name/{name}/{similarity_score}", response_model=UserBase)
def get_user_by_name(name: str, similarity_score: float, db: Session = Depends(get_db)):
    sql = text("""
                SELECT
                    u.full_name,
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

    if not results or (float(results[0][2]) < similarity_score and float(results[0][4]) < similarity_score):
        raise HTTPException(status_code=404, detail="User not found")

    return UserBase(
        full_name=results[0][0],
        account_number=results[0][1]
    )