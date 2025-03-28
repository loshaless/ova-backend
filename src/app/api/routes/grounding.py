from fastapi import APIRouter, Depends

from app.core.dependencies import get_vertex_ai_service
from app.external_services.google_grounding import VertexAIService
from app.schemas.grounding import GroundingRequest, GroundingResponse

router = APIRouter(prefix="/grounding")

@router.post("/", response_model=GroundingResponse)
def grounding(
    request: GroundingRequest,
        vertex_ai_service: VertexAIService = Depends(get_vertex_ai_service)

):
    response_text = vertex_ai_service.generate_content(request.question)
    return {"response": response_text}
