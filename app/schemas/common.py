# SECTION 1: Imports
from pydantic import BaseModel


# SECTION 2: API Schemas
class ChatRequest(BaseModel):
    message: str


class PredictionResponse(BaseModel):
    label: str
    probability: float
    explanation: str
