from pydantic import BaseModel

class TrainResponse(BaseModel):
    ok: bool
    message: str
    new_prompt_id: str | None = None
