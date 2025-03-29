from pydantic import BaseModel

class GenerateContentRequest(BaseModel):
    prompt_text: str
    temperature: float
    top_p: float
    max_tokens: int
    model_name: str