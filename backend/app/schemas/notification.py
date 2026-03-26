import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class NotificationType(str, Enum):
    info = "info"
    warning = "warning"
    error = "error"
    success = "success"


class NotificationCreate(BaseModel):
    user_id: Optional[uuid.UUID] = None
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1, max_length=1000)
    type: NotificationType = Field(default=NotificationType.info)
    is_read: bool = Field(default=False)
    
    model_config = {"from_attributes": True}


class NotificationResponse(BaseModel):
    id: uuid.UUID
    user_id: Optional[uuid.UUID]
    title: str
    message: str
    type: NotificationType
    is_read: bool
    created_at: datetime
    
    model_config = {"from_attributes": True}


class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]
    total: int
    page: int
    page_size: int
    has_more: bool
    
    model_config = {"from_attributes": True}
