import pytest
from tier_3_gold.xero_bridge import XeroClient, XeroInvoice

def test_xero_invoice_creation():
    client = XeroClient()
    inv = XeroInvoice(
        contact_name="Client A",
        amount=500.00,
        date="2026-01-01",
        description="Services"
    )
    assert client.create_invoice(inv) is True