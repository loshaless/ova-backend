# app/core/dependencies.py
from typing import Type

from app.core.config import PROJECT_ID, GOOGLE_APPLICATION_CREDENTIALS
from app.services.external.dify_service import DifyService
from app.services.external.vertex_ai_service import VertexAIService
from app.services.external.google_maps_service import GoogleMapsService
from app.services.external.google_tts import TTSService

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
        project_id=PROJECT_ID,
        credentials_path=GOOGLE_APPLICATION_CREDENTIALS
    )

def get_tts_service() -> Type[TTSService]:
    """
    Dependency injection for TTS service
    """
    return TTSService

def get_dify_service() -> Type[DifyService]:
    return DifyService