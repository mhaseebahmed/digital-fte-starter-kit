import logging
import requests
from dataclasses import dataclass
from typing import List
from shared_foundation.logger import setup_logger
from shared_foundation.config import settings

logger = setup_logger("xero_bridge")

@dataclass
class XeroInvoice:
    contact_name: str
    amount: float
    date: str
    description: str

class XeroClient:
    def __init__(self):
        self.base_url = "https://api.xero.com/api.xro/2.0"
        self.tenant_id = "demo-tenant-id" 
        
    def create_invoice(self, invoice: XeroInvoice):
        logger.info(f"🧾 Creating Xero Invoice for {invoice.contact_name}...")
        
        payload = {
            "Type": "ACCREC",
            "Contact": {"Name": invoice.contact_name},
            "Date": invoice.date,
            "LineItems": [{
                "Description": invoice.description,
                "Quantity": 1.0,
                "UnitAmount": invoice.amount,
                "AccountCode": "200" 
            }]
        }
        
        try:
            logger.info("✅ Invoice Sync Successful (Simulated)")
            return True
        except Exception as e:
            logger.error(f"❌ Xero Sync Failed: {e}")
            return False

    def sync_bank_feed(self):
        logger.info("🏦 Pulling Xero Bank Feed...")
        return []