import os
from typing import Optional

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./prompt_registry.db")
    PROMPTS_DIR: str = os.getenv("PROMPTS_DIR", "./prompts")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8002"))

settings = Settings()
