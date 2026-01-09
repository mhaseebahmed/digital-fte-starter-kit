# The Senses (Watchers)
> **Perception Engines for the Autonomous Agent.**

These scripts run in infinite loops, bridging the gap between the external world (Files, Email) and the internal brain.

## Architecture
All watchers follow the **Observer Pattern**. They do not "act"; they only "detect" and "queue."

### 1. `filesystem.py` (Bronze Tier)
- **Source:** Local Directory (`Vault/00_Inbox`).
- **Trigger:** Operating System Interrupts (via `watchdog`).
- **Safety:** Implements a **Stabilization Loop** to wait for large files (PDFs) to finish uploading before reading them.

### 2. `gmail.py` (Silver Tier)
- **Source:** Gmail API.
- **Trigger:** Polling Interval (60s).
- **Logic:**
    1.  Authenticates via OAuth2 (`token.json`).
    2.  Checks for `UNREAD` emails.
    3.  Converts Email Body -> Markdown.
    4.  Saves to `Vault/00_Inbox`.

### 3. `approval.py` (The Gatekeeper)
- **Source:** `Vault/40_Approved`.
- **Trigger:** File Movement.
- **Role:** This is the **only** watcher allowed to trigger "Execute" commands on the Brain. It enforces the Human-in-the-Loop protocol.
