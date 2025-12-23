from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import date, datetime

# RS.ge Models
class InvoiceStatus(str, Enum):
    RECEIVED = "RECEIVED"
    PROCESSING = "PROCESSING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class InvoiceSubmissionResponse(BaseModel):
    submission_id: str
    status: InvoiceStatus
    message: str

class InvoiceStatusResponse(BaseModel):
    submission_id: str
    status: InvoiceStatus
    error_message: Optional[str] = None

# Bank Models
class BankAccount(BaseModel):
    account_id: str
    iban: str
    currency: str

class TransactionDirection(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"

class BankStatementTransaction(BaseModel):
    tx_id: str
    booking_date: date
    direction: TransactionDirection
    amount: float
    reference: Optional[str] = None

# Payment Models
class PaymentStatus(str, Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class PaymentCheckoutRequest(BaseModel):
    amount: float
    currency: str
    reference: str
    callback_url: Optional[str] = None

class PaymentCheckoutResponse(BaseModel):
    checkout_id: str
    status: PaymentStatus
    payment_url: str

class PaymentStatusResponse(BaseModel):
    checkout_id: str
    status: PaymentStatus

class WebhookEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp: datetime
    payload: dict
