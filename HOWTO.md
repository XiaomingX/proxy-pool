# Proxy Pool HOWTO

This guide provides step-by-step instructions on how to install, run, and use the Proxy Pool application.

## Prerequisites

- **Python 3.11+**
- **Redis**: The application requires a running Redis instance.
- **uv**: The project uses `uv` for dependency management. [Install uv](https://docs.astral.sh/uv/getting-started/installation/).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/XiaomingX/proxypool.git
    cd proxypool
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

## Configuration

1.  **Environment Variables:**
    Create a `.env` file in the root directory to configure the application. You can copy the example below:

    ```env
    # Redis Configuration
    REDIS_HOST=localhost
    REDIS_PORT=6379
    # REDIS_PASSWORD=your_password
    # REDIS_DB=0

    # API Configuration
    API_HOST=0.0.0.0
    API_PORT=8000
    ```

## Running the Application

Start the application using `uv`:

```bash
uv run main.py
```

This will start:
- The **FastAPI** server (default: `http://0.0.0.0:8000`).
- The **Scheduler** (fetching proxies every 30 minutes).
- The **Validator** (validating proxies every 5 minutes).

## Usage Guide

### API Endpoints

Once the application is running, you can interact with it via the following endpoints:

#### 1. Get a Proxy
Fetch a random high-quality proxy (highest score available).

-   **Endpoint:** `GET /get`
-   **Parameters:**
    -   `format` (optional): `json` (default) or `text`.

**Examples:**

*   **JSON Response (Default):**
    ```bash
    curl http://localhost:8000/get
    ```
    *Response:*
    ```json
    {
      "string": "1.2.3.4:8080",
      "score": 100,
      ...
    }
    ```

*   **Text Response (Direct IP:Port):**
    ```bash
    curl "http://localhost:8000/get?format=text"
    ```
    *Response:*
    ```text
    1.2.3.4:8080
    ```

#### 2. View Statistics
Check the health of the proxy pool.

-   **Endpoint:** `GET /stats`

**Example:**
```bash
curl http://localhost:8000/stats
```
*Response:*
```json
{
  "total": 50,
  "high_score": 45,
  "status": "healthy"
}
```

#### 3. List All Proxies
View all proxies currently in the pool.

-   **Endpoint:** `GET /all`

### Core Concepts

-   **Scoring System:**
    -   New proxies start with a score of **10**.
    -   Successful validation: **+10** (Max: 100).
    -   Failed validation: **-20**.
    -   Proxies are **removed** if their score drops to **0**.

-   **Scheduling:**
    -   **Fetch Task:** Runs every 30 minutes to grab new proxies from configured fetchers.
    -   **Validation Task:** Runs every 5 minutes to re-verify existing proxies.

## Troubleshooting

-   **"Pool is empty, refreshing..." (503 Error):**
    This means the pool has no available proxies. Wait for the fetcher to run (you can restart the app to trigger an immediate fetch) or check your network connection/fetcher sources.

-   **Redis Connection Error:**
    Ensure your Redis server is running and the `REDIS_HOST`/`REDIS_PORT` in `.env` are correct.
