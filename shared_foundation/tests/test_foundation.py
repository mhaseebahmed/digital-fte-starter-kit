import logging
import pytest
from pathlib import Path
from shared_foundation.config import GlobalConfig
from shared_foundation.logger import PIILogFilter

def test_config_defaults():
    config = GlobalConfig(_env_file=None)
    assert config.ENV == "dev"
    assert config.VAULT_PATH == Path("./Vault")
    assert config.get_inbox_path() == Path("./Vault/00_Inbox")

def test_pii_filter():
    secret = "super_secret_password"
    log_filter = PIILogFilter(secrets=[secret])
    
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname="", lineno=0,
        msg=f"User login with {secret}", args=(), exc_info=None
    )
    
    log_filter.filter(record)
    
    assert secret not in record.msg
    assert "[REDACTED]" in record.msg