import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any
from shared_foundation.config import settings
from shared_foundation.logger import setup_logger

logger = setup_logger("audit_engine")

class AuditEngine:
    def __init__(self):
        self.log_dir = settings.VAULT_PATH / "99_Logs" / "System"

    def run_weekly_audit(self) -> str:
        if not self.log_dir.exists():
            return "No logs found to audit."

        stats = {
            "total_events": 0,
            "errors": 0,
            "warnings": 0,
            "active_services": set()
        }
        
        cutoff = datetime.now() - timedelta(days=7)
        
        for log_file in self.log_dir.glob("*.json"):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if not line.strip(): continue
                        try:
                            record = json.loads(line)
                        except json.JSONDecodeError:
                            continue

                        stats["total_events"] += 1
                        level = record.get('levelname', 'INFO')
                        
                        if level == 'ERROR':
                            stats["errors"] += 1
                        elif level == 'WARNING':
                            stats["warnings"] += 1
                            
                        if 'name' in record:
                            stats["active_services"].add(record['name'])
                            
            except Exception as e:
                logger.error(f"Failed to audit file {log_file}: {e}")

        return self._format_report(stats)

    def _format_report(self, stats: Dict[str, Any]) -> str:
        success_rate = 100.0
        if stats["total_events"] > 0:
            success_rate = ((stats["total_events"] - stats["errors"]) / stats["total_events"]) * 100

        return f"""# 🛡️ System Health Audit
**Generated:** {datetime.now().isoformat()}

## 🚦 Vital Signs
- **Health Score:** {success_rate:.1f}%
- **Total Events:** {stats['total_events']}
- **Error Count:** {stats['errors']}

## ⚙️ Active Services
{', '.join(stats['active_services'])}

## 🩺 Diagnosis
""" + ("✅ System is healthy." if success_rate > 95 else "⚠️ System requires attention.")