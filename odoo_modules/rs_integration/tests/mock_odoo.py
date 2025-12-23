import sys
from unittest.mock import MagicMock

# ---------------------------------------------------------
# MOCK THE ODOO FRAMEWORK
# ---------------------------------------------------------
# This module must be imported BEFORE any Odoo modules in the tests.

odoo_mock = MagicMock()
sys.modules["odoo"] = odoo_mock
sys.modules["odoo.models"] = odoo_mock.models
sys.modules["odoo.fields"] = odoo_mock.fields
sys.modules["odoo.api"] = odoo_mock.api
sys.modules["odoo.exceptions"] = odoo_mock.exceptions

# Define Exceptions
class UserError(Exception): pass
class ValidationError(Exception): pass
odoo_mock.exceptions.UserError = UserError
odoo_mock.exceptions.ValidationError = ValidationError

# Mock Translation
odoo_mock._ = lambda x: x

# Mock Base Model
class MockModel:
    _inherit = None
    _name = None
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        # Simulate env
        self.env = MagicMock()

    def ensure_one(self):
        return self

    def __iter__(self):
        yield self

    def write(self, vals):
        for key, value in vals.items():
            setattr(self, key, value)

    def message_post(self, body=None, **kwargs):
        pass

odoo_mock.models.Model = MockModel
odoo_mock.models.AbstractModel = MockModel
odoo_mock.models.TransientModel = MockModel

# Mock Fields
def mock_field(*args, **kwargs): return MagicMock()
odoo_mock.fields.Selection = mock_field
odoo_mock.fields.Char = mock_field
odoo_mock.fields.Text = mock_field
