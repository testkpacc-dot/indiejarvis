from pydantic import BaseModel
from typing import Any, Dict

class GenerateRequest(BaseModel):
    prompt_text: str
    context: Dict[str, Any] = {}

class GenerateResponse(BaseModel):
    response_text: str
    trace: str | None = None
    model: str = "mock-llm"
