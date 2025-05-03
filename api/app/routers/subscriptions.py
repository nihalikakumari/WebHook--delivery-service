from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.subscription import subscription
from app.db.session import get_db
from app.schemas.subscription import Subscription, SubscriptionCreate, SubscriptionUpdate

router = APIRouter()

@router.get("/subscriptions", response_model=List[Subscription])
def get_subscriptions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get all subscriptions"""
    return subscription.get_multi(db, skip=skip, limit=limit)

@router.post("/subscriptions", response_model=Subscription)
def create_subscription(
    *,
    db: Session = Depends(get_db),
    subscription_in: SubscriptionCreate
):
    """Create a new subscription"""
    return subscription.create(db=db, obj_in=subscription_in)

@router.get("/subscriptions/{subscription_id}", response_model=Subscription)
def get_subscription(
    subscription_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific subscription by ID"""
    db_subscription = subscription.get(db, subscription_id)
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription

@router.put("/subscriptions/{subscription_id}", response_model=Subscription)
def update_subscription(
    *,
    db: Session = Depends(get_db),
    subscription_id: int,
    subscription_in: SubscriptionUpdate
):
    """Update a subscription"""
    db_subscription = subscription.get(db, subscription_id)
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription.update(db=db, db_obj=db_subscription, obj_in=subscription_in)

@router.delete("/subscriptions/{subscription_id}", response_model=Subscription)
def delete_subscription(
    *,
    db: Session = Depends(get_db),
    subscription_id: int
):
    """Delete a subscription"""
    db_subscription = subscription.get(db, subscription_id)
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription.remove(db=db, id=subscription_id)