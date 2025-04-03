
from app.database.repositories.llm_prompt_repository import LLMPromptRepository
from app.database.repositories.merchant_location_repository import MerchantLocationRepository
from app.database.repositories.user_repository import UserRepository
from app.models.merchant_model import MerchantLocationModel
from app.schemas.external.dify_schema import WorkflowRequest
from google.genai import types
from app.schemas.merchant_schema import BulkCreateRestaurantLocation, MerchantLocationCreate, MerchantLocationDetail
from fastapi import HTTPException
from typing import List
import json

from app.services.external.dify_service import DifyService
from app.services.external.google_maps_service import GoogleMapsService
from app.services.external.vertex_ai_service import VertexAIService

from pydantic import BaseModel, Field

class BrandContentMap(BaseModel):
    brand_id: List[int]
    contents: List[str]

class MerchantService:
    def __init__(
        self,
        user_repository: UserRepository,
        merchant_location_repository: MerchantLocationRepository,
        google_maps_service: GoogleMapsService,
        dify_service: DifyService,
        vertex_ai_service: VertexAIService,
        llm_repository: LLMPromptRepository
    ):
        self.user_repository = user_repository
        self.merchant_location_repository = merchant_location_repository
        self.google_maps_service = google_maps_service
        self.dify_service = dify_service
        self.vertex_ai_service = vertex_ai_service
        self.llm_repository = llm_repository

    def validate_merchant_brand(self, user_id: int):
        brand = self.user_repository.get_user_by_id(user_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Merchant brand not found")

    def create_merchant_location(self, merchant_location_create: MerchantLocationCreate):
        try:
            self.merchant_location_repository.create_merchant_location(
                MerchantLocationModel(
                    name=merchant_location_create.name,
                    address=merchant_location_create.address,
                    latitude=merchant_location_create.latitude,
                    longitude=merchant_location_create.longitude,
                    user_id=merchant_location_create.user_id
                )
            )
        except Exception as e:
            print(e)

    def create_bulk_merchant_location(self, merchant_location_create: BulkCreateRestaurantLocation):
        self.validate_merchant_brand(merchant_location_create.user_id)
        merchants = self.google_maps_service.search_places_by_query(merchant_location_create.query)

        for merchant in merchants:
            self.create_merchant_location(
                MerchantLocationCreate(
                    name=merchant.name,
                    address=merchant.address,
                    latitude=merchant.latitude,
                    longitude=merchant.longitude,
                    user_id=merchant_location_create.user_id
                )
            )

    async def get_distinct_nearby_merchant_locations_by_lat_long_with_promo(
        self,
        category:str,
        latitude: float,
        longitude: float,
        max_distance: float
    ) -> List[MerchantLocationDetail]:
        # GET ALL PROMOS FROM KNOWLEDGE BASE
        workflow = await self.dify_service.execute_workflow(
            WorkflowRequest(
                inputs={
                    "keyword": category,
                }
            )
        )
        promos = workflow["data"]["outputs"]["result"]

        # GET ALL MERCHANT AROUND USER
        list_of_merchant_in_tuple = self.merchant_location_repository.get_distinct_nearby_merchant_locations_by_lat_long(latitude, longitude, max_distance)
        filtered_merchant_id = []
        map_merchant_id_to_promo = {}

        # FILTER MERCHANT BASED ON PROMO
        for merchant in list_of_merchant_in_tuple:
            merchant_name = merchant[0]
            merchant_id = merchant[1]
            for promo in promos:
                if merchant_name.lower() in promo["metadata"]["doc_metadata"]["brand_name"].lower():
                    filtered_merchant_id.append(merchant_id)
                    map_merchant_id_to_promo[merchant_id] = {
                        "content": promo["content"],
                        "brand_name": merchant_name,
                        "link": promo["metadata"]["doc_metadata"]["link"]
                    }
                    break

        # SUMMARIZE CONTENT USING LLM
        llm_prompt = self.llm_repository.get_llm_prompt_by_title("summarize_promo")
        response = self.vertex_ai_service.get_client().models.generate_content(
            model=llm_prompt.model_name,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=json.dumps(map_merchant_id_to_promo))
                    ]
                )
            ],
            config={
                'system_instruction': [types.Part.from_text(text=llm_prompt.prompt_text)],
                'response_mime_type': 'application/json',
                'response_schema': BrandContentMap,
                'temperature': llm_prompt.temperature,
                'top_p': llm_prompt.top_p,
                'max_output_tokens': llm_prompt.max_tokens
            },
        )
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            response = response.candidates[0].content.parts[0].text

        response = json.loads(response)
        map_id_to_promos = {}
        for i, v in enumerate(response["brand_id"]):
            map_id_to_promos[str(v)] = response["contents"][i]

        # GET LAT AND LANG BASE ON MERCHANT USER ID
        list_merchant_detail = self.merchant_location_repository.get_distinct_nearby_merchant_locations_by_lat_long_and_user_id(
            latitude, longitude, max_distance, filtered_merchant_id
        )

        # MAP PROMOS TO THE MERCHANT NEARBY
        result: List[MerchantLocationDetail] = []
        fields = ["brand_name", "user_id", "branch_name", "address", "latitude", "longitude", "distance_meters"]
        for merchant_db in list_merchant_detail:
            merchant_dict = dict(zip(fields, merchant_db))
            user_id: int = merchant_dict["user_id"]
            merchant_dict["content"] = map_id_to_promos[str(user_id)]
            result.append(
                MerchantLocationDetail(
                    brand_name=merchant_dict["brand_name"],
                    branch_name=merchant_dict["branch_name"],
                    brand_promo_details=merchant_dict["content"],
                    address=merchant_dict["address"],
                    latitude=merchant_dict["latitude"],
                    longitude=merchant_dict["longitude"],
                    distance_meters=merchant_dict["distance_meters"],
                    link=map_merchant_id_to_promo[user_id]["link"]
                )
            )

        return result