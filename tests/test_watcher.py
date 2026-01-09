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
def mock_finance():
    return MagicMock()

@pytest.fixture
def handler(mock_brain, mock_finance):
    h = RobustHandler()
    h.brain = mock_brain 
    h.finance = mock_finance
    return h

def test_routing_financial(handler):
    # Test CSV routing
    path = Path("./Vault/10_Processing/bank.csv")
    handler._handle_financial = MagicMock()
    handler._handle_generic = MagicMock()
    
    # Mock stabilization/move to bypass IO
    handler._stabilize_file = MagicMock(return_value=True)
    handler._safe_move = MagicMock(return_value=True)
    
    handler.process_workflow(path)
    
    # Assert Financial Route called
    handler._handle_financial.assert_called()
    handler._handle_generic.assert_not_called()

def test_routing_generic(handler):
    # Test PDF routing
    path = Path("./Vault/10_Processing/invoice.pdf")
    handler._handle_financial = MagicMock()
    handler._handle_generic = MagicMock()
    
    handler._stabilize_file = MagicMock(return_value=True)
    handler._safe_move = MagicMock(return_value=True)
    
    handler.process_workflow(path)
    
    # Assert Generic Route called
    handler._handle_generic.assert_called()
    handler._handle_financial.assert_not_called()