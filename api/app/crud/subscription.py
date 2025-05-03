from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate
from fastapi.encoders import jsonable_encoder
import redis
from app.core.config import settings

# Redis client for caching
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

class CRUDSubscription:
    def get(self, db: Session, id: int) -> Optional[Subscription]:
        # Try cache first
        cached = redis_client.get(f"subscription:{id}")
        if cached:
            return Subscription.parse_raw(cached)
        
        subscription = db.query(Subscription).filter(Subscription.id == id).first()
        if subscription:
            # Cache for 5 minutes
            redis_client.setex(
                f"subscription:{id}",
                300,
                jsonable_encoder(subscription)
            )
        return subscription

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Subscription]:
        return db.query(Subscription).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: SubscriptionCreate) -> Subscription:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Subscription(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Subscription, obj_in: SubscriptionUpdate
    ) -> Subscription:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Invalidate cache
        redis_client.delete(f"subscription:{db_obj.id}")
        return db_obj

    def remove(self, db: Session, *, id: int) -> Subscription:
        obj = db.query(Subscription).get(id)
        db.delete(obj)
        db.commit()
        # Invalidate cache
        redis_client.delete(f"subscription:{id}")
        return obj

subscription = CRUDSubscription()