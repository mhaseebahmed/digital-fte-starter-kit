# Deployment Guide
> **How to keep your Agent alive 24/7/365.**

## Option A: Docker (Recommended for Cloud)
This method isolates the agent in a container.

1.  **Build:**
    ```bash
    docker build -t digital-fte -f deployment/Dockerfile .
    ```
2.  **Run (Background):**
    ```bash
    docker run -d \
      -v $(pwd)/Vault:/app/Vault \
      -v $(pwd)/.env:/app/.env \
      --name my-agent \
      digital-fte
    ```
    *Note: We mount the Vault volume so your files persist even if the container restarts.*

## Option B: PM2 (Recommended for Bare Metal/Linux)
This method runs the agent as a background service on your OS.

1.  **Install PM2:**
    ```bash
    npm install -g pm2
    ```
2.  **Start:**
    ```bash
    pm2 start deployment/ecosystem.config.js
    ```
3.  **Persist (Run on Boot):**
    ```bash
    pm2 startup
    pm2 save
    ```
