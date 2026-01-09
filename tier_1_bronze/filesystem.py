import time
import shutil
import os
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from shared_foundation.logger import setup_logger
from shared_foundation.config import settings
from shared_foundation.exceptions import TransientError
from tier_1_bronze.claude_client import ClaudeClient
from tier_3_gold.finance import FinancialEngine

logger = setup_logger("filesystem_watcher")

class RobustHandler(FileSystemEventHandler):
    def __init__(self):
        self.brain = ClaudeClient()
        self.finance = FinancialEngine()

    def on_created(self, event):
        if event.is_directory: return
        
        file_path = Path(event.src_path)
        if file_path.name.startswith("."): return
        
        logger.info(f"👀 Detected: {file_path.name}")
        self.process_workflow(file_path)

    def process_workflow(self, inbox_path: Path):
        if not self._stabilize_file(inbox_path):
            return

        processing_path = settings.get_processing_path() / inbox_path.name
        if not self._safe_move(inbox_path, processing_path):
            return

        # Routing
        if processing_path.suffix.lower() == '.csv':
            self._handle_financial(processing_path)
        else:
            self._handle_generic(processing_path)

        final_path = settings.get_done_path() / inbox_path.name
        self._safe_move(processing_path, final_path)
        
        logger.info("✨ Task Cycle Complete")

    def _handle_financial(self, file_path: Path):
        logger.info("💰 Routing to Financial Engine...")
        transactions = self.finance.process_csv(file_path)
        report = self.finance.generate_report(transactions)
        
        report_name = f"REPORT_{file_path.stem}.md"
        report_path = settings.get_done_path() / report_name
        report_path.write_text(report, encoding='utf-8')
        logger.info(f"📊 Financial Report generated: {report_name}")

    def _handle_generic(self, file_path: Path):
        logger.info("🧠 Routing to Claude Brain...")
        prompt = f"Read the file '{file_path}'. Follow instructions in Vault/System/Company_Handbook.md."
        self.brain.think(prompt)

    def _stabilize_file(self, path: Path) -> bool:
        last_size = -1
        for _ in range(10):
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
        try:
            shutil.move(str(src), str(dst))
            logger.info(f"🚚 Moved to: {dst.name}")
            return True
        except Exception as e:
            logger.error(f"Failed move: {e}")
            raise e