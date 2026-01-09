import pytest
from pathlib import Path
from tier_3_gold.finance import FinancialEngine, Transaction

def test_financial_rules():
    engine = FinancialEngine()
    
    t1 = Transaction(date="2026-01-01", description="Uber Trip", amount=-15.00)
    engine._categorize(t1)
    assert t1.category == "Travel"

    t2 = Transaction(date="2026-01-01", description="Random Vendor", amount=-50.00)
    engine.brain.think = lambda x: True 
    engine._categorize(t2)
    assert t2.category == "Needs Review"

def test_csv_parsing(tmp_path):
    csv_file = tmp_path / "bank.csv"
    csv_file.write_text("Date,Description,Amount\n2026-01-01,Starbucks,-5.00")
    
    engine = FinancialEngine()
    transactions = engine.process_csv(csv_file)
    
    assert len(transactions) == 1
    assert transactions[0].category == "Meals"