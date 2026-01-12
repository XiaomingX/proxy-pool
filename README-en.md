# ProxyPool Architect

A modern, fast, and reliable proxy pool built with Python 3.11+, FastAPI, and Redis.

## Features
- **Modern Tech Stack**: FastAPI, aiohttp, Redis, APScheduler, Loguru.
- **Asynchronous**: Fully async from crawling to validation.
- **Weighted Scoring**: Dynamic score-based management (Success +10, Failure -20).
- **Easy Deployment**: Managed by `uv`.

## Quick Start

### 1. Install Redis (Prerequisite)

#### macOS
```bash
brew install redis
brew services start redis
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

### 2. Configuration

Create a `.env` file in the root directory to override default settings if necessary:
```env
REDIS_HOST=localhost
REDIS_PORT=6379
# REDIS_PASSWORD=your_password
```

### 3. Install & Run Project
Ensure you have `uv` installed ([Install uv](https://docs.astral.sh/uv/getting-started/installation/)).

```bash
uv sync
uv run main.py
```

## API Endpoints
- `GET /get`: Get a random high-quality proxy. Supports `format=text`.
- `GET /stats`: View pool health and statistics.
- `GET /all`: List all proxies in the pool.

## Built with
![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)

---

## Deployment with Docker

This project supports rapid deployment via Docker and Docker Compose.

### 1. Using Docker Compose (Recommended)
This is the easiest method, which automatically starts Redis and ProxyPool containers:

```bash
docker-compose up -d
```

### 2. Building ProxyPool Image Only
If you already have a running Redis instance:

```bash
# Build the image
docker build -t proxy-pool .

# Run the container (specify Redis address)
docker run -d -p 8000:8000 -e REDIS_HOST=host.docker.internal proxy-pool
```

---

## Quick Usage Examples

Get a proxy and access Google with `curl`:

```bash
# 1. Get a proxy (plain text format)
PROXY=$(curl -s http://localhost:8000/get?format=text)

# 2. Use the proxy to access a website
curl -x "http://$PROXY" https://www.google.com -I
```

Using in a Python script:

```python
import requests

# Get proxy
proxy = requests.get("http://localhost:8000/get?format=text").text

# Use proxy
proxies = {
    "http": f"http://{proxy}",
    "https": f"http://{proxy}",
}
response = requests.get("https://www.google.com", proxies=proxies)
print(response.status_code)
```


## Main Functions

- Automatically crawl proxy IPs from multiple sources
- Real-time validation of proxy IP availability and speed
- Support for batch processing and scheduled updates
- Simple to use and quick to deploy

## Installation and Execution

1. Clone this repository:

```
git clone https://github.com/XiaomingX/proxypool.git
cd proxypool
```

2. Install dependencies (assuming a Python environment, adjust as needed):

```
pip install -r requirements.txt
```

3. Run the proxy crawling script:

```
python main.py
```

4. Run the proxy validation script:

```
python verify.py
```

## Cybersecurity Projects You Might Like:
 - Port Scanner implemented in Rust:
   - https://github.com/XiaomingX/RustProxyHunter
 - Proxy Pool detection implemented in Python:
   - https://github.com/XiaomingX/proxy-pool
 - Supply chain security & CVE-POC automated collection in Golang (Note: No manual review, use with caution):
   - https://github.com/XiaomingX/data-cve-poc
 - .git leak detection tool implemented in Python:
   - https://github.com/XiaomingX/github-sensitive-hack

## References and Inspiration

This project's design and implementation were inspired by the following excellent open-source projects:

- [ProjectDiscovery Katana](https://github.com/projectdiscovery/katana) —— A modern crawler and spider framework.
- [Spider-rs Spider](https://github.com/spider-rs/spider) —— A high-performance, scalable crawler framework.

## Contribution Guidelines

Feel free to submit issues and pull requests to help us improve.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

*Enjoy using ProxyPool! If you have any questions, please contact the author.*
