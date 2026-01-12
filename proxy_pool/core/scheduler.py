from apscheduler.schedulers.asyncio import AsyncIOScheduler
from proxy_pool.fetchers.common import KuaidailiFetcher, ProxyListPlusFetcher
from proxy_pool.core.validator import validator
from proxy_pool.core.storage import storage
from proxy_pool.utils.logger import logger

class Scheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.fetchers = [
            KuaidailiFetcher(),
            ProxyListPlusFetcher()
        ]

    async def fetch_task(self):
        """Task to run all fetchers."""
        logger.info("Starting fetch task...")
        for fetcher in self.fetchers:
            try:
                proxies = await fetcher.fetch()
                for proxy in proxies:
                    await storage.add(proxy)
            except Exception as e:
                logger.error(f"Fetcher {fetcher.name} failed: {e}")
        logger.info("Fetch task complete.")

    async def validate_task(self):
        """Task to run validation."""
        await validator.run_validation()

    def start(self):
        # Initial run
        self.scheduler.add_job(self.fetch_task, 'interval', minutes=30, id='fetch_proxies')
        self.scheduler.add_job(self.validate_task, 'interval', minutes=5, id='validate_proxies')
        
        self.scheduler.start()
        logger.info("Scheduler started.")

scheduler = Scheduler()
