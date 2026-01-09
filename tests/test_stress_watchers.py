import pytest
import os
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch
from watchdog.events import FileCreatedEvent
from src.watchers.filesystem import RobustHandler
from src.watchers.gmail import GmailSentinel

# --- File Watcher Stress ---

@pytest.fixture
def handler():
    h = RobustHandler()
    h.brain = MagicMock()
    h.finance = MagicMock()
    return h

def test_file_watcher_ignores_zero_byte_files(handler):
    """File created but has 0 bytes (upload start)."""
    with patch("os.path.getsize", return_value=0):
        # We mock sleep to make test fast
        with patch("time.sleep"): 
            result = handler._stabilize_file(Path("test.pdf"))
            assert result is False

def test_file_watcher_handles_disappearing_file(handler):
    """File deleted before processing."""
    with patch("os.path.getsize", side_effect=FileNotFoundError):
        result = handler._stabilize_file(Path("ghost.pdf"))
        assert result is False

def test_file_watcher_permission_error_retry(handler):
    """File locked by Windows (PermissionError)."""
    # Fail twice, then succeed
    with patch("shutil.move") as mock_move:
        mock_move.side_effect = [PermissionError, PermissionError, True]
        with patch("time.sleep"): # Skip delays
            handler._safe_move(Path("src"), Path("dst"))
            assert mock_move.call_count == 3

# --- Gmail Stress ---

@pytest.fixture
def sentinel():
    s = GmailSentinel()
    s.service = MagicMock()
    return s

def test_gmail_handles_empty_response(sentinel):
    """API returns empty dict."""
    sentinel.service.users().messages().list().execute.return_value = {}
    # Should not crash
    sentinel.check_for_mail()

def test_gmail_handles_missing_credentials(sentinel):
    """No creds file should abort gracefully."""
    with patch("pathlib.Path.exists", return_value=False):
        assert sentinel.authenticate() is False

def test_gmail_process_message_failure(sentinel):
    """Message get fails."""
    sentinel.service.users().messages().get().execute.side_effect = Exception("API 500")
    # Should log error but not crash the loop
    try:
        sentinel.process_message("123")
    except Exception:
        pytest.fail("Sentinel crashed on message failure")
