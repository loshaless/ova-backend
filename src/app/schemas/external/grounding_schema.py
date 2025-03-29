from pydantic import BaseModel

class GroundingRequest(BaseModel):
    question: str

class GroundingResponse(BaseModel):
    response: str
