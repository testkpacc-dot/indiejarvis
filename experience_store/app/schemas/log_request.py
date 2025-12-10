# Log request schema
from pydantic import BaseModel

class LogRequest(BaseModel):
    prompt_id: str
    response: str
    reward: int  # 0 or 1
    is_verified: bool = False
