from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LLM_MODE: str = "mock"   # mock | openai | other vendors
    OPENAI_API_KEY: str | None = None
    HOST: str = "127.0.0.1"
    PORT: int = 8003

    class Config:
        env_file = ".env"

settings = Settings()
