import time
import multiprocessing
import logging
import sys
from watchdog.observers import Observer
from .foundation.logger import setup_logger
from .foundation.config import settings
from .watchers.filesystem import RobustHandler
from .watchers.approval import ApprovalHandler
from .watchers.gmail import run_gmail_loop

logger = setup_logger("orchestrator")

def run_filesystem_watcher():
    """Process 1: Watches the Inbox for new files."""
    logger.info("📡 File Watcher starting...")
    observer = Observer()
    handler = RobustHandler()
    observer.schedule(handler, path=str(settings.get_inbox_path()), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def run_approval_watcher():
    """Process 2: Watches the Approved folder for human signatures."""
    logger.info("🔐 Approval Sentinel starting...")
    observer = Observer()
    handler = ApprovalHandler()
    observer.schedule(handler, path=str(settings.VAULT_PATH / "40_Approved"), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    logger.info("🌟 Digital FTE Silver Tier Orchestrator Online")
    
    # Ensure environment is ready
    settings.get_inbox_path().mkdir(parents=True, exist_ok=True)
    (settings.VAULT_PATH / "40_Approved").mkdir(parents=True, exist_ok=True)

    processes = []
    
    # 1. Start Senses
    p1 = multiprocessing.Process(target=run_filesystem_watcher, name="FileSystemWatcher")
    processes.append(p1)
    
    # 2. Start Approval Sentinel
    p2 = multiprocessing.Process(target=run_approval_watcher, name="ApprovalSentinel")
    processes.append(p2)

    # 3. Start Gmail Sentinel (Silver Tier)
    p3 = multiprocessing.Process(target=run_gmail_loop, name="GmailSentinel")
    processes.append(p3)

    for p in processes:
        p.start()
        logger.info(f"🚀 Started {p.name} (PID: {p.pid})")

    try:
        while True:
            time.sleep(1)
            # Future: Add health checks here
    except KeyboardInterrupt:
        logger.info("🛑 Shutdown signal received. Terminating processes...")
        for p in processes:
            p.terminate()
            p.join()
        logger.info("👋 All systems offline.")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
