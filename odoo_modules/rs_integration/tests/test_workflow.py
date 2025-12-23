import unittest
import os
import sys
from unittest.mock import MagicMock, patch
from datetime import date

# Setup Mock Framework
sys.path.append(os.getcwd())
from odoo_modules.rs_integration.tests import mock_odoo

# Import Module
from odoo_modules.rs_integration.models.account_move import AccountMove

class TestAccountMoveWorkflow(unittest.TestCase):
    
    def setUp(self):
        # Setup Invoice
        self.invoice = AccountMove(
            name="INV/2023/001",
            state="posted",
            invoice_date=date.today(),
            amount_total=100.0,
            rs_submission_status="draft"
        )
        
        # Mock Relational Fields
        self.invoice.partner_id = MagicMock()
        self.invoice.partner_id.vat = "123"
        self.invoice.company_id = MagicMock()
        self.invoice.company_id.vat = "456"
        self.invoice.currency_id = MagicMock()
        self.invoice.invoice_line_ids = []
        
        # Mock Methods
        self.invoice.write = MagicMock(side_effect=self.invoice.write)
        self.invoice.message_post = MagicMock()
        
        # Mock Environment and Services
        self.mock_connector = MagicMock()
        self.mock_serializer = MagicMock()
        
        # Configure env lookups
        def env_side_effect(model_name):
            if model_name == 'rs.ge.connector':
                return self.mock_connector
            if model_name == 'rs.xml.serializer':
                return self.mock_serializer
            return MagicMock()
            
        self.invoice.env = MagicMock()
        self.invoice.env.__getitem__.side_effect = env_side_effect

    def test_workflow_success(self):
        """Test the full orchestration flow"""
        # Setup Service Returns
        self.mock_serializer.generate_invoice_xml.return_value = b"<xml/>"
        self.mock_connector.sign_xml.return_value = "signature"
        self.mock_connector.send_invoice.return_value = {
            "submission_id": "123",
            "status": "RECEIVED",
            "message": "OK"
        }
        
        # Execute
        self.invoice.action_send_to_rs_ge()
        
        # Verify Calls
        self.mock_serializer.generate_invoice_xml.assert_called_once_with(self.invoice)
        self.mock_connector.sign_xml.assert_called_once_with(b"<xml/>")
        self.mock_connector.send_invoice.assert_called_once_with(b"<xml/>", "signature")
        
        # Verify State Update
        self.assertEqual(self.invoice.rs_submission_status, 'submitted')
        self.assertEqual(self.invoice.rs_document_id, '123')

    def test_workflow_validation_failure(self):
        """Test that validation stops the flow before calling services"""
        self.invoice.state = 'draft'
        
        with self.assertRaises(mock_odoo.UserError):
            self.invoice.action_send_to_rs_ge()
            
        # Services should NOT be called
        self.mock_serializer.generate_invoice_xml.assert_not_called()

    def test_workflow_service_error(self):
        """Test handling of service layer errors"""
        self.mock_serializer.generate_invoice_xml.return_value = b"<xml/>"
        self.mock_connector.sign_xml.return_value = "signature"
        
        # Simulate Connector Error
        self.mock_connector.send_invoice.side_effect = mock_odoo.UserError("Connection Failed")
        
        with self.assertRaises(mock_odoo.UserError):
            self.invoice.action_send_to_rs_ge()
            
        # Status should NOT change to rejected for connection errors (retry allowed)
        self.assertEqual(self.invoice.rs_submission_status, 'draft')
        
        # Error should be logged
        self.invoice.write.assert_called()
        call_args = self.invoice.write.call_args[0][0]
        self.assertEqual(call_args['rs_last_response'], "Connection Failed")

    def test_workflow_rejection(self):
        """Test handling of REJECTED status from RS.ge"""
        self.mock_serializer.generate_invoice_xml.return_value = b"<xml/>"
        self.mock_connector.sign_xml.return_value = "signature"
        self.mock_connector.send_invoice.return_value = {
            "submission_id": "124",
            "status": "REJECTED",
            "message": "Invalid VAT"
        }
        
        self.invoice.action_send_to_rs_ge()
        
        self.assertEqual(self.invoice.rs_submission_status, 'rejected')
        self.assertEqual(self.invoice.rs_document_id, '124')
        # Verify rejection message was logged
        self.invoice.message_post.assert_called_with(body="RS.ge Rejection: Invalid VAT")

if __name__ == '__main__':
    unittest.main()
