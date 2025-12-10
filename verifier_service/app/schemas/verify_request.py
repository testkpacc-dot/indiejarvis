# Verify request schema
from pydantic import BaseModel

class VerifyRequest(BaseModel):
    response: str
    context: str = ""
