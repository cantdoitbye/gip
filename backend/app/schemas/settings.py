from typing import Optional, Dict, Any
from pydantic import BaseModel


class NotificationPreferences(BaseModel):
    email_notifications: Dict[str, Any] = {"enabled": True}
    push_notifications: Dict[str, Any] = {"enabled": True}
    alert_notifications: Dict[str, Any] = {"enabled": True}


class DisplayPreferences(BaseModel):
    theme: str = "light"
    language: str = "en"
    timezone: str = "UTC"


class DashboardPreferences(BaseModel):
    default_view: str = "grid"
    items_per_page: int = 20


class SettingsUpdate(BaseModel):
    notification_preferences: Optional[Dict[str, Any]] = None
    display_preferences: Optional[Dict[str, Any]] = None
    dashboard_preferences: Optional[Dict[str, Any]] = None
    
    model_config = {"from_attributes": True}


class SettingsResponse(BaseModel):
    settings: Dict[str, Any]
    user_id: str
    
    model_config = {"from_attributes": True}
