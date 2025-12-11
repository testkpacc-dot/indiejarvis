import os
from app.utils.http_client import AsyncHttpClient

INFERENCE_URL = os.getenv("INFERENCE_URL", "http://localhost:8003")


async def generate(client: AsyncHttpClient, prompt_id: str, prompt_text: str, context: dict) -> dict:
    if os.getenv("DEV_MOCK_MODE", "0") == "1":
        return {"response_text": f"[MOCK] response for: {context.get('query_text')}", "trace": None}
    url = f"{INFERENCE_URL.rstrip('/')}/api/v1/generate"
    payload = {"prompt_id": prompt_id, "prompt_text": prompt_text, "context": context}
    resp = await client.post(url, json=payload)
    if not resp.get("ok"):
        raise RuntimeError("inference generate failed")
    return resp["data"]
