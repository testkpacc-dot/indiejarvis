import os
import requests

EXPERIENCE_STORE_URL = os.getenv("EXPERIENCE_STORE_URL", "http://localhost:8005")
VERIFIER_URL = os.getenv("VERIFIER_URL", "http://localhost:8004")

DEBUG = os.getenv("DEBUG_UTILS", "0") == "1"


def fetch_experiences(limit=200):
    """
    Retrieve experience logs from the Experience Store.
    Returns an empty list on failure to avoid pipeline crashes.
    """
    url = f"{EXPERIENCE_STORE_URL}/api/v1/experiences?limit={limit}"

    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        if DEBUG:
            print(f"[UTILS] Fetched {len(data)} experiences.")
        return data
    except Exception as e:
        if DEBUG:
            print(f"[UTILS] Error fetching experiences: {e}")
        return []


def verify_output(prompt_id, context, new_output):
    """
    Send output to the Verifier microservice.

    Expected return structure:
        {"reward": 1 or 0}

    This function ALWAYS returns a valid dict to prevent RL failures.
    """
    payload = {
        "prompt_id": prompt_id,
        "context": context,
        "response": {"text": new_output}
    }

    try:
        resp = requests.post(
            f"{VERIFIER_URL}/api/v1/verify",
            json=payload,
            timeout=5
        )
        resp.raise_for_status()
        data = resp.json().get("data", {})

        reward = data.get("reward", 0)
        if DEBUG:
            print(f"[UTILS] Verification reward: {reward}")

        return {"reward": reward}

    except Exception as e:
        if DEBUG:
            print(f"[UTILS] Verifier error: {e}")
        return {"reward": 0}
