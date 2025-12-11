from pydantic import BaseModel
from typing import Optional, Dict, Any


class QueryRequest(BaseModel):
    user_id: str
    session_id: str
    text: str
    features: Optional[Dict[str, Any]] = None
    memory: Optional[Dict[str, Any]] = None
