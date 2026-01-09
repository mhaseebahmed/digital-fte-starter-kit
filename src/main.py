import time
import multiprocessing
import logging
import sys
import schedule
from watchdog.observers import Observer

# Updated Imports for Tiered Structure
from shared_foundation.logger import setup_logger
from shared_foundation.config import settings

from tier_1_bronze.filesystem import RobustHandler
from tier_2_silver.approval import ApprovalHandler
from tier_2_silver.gmail import run_gmail_loop
from tier_2_silver.whatsapp import WhatsAppSentinel
from tier_3_gold.auditor import AuditEngine

logger = setup_logger("orchestrator")

def run_filesystem_watcher():
    logger.info("📡 File Watcher starting...")
    observer = Observer()
    handler = RobustHandler()
    observer.schedule(handler, path=str(settings.get_inbox_path()), recursive=False)
    observer.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def run_approval_watcher():
    logger.info("🔐 Approval Sentinel starting...")
    observer = Observer()
    handler = ApprovalHandler()
    observer.schedule(handler, path=str(settings.VAULT_PATH / "40_Approved"), recursive=False)
    observer.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def run_whatsapp_sentinel():
    sentinel = WhatsAppSentinel()
    if sentinel.state_path.exists():
        logger.info("📱 WhatsApp Sentinel starting...")
        sentinel.run_monitor()
    else:
        logger.warning("⚠️ WhatsApp Session missing. Skipping Sentinel.")

def run_scheduler():
    logger.info("⏳ Scheduler starting...")
    auditor = AuditEngine()
    
    def job():
        logger.info("⏰ Running Weekly Audit")
        report = auditor.run_weekly_audit()
        report_path = settings.VAULT_PATH / "00_Inbox" / f"Audit_{int(time.time())}.md"
        report_path.write_text(report, encoding='utf-8')
        logger.info("📄 Audit Report Delivered")

    schedule.every().monday.at("09:00").do(job)
    job()
    
    while True:
        schedule.run_pending()
        time.sleep(60)

def main():
    logger.info("🌟 Digital FTE Platinum Tier Orchestrator Online")
    
    settings.get_inbox_path().mkdir(parents=True, exist_ok=True)
    (settings.VAULT_PATH / "40_Approved").mkdir(parents=True, exist_ok=True)

    processes = [
        multiprocessing.Process(target=run_filesystem_watcher, name="FS"),
        multiprocessing.Process(target=run_approval_watcher, name="Approval"),
        multiprocessing.Process(target=run_gmail_loop, name="Gmail"),
        multiprocessing.Process(target=run_whatsapp_sentinel, name="WhatsApp"),
        multiprocessing.Process(target=run_scheduler, name="Scheduler")
    ]

    for p in processes:
        p.start()
        logger.info(f"🚀 Started {p.name} (PID: {p.pid})")

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down...")
        for p in processes:
            p.terminate()
            p.join()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()