from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional
import uuid
import random
from models import (
    PaymentCheckoutRequest, 
    PaymentCheckoutResponse, 
    PaymentStatusResponse, 
    PaymentStatus,
    WebhookEvent
)

router = APIRouter(tags=["Payment"])

# In-memory storage
payments = {}

@router.post("/pay/checkout", response_model=PaymentCheckoutResponse)
async def create_checkout(request: PaymentCheckoutRequest):
    checkout_id = str(uuid.uuid4())
    payments[checkout_id] = PaymentStatus.CREATED
    
    return PaymentCheckoutResponse(
        checkout_id=checkout_id,
        status=PaymentStatus.CREATED,
        payment_url=f"https://mock-payment.example.com/pay/{checkout_id}"
    )

@router.get("/pay/status/{checkout_id}", response_model=PaymentStatusResponse)
async def get_payment_status(checkout_id: str):
    if checkout_id not in payments:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    # Simulate status change
    current_status = payments[checkout_id]
    if current_status == PaymentStatus.CREATED:
        # Randomly move to PENDING or PAID or FAILED
        new_status = random.choice([
            PaymentStatus.PENDING, 
            PaymentStatus.PAID, 
            PaymentStatus.FAILED
        ])
        payments[checkout_id] = new_status
    
    return PaymentStatusResponse(
        checkout_id=checkout_id,
        status=payments[checkout_id]
    )

@router.post("/webhooks/payment")
async def receive_webhook(event: WebhookEvent):
    # This endpoint simulates the provider receiving a webhook? 
    # Or is it an endpoint for the user to TEST their webhook handling?
    # Given the context, we'll just log it and return 200.
    print(f"Received webhook event: {event.event_id} - {event.event_type}")
    return {"received": True}
