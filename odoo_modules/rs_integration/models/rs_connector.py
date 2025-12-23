import requests
import logging
from odoo import models, _
from odoo.exceptions import UserError
from ..config import Config

_logger = logging.getLogger(__name__)

class RsGeConnector(models.AbstractModel):
    _name = 'rs.ge.connector'
    _description = 'RS.ge API Connector'

    def _get_api_url(self):
        return Config.RS_GE_BASE_URL

    def _get_timeout(self):
        return Config.RS_GE_TIMEOUT

    def send_invoice(self, xml_content, signature):
        """
        Sends the signed XML to RS.ge.
        
        Args:
            xml_content (bytes): The XML payload.
            signature (str): The digital signature.
            
        Returns:
            dict: The JSON response from the API.
            
        Raises:
            UserError: If connection fails or API returns 4xx/5xx.
        """
        base_url = self._get_api_url()
        endpoint = f"{base_url}/rs/einvoice/submit"
        
        headers = {
            "Content-Type": "application/xml",
            "X-Signature": signature,
        }

        _logger.info(f"Sending payload to {endpoint}")

        try:
            response = requests.post(
                endpoint, 
                data=xml_content, 
                headers=headers, 
                timeout=self._get_timeout()
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            _logger.error("RS.ge API Timeout")
            raise UserError(_("Connection to RS.ge timed out. Please try again."))
        except requests.exceptions.ConnectionError:
            _logger.error("RS.ge API Connection Refused")
            raise UserError(_("Could not connect to RS.ge server."))
        except requests.exceptions.RequestException as e:
            _logger.error(f"RS.ge API Error: {e}")
            raise UserError(_("Failed to connect to RS.ge: %s") % str(e))

    def sign_xml(self, xml_content):
        """
        Digitally signs the XML content.
        
        Args:
            xml_content (bytes): The XML to sign.
            
        Returns:
            str: The generated signature.
        """
        # In production, this might call a local crypto library or an external signing service.
        # For now, we return a mock signature.
        if not xml_content:
            raise UserError(_("Cannot sign empty content."))
            
        return "mock_signature_base64_encoded_string"
