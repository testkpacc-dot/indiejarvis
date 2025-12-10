# Experience record schema
from pydantic import BaseModel
from datetime import datetime

class ExperienceRecord(BaseModel):
    id: int
    prompt_id: str
    response: str
    reward: int
    is_verified: bool
    timestamp: datetime
    
    class Config:
        from_attributes = True
