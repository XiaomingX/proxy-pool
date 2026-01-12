import asyncio
import aiohttp
from proxy_pool.schemas.proxy import Proxy
from proxy_pool.core.storage import storage
from proxy_pool.utils.logger import logger
from proxy_pool.utils.config import settings

class Validator:
    def __init__(self):
        self.test_url = "http://httpbin.org/get"
        self.semaphore = asyncio.Semaphore(200)  # Concurrent validation limit

    async def validate_one(self, proxy: Proxy):
        """Validate a single proxy and update storage."""
        async with self.semaphore:
            proxy_url = f"http://{proxy.string}"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        self.test_url, 
                        proxy=proxy_url, 
                        timeout=10,
                        allow_redirects=False
                    ) as response:
                        if response.status == 200:
                            await storage.increase(proxy)
                            return True
            except Exception:
                pass
            
            await storage.decrease(proxy)
            return False

    async def run_validation(self):
        """Run validation for all stored proxies."""
        proxies = await storage.get_all()
        if not proxies:
            logger.info("No proxies to validate.")
            return

        logger.info(f"Starting validation for {len(proxies)} proxies...")
        tasks = [self.validate_one(p) for p in proxies]
        await asyncio.gather(*tasks)
        logger.info("Validation cycle complete.")

validator = Validator()
