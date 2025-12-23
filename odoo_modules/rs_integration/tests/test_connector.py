import unittest
import os
import sys
from unittest.mock import MagicMock, patch
import requests

# Setup Mock Framework
sys.path.append(os.getcwd())
from odoo_modules.rs_integration.tests import mock_odoo

# Import Module
from odoo_modules.rs_integration.models.rs_connector import RsGeConnector

class TestRsConnector(unittest.TestCase):
    
    def setUp(self):
        self.connector = RsGeConnector()

    def test_sign_xml(self):
        """Test signing logic"""
        xml_content = b"<Invoice>...</Invoice>"
        signature = self.connector.sign_xml(xml_content)
        self.assertTrue(isinstance(signature, str))
        self.assertTrue(len(signature) > 0)

    def test_sign_empty_xml(self):
        """Test signing empty content raises error"""
        with self.assertRaises(mock_odoo.UserError):
            self.connector.sign_xml(b"")

    @patch('requests.post')
    def test_send_invoice_success(self, mock_post):
        """Test successful API transmission"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "RECEIVED"}
        mock_post.return_value = mock_response
        
        response = self.connector.send_invoice(b"<xml/>", "sig")
        self.assertEqual(response['status'], "RECEIVED")
        
        # Verify headers
        call_args = mock_post.call_args
        headers = call_args[1]['headers']
        self.assertEqual(headers['X-Signature'], "sig")
        self.assertEqual(headers['Content-Type'], "application/xml")

    @patch('requests.post')
    def test_send_invoice_timeout(self, mock_post):
        """Test timeout handling"""
        mock_post.side_effect = requests.exceptions.Timeout
        
        with self.assertRaises(mock_odoo.UserError) as cm:
            self.connector.send_invoice(b"<xml/>", "sig")
        self.assertIn("timed out", str(cm.exception))

    @patch('requests.post')
    def test_send_invoice_connection_error(self, mock_post):
        """Test connection error handling"""
        mock_post.side_effect = requests.exceptions.ConnectionError
        
        with self.assertRaises(mock_odoo.UserError) as cm:
            self.connector.send_invoice(b"<xml/>", "sig")
        self.assertIn("Could not connect", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
