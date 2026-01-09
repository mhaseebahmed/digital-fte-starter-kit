# Changelog

All notable changes to the **Digital FTE Starter Kit** will be documented in this file.

## [1.0.0] - 2026-01-09

### 🚀 Major Features
*   **Gold Tier Release:** Full autonomous loop including Financial Auditing and Executive Reporting.
*   **Silver Tier Release:** Integration of Gmail (OAuth2), WhatsApp (Headless), and Approval Workflows.
*   **Bronze Tier Release:** Robust File System Watcher with upload stabilization logic.

### 🏗️ Architecture
*   **Monorepo Restructure:** Codebase split into `shared_foundation` and tiered modules (`tier_1`, `tier_2`, `tier_3`).
*   **Enterprise Foundation:** Implemented `pydantic` configuration and `python-json-logger`.
*   **Resilience:** Added `tenacity` retry decorators for all network calls.

### 🧪 Quality Assurance
*   **Test Suite:** Added 29 stress tests covering API timeouts, file locks, and CSV parsing edge cases.
*   **CI/CD:** Docker and PM2 configurations added for production deployment.
