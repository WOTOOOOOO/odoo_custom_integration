# RS.ge Integration Module

This Odoo module implements the integration with the RS.ge electronic invoice system.

## Features

*   **Validation**: Ensures invoices are posted and contain valid VAT/TIN and amounts before submission.
*   **XML Generation**: Converts Odoo invoice data into the required RS.ge XML format.
*   **Mock Signing**: Implements a placeholder for digital signature generation.
*   **API Integration**: Submits documents to the RS.ge REST API.
*   **Status Tracking**: Tracks the submission status (Draft -> Submitted -> Accepted/Rejected) and stores the RS.ge Document ID.
*   **Error Handling**: Captures API errors and validation failures, logging them to the invoice record.

## Architecture

This module follows the **Service Layer Pattern** to separate concerns:

1.  **`account.move` (Model)**: Orchestrates the workflow. It handles validation, state updates, and calls the services.
2.  **`rs.ge.connector` (AbstractModel)**: Handles all HTTP communication with the RS.ge API. It manages timeouts, headers, and connection errors.
3.  **`rs.xml.serializer` (AbstractModel)**: Responsible solely for generating the XML payload from the invoice data.
4.  **`config.py`**: Centralized configuration reading from environment variables.

## Configuration

The module uses environment variables for configuration (defined in `config.py`).

| Variable | Default | Description |
|----------|---------|-------------|
| `RS_GE_BASE_URL` | `http://localhost:8000` | The base URL of the RS.ge API. |
| `RS_GE_TIMEOUT` | `10` | Request timeout in seconds. |
| `RS_GE_SIGNING_KEY` | `mock_key` | Key used for digital signing (mock). |

## Installation

1.  Place the `rs_integration` folder into the Odoo addons path.
2.  Update the App List in Odoo (Activate Developer Mode -> Apps -> Update App List).
3.  Install the "RS.ge Integration" module.

## Usage

1.  Create a Customer Invoice.
2.  Ensure the Customer has a VAT number set.
3.  Confirm (Post) the invoice.
4.  Click the **"Send to RS.ge"** button in the header.
5.  Check the "RS.ge Integration" tab for status and response details.

## Testing

The module includes a comprehensive test suite that mocks the Odoo framework, allowing tests to run without a running Odoo server.

To run the tests:
```bash
python3 run_tests.py
```

## Technical Details

*   **Dependencies**: `requests`, `lxml`.
