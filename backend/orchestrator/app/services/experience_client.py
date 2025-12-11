import os
from app.utils.http_client import AsyncHttpClient

EXPERIENCE_URL = os.getenv("EXPERIENCE_URL", "http://localhost:8005")


async def log(client: AsyncHttpClient, experience: dict) -> dict:
    if os.getenv("DEV_MOCK_MODE", "0") == "1":
        return {"ok": True, "data": {"id": f"mock-{int(experience.get('timestamp', 0))}", "timestamp": experience.get("timestamp")}}
    url = f"{EXPERIENCE_URL.rstrip('/')}/api/v1/log"
    resp = await client.post(url, json=experience)
    if not resp.get("ok"):
        raise RuntimeError("experience log failed")
    return resp
