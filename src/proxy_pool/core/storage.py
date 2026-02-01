import json
import random
from redis import asyncio as aioredis
from proxy_pool.utils.config import settings
from proxy_pool.schemas.proxy import Proxy
from proxy_pool.utils.logger import logger

class RedisClient:
    def __init__(self):
        self.redis = aioredis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )
        self.key = "proxies"

    async def add(self, proxy: Proxy):
        """Add a proxy if it doesn't exist, otherwise ignore."""
        if not await self.redis.hexists(self.key, proxy.string):
            return await self.redis.hset(self.key, proxy.string, proxy.model_dump_json())

    async def update(self, proxy: Proxy):
        """Update proxy information."""
        return await self.redis.hset(self.key, proxy.string, proxy.model_dump_json())

    async def decrease(self, proxy: Proxy):
        """Decrease score and delete if below minimum."""
        proxy.score -= settings.SCORE_DECREMENT
        if proxy.score <= settings.MIN_SCORE:
            logger.info(f"Removing proxy {proxy.string} (score {proxy.score})")
            return await self.redis.hdel(self.key, proxy.string)
        return await self.update(proxy)

    async def increase(self, proxy: Proxy):
        """Increase score up to maximum."""
        proxy.score = min(proxy.score + settings.SCORE_INCREMENT, settings.MAX_SCORE)
        return await self.update(proxy)

    async def get_random(self) -> Proxy | None:
        """Get a random high-score proxy."""
        proxies = await self.redis.hvals(self.key)
        if not proxies:
            return None
        
        proxy_list = [Proxy.model_validate_json(p) for p in proxies]
        max_score = max(p.score for p in proxy_list)
        best_proxies = [p for p in proxy_list if p.score == max_score]
        
        return random.choice(best_proxies)

    async def get_all(self) -> list[Proxy]:
        proxies = await self.redis.hvals(self.key)
        return [Proxy.model_validate_json(p) for p in proxies]

    async def count(self) -> int:
        return await self.redis.hlen(self.key)

storage = RedisClient()
