# Gold Tier: The Executive
> **Finance & Strategy.**

This module adds the "Brain Power" to handle money and high-level reporting.

## 📊 The Audit Pipeline

```mermaid
graph LR
    subgraph "Data Sources"
        A[Log Files *.json]
        B[Bank CSVs]
        C[Xero API]
    end

    subgraph "Processing"
        D{Scheduler} -->|Trigger (Mon 9AM)| E[Audit Engine]
        E -->|Read| A
        E -->|Calculate| F[Metrics & KPIs]
        G[Financial Engine] -->|Parse| B
        G -->|Categorize| H[P&L Statement]
    end

    subgraph "Output"
        F --> I(Monday_Briefing.md)
        H --> I
    end
```

## Components
*   **`finance.py`**: Rule-based transaction categorization engine.
*   **`auditor.py`**: Mathematical log analysis.
*   **`xero_bridge.py`**: Accounting integration.
*   **`social_media.py`**: Marketing automation stub.

## Running Tests
```bash
uv run pytest tier_3_gold/tests
```