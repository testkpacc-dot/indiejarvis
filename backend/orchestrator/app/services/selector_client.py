import os
from app.utils.http_client import AsyncHttpClient

SELECTOR_URL = os.getenv("SELECTOR_URL", "http://localhost:8001")


async def choose(client: AsyncHttpClient, context: dict) -> str:
    if os.getenv("DEV_MOCK_MODE", "0") == "1":
        return f"mock_prompt_{int(context.get('timestamp', 0))}"
    url = f"{SELECTOR_URL.rstrip('/')}/api/v1/choose"
    payload = {"session_id": context.get("session_id"), "context_features": context.get("features", {})}
    resp = await client.post(url, json=payload)
    if not resp.get("ok"):
        raise RuntimeError("selector choose failed")
    return resp["data"]["prompt_id"]


async def reward(client: AsyncHttpClient, prompt_id: str, reward: int, metadata: dict = None):
    if os.getenv("DEV_MOCK_MODE", "0") == "1":
        return {"ok": True}
    url = f"{SELECTOR_URL.rstrip('/')}/api/v1/reward"
    payload = {"prompt_id": prompt_id, "reward": reward, "metadata": metadata or {}}
    resp = await client.post(url, json=payload)
    if not resp.get("ok"):
        raise RuntimeError("selector reward failed")
    return resp
