import logging
import pytest
from pathlib import Path
from src.foundation.config import GlobalConfig
from src.foundation.logger import PIILogFilter

# 1. Config Test
def test_config_defaults():
    # It should initialize without env vars (Defaults are safe)
    config = GlobalConfig()
    assert config.ENV == "dev"
    assert config.VAULT_PATH == Path("./Vault")
    assert config.get_inbox_path() == Path("./Vault/00_Inbox")

# 2. Logger PII Redaction Test
def test_pii_filter():
    secret = "super_secret_password"
    log_filter = PIILogFilter(secrets=[secret])
    
    # Create a dummy log record
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname="", lineno=0,
        msg=f"User login with {secret}", args=(), exc_info=None
    )
    
    log_filter.filter(record)
    
    # Assert secret is gone
    assert secret not in record.msg
    assert "[REDACTED]" in record.msg
