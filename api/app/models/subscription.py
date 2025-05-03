from sqlalchemy import Column, Integer, String, Boolean, DateTime, ARRAY
from sqlalchemy.sql import func
from app.db.base_class import Base

class Subscription(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    target_url = Column(String, nullable=False)
    secret_key = Column(String, nullable=True)
    event_types = Column(ARRAY(String), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
