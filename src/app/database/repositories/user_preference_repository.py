from sqlalchemy.orm import Session
from sqlalchemy import func, text
from app.models.user_preference_model import UserPreferenceModel
from app.schemas.user_preference_schema import UserPreferenceUpdate
import json


class UserPreferenceRepository:
    def __init__(self, db_session: Session):
        self.session = db_session

    def get_user_id_by_full_name(self, full_name: str):
        """ Mengambil user_id berdasarkan full_name """
        result = self.session.execute(text("""
            SELECT user_id FROM "USER" WHERE full_name = :full_name
        """), {"full_name": full_name}).fetchone()

        return result[0] if result else None

    def get_user_preference_by_user_id(self, user_id: int):
        return self.session.query(UserPreferenceModel).filter(UserPreferenceModel.user_id == user_id).first()
    
    def get_user_preference_by_full_name(self, full_name: str):
        """ Mengambil preferensi user berdasarkan full_name """
        user_id = self.get_user_id_by_full_name(full_name)
        if not user_id:
            return None
        
        return self.get_user_preference_by_user_id(user_id)
    
    def get_user_preferences_by_name(db: Session, full_name: str):
        spending_query = db.execute(text("""
            SELECT cm.name AS main_category, AVG(t.amount) AS avg_spent
            FROM transaction t
            JOIN account sa ON t.sender_account_id = sa.account_id
            JOIN "USER" sender ON sa.user_id = sender.user_id
            JOIN category_main cm ON t.category_main_id = cm.category_main_id
            WHERE sender.full_name = :full_name
            GROUP BY cm.name
            ORDER BY avg_spent DESC
        """), {"full_name": full_name}).fetchall()

        average_spending_dict = {row[0]: float(row[1]) for row in spending_query}

        return {
            "average_spending": average_spending_dict
        }

    def create_user_preference(
        self,
        user_id: int,
        preference_update: UserPreferenceUpdate,
    ):
        persona = (
            preference_update.persona.model_dump(mode="json")
            if preference_update.persona
            else {}
        )

        preferences = self.get_user_preferences(full_name=preference_update.full_name)

        user_preference = UserPreferenceModel(
            user_id=user_id,
            preferences=preferences,
            persona=persona,
            pekerjaan=preference_update.pekerjaan,
            usia=preference_update.usia,
            marital_status=preference_update.marital_status,
            penghasilan_perbulan=preference_update.penghasilan_perbulan,
            last_updated=func.timezone("Asia/Jakarta", func.now()),
        )

        self.session.add(user_preference)
        self.session.commit() 
        return user_preference

    
    def get_user_preferences(self, full_name: str):
                # Average Core Spending 
                average_spending = self.session.execute(text("""
                    SELECT cm.name AS main_category, AVG(t.amount) AS avg_spent
                    FROM transaction t
                    JOIN account sa ON t.sender_account_id = sa.account_id
                    JOIN "USER" sender ON sa.user_id = sender.user_id
                    JOIN category_main cm ON t.category_main_id = cm.category_main_id
                    WHERE sender.full_name = :full_name
                    GROUP BY cm.name
                    ORDER BY avg_spent DESC
                """), {"full_name": full_name}).fetchall()

                average_spending_dict = {row[0]: float(row[1]) for row in average_spending}


                # Total Core Spending
                core_spending = self.session.execute(text("""
                    SELECT cm.name AS main_category, SUM(t.amount) AS total_spent
                    FROM transaction t
                    JOIN account sa ON t.sender_account_id = sa.account_id
                    JOIN "USER" sender ON sa.user_id = sender.user_id
                    JOIN category_main cm ON t.category_main_id = cm.category_main_id
                    WHERE sender.full_name = :full_name
                    GROUP BY cm.name
                    ORDER BY total_spent DESC
                    LIMIT 5
                """), {"full_name": full_name}).fetchall()
                
                core_spending_dict = {row[0]: float(row[1]) for row in core_spending}

                # Query Merchant Pattern
                frequently_visited = self.session.execute(text("""
                    SELECT receiver_name AS merchant, COUNT(*) AS visit_count
                    FROM transaction t
                    JOIN account sa ON t.sender_account_id = sa.account_id
                    JOIN "USER" sender ON sa.user_id = sender.user_id
                    WHERE sender.full_name = :full_name
                    GROUP BY receiver_name
                    ORDER BY visit_count DESC
                    LIMIT 5
                """), {"full_name": full_name}).fetchall()

                frequently_visited_dict = {row[0]: row[1] for row in frequently_visited}

                # recurring_services = db.execute(text("""
                #     SELECT DISTINCT receiver_name AS service
                #     FROM transaction t
                #     JOIN account sa ON t.sender_account_id = sa.account_id
                #     JOIN "USER" sender ON sa.user_id = sender.user_id
                #     WHERE sender.full_name = :full_name AND t.is_scheduled = TRUE
                # """), {"full_name": full_name}).fetchall()
                
                # recurring_services_list = [row[0] for row in recurring_services]

                # Query Transaction Characteristics
                payment_methods = self.session.execute(text("""
                    SELECT transaction_type, COUNT(*) * 1.0 / (
                        SELECT COUNT(*) FROM transaction t
                        JOIN account sa ON t.sender_account_id = sa.account_id
                        JOIN "USER" sender ON sa.user_id = sender.user_id
                        WHERE sender.full_name = :full_name
                    ) AS ratio
                    FROM transaction t
                    JOIN account sa ON t.sender_account_id = sa.account_id
                    JOIN "USER" sender ON sa.user_id = sender.user_id
                    WHERE sender.full_name = :full_name
                    GROUP BY transaction_type
                    ORDER BY transaction_type DESC
                    LIMIT 5
                """), {"full_name": full_name}).fetchall()
                
                payment_methods_dict = {row[0]: float(row[1]) for row in payment_methods}

                transaction_timing = self.session.execute(text("""
                    SELECT 
                        CASE 
                            WHEN EXTRACT(HOUR FROM transaction_time) BETWEEN 6 AND 11 THEN 'morning'
                            WHEN EXTRACT(HOUR FROM transaction_time) BETWEEN 12 AND 17 THEN 'afternoon'
                            ELSE 'evening'
                        END AS time_of_day,
                        COUNT(*) * 1.0 / (
                            SELECT COUNT(*) FROM transaction t
                            JOIN account sa ON t.sender_account_id = sa.account_id
                            JOIN "USER" sender ON sa.user_id = sender.user_id
                            WHERE sender.full_name = :full_name
                        ) AS ratio
                    FROM transaction t
                    JOIN account sa ON t.sender_account_id = sa.account_id
                    JOIN "USER" sender ON sa.user_id = sender.user_id
                    WHERE sender.full_name = :full_name
                    GROUP BY time_of_day
                    ORDER BY time_of_day DESC
                """), {"full_name": full_name}).fetchall()
                
                transaction_timing_dict = {row[0]: float(row[1]) for row in transaction_timing}

                location = self.session.execute(text("""
                    SELECT receiver_location, COUNT(*) * 1.0 / (
                        SELECT COUNT(*) FROM transaction t
                        JOIN account sa ON t.sender_account_id = sa.account_id
                        JOIN "USER" sender ON sa.user_id = sender.user_id
                        WHERE sender.full_name = :full_name
                    ) AS ratio
                    FROM transaction t
                    JOIN account sa ON t.sender_account_id = sa.account_id
                    JOIN "USER" sender ON sa.user_id = sender.user_id
                    WHERE sender.full_name = :full_name
                    GROUP BY receiver_location
                    ORDER BY receiver_location DESC
                    LIMIT 5
                """), {"full_name": full_name}).fetchall()
                
                location_dict = {row[0]: float(row[1]) for row in location}

                preferences_json_2 = {
                    "average_spending":average_spending_dict, 
                    "total_spending": core_spending_dict,
                    "merchant_pattern": {
                        "frequently_visited":frequently_visited_dict
                    },
                    "transaction_characteristics": {
                        "payment_methods": payment_methods_dict,
                        "transaction_timing": transaction_timing_dict,
                        "location": location_dict
                    }
                }

                return preferences_json_2

    def update_user_preference(self, user_preference: UserPreferenceModel, preference_update: UserPreferenceUpdate):

        if preference_update.persona is not None:
            user_preference.persona = preference_update.persona.model_dump(mode="json")
            user_preference.preferences = self.get_user_preferences(full_name=preference_update.full_name)

        # Update last_updated timestamp
        user_preference.last_updated = func.timezone('Asia/Jakarta', func.now())

        if preference_update.usia is not None:
            user_preference.usia = preference_update.usia

        if preference_update.pekerjaan is not None:
            user_preference.pekerjaan = preference_update.pekerjaan

        if preference_update.marital_status is not None:
            user_preference.marital_status = preference_update.marital_status

        if preference_update.penghasilan_perbulan is not None:
            user_preference.penghasilan_perbulan = preference_update.penghasilan_perbulan


    def commit(self):
        self.session.commit()

    def refresh(self, obj):
        self.session.refresh(obj)


