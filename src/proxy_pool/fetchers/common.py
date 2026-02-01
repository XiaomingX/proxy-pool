import re
from proxy_pool.fetchers.base import BaseFetcher
from proxy_pool.schemas.proxy import Proxy
from proxy_pool.utils.logger import logger

class KuaidailiFetcher(BaseFetcher):
    name = "kuaidaili"

    async def fetch(self) -> list[Proxy]:
        """Fetch proxies from kuaidaili."""
        proxies = []
        # Example for multiple pages
        for page in range(1, 4):
            url = f"https://www.kuaidaili.com/free/inha/{page}/"
            html = await self.get_html(url)
            if not html:
                continue
            
            # Simple regex for host:port in typical free proxy lists
            # Note: Real world might need more complex parsing or specialized fetchers
            found = re.findall(r'(\d+\.\d+\.\d+\.\d+)</td>\s*<td.*?>(\d+)</td>', html)
            for host, port in found:
                proxies.append(Proxy(host=host, port=int(port), source=self.name))
            
        logger.info(f"Fetcher {self.name} found {len(proxies)} proxies")
        return proxies

class ProxyListPlusFetcher(BaseFetcher):
    name = "proxylistplus"

    async def fetch(self) -> list[Proxy]:
        proxies = []
        url = "https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1"
        html = await self.get_html(url)
        if html:
            found = re.findall(r'(\d+\.\d+\.\d+\.\d+)</td>\s*<td>(\d+)</td>', html)
            for host, port in found:
                proxies.append(Proxy(host=host, port=int(port), source=self.name))
        logger.info(f"Fetcher {self.name} found {len(proxies)} proxies")
        return proxies
