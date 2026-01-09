import logging
import shutil
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from ..foundation.logger import setup_logger
from ..foundation.config import settings
from ..brains.claude_client import ClaudeClient

logger = setup_logger("approval_watcher")

class ApprovalHandler(FileSystemEventHandler):
    def __init__(self):
        self.brain = ClaudeClient()

    def on_moved(self, event):
        """
        Detects when a file is moved into the /40_Approved directory.
        """
        dest_path = Path(event.dest_path)
        
        # Security: Only trigger if the destination is exactly the Approved folder
        approved_dir = settings.VAULT_PATH / "40_Approved"
        
        # We resolve to ensure absolute path comparison
        if dest_path.parent.resolve() == approved_dir.resolve():
            logger.info(f"✅ Signature Detected: {dest_path.name}")
            self._safe_execute(dest_path)
            self._archive_task(dest_path)

    def _safe_execute(self, file_path: Path):
        """Calls the Brain to execute the approved plan."""
        logger.info(f"🚀 Executing Approved Plan: {file_path.name}")
        
        prompt = (
            f"The plan in '{file_path}' has been APPROVED by the manager. "
            "Execute the actions described in this plan immediately using your available tools."
        )
        
        success = self.brain.think(prompt)
        
        if success:
            logger.info(f"✨ Execution Successful: {file_path.name}")
        else:
            logger.error(f"❌ Execution Failed: {file_path.name}")

    def _archive_task(self, file_path: Path):
        """Moves the executed plan to the Done folder."""
        done_dir = settings.get_done_path()
        target = done_dir / file_path.name
        
        try:
            shutil.move(str(file_path), str(target))
            logger.info(f"📁 Archived to /Done: {target.name}")
        except Exception as e:
            logger.error(f"Failed to archive approved task: {e}")
