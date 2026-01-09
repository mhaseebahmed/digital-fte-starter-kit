# Digital FTE: The Autonomous Agent Starter Kit
> **The production-ready boilerplate for building Full-Time Equivalent AI Employees.**

This repository is the official companion to the [Digital FTE Architectural Specs](https://github.com/mhaseebahmed/Digital_FTE_Architectural_Specs). It provides a pre-configured, tested Python project structure designed for high-agency autonomous work.

## 🚀 Key Features
- **Modern Package Management:** Uses `uv` for lightning-fast, deterministic environment setup.
- **Robust Watchers:** Event-driven file system monitoring with upload-stabilization loops.
- **Enterprise Foundation:** Structured JSON logging, Pydantic-based configuration, and automated retry protocols.
- **Claude Native:** Pre-configured to interact with the Claude Code CLI for local-first reasoning.
- **TDD Backed:** 100% test coverage for core foundation and sensory logic.

---

## 🛠️ Quick Start

### 1. Prerequisites
- **Python 3.12+**
- **UV:** `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **Claude Code CLI:** `npm install -g @anthropic/claude-code`

### 2. Installation
```bash
# Clone and enter
git clone https://github.com/mhaseebahmed/digital-fte-starter-kit.git
cd digital-fte-starter-kit

# Sync environment
uv sync
```

### 3. Setup the Office
```bash
uv run scripts/setup_vault.py
```
This creates your `Vault/` hierarchy and the `Company_Handbook.md`.

### 4. Authenticate Claude
```bash
claude login
```

### 5. Launch the Agent
```bash
uv run src/main.py
```

---

## 🏗️ Project Structure (Tiered Monorepo)
The codebase is organized into atomic tiers to separate concerns.

```text
digital-fte-starter-kit/
├── shared_foundation/      # The Bedrock (Config, Logging, Exceptions)
├── tier_1_bronze/          # Perception (File Watcher, Brain Interface)
├── tier_2_silver/          # Communication (Gmail, WhatsApp, Approval)
├── tier_3_gold/            # Strategy (Finance, Audit, Social Media)
├── src/                    # The Entry Point (Orchestrator)
├── scripts/                # Infrastructure setup tools
├── tests/                  # Automated Test Suite (Pytest)
├── pyproject.toml          # Dependency Management (uv)
└── .gitignore              # Multi-layer privacy filters
```

## 🛡️ Privacy & Security
- **Local-First:** All files, logs, and state remain in your local `Vault/`.
- **Secret Redaction:** Logs automatically scrub sensitive keys.
- **State Machine:** Financial and high-risk actions require manual movement of files to `/Approved/`.

---

## 🤝 Contribution
Built for millions of students and developers. Join the autonomous revolution.