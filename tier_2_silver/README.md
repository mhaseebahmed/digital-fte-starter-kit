# Silver Tier: The Assistant
> **Communication & Approval.**

This module adds external senses (Gmail, WhatsApp) and the critical Human-in-the-Loop safety valve.

## 🔐 OAuth2 Authentication Flow (Gmail)

```mermaid
sequenceDiagram
    participant Agent
    participant LocalStore
    participant Google

    Agent->>LocalStore: Check token.json
    alt Token Missing
        Agent->>Google: Open Login URL
        Google->>Agent: Return Auth Code
        Agent->>Google: Exchange for Token
        Agent->>LocalStore: Save token.json
    else Token Expired
        Agent->>Google: Use Refresh Token
        Google->>Agent: New Access Token
    end
    Agent->>Google: Fetch Emails
```

## ✋ Human-in-the-Loop State Machine

```mermaid
stateDiagram-v2
    [*] --> Pending: Agent Creates Draft
    Pending --> Approved: Human Moves File
    Pending --> Rejected: Human Moves File
    Approved --> Executing: Watcher Detects Move
    Executing --> Done: Task Completed
    Rejected --> [*]: Task Cancelled
```

## Components
*   **`gmail.py`**: OAuth2 Polling engine.
*   **`whatsapp.py`**: Headless browser sentinel.
*   **`approval.py`**: State machine for manual sign-off.

## Running Tests
```bash
uv run pytest tier_2_silver/tests
```