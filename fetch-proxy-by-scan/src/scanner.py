 """
 Function: Proxy Scanner Core
 Business Problem: 快速扫描互联网上的代理服务器，验证其可用性、延迟及匿名性，为爬虫系统提供稳定的代理资源池。
 """
 
 import asyncio
 import httpx
 import time
 from typing import List, Dict, Optional, Any
 from dataclasses import dataclass
 
 @dataclass
 class ProxyResult:
     url: str
     is_active: bool
     latency_ms: float
     protocol: Optional[str] = None
     error: Optional[str] = None
     status_code: Optional[int] = None
     server_header: Optional[str] = None
 
 class ProxyScanner:
     def __init__(self, target_url: str = "http://httpbin.org/ip", limit: int = 100, timeout: float = 5.0):
         self.target_url = target_url
         self.semaphore = asyncio.Semaphore(limit)
         self.timeout = timeout
         self.results: List[ProxyResult] = []
 
     async def _probe_protocol(self, proxy_address: str, protocol_label: str) -> Optional[ProxyResult]:
         """Helper to probe a specific protocol."""
         start_time = time.time()
         try:
             proxies = {
                 "http://": proxy_address,
                 "https://": proxy_address,
             }
             
             async with httpx.AsyncClient(proxies=proxies, timeout=self.timeout, follow_redirects=True) as client:
                 resp = await client.get(self.target_url)
                 latency = (time.time() - start_time) * 1000
                 
                 if resp.status_code < 400:
                     return ProxyResult(
                         url=proxy_address,
                         is_active=True,
                         latency_ms=latency,
                         protocol=protocol_label,
                         status_code=resp.status_code,
                         server_header=resp.headers.get("Server")
                     )
         except Exception:
             pass
         return None
 
     async def check_proxy(self, proxy_url: str) -> ProxyResult:
         """
         验证单个代理服务器的可用性，支持协议自动探测。
         """
         async with self.semaphore:
             # If scheme is explicitly provided, test only that.
             if "://" in proxy_url:
                 scheme = proxy_url.split("://")[0]
                 result = await self._probe_protocol(proxy_url, scheme)
                 if result:
                     self.results.append(result)
                     return result
                 else:
                     return ProxyResult(url=proxy_url, is_active=False, latency_ms=0, error="Connection failed")
 
             # Heuristic: Probe protocols based on common ports + fallbacks
             port = proxy_url.split(":")[-1] if ":" in proxy_url else ""
             protocols_to_try = []
 
             if port == "1080":
                 protocols_to_try = [("socks5://", "socks5"), ("http://", "http")]
             else:
                 protocols_to_try = [("http://", "http"), ("socks5://", "socks5")]
 
             for prefix, label in protocols_to_try:
                 target_proxy = f"{prefix}{proxy_url}"
                 result = await self._probe_protocol(target_proxy, label)
                 if result:
                     self.results.append(result)
                     return result
             
             # If all failed
             return ProxyResult(url=proxy_url, is_active=False, latency_ms=0, error="All protocols failed")
 
     async def run(self, proxy_list: List[str]) -> List[ProxyResult]:
         """
         批量执行代理扫描
         """
         print(f"[*] Starting proxy scan for {len(proxy_list)} candidates...")
         print(f"[*] Target: {self.target_url} | Concurrency: {self.semaphore._value}")
         
         tasks = [self.check_proxy(p) for p in proxy_list]
         # Use asyncio.gather to run all tasks
         # In a real heavy scan, might want to stream results or use as_completed
         results = await asyncio.gather(*tasks)
         
         active_count = sum(1 for r in results if r.is_active)
         print(f"[+] Scan completed. Found {active_count} active proxies.")
         return [r for r in results if r.is_active]
