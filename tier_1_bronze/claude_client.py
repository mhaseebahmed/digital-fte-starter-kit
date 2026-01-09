import subprocess
import logging
from shared_foundation.logger import setup_logger
from shared_foundation.config import settings

logger = setup_logger("brain")

class ClaudeClient:
    def __init__(self):
        self.cmd = ["claude", "-p"]

    def think(self, prompt: str) -> bool:
        logger.info("🧠 Thinking...", extra={"prompt_preview": prompt[:50]})
        try:
            result = subprocess.run(
                self.cmd + [prompt],
                capture_output=True,
                text=True,
                timeout=300 
            )
            if result.returncode == 0:
                logger.info("✅ Thought Complete")
                return True
            else:
                logger.error(f"❌ Brain Freeze: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            logger.error("⏰ Brain Timeout (5m limit exceeded)")
            return False
        except Exception as e:
            logger.error(f"💥 Brain Error: {e}")
            return False