# app/core/dependencies.py
from typing import Type

from app.core.config import get_settings
from app.services.external.google_grounding import VertexAIService
from app.services.external.google_maps_service import GoogleMapsService
from app.services.external.google_tts import TTSService

settings = get_settings()

def get_google_maps_service() -> Type[GoogleMapsService]:
    """
    Dependency injection for Google Maps service
    """
    return GoogleMapsService

def get_vertex_ai_service() -> VertexAIService:
    """
    Cached dependency for Vertex AI Service

    Returns:
        VertexAIService: Configured Vertex AI service
    """
    return VertexAIService(
        project_id=settings.PROJECT_ID,
        credentials_path=settings.GOOGLE_APPLICATION_CREDENTIALS
    )

def get_tts_service() -> Type[TTSService]:
    """
    Dependency injection for TTS service
    """
    return TTSService