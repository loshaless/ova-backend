from sqlalchemy import Column, Integer, String, Text, Float, ARRAY, TIMESTAMP, func
from app.database.connection import Base

class LLMPromptModel(Base):
    __tablename__ = "llm_prompts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    prompt_text = Column(Text, nullable=False)
    temperature = Column(Float)
    max_tokens = Column(Integer)
    top_p = Column(Float)
    tags = Column(ARRAY(String(255)))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    model_name = Column(String(255), nullable=False)