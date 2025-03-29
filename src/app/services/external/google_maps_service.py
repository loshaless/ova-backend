# app/external_services/google_maps_service.py
import requests
from typing import List

from app.core.config import get_settings
from app.schemas.external.google_map import GoogleMapResponse

settings = get_settings()

class GoogleMapsService:
    BASE_URLS = {
        'text_search': "https://maps.googleapis.com/maps/api/place/textsearch/json",
        'nearby_search': "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    }

    @classmethod
    def search_places_by_query(cls, query: str) -> List[GoogleMapResponse]:
        """
        Search places by text query

        Args:
            query (str): Search query

        Returns:
            List[GoogleMapResponse]: List of place results
        """
        params = {
            "query": query,
            "key": settings.GOOGLE_MAP_API_KEY
        }

        response = requests.get(cls.BASE_URLS['text_search'], params=params)
        results = response.json().get('results', [])

        return [
            GoogleMapResponse(
                name=place.get('name', ''),
                address=place.get('formatted_address', ''),
                latitude=place['geometry']['location']['lat'],
                longitude=place['geometry']['location']['lng']
            ) for place in results
        ]

    @classmethod
    def nearby_search_places(
            cls,
            latitude: float,
            longitude: float,
            type_name: str,
            keyword: str,
            radius: float
    ) -> List[GoogleMapResponse]:
        """
        Search nearby places

        Args:
            latitude (float): Latitude of search center
            longitude (float): Longitude of search center
            type_name (str): Type of place
            keyword (str): Search keyword
            radius (float): Search radius in meters

        Returns:
            List[GoogleMapResponse]: List of nearby places
        """
        params = {
            "location": f"{latitude},{longitude}",
            "radius": radius,
            "key": settings.GOOGLE_MAP_API_KEY,
            "keyword": keyword,
            "type": type_name
        }

        response = requests.get(cls.BASE_URLS['nearby_search'], params=params)
        results = response.json().get('results', [])

        return [
            GoogleMapResponse(
                name=place.get('name', ''),
                address=place.get('formatted_address') or place.get('vicinity') or '',
                latitude=place['geometry']['location']['lat'],
                longitude=place['geometry']['location']['lng']
            ) for place in results
        ]