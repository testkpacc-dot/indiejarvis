import httpx
import asyncio


class AsyncHttpClient:
    def __init__(self, timeout: float = 8.0, retries: int = 2, backoff: float = 0.25):
        self.timeout = timeout
        self.retries = retries
        self.backoff = backoff
        self._client = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._client.aclose()

    async def post(self, url: str, json: dict):
        last_exc = None
        for i in range(self.retries + 1):
            try:
                r = await self._client.post(url, json=json, timeout=self.timeout)
                r.raise_for_status()
                return r.json()
            except Exception as e:
                last_exc = e
                if i < self.retries:
                    await asyncio.sleep(self.backoff * (i + 1))
        raise last_exc

    async def get(self, url: str):
        last_exc = None
        for i in range(self.retries + 1):
            try:
                r = await self._client.get(url, timeout=self.timeout)
                r.raise_for_status()
                return r.json()
            except Exception as e:
                last_exc = e
                if i < self.retries:
                    await asyncio.sleep(self.backoff * (i + 1))
        raise last_exc
