# Base Image: Python 3.12 (Slim)
FROM python:3.12-slim

# 1. Install System Dependencies (Node.js required for Claude)
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Claude Code CLI
RUN npm install -g @anthropic/claude-code

# 3. Install UV (Package Manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 4. Setup Work Directory
WORKDIR /app
COPY . .

# 5. Sync Dependencies
RUN uv sync

# 6. Create Vault Structure (Runtime)
RUN uv run scripts/setup_vault.py

# 7. Command
# Note: You must mount the /app/Vault volume to persist data!
CMD ["uv", "run", "src/main.py"]
