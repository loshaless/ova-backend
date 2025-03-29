from fastapi import APIRouter, Depends

from app.core.dependencies import get_vertex_ai_service
from app.services.external.google_grounding import VertexAIService
from app.schemas.external.grounding_schema import GroundingRequest, GroundingResponse

router = APIRouter(prefix="/google/grounding")

@router.post("/", response_model=GroundingResponse)
def grounding(
    request: GroundingRequest,
    vertex_ai_service: VertexAIService = Depends(get_vertex_ai_service)
):
    response_text = vertex_ai_service.generate_content(request.question)
    return {"response": response_text}
