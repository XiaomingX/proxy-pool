from fastapi import APIRouter, HTTPException, Query
from proxy_pool.core.storage import storage
from proxy_pool.schemas.proxy import Proxy
from typing import Literal

router = APIRouter()

@router.get("/get")
async def get_proxy(
    format: Literal["json", "text"] = Query("json", description="Response format")
):
    proxy = await storage.get_random()
    if not proxy:
        raise HTTPException(status_code=503, detail={"msg": "Pool is empty, refreshing..."})
    
    if format == "text":
        return proxy.string
    return proxy

@router.get("/stats")
async def get_stats():
    count = await storage.count()
    proxies = await storage.get_all()
    high_score_count = sum(1 for p in proxies if p.score >= 100)
    
    return {
        "total": count,
        "high_score": high_score_count,
        "status": "healthy" if count > 0 else "empty"
    }

@router.get("/all")
async def get_all_proxies():
    return await storage.get_all()
