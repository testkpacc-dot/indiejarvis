from fastapi import APIRouter
from pydantic import BaseModel
import os
import asyncio
import httpx

router = APIRouter()


class StatusResponse(BaseModel):
    ok: bool
    services: dict


@router.get("/status", response_model=StatusResponse)
async def status():
    urls = {
        "selector": os.getenv("SELECTOR_URL", "http://localhost:8001"),
        "prompt_registry": os.getenv("PROMPT_REGISTRY_URL", "http://localhost:8002"),
        "inference": os.getenv("INFERENCE_URL", "http://localhost:8003"),
        "verifier": os.getenv("VERIFIER_URL", "http://localhost:8004"),
        "experience": os.getenv("EXPERIENCE_URL", "http://localhost:8005"),
    }

    async def ping(url: str):
        try:
            async with httpx.AsyncClient(timeout=1.5) as c:
                r = await c.get(url.rstrip("/") + "/api/v1/status", timeout=1.5)
                return "ok" if r.status_code == 200 else "unreachable"
        except Exception:
            return "down"

    tasks = [ping(u) for u in urls.values()]
    results = await asyncio.gather(*tasks, return_exceptions=False)
    services = dict(zip(urls.keys(), results))
    return {"ok": True, "services": services}
