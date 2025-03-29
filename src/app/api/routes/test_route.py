import logging
import os
import threading

from fastapi import APIRouter
from starlette.responses import JSONResponse
from time import sleep
from vertexai.generative_models import GenerativeModel, GenerationConfig, Part

from app.core.config import get_settings

settings = get_settings()
_LOGGER = logging.getLogger(__name__)
router = APIRouter(prefix="/test")

@router.get("/sleep")
def go_to_sleep():
    sleep(5)
    result = {
        "process_id": os.getpid(),
        "thread_id": threading.get_ident()
    }
    _LOGGER.info(result)
    return JSONResponse(status_code=200, content=result)

@router.get("/env")
def protected_route():
    _LOGGER.info(f"Project ID: {settings.PROJECT_ID}")
    return {"project_id": settings.PROJECT_ID}

@router.get("/transcribe-mp3-example")
def vertex_ai():
    model = GenerativeModel("gemini-1.5-flash-002")
    prompt = """
    Can you transcribe this interview, in the format of timecode, speaker, caption.
    Use speaker A, speaker B, etc. to identify speakers.
    """
    audio_file_uri = "gs://cloud-samples-data/generative-ai/audio/pixel.mp3"
    audio_file = Part.from_uri(audio_file_uri, mime_type="audio/mpeg")

    contents = [audio_file, prompt]

    response = model.generate_content(contents, generation_config=GenerationConfig(audio_timestamp=True))
    return {"message": response.text}