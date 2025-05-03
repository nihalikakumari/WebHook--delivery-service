from typing import Optional, List
from pydantic import BaseModel, HttpUrl

class SubscriptionBase(BaseModel):
    name: str
    target_url: HttpUrl
    secret_key: Optional[str] = None
    event_types: Optional[List[str]] = None

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(SubscriptionBase):
    name: Optional[str] = None
    target_url: Optional[HttpUrl] = None
    is_active: Optional[bool] = None

class Subscription(SubscriptionBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
