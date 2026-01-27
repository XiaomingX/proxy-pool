 # Proxy Hunter HOWTO
 
 High-performance async validation tool for proxy servers, built with Python 3.11+ and `uv`.
 
 ## Quick Start
 
 ### 1. Installation
 
 Ensure you have `uv` installed.
 
 ```bash
 # Initialize environment and install dependencies
 uv sync
 ```
 
 ### 2. Usage Examples
 
 #### Automatically Fetch & Scan Public Proxies
 Fetch fresh proxies from public lists (GitHub, etc.) and verify them:
 ```bash
 uv run src/main.py --fetch
 ```
 
 #### Scan Your Own List
 Scan a local file containing proxies (one per line, e.g., `ip:port`):
 ```bash
 uv run src/main.py -f data/proxies.txt
 ```
 
 #### Combine Sources
 Fetch public proxies AND add your local list:
 ```bash
 uv run src/main.py --fetch -f data/proxies.txt
 ```
 
 ### 3. CLI Options
 
 | Argument | Description | Default |
 |----------|-------------|---------|
 | `--fetch` | Auto-fetch proxies from public internet sources | False |
 | `-f, --file` | Path to a local file containing proxy list | None |
 | `-o, --output`| File path to save active proxies | `active_proxies.txt` |
 | `-t, --target`| Content verification target URL | `http://httpbin.org/ip` |
 | `-l, --limit` | Concurrency limit (higher = faster but riskier) | 100 |
 
 ### 4. Output
 
 Active proxies are saved to `active_proxies.txt` by default, with their latency:
 ```csv
 192.168.1.1:8080,150.20ms
 203.0.113.5:3128,45.10ms
 ```
