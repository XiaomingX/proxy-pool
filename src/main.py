import uvicorn
from fastapi import FastAPI
from proxy_pool.api.routes import router
from proxy_pool.utils.config import settings
from proxy_pool.utils.logger import logger

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("ProxyPool starting...")
    from proxy_pool.core.scheduler import scheduler
    scheduler.start()
    
    # Trigger initial tasks
    import asyncio
    asyncio.create_task(scheduler.fetch_task())
    asyncio.create_task(scheduler.validate_task())
    
    yield
    
    # Shutdown logic
    logger.info("ProxyPool shutting down...")

app = FastAPI(title="ProxyPool API", version="0.1.0", lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)