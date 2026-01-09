import pytest
import logging
from pathlib import Path
from pydantic import ValidationError
from shared_foundation.config import GlobalConfig
from shared_foundation.logger import PIILogFilter, setup_logger
from shared_foundation.exceptions import TransientError, ConfigurationError

def test_config_invalid_env_value():
    with pytest.raises(ValidationError):
        GlobalConfig(ENV="staging", _env_file=None) 

def test_config_invalid_poll_interval():
    with pytest.raises(ValidationError):
        GlobalConfig(POLL_INTERVAL=1, _env_file=None) 

def test_config_path_validation(tmp_path):
    f = tmp_path / "file.txt"
    f.touch()
    
    with pytest.raises(ValidationError):
        GlobalConfig(VAULT_PATH=f, _env_file=None)

@pytest.mark.parametrize("secret, message, expected", [
    ("123", "User 123 login", "User [REDACTED] login"),
    ("abc", "abc", "[REDACTED]"),
    (None, "User 123", "User 123"), 
    ("key", "No secrets here", "No secrets here"),
])
def test_pii_filter_variations(secret, message, expected):
    log_filter = PIILogFilter(secrets=[secret] if secret else [])
    record = logging.LogRecord("name", logging.INFO, "", 0, message, (), None)
    log_filter.filter(record)
    assert record.msg == expected

def test_logger_file_creation(tmp_path):
    with pytest.MonkeyPatch.context() as m:
        m.setattr("shared_foundation.logger.LOG_DIR", tmp_path)
        logger = setup_logger("test_service")
        logger.info("Test Message")
        
        log_file = tmp_path / "test_service.json"
        assert log_file.exists()
        assert "Test Message" in log_file.read_text()

def test_custom_exceptions():
    try:
        raise TransientError("Network Down")
    except Exception as e:
        assert isinstance(e, TransientError)
        assert str(e) == "Network Down"
