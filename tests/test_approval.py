import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from watchdog.events import FileMovedEvent
from src.watchers.approval import ApprovalHandler

@pytest.fixture
def mock_brain():
    return MagicMock()

@pytest.fixture
def handler(mock_brain):
    h = ApprovalHandler()
    h.brain = mock_brain
    return h

def test_approval_triggers_execution(handler, mock_brain):
    # Setup paths
    src = Path("./Vault/30_Pending_Approval/task.md")
    dst = Path("./Vault/40_Approved/task.md")
    
    # Mock Event
    event = FileMovedEvent(src_path=str(src), dest_path=str(dst))
    
    # Mock internal methods
    handler._safe_execute = MagicMock()
    handler._archive_task = MagicMock()
    
    # Trigger
    handler.on_moved(event)
    
    # Assert
    handler._safe_execute.assert_called_once_with(dst)
    handler._archive_task.assert_called_once_with(dst)

def test_approval_ignored_if_not_in_approved_folder(handler):
    # Move to processing instead of approved
    src = Path("./Vault/00_Inbox/task.md")
    dst = Path("./Vault/10_Processing/task.md")
    
    event = FileMovedEvent(src_path=str(src), dest_path=str(dst))
    handler._safe_execute = MagicMock()
    
    handler.on_moved(event)
    
    # Assert NOT called
    handler._safe_execute.assert_not_called()
