# Mock API for Odoo Integration

This is a FastAPI application that mocks the external services required for the Odoo integration project.

## Services Mocked

1.  **RS.ge (Electronic Invoice API)**
    *   Authentication
    *   Invoice Submission (XML)
    *   Status Checking

2.  **Bank API**
    *   Account Listing
    *   Statement Retrieval

3.  **Payment Provider API**
    *   Checkout Creation
    *   Status Checking
    *   Webhook Simulation

## Setup & Running

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Server:**
    ```bash
    uvicorn main:app --reload --port 8000
    ```

3.  **Access Documentation:**
    Open [http://localhost:8000/docs](http://localhost:8000/docs) to see the interactive Swagger UI.

## Authentication

*   **Token:** `test_token_123`
*   Most endpoints require the header: `Authorization: Bearer test_token_123`

## RS.ge Signing Approach

For the mock API, the `X-Signature` header is required on the `/rs/einvoice/submit` endpoint, but its content is not cryptographically verified. Any non-empty string is accepted as a valid signature.

## Error Handling

The API simulates various states:
*   **RS.ge:** Submitting an invoice without `BuyerTIN`, `SellerTIN`, or `TotalAmount` in the XML will result in a `REJECTED` status.
*   **Bank:** Requesting statements with `from > to` date will return a 400 error.
*   **Payment:** Payment status randomly transitions between `CREATED`, `PENDING`, `PAID`, and `FAILED` when checked.
