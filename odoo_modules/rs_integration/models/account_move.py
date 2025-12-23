import logging
import json
from odoo import models, fields, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    rs_submission_status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], string='RS.ge Status', default='draft', copy=False, tracking=True)
    
    rs_document_id = fields.Char(string='RS.ge Document ID', copy=False, readonly=True)
    rs_last_response = fields.Text(string='Last RS.ge Response', copy=False, readonly=True)

    def action_send_to_rs_ge(self):
        """
        Main action triggered by the 'Send to RS.ge' button.
        Delegates logic to specialized service models.
        """
        connector = self.env['rs.ge.connector']
        serializer = self.env['rs.xml.serializer']
        
        for move in self:
            # 1. Idempotence & State Check
            if move.rs_submission_status in ['submitted', 'accepted']:
                raise UserError(_("This invoice has already been submitted to RS.ge."))
            
            # 2. Validation
            move._validate_for_rs_submission()

            try:
                # 3. Generate XML
                xml_content = serializer.generate_invoice_xml(move)

                # 4. Sign XML
                signature = connector.sign_xml(xml_content)

                # 5. Send to API
                response_data = connector.send_invoice(xml_content, signature)

                # 6. Process Response
                move._process_rs_response(response_data)

            except UserError as e:
                # Known errors (validation, connection)
                move.write({'rs_last_response': str(e)})
                raise e
            except Exception as e:
                # Unexpected errors
                error_msg = f"Unexpected Error: {str(e)}"
                move.write({
                    'rs_last_response': error_msg,
                    'rs_submission_status': 'rejected'
                })
                _logger.exception("RS.ge Submission Failed")
                raise UserError(_("An error occurred during submission: %s") % str(e))

    def _validate_for_rs_submission(self):
        """Validates the invoice data against RS.ge requirements."""
        self.ensure_one()
        
        if self.state != 'posted':
            raise UserError(_("Only posted invoices can be submitted to RS.ge."))
        
        if not self.partner_id.vat:
            raise UserError(_("Customer VAT/TIN is missing."))
            
        if not self.company_id.vat:
            raise UserError(_("Company VAT/TIN is missing."))

        if self.amount_total <= 0:
            raise UserError(_("Invoice total amount must be greater than 0."))

    def _process_rs_response(self, response_data):
        """Parses the API response and updates the invoice."""
        self.ensure_one()
        
        status_map = {
            'RECEIVED': 'submitted',
            'PROCESSING': 'submitted',
            'ACCEPTED': 'accepted',
            'REJECTED': 'rejected'
        }
        
        api_status = response_data.get('status')
        submission_id = response_data.get('submission_id')
        message = response_data.get('message')

        odoo_status = status_map.get(api_status, 'draft')
        
        self.write({
            'rs_submission_status': odoo_status,
            'rs_document_id': submission_id,
            'rs_last_response': json.dumps(response_data, indent=2)
        })
        
        if odoo_status == 'rejected':
            # Log rejection specifically
            self.message_post(body=f"RS.ge Rejection: {message}")
        else:
            self.message_post(body=f"RS.ge Submission Successful. ID: {submission_id}. Status: {api_status}")
