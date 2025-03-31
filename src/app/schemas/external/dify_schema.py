from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field

class RetrievalModel(BaseModel):
    search_method: str = "semantic_search"
    reranking_enable: bool = False
    reranking_mode: Optional[str] = None
    reranking_model: Optional[Dict[str, str]] = None
    weights: Optional[Any] = None
    top_k: int = 10
    score_threshold_enabled: bool = False
    score_threshold: Optional[float] = None

class RetrievalRequest(BaseModel):
    query: str
    retrieval_model: RetrievalModel = Field(default_factory=RetrievalModel)


# RESPONSE
class Record(BaseModel):
    content: str
    score: float
    doc_metadata: Optional[dict] = None