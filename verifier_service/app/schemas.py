from typing import Any, Dict, List
from pydantic import BaseModel


class VerifyRequest(BaseModel):
    prompt_id: str
    context: Dict[str, Any]
    response: str


class VerifierResult(BaseModel):
    reward: int
    tags: List[str]
    details: Dict[str, Any]
