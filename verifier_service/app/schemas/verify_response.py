# Verify response schema
from pydantic import BaseModel
from typing import List

class VerifyResponse(BaseModel):
    is_valid: bool
    issues: List[str]
    message: str
