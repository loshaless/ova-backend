from fastapi import APIRouter, Depends

from app.core.dependencies import get_vertex_ai_service
from app.database.repositories.llm_prompt_repository import LLMPromptRepository
from app.schemas.external.grounding_schema import GroundingRequest, GroundingResponse
from app.services.grounding_service import GroundingService
from sqlalchemy.orm import Session
from app.database.connection import get_db

router = APIRouter(prefix="/google/grounding")

def get_grounding_service(db: Session = Depends(get_db)) -> GroundingService:
    return GroundingService(LLMPromptRepository(db), get_vertex_ai_service())

@router.post("/currency", response_model=GroundingResponse)
async def grounding(
    request: GroundingRequest,
    grounding_service: GroundingService = Depends(get_grounding_service)
):
    result = await grounding_service.grounding_currency(request.question)
    return {"response": result}

@router.post("/market_update", response_model=GroundingResponse)
async def grounding(
    request: GroundingRequest,
    grounding_service: GroundingService = Depends(get_grounding_service)
):
    result = await grounding_service.grounding_market_update(request.question)
    return {"response": result}
