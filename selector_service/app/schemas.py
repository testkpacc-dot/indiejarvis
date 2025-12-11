from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ChooseRequest(BaseModel):
    session_id: str
    context_features: Dict[str, Any] = {}


class ChooseResponse(BaseModel):
    prompt_id: str


class RewardRequest(BaseModel):
    prompt_id: str
    reward: int  # 0 or 1
    metadata: Optional[Dict[str, Any]] = None


class BanditArmOut(BaseModel):
    prompt_id: str
    alpha: int
    beta: int
    samples: int
    risk: str

    class Config:
        from_attributes = True


class ArmsListResponse(BaseModel):
    arms: List[BanditArmOut]
