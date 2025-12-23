from fastapi import APIRouter, Header, HTTPException, Request, Response
from typing import Optional
import uuid
import random
from lxml import etree
from models import TokenResponse, InvoiceSubmissionResponse, InvoiceStatusResponse, InvoiceStatus

router = APIRouter(prefix="/rs", tags=["RS.ge"])

# In-memory storage for submissions
submissions = {}

@router.post("/auth/token", response_model=TokenResponse)
async def get_token():
    return TokenResponse(
        access_token="test_token_123",
        expires_in=3600
    )

@router.post("/einvoice/submit", response_model=InvoiceSubmissionResponse)
async def submit_invoice(request: Request, x_signature: Optional[str] = Header(None)):
    if not x_signature:
        raise HTTPException(status_code=400, detail="Missing X-Signature header")

    try:
        body = await request.body()
        root = etree.fromstring(body)
        
        # Basic Validation
        buyer_tin = root.find(".//BuyerTIN")
        seller_tin = root.find(".//SellerTIN")
        total_amount = root.find(".//TotalAmount")

        if buyer_tin is None or seller_tin is None or total_amount is None:
             submission_id = str(uuid.uuid4())
             submissions[submission_id] = InvoiceStatus.REJECTED
             return InvoiceSubmissionResponse(
                 submission_id=submission_id,
                 status=InvoiceStatus.REJECTED,
                 message="Missing required fields (BuyerTIN, SellerTIN, TotalAmount)"
             )

        submission_id = str(uuid.uuid4())
        # Simulate processing time or random success/failure
        submissions[submission_id] = InvoiceStatus.ACCEPTED
        
        return InvoiceSubmissionResponse(
            submission_id=submission_id,
            status=InvoiceStatus.RECEIVED,
            message="Invoice received successfully"
        )

    except etree.XMLSyntaxError:
        raise HTTPException(status_code=400, detail="Invalid XML format")

@router.get("/einvoice/status/{submission_id}", response_model=InvoiceStatusResponse)
async def get_status(submission_id: str):
    if submission_id not in submissions:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    status = submissions[submission_id]
    return InvoiceStatusResponse(
        submission_id=submission_id,
        status=status,
        error_message="Validation failed" if status == InvoiceStatus.REJECTED else None
    )
