from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base_class import Base

class DeliveryLog(Base):
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscription.id"))
    webhook_id = Column(String, index=True)
    payload = Column(JSON)
    attempt_number = Column(Integer)
    status = Column(String)  # "pending", "success", "failed", "retrying"
    status_code = Column(Integer, nullable=True)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    next_retry_at = Column(DateTime(timezone=True), nullable=True)