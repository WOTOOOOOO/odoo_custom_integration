import unittest
import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import tests
# We must import mock_odoo BEFORE importing any module that uses odoo
sys.path.insert(0, os.path.join(current_dir, 'tests'))
import mock_odoo

# Alias the mock module so subsequent imports use the same instance
sys.modules["odoo_modules.rs_integration.tests.mock_odoo"] = mock_odoo

from odoo_modules.rs_integration.tests.test_xml_generation import TestRsXmlSerializer
from odoo_modules.rs_integration.tests.test_connector import TestRsConnector
from odoo_modules.rs_integration.tests.test_workflow import TestAccountMoveWorkflow

if __name__ == '__main__':
    # Create Test Suite
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    suite.addTests(loader.loadTestsFromTestCase(TestRsXmlSerializer))
    suite.addTests(loader.loadTestsFromTestCase(TestRsConnector))
    suite.addTests(loader.loadTestsFromTestCase(TestAccountMoveWorkflow))
    
    # Run
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if not result.wasSuccessful():
        sys.exit(1)
