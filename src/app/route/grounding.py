from fastapi import APIRouter
from app.schemas.grounding import GroundingRequest, GroundingResponse
from app.third_party.google_grounding import get_grounding_response

router = APIRouter(prefix="/grounding")

@router.post("/", response_model=GroundingResponse)
def grounding(request: GroundingRequest):
    response_text = get_grounding_response(request.question)
    return {"response": response_text}
