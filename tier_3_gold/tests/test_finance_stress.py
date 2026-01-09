import pytest
import csv
from pathlib import Path
from unittest.mock import MagicMock, patch
from tier_3_gold.finance import FinancialEngine, Transaction

def test_csv_missing_columns(tmp_path):
    f = tmp_path / "bad.csv"
    f.write_text("Date,Amount\n2026-01-01,100") 
    
    engine = FinancialEngine()
    txs = engine.process_csv(f)
    assert len(txs) == 0 

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

