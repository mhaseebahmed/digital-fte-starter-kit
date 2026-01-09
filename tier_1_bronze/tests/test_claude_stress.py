import pytest
from unittest.mock import MagicMock, patch
from tier_1_bronze.claude_client import ClaudeClient

def test_claude_timeout_handling():
    client = ClaudeClient()
    with patch("subprocess.run", side_effect=TimeoutError):
        result = client.think("prompt")
        assert result is False

def test_claude_utf8_error():
    client = ClaudeClient()
    mock_res = MagicMock()
    mock_res.stdout = b'\x80abc' 
    
    with patch("subprocess.run", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "")):
        result = client.think("prompt")
        assert result is False
