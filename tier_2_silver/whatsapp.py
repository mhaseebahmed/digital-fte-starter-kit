import time
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from tenacity import retry, stop_after_attempt, wait_fixed

from shared_foundation.logger import setup_logger
from shared_foundation.config import settings

logger = setup_logger("whatsapp_sentinel")

class WhatsAppSentinel:
    def __init__(self):
        self.state_path = settings.VAULT_PATH / "System" / "whatsapp_state.json"
        self.headless = True

    def login(self):
        logger.info("📱 Launching Headful Browser for Login... Please scan QR Code.")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://web.whatsapp.com")
            try:
                page.wait_for_selector('div[aria-label="Chat list"]', timeout=60000)
                logger.info("✅ Login Successful. Saving Session.")
                page.context.storage_state(path=str(self.state_path))
            except PlaywrightTimeout:
                logger.error("❌ Login Timeout. Please try again.")
            browser.close()

    def run_monitor(self):
        if not self.state_path.exists():
            logger.warning("⚠️ No Session found. Run 'login' first.")
            return

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(storage_state=str(self.state_path))
            page = context.new_page()
            try:
                logger.info("📡 Connecting to WhatsApp...")
                page.goto("https://web.whatsapp.com")
                page.wait_for_selector('div[aria-label="Chat list"]', timeout=30000)
                logger.info("👀 Watching for unread messages...")
                
                while True:
                    unread = page.locator('span[aria-label*="unread"]')
                    if unread.count() > 0:
                        logger.info(f"📨 Detected {unread.count()} unread chats.")
                        self._alert_brain()
                    time.sleep(5)
            except Exception as e:
                logger.error(f"❌ Sentinel Crashed: {e}")
            finally:
                browser.close()

    def _alert_brain(self):
        note = f"WHATSAPP_ACTIVITY_{int(time.time())}.md"
        path = settings.get_inbox_path() / note
        path.write_text("# 📱 WhatsApp Activity Detected\nPlease check the web interface.", encoding='utf-8')
        logger.info(f"🔔 Alert sent to Inbox: {note}")

if __name__ == "__main__":
    sentinel = WhatsAppSentinel()
    if not sentinel.state_path.exists():
        sentinel.login()
    else:
        sentinel.run_monitor()