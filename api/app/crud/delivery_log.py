from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from app.models.delivery_log import DeliveryLog

class CRUDDeliveryLog:
    def create_success(
        self,
        db: Session,
        *,
        webhook_id: str,
        subscription_id: int,
        attempt_number: int,
        status_code: int
    ) -> DeliveryLog:
        db_obj = DeliveryLog(
            webhook_id=webhook_id,
            subscription_id=subscription_id,
            attempt_number=attempt_number,
            status="success",
            status_code=status_code
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_failure(
        self,
        db: Session,
        *,
        webhook_id: str,
        subscription_id: int,
        attempt_number: int,
        error_message: str,
        next_retry_at: Optional[datetime] = None
    ) -> DeliveryLog:
        db_obj = DeliveryLog(
            webhook_id=webhook_id,
            subscription_id=subscription_id,
            attempt_number=attempt_number,
            status="failed" if attempt_number >= 5 else "retrying",
            error_message=error_message,
            next_retry_at=next_retry_at
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_webhook_id(
        self,
        db: Session,
        webhook_id: str
    ) -> List[DeliveryLog]:
        return db.query(DeliveryLog)\
            .filter(DeliveryLog.webhook_id == webhook_id)\
            .order_by(desc(DeliveryLog.created_at))\
            .all()

    def get_by_subscription(
        self,
        db: Session,
        subscription_id: int,
        limit: int = 20
    ) -> List[DeliveryLog]:
        return db.query(DeliveryLog)\
            .filter(DeliveryLog.subscription_id == subscription_id)\
            .order_by(desc(DeliveryLog.created_at))\
            .limit(limit)\
            .all()

    def remove_old_logs(
        self,
        db: Session,
        cutoff_date: datetime
    ) -> None:
        db.query(DeliveryLog)\
            .filter(DeliveryLog.created_at < cutoff_date)\
            .delete()
        db.commit()

delivery_log = CRUDDeliveryLog()