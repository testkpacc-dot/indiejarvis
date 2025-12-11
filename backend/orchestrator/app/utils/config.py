import os

SELECTOR_URL = os.getenv("SELECTOR_URL", "http://localhost:8001")
PROMPT_REGISTRY_URL = os.getenv("PROMPT_REGISTRY_URL", "http://localhost:8002")
INFERENCE_URL = os.getenv("INFERENCE_URL", "http://localhost:8003")
VERIFIER_URL = os.getenv("VERIFIER_URL", "http://localhost:8004")
EXPERIENCE_URL = os.getenv("EXPERIENCE_URL", "http://localhost:8005")
PROMPT_SQLITE_PATH = os.getenv("PROMPT_SQLITE_PATH", "")
DEV_MOCK_MODE = os.getenv("DEV_MOCK_MODE", "0")
