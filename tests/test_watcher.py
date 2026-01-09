import time
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from watchdog.events import FileCreatedEvent
from src.watchers.filesystem import RobustHandler

@pytest.fixture
def mock_brain():
    return MagicMock()

@pytest.fixture
def handler(mock_brain):
    h = RobustHandler()
    # Inject mock brain
    h.brain = mock_brain 
    return h

def test_ignore_hidden_files(handler):
    # Event for .DS_Store
    event = FileCreatedEvent("./Vault/00_Inbox/.DS_Store")
    
    # Mock the internal logic to fail if called
    handler.process_workflow = MagicMock()
    
    handler.on_created(event)
    
    # Assert process was NOT called
    handler.process_workflow.assert_not_called()

def test_valid_file_triggers_workflow(handler):
    event = FileCreatedEvent("./Vault/00_Inbox/invoice.pdf")
    
    # Mock process
    handler.process_workflow = MagicMock()
    
    handler.on_created(event)
    
    # Assert CALLED
    handler.process_workflow.assert_called_once()
