import pytest
import csv
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.brains.finance import FinancialEngine, Transaction
from src.brains.claude_client import ClaudeClient

# --- Finance Engine Stress ---

def test_csv_missing_columns(tmp_path):
    f = tmp_path / "bad.csv"
    f.write_text("Date,Amount\n2026-01-01,100") # Missing Description
    
    engine = FinancialEngine()
    txs = engine.process_csv(f)
    assert len(txs) == 0 # Should skip bad row

def test_csv_currency_formatting(tmp_path):
    f = tmp_path / "money.csv"
    f.write_text("Date,Description,Amount\n2026-01-01,Uber,\"$1,200.50\"")
    
    engine = FinancialEngine()
    txs = engine.process_csv(f)
    assert txs[0].amount == 1200.50

def test_csv_empty_file(tmp_path):
    f = tmp_path / "empty.csv"
    f.touch()
    engine = FinancialEngine()
    txs = engine.process_csv(f)
    assert len(txs) == 0

# --- Claude Client Stress ---

def test_claude_timeout_handling():
    client = ClaudeClient()
    # Mock subprocess to timeout
    with patch("subprocess.run", side_effect=TimeoutError):
        result = client.think("prompt")
        assert result is False

def test_claude_utf8_error():
    client = ClaudeClient()
    # Mock return with garbage bytes
    mock_res = MagicMock()
    mock_res.stdout = b'\x80abc' # Invalid UTF-8
    
    # In real code we use text=True, so python handles this,
    # but we test the exception handler generally.
    with patch("subprocess.run", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "")):
        result = client.think("prompt")
        assert result is False
