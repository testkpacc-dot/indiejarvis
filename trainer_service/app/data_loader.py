import httpx
from .config import settings

async def load_experiences(limit: int = 256):
    url = f"{settings.EXPERIENCE_URL}/api/v1/experiences"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code != 200:
            return []
        data = r.json().get("data", [])
        return data[:limit]
