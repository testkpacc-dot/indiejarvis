import os
import requests

EXPERIENCE_STORE_URL = os.getenv("EXPERIENCE_STORE_URL", "http://localhost:8005")
VERIFIER_URL = os.getenv("VERIFIER_URL", "http://localhost:8004")

def fetch_experiences(limit=200):
    url = f"{EXPERIENCE_STORE_URL}/api/v1/experiences?limit={limit}"
    return requests.get(url).json()["data"]

def verify_output(prompt_id, context, new_output):
    payload = {
        "prompt_id": prompt_id,
        "context": context,
        "response": {"text": new_output}
    }
    return requests.post(f"{VERIFIER_URL}/api/v1/verify", json=payload).json()["data"]
