import os
import json
from pathlib import Path
from .config import settings

PROMPTS_DIR = Path(settings.PROMPTS_DIR)
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

def save_prompt_file(prompt_id: str, payload: dict) -> str:
    """
    Save prompt JSON under prompts/{prompt_id}.json
    Return relative path as string.
    """
    fname = f"{prompt_id}.json"
    path = PROMPTS_DIR / fname
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return str(path)

def load_prompt_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
