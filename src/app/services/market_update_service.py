from app.database.repositories.market_update_repository import fetch_market_data, fetch_bi_rate

def get_market_summary_service():
    return fetch_market_data()

def get_bi_rate_service():
    return fetch_bi_rate()
