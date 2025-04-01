from pydantic import BaseModel

class GenerateContentRequest(BaseModel):
    prompt_text: str = ""
    temperature: float = 0.1
    top_p: float = 0.7
    max_tokens: int = 8192
    model_name: str = "gemini-2.0-flash-001"