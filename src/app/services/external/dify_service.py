from app.core.config import DIFY_DATASET_PROMO_API_KEY, DIFY_BASE_URL, DIFT_WORKFLOW_API_KEY
from typing import Optional, List
import httpx

from app.schemas.external.dify_schema import RetrievalModel, RetrievalRequest, Record, WorkflowRequest


class DifyService:
    BASE_URL = DIFY_BASE_URL

    @classmethod
    async def retrieve_from_knowledge(
        cls,
        dataset_id: str,
        query: str,
        search_method: str = "semantic_search",
        reranking_enable: bool = False,
        top_k: int = 10,
        score_threshold_enabled: bool = False,
        score_threshold: Optional[float] = None
    )-> List[Record]:
        url = f"{cls.BASE_URL}/v1/datasets/{dataset_id}/retrieve"

        headers = {
            "Authorization": f"Bearer {DIFY_DATASET_PROMO_API_KEY}",
            "Content-Type": "application/json"
        }
        retrieval_model = RetrievalModel(
            search_method=search_method,
            reranking_enable=reranking_enable,
            top_k=top_k,
            score_threshold_enabled=score_threshold_enabled,
            score_threshold=score_threshold
        )

        payload = RetrievalRequest(
            query=query,
            retrieval_model=retrieval_model
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload.dict(),
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            knowledge_json = response.json()["records"]
            records: List[Record] = []
            for knowledge in knowledge_json:
                score = knowledge["score"]
                segment = knowledge["segment"]
                content = segment["content"]
                doc_metadata = segment["document"]["doc_metadata"]
                record = Record(
                    score=score,
                    doc_metadata=doc_metadata,
                    content=content
                )
                records.append(record)

            return records

    @classmethod
    async def execute_workflow(cls, workflow_request: WorkflowRequest):
        url = f"{cls.BASE_URL}/v1/workflows/run"

        headers = {
            "Authorization": f"Bearer {DIFT_WORKFLOW_API_KEY}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=workflow_request.model_dump(),
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()