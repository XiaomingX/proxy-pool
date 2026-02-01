# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ProxyPool is a modern, asynchronous proxy pool management system built with Python 3.11+, FastAPI, and Redis. It automatically fetches, validates, and serves high-quality HTTP proxies through a REST API.

## Development Commands

### Setup and Installation
```bash
# Install dependencies (requires uv: https://docs.astral.sh/uv/getting-started/installation/)
uv sync

# Run the application
uv run src/main.py

# Alternative: Run with explicit path
uv run main.py
```

### Docker Deployment
```bash
# Using Docker Compose (includes Redis)
docker-compose up -d

# Build Docker image only
docker build -t proxy-pool .

# Run container (requires external Redis)
docker run -d -p 8000:8000 -e REDIS_HOST=host.docker.internal proxy-pool
```

### Configuration
Create a `.env` file in the root directory to override defaults:
```env
REDIS_HOST=localhost
REDIS_PORT=6379
# REDIS_PASSWORD=your_password
API_HOST=0.0.0.0
API_PORT=8000
```

## Architecture

### Core Components

1. **API Layer** (`src/proxy_pool/api/`)
   - FastAPI-based REST endpoints
   - Routes: `/get`, `/stats`, `/all`
   - Supports both JSON and text response formats

2. **Storage Layer** (`src/proxy_pool/core/storage.py`)
   - Redis-backed storage using Hash data structure
   - Key operations: add, update, increase/decrease score, get_random
   - **Performance Note**: Current implementation uses `hvals()` which loads ALL proxies into memory (O(N) complexity). For large-scale deployments (>10k proxies), consider migrating to Redis Sorted Sets (ZSET) for O(log N) performance.

3. **Scheduler** (`src/proxy_pool/core/scheduler.py`)
   - APScheduler-based task management
   - Fetch task: Runs every 30 minutes
   - Validation task: Runs every 5 minutes
   - Tasks are triggered immediately on startup

4. **Validator** (`src/proxy_pool/core/validator.py`)
   - Validates proxies against `http://httpbin.org/get`
   - Concurrent validation with semaphore limit (200)
   - Score adjustment: +10 on success, -20 on failure
   - Proxies removed when score reaches 0

5. **Fetchers** (`src/proxy_pool/fetchers/`)
   - Base class: `BaseFetcher` (abstract)
   - Current implementations: `KuaidailiFetcher`, `ProxyListPlusFetcher`
   - Uses regex-based HTML parsing
   - To add new fetchers: Extend `BaseFetcher` and register in `scheduler.py`

### Data Model

**Proxy Schema** (`src/proxy_pool/schemas/proxy.py`):
- `host`: IP address
- `port`: Port number
- `score`: Quality score (0-100, default: 10)
- `protocol`: Protocol type (default: "http")
- `anonymous`: Anonymity flag (default: True)
- `source`: Fetcher source name

### Scoring System
- Initial score: 10
- Successful validation: +10 (max: 100)
- Failed validation: -20
- Removal threshold: score ≤ 0

## Technology Stack

- **Package Manager**: `uv` (mandatory for all operations)
- **Web Framework**: FastAPI with `lifespan` context manager
- **HTTP Client**: `aiohttp` for fetching, `httpx` for validation
- **Scheduler**: APScheduler (AsyncIOScheduler)
- **Storage**: Redis (async mode via `redis-py`)
- **Logging**: Loguru
- **Config**: Pydantic Settings with `.env` support

## Coding Standards

- **Python Version**: 3.11+ required
- **Type Hints**: Mandatory for all functions
- **Async First**: All I/O operations must be async
- **Modern FastAPI**: Use `lifespan` context manager, not deprecated `on_event`
- **Style**: Follow PEP 8 (consider using Ruff for linting)
- **Dependencies**: Manage through `pyproject.toml`, use `uv add` to add new packages

## Known Limitations

1. **Storage Scalability**: Current Redis Hash implementation has O(N) complexity for retrieving random proxies. See ARCHITECTURE_REPORT.md for migration path to Sorted Sets.

2. **Validation Single Point of Failure**: All proxies validated against single endpoint (`httpbin.org`). If this service is down, all proxies will fail validation.

3. **Limited Fetcher Sources**: Only 2 proxy sources currently implemented. Fetchers are fragile to HTML structure changes.

4. **No Tests**: Project currently has no test suite.

## API Usage Examples

```bash
# Get a proxy (text format)
curl "http://localhost:8000/get?format=text"

# Get a proxy (JSON format)
curl http://localhost:8000/get

# View pool statistics
curl http://localhost:8000/stats

# List all proxies
curl http://localhost:8000/all

# Use proxy with curl
PROXY=$(curl -s http://localhost:8000/get?format=text)
curl -x "http://$PROXY" https://www.baidu.com -I
```

## Project Philosophy

From `.prompt/Agent.md`:
- **Modern & Fast**: Leverage modern Python tooling (`uv`, `Ruff`, `Pydantic V2`)
- **User-Centric API**: APIs should be convenient and intuitive
- **Async First**: Full async pipeline for high concurrency
- **Reliability**: Only verified, high-scoring proxies are served
