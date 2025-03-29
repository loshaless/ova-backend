import logging
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.core.dependencies import get_tts_service
from app.schemas.external.transcript_schema import TTSRequest
from app.services.external.google_tts import TTSService

_LOGGER = logging.getLogger(__name__)
router = APIRouter(prefix="/google/transcript")

@router.post("/text-to-speech")
def transcribe_text_to_speech(
        request: TTSRequest,
        tts_service: TTSService = Depends(get_tts_service)
):
    return tts_service.synthesize_speech(request.text)



