from lxml import etree
from odoo import models, api, _
from odoo.exceptions import UserError

class RsXmlSerializer(models.AbstractModel):
    _name = 'rs.xml.serializer'
    _description = 'RS.ge XML Serializer'

    def generate_invoice_xml(self, invoice):
        """
        Generates the XML content required by RS.ge for a given invoice.
        
        Args:
            invoice (account.move): The invoice record.
            
        Returns:
            bytes: The generated XML string.
        """
        self._validate_data(invoice)
        
        root = etree.Element("Invoice")
        
        # Header
        self._build_header(root, invoice)
        
        # Parties
        self._build_seller(root, invoice)
        self._build_buyer(root, invoice)
        
        # Lines
        self._build_lines(root, invoice)
        
        # Totals
        self._build_totals(root, invoice)

        return etree.tostring(root, pretty_print=True, encoding='UTF-8')

    def _validate_data(self, invoice):
        """Ensure essential data for XML generation is present."""
        if not invoice.name:
            raise UserError(_("Invoice number is missing."))
        if not invoice.invoice_date:
            raise UserError(_("Invoice date is missing."))

    def _build_header(self, root, invoice):
        header = etree.SubElement(root, "Header")
        etree.SubElement(header, "InvoiceNumber").text = str(invoice.name)
        etree.SubElement(header, "Date").text = str(invoice.invoice_date)

    def _build_seller(self, root, invoice):
        seller = etree.SubElement(root, "Seller")
        # Use safe navigation or ensure validation happened before
        vat = invoice.company_id.vat or ''
        name = invoice.company_id.name or ''
        etree.SubElement(seller, "SellerTIN").text = vat
        etree.SubElement(seller, "Name").text = name

    def _build_buyer(self, root, invoice):
        buyer = etree.SubElement(root, "Buyer")
        vat = invoice.partner_id.vat or ''
        name = invoice.partner_id.name or ''
        etree.SubElement(buyer, "BuyerTIN").text = vat
        etree.SubElement(buyer, "Name").text = name

    def _build_lines(self, root, invoice):
        lines = etree.SubElement(root, "Lines")
        for line in invoice.invoice_line_ids:
            if line.display_type == 'product':
                line_elem = etree.SubElement(lines, "Line")
                etree.SubElement(line_elem, "Product").text = str(line.name)
                etree.SubElement(line_elem, "Quantity").text = str(line.quantity)
                etree.SubElement(line_elem, "Price").text = str(line.price_unit)
                etree.SubElement(line_elem, "Amount").text = str(line.price_subtotal)

    def _build_totals(self, root, invoice):
        etree.SubElement(root, "TotalAmount").text = str(invoice.amount_total)
        currency_name = invoice.currency_id.name if invoice.currency_id else 'GEL'
        etree.SubElement(root, "Currency").text = currency_name
