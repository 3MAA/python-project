from pydantic import BaseModel, Field
from datetime import datetime

class OperationRequest(BaseModel):
    operation: str
    input_data: str
    result: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
