import time
import shutil
import os
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from ..foundation.logger import setup_logger
from ..foundation.config import settings
from ..brains.claude_client import ClaudeClient

logger = setup_logger("filesystem_watcher")

class RobustHandler(FileSystemEventHandler):
    def __init__(self):
        self.brain = ClaudeClient()

    def on_created(self, event):
        if event.is_directory: return
        
        file_path = Path(event.src_path)
        if file_path.name.startswith("."): return
        
        logger.info(f"👀 Detected: {file_path.name}")
        self.process_workflow(file_path)

    def process_workflow(self, inbox_path: Path):
        """
        The Atomic Lifecycle: Stabilize -> Lock -> Think -> Archive
        """
        if not self._stabilize_file(inbox_path):
            return

        # 1. LOCK (Move to Processing)
        processing_path = settings.get_processing_path() / inbox_path.name
        if not self._safe_move(inbox_path, processing_path):
            return

        # 2. THINK (Call Claude)
        prompt = f"Read the file '{processing_path}'. Follow instructions in Vault/System/Company_Handbook.md."
        success = self.brain.think(prompt)

        # 3. ARCHIVE (Move to Done)
        final_path = settings.get_done_path() / inbox_path.name
        self._safe_move(processing_path, final_path)
        
        if success:
            logger.info("✨ Task Cycle Complete")
        else:
            logger.warning("⚠️ Task Complete (But Brain Reported Errors)")

    def _stabilize_file(self, path: Path) -> bool:
        """Waits for file size to stop changing."""
        last_size = -1
        for _ in range(10): # 10 seconds max
            try:
                current_size = os.path.getsize(path)
                if current_size == last_size and current_size > 0:
                    return True
                last_size = current_size
                time.sleep(1.0)
            except FileNotFoundError:
                return False
        
        logger.error(f"❌ File Stabilization Timeout: {path}")
        return False

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1), retry=retry_if_exception_type(PermissionError))
    def _safe_move(self, src: Path, dst: Path) -> bool:
        """Atomic move with retry for Windows locking."""
        try:
            shutil.move(str(src), str(dst))
            logger.info(f"🚚 Moved to: {dst.name}")
            return True
        except Exception as e:
            logger.error(f"Failed move: {e}")
            raise e