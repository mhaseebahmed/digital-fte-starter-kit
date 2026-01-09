# The Brains
> **Cognitive Interfaces for Reasoning.**

This module wraps the LLM (Large Language Model) CLI tools into Python classes that handle timeouts and error parsing.

## Modules

### 1. `claude_client.py`
- **Role:** Wrapper around the `@anthropic/claude-code` CLI.
- **Key Features:**
    - **Timeouts:** Kills the process if it hangs for more than 5 minutes.
    - **Subprocess Isolation:** Runs Claude in a separate memory space to prevent leaks.
    - **Logging:** Captures `stdout` and `stderr` for audit trails.

## Usage
```python
from src.brains.claude_client import ClaudeClient

brain = ClaudeClient()
success = brain.think("Analyze this invoice.")
```
