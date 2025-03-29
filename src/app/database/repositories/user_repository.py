from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text

from app.models.user_model import UserModel


class UserRepository:
    def __init__(self, db_session: Session):
        self.session = db_session

    def get_user_by_id(self, user_id: int):
        return self.session.query(UserModel).filter(UserModel.user_id == user_id).first()

    def get_all_users_join_accounts(self, skip: int = 0, limit: int = 100):
        return (self.session.query(UserModel)
                .options(joinedload(UserModel.accounts))
                .where(UserModel.user_type != "merchant")
                .offset(skip).limit(limit).all())

    def get_user_by_id_join_accounts(self, user_id: int):
        return self.session.query(UserModel).options(joinedload(UserModel.accounts)).filter(UserModel.user_id == user_id).first()

    def get_user_by_name(self, name: str, similarity_score: float):
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
        result = self.session.execute(sql, {"search_name": name})
        return result.fetchall()