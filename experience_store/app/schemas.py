from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ExperienceLogIn(BaseModel):
    context: Dict[str, Any]
    prompt_id: str
    response: Dict[str, Any]
    trace: Optional[str] = None
    verifier_result: Dict[str, Any]
    feedback: Optional[Dict[str, Any]] = None


class ExperienceOut(BaseModel):
    id: int
    timestamp: datetime
    context: Dict[str, Any]
    prompt_id: str
    response: Dict[str, Any]
    trace: Optional[str]
    verifier_result: Dict[str, Any]
    feedback: Optional[Dict[str, Any]]

    class Config:
        orm_mode = True


class ExperiencesListResponse(BaseModel):
    items: List[ExperienceOut]
