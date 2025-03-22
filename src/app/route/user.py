from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import UserResponseNoPin, UserBase, UserWithAccount, UserResponseJoinAccount
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

@router.get("/{user_id}", response_model=UserResponseJoinAccount)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    sql = text("""
        select u.user_id, u.full_name, a.account_id, a.account_number, a.balance, a.status, a.account_type
        from "USER" u
        join account a on a.user_id = u.user_id
        where a.user_id = :user_id;
    """)
    result = db.execute(sql, {"user_id": user_id})
    user = result.fetchone()

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