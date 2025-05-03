from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import subscription
from app.crud.delivery_log import delivery_log
from app.models.delivery_log import DeliveryLog
from app.worker import deliver_webhook
import hmac
import hashlib
import json
from typing import Optional, List
import uuid
from datetime import datetime, timedelta
from sqlalchemy import desc
from pydantic import BaseModel

router = APIRouter()

class DeliveryLogResponse(BaseModel):
    id: int
    webhook_id: str
    subscription_id: int
    attempt_number: int
    status: str
    status_code: Optional[int]
    error_message: Optional[str]
    created_at: datetime
    next_retry_at: Optional[datetime]

    class Config:
        from_attributes = True

def verify_signature(payload: bytes, secret: str, signature: str) -> bool:
    computed = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed, signature.replace('sha256=', ''))

@router.post("/webhooks/ingest/{subscription_id}", status_code=status.HTTP_202_ACCEPTED)
async def ingest_webhook(
    subscription_id: int,
    request: Request,
    x_hub_signature_256: Optional[str] = Header(None),
    x_event_type: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Ingest a webhook for delivery.
    """
    # Get subscription
    sub = subscription.get(db, subscription_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    # Read raw payload for signature verification
    payload = await request.body()
    
    try:
        payload_json = json.loads(payload)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    # Verify signature if secret is set
    if sub.secret_key:
        if not x_hub_signature_256:
            raise HTTPException(
                status_code=400,
                detail="Missing X-Hub-Signature-256 header"
            )
        if not verify_signature(payload, sub.secret_key, x_hub_signature_256):
            raise HTTPException(
                status_code=400,
                detail="Invalid signature"
            )
    
    # Check event type if specified
    if sub.event_types and x_event_type:
        if x_event_type not in sub.event_types:
            return {"status": "skipped", "reason": "Event type not subscribed"}
    
    # Generate webhook ID
    webhook_id = str(uuid.uuid4())
    
    # Queue delivery task
    deliver_webhook.delay(
        webhook_id=webhook_id,
        subscription_id=subscription_id,
        target_url=str(sub.target_url),
        payload=payload_json
    )
    
    return {"status": "accepted", "webhook_id": webhook_id}

@router.get("/webhooks/logs", response_model=List[DeliveryLogResponse])
def get_all_logs(
    db: Session = Depends(get_db),
    limit: int = 100,
    skip: int = 0
):
    """
    Get all webhook delivery logs.
    """
    return db.query(DeliveryLog).order_by(desc(DeliveryLog.created_at)).offset(skip).limit(limit).all()

@router.get("/webhooks/status/{webhook_id}", response_model=List[DeliveryLogResponse])
def get_webhook_status(
    webhook_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the status and history of a webhook delivery.
    """
    logs = delivery_log.get_by_webhook_id(db, webhook_id)
    if not logs:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return logs

@router.get("/webhooks/subscription/{subscription_id}/logs", response_model=List[DeliveryLogResponse])
def get_subscription_logs(
    subscription_id: int,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get recent delivery logs for a subscription.
    """
    logs = delivery_log.get_by_subscription(db, subscription_id, limit)
    return logs