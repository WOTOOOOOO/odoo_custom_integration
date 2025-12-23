from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date
import uuid
import random
from models import BankAccount, BankStatementTransaction, TransactionDirection

router = APIRouter(prefix="/bank", tags=["Bank"])

# Mock Data
ACCOUNTS = [
    BankAccount(account_id="acc_1", iban="GE00BG0000000123456789", currency="GEL"),
    BankAccount(account_id="acc_2", iban="GE00BG0000000987654321", currency="USD"),
]

TRANSACTIONS = []

# Generate some mock transactions
for i in range(10):
    TRANSACTIONS.append(
        BankStatementTransaction(
            tx_id=f"tx_{i}",
            booking_date=date.today(),
            direction=random.choice([TransactionDirection.CREDIT, TransactionDirection.DEBIT]),
            amount=round(random.uniform(10.0, 1000.0), 2),
            reference=f"INV/2023/{i}" if random.random() > 0.5 else None
        )
    )

@router.get("/accounts", response_model=List[BankAccount])
async def get_accounts():
    return ACCOUNTS

@router.get("/statements", response_model=List[BankStatementTransaction])
async def get_statements(
    account_id: str,
    date_from: date = Query(..., alias="from"),
    date_to: date = Query(..., alias="to")
):
    if date_from > date_to:
        raise HTTPException(status_code=400, detail="'from' date cannot be greater than 'to' date")
    
    # In a real app, we would filter by account_id and date range
    # For mock, we just return the static list if account exists
    
    account_exists = any(acc.account_id == account_id for acc in ACCOUNTS)
    if not account_exists:
        raise HTTPException(status_code=404, detail="Account not found")

    return TRANSACTIONS
