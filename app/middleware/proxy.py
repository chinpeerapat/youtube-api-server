from typing import Optional

import httpx

from app.core.config import settings


class ProxyClient:
    """Shared HTTP client with optional generic proxy support."""

    def __init__(self) -> None:
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                proxy=settings.proxy_url or None,
                timeout=30.0,
                follow_redirects=True,
            )
        return self._client

    async def get(self, url: str, **kwargs) -> httpx.Response:
        return await self.client.get(url, **kwargs)

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None


proxy_client = ProxyClient()
