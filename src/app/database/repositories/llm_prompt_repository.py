from sqlalchemy.orm import Session
from typing import Optional

from app.models.llm_prompt_model import LLMPromptModel

class LLMPromptRepository:
    def __init__(self, db_session: Session):
        self.session = db_session
        
    def get_llm_prompt_by_title(self, title: str) -> Optional[LLMPromptModel]:
        return self.session.query(LLMPromptModel).filter(LLMPromptModel.title == title).first()
