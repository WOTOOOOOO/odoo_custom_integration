import unittest
import os
import sys
from unittest.mock import MagicMock
from datetime import date

# Setup Mock Framework
sys.path.append(os.getcwd())
from odoo_modules.rs_integration.tests import mock_odoo

# Import Module
from odoo_modules.rs_integration.models.rs_xml_serializer import RsXmlSerializer

class TestRsXmlSerializer(unittest.TestCase):
    
    def setUp(self):
        self.serializer = RsXmlSerializer()
        
        # Setup Mock Invoice
        self.invoice = MagicMock()
        self.invoice.name = "INV/2023/001"
        self.invoice.invoice_date = date(2023, 12, 23)
        self.invoice.amount_total = 150.00
        
        self.invoice.company_id.vat = "987654321"
        self.invoice.company_id.name = "My Company"
        
        self.invoice.partner_id.vat = "123456789"
        self.invoice.partner_id.name = "Customer Ltd"
        
        self.invoice.currency_id.name = "GEL"
        
        # Lines
        line1 = MagicMock()
        line1.display_type = 'product'
        line1.name = "Product A"
        line1.quantity = 1
        line1.price_unit = 100.0
        line1.price_subtotal = 100.0
        
        line2 = MagicMock()
        line2.display_type = 'product'
        line2.name = "Product B"
        line2.quantity = 1
        line2.price_unit = 50.0
        line2.price_subtotal = 50.0
        
        self.invoice.invoice_line_ids = [line1, line2]

    def test_xml_structure(self):
        """Test that generated XML contains key elements"""
        xml_bytes = self.serializer.generate_invoice_xml(self.invoice)
        xml_str = xml_bytes.decode('utf-8')
        
        self.assertIn('<Invoice>', xml_str)
        self.assertIn('<InvoiceNumber>INV/2023/001</InvoiceNumber>', xml_str)
        self.assertIn('<SellerTIN>987654321</SellerTIN>', xml_str)
        self.assertIn('<BuyerTIN>123456789</BuyerTIN>', xml_str)
        self.assertIn('<TotalAmount>150.0</TotalAmount>', xml_str)
        self.assertIn('<Product>Product A</Product>', xml_str)
        self.assertIn('<Product>Product B</Product>', xml_str)

    def test_missing_invoice_number(self):
        """Test validation for missing invoice number"""
        self.invoice.name = False
        with self.assertRaises(mock_odoo.UserError):
            self.serializer.generate_invoice_xml(self.invoice)

if __name__ == '__main__':
    unittest.main()
