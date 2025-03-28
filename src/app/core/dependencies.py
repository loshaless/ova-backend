# app/core/dependencies.py
from typing import Type

from app.core.config import get_creds, get_project_id
from app.external_services.google_grounding import VertexAIService
from app.external_services.google_maps_service import GoogleMapsService

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
        project_id=get_project_id(),
        credentials_path=get_creds()
    )