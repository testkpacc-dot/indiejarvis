import os
from app.utils.http_client import AsyncHttpClient

PROMPT_REGISTRY_URL = os.getenv("PROMPT_REGISTRY_URL", "http://localhost:8002")


async def get_prompt(client: AsyncHttpClient, prompt_id: str) -> dict:
    if os.getenv("DEV_MOCK_MODE", "0") == "1":
        return {"prompt_id": prompt_id, "text": f"SYSTEM: Be concise. (mock for {prompt_id})", "metadata": {"risk": "low"}}
    url = f"{PROMPT_REGISTRY_URL.rstrip('/')}/api/v1/prompt/{prompt_id}"
    resp = await client.get(url)
    if not resp.get("ok"):
        raise RuntimeError("prompt registry get failed")
    return resp["data"]
