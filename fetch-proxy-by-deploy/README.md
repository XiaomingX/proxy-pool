# Deploy Proxy Server Tutorial

This tutorial guides you through setting up your own high-anonymity proxy server on a fresh Ubuntu cloud server (e.g., Linode, DigitalOcean, AWS).

## Prerequisites

-   A fresh **Ubuntu 20.04/22.04 LTS** server.
-   **Root access** (or sudo privileges).

## Quick Start

1.  **Connect to your server via SSH:**
    ```bash
    ssh root@<YOUR_SERVER_IP>
    ```

2.  **Download and Run the Deployment Script:**
    Copy the `deploy.sh` script to your server and run it.

    ```bash
    # Create the file
    nano deploy.sh
    # (Paste the content of deploy.sh here, verify it, then Save & Exit)
    
    # Give execution permissions
    chmod +x deploy.sh
    
    # Run the script
    ./deploy.sh
    ```

3.  **Follow the Prompts:**
    -   Enter a **Username** (e.g., `myproxyuser`).
    -   Enter a **Password** (e.g., `StrongPassword123!`).

4.  **Get Your Proxy:**
    The script will output your connection string:
    ```text
    http://myproxyuser:StrongPassword123!@<YOUR_IP>:3128
    ```

## Features of this Setup

-   **Authentication:** Protected by username/password (Basic Auth).
-   **High Anonymity:** Configured to hide your client IP (`X-Forwarded-For` removed).
-   **No Caching:** Configured to act as a pure tunnel, not caching content.

## Testing Your Proxy

You can test the proxy from your local machine using `curl`:

```bash
curl -x "http://myproxyuser:StrongPassword123!@<YOUR_IP>:3128" http://httpbin.org/ip
```

If successful, the response should show the **Server's IP**, not your local IP.
