from pathlib import Path
import sys

# Hack to import from src without installing package yet
sys.path.append(str(Path(__file__).parent.parent))

from src.foundation.config import settings
from src.foundation.logger import setup_logger

logger = setup_logger("setup")

def build_office():
    root = settings.VAULT_PATH
    
    folders = [
        "00_Inbox", "10_Processing", "20_Done",
        "30_Pending_Approval", "40_Approved", "99_Logs/System", "System"
    ]

    for f in folders:
        (root / f).mkdir(parents=True, exist_ok=True)
        logger.info(f"📂 Created: {f}")

    # Handbook
    handbook = root / "System" / "Company_Handbook.md"
    if not handbook.exists():
        handbook.write_text("# Handbook\n1. Safety First.\n2. Be concise.")
        logger.info("📘 Created Handbook")

if __name__ == "__main__":
    build_office()

