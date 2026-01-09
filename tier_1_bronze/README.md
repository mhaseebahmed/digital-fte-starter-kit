# Bronze Tier: The Foundation
> **Perception & Reasoning.**

This module implements the core "Loop": See File -> Think -> Act.

## 🔄 The Logic Loop

```mermaid
sequenceDiagram
    participant User
    participant Watcher
    participant Brain
    participant Vault

    User->>Vault: Drop File (invoice.pdf)
    Vault->>Watcher: Event (OnCreated)
    
    loop Stabilization
        Watcher->>Vault: Check File Size
        Vault->>Watcher: Size = 10MB
        Watcher->>Watcher: Wait 1s
    end
    
    Watcher->>Vault: Move to /10_Processing
    Watcher->>Brain: Invoke Claude ("Analyze this")
    Brain->>Vault: Read File
    Brain->>Vault: Write Result
    Watcher->>Vault: Move to /20_Done
```

## Components
*   **`filesystem.py`**: A robust file watcher with upload stabilization.
*   **`claude_client.py`**: The interface to the Brain.

## Running Tests
```bash
uv run pytest tier_1_bronze/tests
```