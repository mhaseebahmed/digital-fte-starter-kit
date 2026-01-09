# Core Foundation
> **The Bedrock of the Digital FTE.**

This module contains the shared libraries that ensure stability, security, and observability across the entire agent.

## Modules

### 1. `config.py` (The DNA)
- **Role:** Loads environment variables from `.env` and validates them using Pydantic.
- **Why:** Prevents the agent from starting with missing keys or invalid paths.
- **Key Feature:** Strict Type Checking. If `POLL_INTERVAL` is "fast", it crashes (because it expects an Integer).

### 2. `logger.py` (The Black Box)
- **Role:** Records every action the agent takes.
- **Format:** Structured JSON (`{"level": "INFO", "msg": "..."}`) for machine readability.
- **Safety:** Includes a **PII Filter** that automatically redacts secrets (like API keys) so they never appear in log files.

### 3. `exceptions.py` (The Vocabulary of Failure)
- **Role:** Defines the specific errors the agent can understand.
- **Types:**
    - `TransientError`: "I should try again later." (Network glitch).
    - `ConfigurationError`: "I cannot start." (Missing file).
    - `SafetyError`: "I am forbidden from doing this." (Unauthorized action).
