import pytest
import os
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch
from watchdog.events import FileCreatedEvent
from tier_1_bronze.filesystem import RobustHandler
from tier_2_silver.gmail import GmailSentinel

@pytest.fixture
def handler():
    h = RobustHandler()
    h.brain = MagicMock()
    h.finance = MagicMock()
    return h

def test_file_watcher_ignores_zero_byte_files(handler):
    with patch("os.path.getsize", return_value=0):
        with patch("time.sleep"): 
            result = handler._stabilize_file(Path("test.pdf"))
            assert result is False

def test_file_watcher_handles_disappearing_file(handler):
    with patch("os.path.getsize", side_effect=FileNotFoundError):
        result = handler._stabilize_file(Path("ghost.pdf"))
        assert result is False

def test_file_watcher_permission_error_retry(handler):
    with patch("shutil.move") as mock_move:
        mock_move.side_effect = [PermissionError, PermissionError, True]
        with patch("time.sleep"): 
            handler._safe_move(Path("src"), Path("dst"))
            assert mock_move.call_count == 3

@pytest.fixture
def sentinel():
    s = GmailSentinel()
    s.service = MagicMock()
    return s

def test_gmail_handles_empty_response(sentinel):
    sentinel.service.users().messages().list().execute.return_value = {}
    sentinel.check_for_mail()

def test_gmail_handles_missing_credentials(sentinel):
    with patch("pathlib.Path.exists", return_value=False):
        assert sentinel.authenticate() is False

def test_gmail_process_message_failure(sentinel):
    sentinel.service.users().messages().get().execute.side_effect = Exception("API 500")
    try:
        sentinel.process_message("123")
    except Exception:
        pytest.fail("Sentinel crashed on message failure")