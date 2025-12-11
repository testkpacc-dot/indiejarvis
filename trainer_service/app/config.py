from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    EXPERIENCE_URL: str = "http://127.0.0.1:8005"
    PROMPT_REGISTRY_URL: str = "http://127.0.0.1:8002"
    TRAIN_BATCH_SIZE: int = 32
    K_SAMPLES: int = 4
    KL_TARGET: float = 0.01
    LEARNING_RATE: float = 1e-4
    MODEL_PATH: str = "./model.pt"
    NEW_PROMPT_VERSION_PREFIX: str = "p_v"
    HOST: str = "127.0.0.1"
    PORT: int = 8006

    class Config:
        env_file = ".env"

settings = Settings()
