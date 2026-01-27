 """
 Function: Proxy Source Fetcher
 Business Problem: 从公开的互联网源自动获取代理服务器列表，作为验证引擎的输入源。
 """
 
 import httpx
 import re
 from typing import List, Set
 
 class ProxyFetcher:
     # Public proxy list sources (Text format preferred for simplicity)
     SOURCES = [
         "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
         "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
         # "https://www.sslproxies.org/", # Requires HTML parsing, skipping for simplicity unless needed
     ]
 
     @staticmethod
     async def fetch_all() -> List[str]:
         """
         Fetch unique proxies from all defined sources.
         """
         proxies: Set[str] = set()
         
         async with httpx.AsyncClient(timeout=10.0) as client:
             for url in ProxyFetcher.SOURCES:
                 try:
                     print(f"[*] Fetching from {url}...")
                     resp = await client.get(url)
                     if resp.status_code == 200:
                         # Extract ip:port pattern
                         found = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+", resp.text)
                         print(f"    -> Found {len(found)} proxies.")
                         proxies.update(found)
                     else:
                         print(f"    -> Failed with status {resp.status_code}")
                 except Exception as e:
                     print(f"    -> Error: {str(e)}")
         
         return list(proxies)
