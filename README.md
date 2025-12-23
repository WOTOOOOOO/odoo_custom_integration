# RS.ge Integration Project

This project implements an Odoo module for integrating with the RS.ge Revenue Service, along with a mock API for testing and development.

## Project Components

### 1. RS.ge Integration Module
The main Odoo module that handles invoice submission, XML generation, and digital signing.
*   **Location**: `odoo_modules/rs_integration/`
*   **Documentation**: [Read more](odoo_modules/rs_integration/README.md)

### 2. Mock API
A FastAPI-based service that simulates the RS.ge SOAP/REST endpoints. It allows for offline development and testing of the integration logic.
*   **Location**: `mock_api/`
*   **Documentation**: [Read more](mock_api/README.md)

### 3. Test Suite
A standalone test runner that mocks the Odoo environment to run unit tests without a running Odoo server.
*   **Location**: `odoo_modules/rs_integration/run_tests.py` (Runner) & `tests/` (Mock Framework)

## Getting Started

For detailed instructions on how to run the project using Docker, please refer to [RUN_INSTRUCTIONS.md](RUN_INSTRUCTIONS.md).
