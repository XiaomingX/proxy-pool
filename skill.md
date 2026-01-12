# Skills & Capabilities

## Skill 1: Modern Project Setup (uv-based project construction)
**Goal:** Create a modern Python project with environment isolation and clear dependencies.
**Actionable Steps:**
1.  **Initialization:** Use `uv init` to initialize the project structure and generate `pyproject.toml`.
2.  **Dependency Management:** Use `uv add fastapi uvicorn[standard] aiohttp apscheduler redis pydantic-settings loguru` to add core dependencies.
3.  **Development Environment:** Configure `.python-version` to lock the Python version, ensuring consistency in team collaboration.

## Skill 2: Core Logic Implementation (Collection & Intelligent Scoring)
**Goal:** Establish a dynamic proxy pool maintenance mechanism based on scores.
**Actionable Steps:**
1.  **Asynchronous Fetcher:** Define `BaseFetcher` and implement multi-source asynchronous crawling.
2.  **Weighted Scoring System:**
    -   Initial Score: 10
    -   Successful Verification: +10 (max 100)
    -   Failed Verification: -20 (min 0, delete if it reaches 0)
    -   *Purpose:* Only extremely stable proxies are retained long-term.
3.  **Concurrent Verification:** Use `asyncio.Semaphore` to limit the number of concurrent verifications (e.g., 200) to prevent crashing your own machine or getting banned by target websites.

## Skill 3: UX-First API Implementation (User Experience First Interfaces)
**Goal:** Create a flexible and easy-to-integrate proxy acquisition interface.
**Actionable Steps:**
1.  **Smart Polling Strategy (`GET /get`):**
    -   **Logic:** Prioritize returning the highest-scoring (100 points) proxies. Within the highest score bracket, use **Random** or **Round-Robin** strategies to avoid multiple people getting the same IP in a short period.
    -   **Parameter Filtering (Query Params):**
        -   `type`: `http` | `https` (fetch as needed)
        -   `anonymous`: `true` | `false` (whether it is highly anonymous)
    -   **Multi-format Response:**
        -   `format=json` (default): Returns detailed info `{"ip": "...", "port": 8080, "score": 100, "source": "..."}`.
        -   `format=text`: Only returns the `ip:port` string. Convenient for users to call directly in scripts: `proxies={"http": requests.get("...").text}`.
2.  **Health Dashboard (`GET /stats`):**
    -   Returns total pool count, percentage of high-scoring proxies, and the time of the last check.
3.  **Friendly Error Handling:**
    -   When the pool is empty, return HTTP 503 Service Unavailable with a clear JSON message `{"msg": "Pool is empty, refreshing..."}`, instead of letting the client time out.

## Skill 4: Documentation & Developer Experience (Docs & DX)
**Goal:** Let users get the project running within one minute.
**Actionable Steps:**
1.  **README Structure Optimization:**
    -   **Badge:** Prominently display the `Built with uv` badge.
    -   **Quick Start:**
        ```bash
        # Minimalist startup
        git clone ...
        uv sync
        uv run main.py
        ```
    -   **API Documentation:** Showcase screenshots of the Swagger UI (`/docs`) to intuitively demonstrate ease of use.
2.  **Development Guide:** Explain how to add new dependencies via `uv add` and how to write custom Fetcher extensions.
