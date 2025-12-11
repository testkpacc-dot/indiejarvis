from pydantic import BaseModel
from typing import Any, Dict, Optional


class QueryResponse(BaseModel):
    response_text: str
    prompt_id: Optional[str]
    verifier_result: Optional[Dict[str, Any]]
    meta: Optional[Dict[str, Any]]
