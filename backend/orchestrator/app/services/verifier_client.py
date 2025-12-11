import os
from app.utils.http_client import AsyncHttpClient

VERIFIER_URL = os.getenv("VERIFIER_URL", "http://localhost:8004")


async def verify(client: AsyncHttpClient, prompt_id: str, context: dict, response_text: str) -> dict:
    if os.getenv("DEV_MOCK_MODE", "0") == "1":
        reward = 1 if len(response_text) < 500 else 0
        return {"reward": reward, "tags": ["ok"] if reward else ["needs_review"], "details": {"mock": True}}
    url = f"{VERIFIER_URL.rstrip('/')}/api/v1/verify"
    payload = {"prompt_id": prompt_id, "context": context, "response": response_text}
    resp = await client.post(url, json=payload)
    if not resp.get("ok"):
        raise RuntimeError("verifier verify failed")
    return resp["data"]
