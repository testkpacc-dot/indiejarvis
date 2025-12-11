from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class PromptIn(BaseModel):
    prompt_id: str
    version: Optional[int] = 1
    text: str
    meta_json: Optional[Dict[str, Any]] = {}

class PromptOut(BaseModel):
    prompt_id: str
    version: int
    text: str
    meta_json: Optional[Dict[str, Any]] = {}
    created_at: datetime
    file_path: Optional[str]

    model_config = {"from_attributes": True}

class PromptListItem(BaseModel):
    prompt_id: str
    version: int
    meta_json: Optional[Dict[str, Any]] = {}

    model_config = {"from_attributes": True}

class ListPromptsResponse(BaseModel):
    items: List[PromptListItem]
