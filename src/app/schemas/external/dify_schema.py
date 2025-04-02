from random import Random
from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field

from app.helper.string_helper import generate_random_string


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

class WorkflowRequest(BaseModel):
    inputs: Optional[dict[str, Any]]
    response_mode: str = "blocking"
    user: str = generate_random_string(10)

# RESPONSE
class Record(BaseModel):
    content: str
    score: float
    doc_metadata: Optional[dict] = None