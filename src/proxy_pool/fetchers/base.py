import aiohttp
from abc import ABC, abstractmethod
from proxy_pool.schemas.proxy import Proxy
from proxy_pool.utils.logger import logger

class BaseFetcher(ABC):
    name: str = "Base"

    @abstractmethod
    async def fetch(self) -> list[Proxy]:
        pass

    async def get_html(self, url: str) -> str | None:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        return await response.text()
            except Exception as e:
                logger.error(f"Fetcher {self.name} failed to get {url}: {e}")
        return None
