# Contributing to Digital FTE

We welcome contributions to the Autonomous Agent ecosystem. Please follow these guidelines to ensure stability.

## 🛠️ Development Setup

1.  **Fork & Clone** the repository.
2.  **Install Dependencies:**
    ```bash
    uv sync
    ```
3.  **Install Pre-commit Hooks:**
    ```bash
    uv run pre-commit install
    ```

## 🧪 Testing Protocol
You **must** run the full test suite before submitting a Pull Request.

```bash
uv run pytest
```
*Expected: 29 passed, 0 failed.*

## 📐 Coding Standards
*   **Type Hinting:** All functions must have Python type hints.
*   **Logging:** Never use `print()`. Always use `logger`.
*   **Config:** Never hardcode paths. Use `settings.VAULT_PATH`.

## 🔄 Branching Strategy
*   `master`: Stable, production-ready code.
*   `feat/feature-name`: For new watchers or brains.
*   `fix/bug-name`: For bug fixes.

## 📝 Pull Request Process
1.  Update `CHANGELOG.md` with your changes.
2.  Ensure CI passes.
3.  Request review from maintainers.
