from celery import Celery
from app.core.config import settings
import httpx
import time
from datetime import datetime, timedelta

celery = Celery(
    "webhook_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

@celery.task(bind=True, max_retries=settings.MAX_RETRY_ATTEMPTS)
def deliver_webhook(self, webhook_id: str, subscription_id: int, target_url: str, payload: dict):
    from app.crud.delivery_log import delivery_log
    from app.db.session import SessionLocal
    
    db = SessionLocal()
    try:
        with httpx.Client(timeout=settings.DELIVERY_TIMEOUT) as client:
            response = client.post(target_url, json=payload)
            response.raise_for_status()
            
            # Log successful delivery
            delivery_log.create_success(
                db=db,
                webhook_id=webhook_id,
                subscription_id=subscription_id,
                attempt_number=self.request.retries + 1,
                status_code=response.status_code
            )
            
            return {"status": "success", "attempt": self.request.retries + 1}
            
    except Exception as exc:
        # Calculate next retry with exponential backoff
        retry_delay = min(
            settings.INITIAL_RETRY_DELAY * (2 ** self.request.retries),
            settings.MAX_RETRY_DELAY
        )
        
        # Log failed attempt
        delivery_log.create_failure(
            db=db,
            webhook_id=webhook_id,
            subscription_id=subscription_id,
            attempt_number=self.request.retries + 1,
            error_message=str(exc),
            next_retry_at=datetime.utcnow() + timedelta(seconds=retry_delay)
        )
        
        # Raise for retry if attempts remain
        if self.request.retries < settings.MAX_RETRY_ATTEMPTS - 1:
            self.retry(exc=exc, countdown=retry_delay)
        
        return {"status": "failed", "error": str(exc), "attempt": self.request.retries + 1}
    finally:
        db.close()

@celery.task
def cleanup_old_logs():
    from app.crud.delivery_log import delivery_log
    from app.db.session import SessionLocal
    
    db = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=settings.LOG_RETENTION_DAYS)
        delivery_log.remove_old_logs(db, cutoff_date)
    finally:
        db.close()

# Schedule cleanup task to run daily
celery.conf.beat_schedule = {
    'cleanup-old-logs': {
        'task': 'app.worker.cleanup_old_logs',
        'schedule': timedelta(days=1),
    },
}