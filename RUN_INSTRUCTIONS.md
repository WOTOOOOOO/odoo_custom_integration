# How to Run the Project

## Prerequisites
- Docker and Docker Compose installed.

## Steps

1.  **Start the Environment**
    Run the following command in the project root:
    ```bash
    docker-compose up --build
    ```

2.  **Access Odoo**
    Open the browser and go to: [http://localhost:8069/web?debug=1](http://localhost:8069/web?debug=1)

3.  **Initialize Database**
    - Master Password: (leave as is or set one)
    - Database Name: `odoo`
    - Email: `admin`
    - Password: `admin`
    - Click **Create Database** (this takes a minute).

4.  **Install The Module**
    - Once logged in, go to the **Apps** menu.
    - In the search bar, remove the "Apps" filter.
    - Click **Update Apps List**.
    - Search for **RS.ge Integration**.
    - Click **Activate**.
    - **Important**: Since this is a fresh database, you also need to set up basic accounting to avoid "No journal found" errors.
    - Clear the search bar and search for **Generic - Accounting** (technical name: `l10n_generic_coa`).
    - Click **Activate** on that module as well. This automatically creates the necessary Sales Journal and Chart of Accounts.

5.  **Test the Integration**
    - Refresh the browser page to ensure the menus are updated.
    - Click the **Home Menu** icon.
    - Select the **Invoicing** app.
    - In the top menu bar, click **Customers**, then select **Invoices**.
    - Click **New** (or Create) to start a new invoice.
    - Select a Customer.
    - **Set VAT**: Click the "External Link" icon (small arrow to the right of the Customer dropdown) to open their profile.
        - In the **Tax ID** field (sometimes labeled **VAT**), enter a dummy number like `123456789`.
        - Click **Save** to close the customer dialog.
    - Add a product line.
    - Click **Confirm** to post the invoice.
    - You will see the **"Send to RS.ge"** button appear. Click it!
    - Check the "RS.ge Integration" tab on the invoice for the status and response.

## Troubleshooting
- **Mock API URL**: The Odoo container talks to the API via `http://mock-api:8000` (internal Docker network). You can access the API docs locally at `http://localhost:8000/docs`.
