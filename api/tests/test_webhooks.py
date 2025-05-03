import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.crud.subscription import subscription
from app.schemas.subscription import SubscriptionCreate
import hmac
import hashlib
import json

client = TestClient(app)

def test_create_subscription(db_session):
    subscription_data = {
        "name": "Test Webhook",
        "target_url": "https://example.com/webhook",
        "secret_key": "test-secret",
        "event_types": ["order.created", "user.updated"]
    }
    response = client.post("/api/subscriptions", json=subscription_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == subscription_data["name"]
    assert data["target_url"] == subscription_data["target_url"]

def test_webhook_signature_verification(db_session):
    # Create subscription with secret
    sub = subscription.create(
        db_session,
        obj_in=SubscriptionCreate(
            name="Test",
            target_url="https://example.com/webhook",
            secret_key="test-secret"
        )
    )
    
    payload = {"test": "data"}
    payload_bytes = json.dumps(payload).encode()
    
    # Generate valid signature
    signature = hmac.new(
        "test-secret".encode(),
        payload_bytes,
        hashlib.sha256
    ).hexdigest()
    
    # Test with valid signature
    response = client.post(
        f"/api/webhooks/ingest/{sub.id}",
        json=payload,
        headers={"X-Hub-Signature-256": f"sha256={signature}"}
    )
    assert response.status_code == 200
    
    # Test with invalid signature
    response = client.post(
        f"/api/webhooks/ingest/{sub.id}",
        json=payload,
        headers={"X-Hub-Signature-256": "sha256=invalid"}
    )
    assert response.status_code == 400

def test_event_type_filtering(db_session):
    # Create subscription with event types
    sub = subscription.create(
        db_session,
        obj_in=SubscriptionCreate(
            name="Test",
            target_url="https://example.com/webhook",
            event_types=["order.created"]
        )
    )
    
    # Test matching event type
    response = client.post(
        f"/api/webhooks/ingest/{sub.id}",
        json={"test": "data"},
        headers={"X-Event-Type": "order.created"}
    )
    assert response.status_code == 200
    
    # Test non-matching event type
    response = client.post(
        f"/api/webhooks/ingest/{sub.id}",
        json={"test": "data"},
        headers={"X-Event-Type": "user.updated"}
    )
    data = response.json()
    assert data["status"] == "skipped"