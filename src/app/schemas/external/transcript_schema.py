from pydantic import BaseModel

class TTSRequest(BaseModel):
    text: str

class TTSResponse(BaseModel):
    success: bool
    message: str
    data: dict
