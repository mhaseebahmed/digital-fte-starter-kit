import logging
import shutil
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from shared_foundation.logger import setup_logger
from shared_foundation.config import settings
from tier_1_bronze.claude_client import ClaudeClient

logger = setup_logger("approval_watcher")

class ApprovalHandler(FileSystemEventHandler):
    def __init__(self):
        self.brain = ClaudeClient()

    def on_moved(self, event):
        dest_path = Path(event.dest_path)
        approved_dir = settings.VAULT_PATH / "40_Approved"
        
        if dest_path.parent.resolve() == approved_dir.resolve():
            logger.info(f"✅ Signature Detected: {dest_path.name}")
            self._safe_execute(dest_path)
            self._archive_task(dest_path)

    def _safe_execute(self, file_path: Path):
        logger.info(f"🚀 Executing Approved Plan: {file_path.name}")
        prompt = f"The plan in '{file_path}' has been APPROVED by the manager. Execute the actions described in this plan immediately."
        success = self.brain.think(prompt)
        if success:
            logger.info(f"✨ Execution Successful: {file_path.name}")
        else:
            logger.error(f"❌ Execution Failed: {file_path.name}")

    def _archive_task(self, file_path: Path):
        done_dir = settings.get_done_path()
        target = done_dir / file_path.name
        try:
            shutil.move(str(file_path), str(target))
            logger.info(f"📁 Archived to /Done: {target.name}")
        except Exception as e:
            logger.error(f"Failed to archive approved task: {e}")