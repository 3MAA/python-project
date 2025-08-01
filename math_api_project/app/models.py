from pydantic import BaseModel, Field
from datetime import datetime

class PowRequest(BaseModel):
    base: int
    exp: int

class SingleIntRequest(BaseModel):
    n: int

class OperationResponse(BaseModel):
    operation: str
    input_data: str
    result: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
