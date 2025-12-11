import os
import requests

EXPERIENCE_STORE_URL = os.getenv("EXPERIENCE_STORE_URL", "http://localhost:8005")
VERIFIER_URL = os.getenv("VERIFIER_URL", "http://localhost:8004")

def fetch_experiences(limit=200):
    url = f"{EXPERIENCE_STORE_URL}/api/v1/experiences?limit={limit}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json().get("data", [])
    except Exception:
        return []

def verify_output(prompt_id, context, new_output):
    payload = {
        "prompt_id": prompt_id,
        "context": context,
        "response": {"text": new_output}
    }
    try:
        resp = requests.post(f"{VERIFIER_URL}/api/v1/verify", json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json().get("data", {"reward": 0})
    except Exception:
        return {"reward": 0}