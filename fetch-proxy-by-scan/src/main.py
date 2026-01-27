 """
 Function: Proxy Scanner CLI Application
 Business Problem: 提供命令行接口，允许用户指定代理列表文件和目标URL，执行大规模并发代理验证并输出可用结果。
 """
 
 import asyncio
 import argparse
 import sys
 from typing import List
 from scanner import ProxyScanner
 from sources import ProxyFetcher
 
 def load_proxies(file_path: str) -> List[str]:
     """Load proxies from a file"""
     try:
         with open(file_path, 'r', encoding='utf-8') as f:
             lines = [line.strip() for line in f if line.strip()]
         return lines
     except FileNotFoundError:
         print(f"[!] Error: File not found: {file_path}")
         sys.exit(1)
 
 async def main():
     parser = argparse.ArgumentParser(description="High Performance Async Proxy Scanner")
     parser.add_argument("-f", "--file", type=str, help="Path to proxy list file (one per line)")
     parser.add_argument("--fetch", action="store_true", help="Fetch proxies from public sources")
     parser.add_argument("-t", "--target", type=str, default="http://httpbin.org/ip", help="Target URL to verify against")
     parser.add_argument("-o", "--output", type=str, default="active_proxies.txt", help="Output file for active proxies")
     parser.add_argument("-l", "--limit", type=int, default=100, help="Concurrency limit (default: 100)")
     
     args = parser.parse_args()
 
     proxies = []
     
     if args.fetch:
         print("[*] Fetching public proxies...")
         fetched = await ProxyFetcher.fetch_all()
         print(f"[*] Fetched {len(fetched)} unique proxies.")
         proxies.extend(fetched)
 
     if args.file:
         file_proxies = load_proxies(args.file)
         print(f"[*] Loaded {len(file_proxies)} proxies from {args.file}")
         proxies.extend(file_proxies)
 
     if not proxies:
         print("[!] No proxies provided. Use -f to specify a file or --fetch to get from internet.")
         sys.exit(1)
     
     # Remove duplicates from combined sources
     proxies = list(set(proxies))
     print(f"[*] Total unique proxies to scan: {len(proxies)}")
     
     scanner = ProxyScanner(target_url=args.target, limit=args.limit)
     results = await scanner.run(proxies)
     
     # Save results
     if results:
         with open(args.output, 'w', encoding='utf-8') as f:
             for r in results:
                 # Format: protocol://url,latency
                 line = f"{r.protocol}://{r.url.replace('http://','').replace('https://','').replace('socks5://','')},{r.latency_ms:.2f}ms"
                 f.write(line + "\n")
         print(f"[+] Saved {len(results)} active proxies to {args.output}")
     else:
         print("[-] No active proxies found.")
 
 if __name__ == "__main__":
     try:
         asyncio.run(main())
     except KeyboardInterrupt:
         print("\n[!] Scan interrupted by user.")
