import logging
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.core.dependencies import get_tts_service
from app.schemas.external.transcript import TTSResponse, TTSRequest
from app.services.external.google_tts import TTSService

_LOGGER = logging.getLogger(__name__)
router = APIRouter(prefix="/google/transcript")

@router.post("/text-to-speech", response_model=TTSResponse)
def transcribe_text_to_speech(
        request: TTSRequest,
        tts_service: TTSService = Depends(get_tts_service)
):
    try:
        audio_content_b64 = tts_service.synthesize_speech(request.text)

        return TTSResponse(
            success=True,
            message="Transcription successful",
            data={
                "audio_content": audio_content_b64,
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Transcription failed: {str(e)}",
                "data": None
            }
        )



