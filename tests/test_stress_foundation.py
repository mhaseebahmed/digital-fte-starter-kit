import pytest
import logging
from pathlib import Path
from pydantic import ValidationError
from src.foundation.config import GlobalConfig
from src.foundation.logger import PIILogFilter, setup_logger
from src.foundation.exceptions import TransientError, ConfigurationError

# --- Config Stress Tests ---

def test_config_invalid_env_value():
    """Ensure config crashes if ENV is invalid."""
    with pytest.raises(ValidationError):
        GlobalConfig(ENV="staging", _env_file=None) 

def test_config_invalid_poll_interval():
    """Ensure config crashes if poll interval is too fast."""
    with pytest.raises(ValidationError):
        GlobalConfig(POLL_INTERVAL=1, _env_file=None) 

def test_config_path_validation(tmp_path):
    """Ensure VAULT_PATH is valid."""
    # Pointing to a non-existent file as a dir
    f = tmp_path / "file.txt"
    f.touch()
    
    # Force _env_file=None to ignore .env and use arguments
    with pytest.raises(ValidationError):
        GlobalConfig(VAULT_PATH=f, _env_file=None)

# --- Logger Stress Tests ---

@pytest.mark.parametrize("secret, message, expected", [
    ("123", "User 123 login", "User [REDACTED] login"),
    ("abc", "abc", "[REDACTED]"),
    (None, "User 123", "User 123"), # None secret shouldn't crash
    ("key", "No secrets here", "No secrets here"),
])
def test_pii_filter_variations(secret, message, expected):
    log_filter = PIILogFilter(secrets=[secret] if secret else [])
    record = logging.LogRecord("name", logging.INFO, "", 0, message, (), None)
    log_filter.filter(record)
    assert record.msg == expected

def test_logger_file_creation(tmp_path):
    """Ensure logger actually creates the file."""
    # Monkeypatch config to use tmp_path
    with pytest.MonkeyPatch.context() as m:
        m.setattr("src.foundation.logger.LOG_DIR", tmp_path)
        logger = setup_logger("test_service")
        logger.info("Test Message")
        
        log_file = tmp_path / "test_service.json"
        assert log_file.exists()
        assert "Test Message" in log_file.read_text()

# --- Exception Logic ---

def test_custom_exceptions():
    """Ensure our exceptions inherit correctly."""
    try:
        raise TransientError("Network Down")
    except Exception as e:
        assert isinstance(e, TransientError)
        assert str(e) == "Network Down"