# Reward request schema
from pydantic import BaseModel

class RewardRequest(BaseModel):
    prompt_id: str
    reward: int  # 0 or 1

class ChooseResponse(BaseModel):
    prompt_id: str

class ArmInfo(BaseModel):
    prompt_id: str
    alpha: int
    beta: int
    samples: int
    risk: str
    
    class Config:
        from_attributes = True

