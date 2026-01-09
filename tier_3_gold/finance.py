import csv
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict
from shared_foundation.logger import setup_logger
from tier_1_bronze.claude_client import ClaudeClient

logger = setup_logger("finance_engine")

@dataclass
class Transaction:
    date: str
    description: str
    amount: float
    category: str = "Uncategorized"

class FinancialEngine:
    def __init__(self):
        self.brain = ClaudeClient()
        self.rules = {
            "uber": "Travel",
            "lyft": "Travel",
            "starbucks": "Meals",
            "aws": "Software",
            "github": "Software",
            "subway": "Meals",
            "delta": "Travel"
        }

    def process_csv(self, file_path: Path) -> List[Transaction]:
        transactions = []
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    desc = row.get('Description') or row.get('Memo') or row.get('Payee')
                    amt = row.get('Amount') or row.get('Debit') or row.get('Value')
                    date = row.get('Date') or row.get('Posting Date')
                    
                    if not desc or not amt: continue

                    t = Transaction(
                        date=date,
                        description=desc,
                        amount=float(amt.replace('$', '').replace(',', ''))
                    )
                    self._categorize(t)
                    transactions.append(t)
        except Exception as e:
            logger.error(f"Failed to process CSV {file_path}: {e}")
            return []
        return transactions

    def _categorize(self, transaction: Transaction):
        desc_lower = transaction.description.lower()
        for keyword, category in self.rules.items():
            if keyword in desc_lower:
                transaction.category = category
                logger.info(f"⚡ Auto-Categorized '{transaction.description}' as {category}")
                return
        
        prompt = f"Categorize this bank transaction: '{transaction.description}' ($ {transaction.amount}). Return ONLY the category name."
        transaction.category = "Needs Review" 
        logger.info(f"⚠️ Flagged for Review: {transaction.description}")

    def generate_report(self, transactions: List[Transaction]) -> str:
        total_spend = sum(t.amount for t in transactions if t.amount < 0)
        total_income = sum(t.amount for t in transactions if t.amount > 0)
        
        categories: Dict[str, float] = {}
        for t in transactions:
            categories[t.category] = categories.get(t.category, 0) + t.amount

        report = f"""# 💰 Financial Pulse
**Period:** {transactions[0].date if transactions else 'Unknown'} - {transactions[-1].date if transactions else 'Unknown'}

## 📊 Summary
- **Income:** ${total_income:,.2f}
- **Expenses:** ${total_spend:,.2f}
- **Net:** ${total_income + total_spend:,.2f}

## 📂 Categorization
"""
        for cat, amount in categories.items():
            report += f"- **{cat}:** ${amount:,.2f}\n"
        return report