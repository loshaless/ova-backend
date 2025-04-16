from fastapi import APIRouter
from typing import Dict, Union

from app.services.market_update_service import get_market_summary_service, get_bi_rate_service
from app.models.market_update_model import MarketSummary, BIRate

router = APIRouter(
    prefix="/market-update"
)

@router.get("/market-summary", response_model=Dict[str, Union[float, str]])
async def market_summary():
    return get_market_summary_service()

@router.get("/bi-rate", response_model=Dict[str, str])
async def bi_rate():
    return get_bi_rate_service()
