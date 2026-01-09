import logging
import sys
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler
from pathlib import Path
from .config import settings

# Ensure Log Directory Exists
LOG_DIR = settings.VAULT_PATH / "99_Logs" / "System"
LOG_DIR.mkdir(parents=True, exist_ok=True)

class PIILogFilter(logging.Filter):
    def __init__(self, secrets=None):
        super().__init__()
        self.secrets = secrets or []

    def filter(self, record):
        msg = str(record.msg)
        for secret in self.secrets:
            if secret and secret in msg:
                msg = msg.replace(secret, "[REDACTED]")
        record.msg = msg
        return True

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # JSON Handler (File)
    json_handler = RotatingFileHandler(
        LOG_DIR / f"{name}.json", maxBytes=5*1024*1024, backupCount=3
    )
    json_handler.setFormatter(jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    ))
    logger.addHandler(json_handler)

    # Console Handler (Text)
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(console)

    return logger