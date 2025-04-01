from sqlalchemy.orm import Session
from sqlalchemy import text, bindparam
from typing import List

from app.models.merchant_model import MerchantLocationModel


class MerchantLocationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_merchant_location(self, merchant_location: MerchantLocationModel):
        self.db.add(merchant_location)
        self.db.commit()
        self.db.refresh(merchant_location)
        return merchant_location

    def get_distinct_nearby_merchant_locations_by_lat_long(self, latitude: float, longitude: float, max_distance: float):
        query = text("""
                    WITH user_location AS (
                        SELECT ST_Transform(ST_SetSRID(ST_MakePoint(:user_longitude, :user_latitude), 4326), 3857) AS user_point
                    )
                    SELECT u.full_name, u.user_id
                    FROM merchant_locations rl
                    JOIN "USER" u ON u.user_id = rl.user_id
                    CROSS JOIN user_location
                    WHERE ST_Distance(
                        ST_Transform(ST_SetSRID(ST_MakePoint(rl.longitude, rl.latitude), 4326), 3857),
                        user_location.user_point
                    ) <= :parameter_distance
                    GROUP BY u.full_name, u.user_id;
                                    """)

        return self.db.execute(
            query,
            {
                "user_longitude": longitude,
                "user_latitude": latitude,
                "parameter_distance": max_distance
            }
        )

    def get_distinct_nearby_merchant_locations_by_lat_long_and_user_id(self, latitude: float, longitude: float,
                                                                       max_distance: float, user_id_list: List[int]):
        query = text("""
            WITH user_location AS (
                SELECT
                    ST_Transform(ST_SetSRID(ST_MakePoint(:user_longitude, :user_latitude), 4326), 3857) AS user_point
            ),
            distance_data AS (
                SELECT
                    u.full_name,
                    rl.user_id,
                    rl.name,
                    rl.address,
                    rl.latitude,
                    rl.longitude,
                    ST_Distance(
                        ST_Transform(ST_SetSRID(ST_MakePoint(rl.longitude, rl.latitude), 4326), 3857),
                        (SELECT user_point FROM user_location)
                    ) AS distance_meters
                FROM
                    merchant_locations rl
                JOIN "USER" u ON u.user_id = rl.user_id
                CROSS JOIN user_location
                WHERE
                    rl.user_id IN :user_id_list  -- Note: no parentheses around the parameter
                    AND ST_Distance(
                        ST_Transform(ST_SetSRID(ST_MakePoint(rl.longitude, rl.latitude), 4326), 3857),
                        (SELECT user_point FROM user_location)
                    ) <= :parameter_distance
            )
            SELECT DISTINCT ON (user_id) *
            FROM distance_data
            ORDER BY user_id, distance_meters;
        """).bindparams(bindparam('user_id_list', expanding=True))

        return self.db.execute(
            query,
            {
                "user_longitude": longitude,
                "user_latitude": latitude,
                "parameter_distance": max_distance,
                "user_id_list": user_id_list
            }
        )