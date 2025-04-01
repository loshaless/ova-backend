from app.constants.DifyDatasetID import DatasetID
from app.database.repositories.llm_prompt_repository import LLMPromptRepository
from app.database.repositories.merchant_location_repository import MerchantLocationRepository
from app.database.repositories.user_repository import UserRepository
from app.models.merchant_model import MerchantLocationModel
from app.schemas.external.vertex_ai_schema import GenerateContentRequest
from app.schemas.merchant_schema import BulkCreateRestaurantLocation, MerchantLocationCreate
from fastapi import HTTPException

from app.services.external.dify_service import DifyService
from app.services.external.google_maps_service import GoogleMapsService
from app.services.external.vertex_ai_service import VertexAIService

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

    async def get_distinct_nearby_merchant_locations_by_lat_long_with_promo(self, latitude: float, longitude: float, max_distance: float):
        # GET ALL PROMOS FROM KNOWLEDGE BASE
        promos = await self.dify_service.retrieve(
           dataset_id=DatasetID.WEBSITE.value,
           query="apa saja produk cimb niaga?"
        )

        # GET ALL MERCHANT AROUND USER
        list_of_merchant_in_tuple = self.merchant_location_repository.get_distinct_nearby_merchant_locations_by_lat_long(latitude, longitude, max_distance)
        filtered_merchant_id = []
        map_merchant_id_to_promo = {}

        # FILTER MERCHANT BASED ON PROMO
        for merchant in list_of_merchant_in_tuple:
            merchant_name = merchant[0]
            merchant_id = merchant[1]
            for promo in promos:
                if merchant_name in promo.doc_metadata["brand_name"]:
                    filtered_merchant_id.append(merchant_id)
                    map_merchant_id_to_promo[merchant_id] = promo
                    break

        # GET LAT AND LANG BASE ON MERCHANT USER ID

        # summarize using LLM
        llm_prompt = self.llm_repository.get_llm_prompt_by_title("summarize_promo")

        result = self.vertex_ai_service.generate_content(
           question="hari ini hari apa",
           generate_content_request=GenerateContentRequest(**vars(llm_prompt))
        )

        return filtered_merchant_id