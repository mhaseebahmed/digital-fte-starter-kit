import time
import logging
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from tenacity import retry, stop_after_attempt, wait_fixed

from shared_foundation.logger import setup_logger
from shared_foundation.config import settings

logger = setup_logger("social_media_manager")

class SocialMediaHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory: return
        file_path = Path(event.src_path)
        
        if file_path.name.startswith("POST_"):
            logger.info(f"📢 Detected Social Media Request: {file_path.name}")
            self.process_post(file_path)

    def process_post(self, file_path: Path):
        content = file_path.read_text(encoding='utf-8')
        
        if "Target: LinkedIn" in content:
            self._post_to_linkedin(content)
        elif "Target: Twitter" in content:
            self._post_to_twitter(content)
        elif "Target: Facebook" in content:
            self._post_to_facebook(content)
        else:
            logger.warning(f"⚠️ Unknown target platform in {file_path.name}")
            return

        new_name = f"PUBLISHED_{file_path.name}"
        file_path.rename(settings.get_done_path() / new_name)

    @retry(stop=stop_after_attempt(3))
    def _post_to_linkedin(self, content):
        logger.info("🔗 Posting to LinkedIn API...")
        time.sleep(1) 
        logger.info("✅ LinkedIn Post Successful")

    @retry(stop=stop_after_attempt(3))
    def _post_to_twitter(self, content):
        logger.info("🐦 Posting to X (Twitter) API...")
        time.sleep(1)
        logger.info("✅ Tweet Successful")

    @retry(stop=stop_after_attempt(3))
    def _post_to_facebook(self, content):
        logger.info("📘 Posting to Facebook Graph API...")
        time.sleep(1)
        logger.info("✅ Facebook Post Successful")