from app.database.repositories.llm_prompt_repository import LLMPromptRepository
from app.services.external.vertex_ai_service import VertexAIService
from app.schemas.external.vertex_ai_schema import GenerateContentRequest

class GroundingService:
    def __init__(
        self,
        llm_repository: LLMPromptRepository,
        vertexai_service: VertexAIService
    ):
        self.llm_repository = llm_repository
        self.vertexai_service = vertexai_service

    async def grounding_currency(self, question: str):
        llm_prompt = self.llm_repository.get_llm_prompt_by_title("currency_prompt")

        if not llm_prompt:
            raise ValueError("LLM prompt not found for currency_prompt")

        generate_content_request = GenerateContentRequest(**vars(llm_prompt))
        response = await self.vertexai_service.generate_content_stream(
            question,
            generate_content_request
        )

        return response
    
    async def grounding_market_update(self, question: str):
        llm_prompt = self.llm_repository.get_llm_prompt_by_title("market_update")

        if not llm_prompt:
            raise ValueError("LLM prompt not found for currency_prompt")

        generate_content_request = GenerateContentRequest(**vars(llm_prompt))
        response = await self.vertexai_service.generate_content_stream(
            question,
            generate_content_request
        )

        return response