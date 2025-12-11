import httpx
from .config import settings

async def write_new_prompt_version(prompt_text: str, version: int):
    prompt_id = f"{settings.NEW_PROMPT_VERSION_PREFIX}{version}_trainer"

    payload = {
        "prompt_id": prompt_id,
        "version": version,
        "text": prompt_text,
        "meta_json": {
            "generated_by": "trainer",
            "canary": True,
            "risk": "low"
        }
    }

    url = f"{settings.PROMPT_REGISTRY_URL}/api/v1/prompt"
    async with httpx.AsyncClient() as client:
        res = await client.post(url, json=payload)
        if res.status_code not in (200, 201):
            return None
        return prompt_id
