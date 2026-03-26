import json
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.database import get_db
from app.middleware.auth import CurrentUser
from app.models.user import User
from app.schemas.settings import SettingsResponse, SettingsUpdate
from app.services.audit import log_action

from app.config import settings


router = APIRouter(prefix="/settings", tags=["settings"])


class UserSettings(BaseModel):
    notification_preferences: dict = {
        "email_notifications": {"enabled": True},
        "push_notifications": {"enabled": True},
        "alert_notifications": {"enabled": True},
    }
    display_preferences: dict = {
        "theme": "light",
        "language": "en",
        "timezone": "UTC",
    }
    dashboard_preferences: dict = {
        "default_view": "grid",
        "items_per_page": 20,
    }


DEFAULT_SETTINGS = UserSettings().model_dump()


@router.get("", response_model=SettingsResponse)
async def get_settings(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SettingsResponse:
    result = await db.execute(
        select(User).where(User.id == current_user.id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_settings = DEFAULT_SETTINGS.copy()
    if hasattr(user, "settings") and user.settings:
        user_settings.update(user.settings)
    
    return SettingsResponse(
        settings=user_settings,
        user_id=current_user.id,
    )


@router.put("", response_model=SettingsResponse)
async def update_settings(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    settings_update: SettingsUpdate,
) -> SettingsResponse:
    result = await db.execute(
        select(User).where(User.id == current_user.id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_settings = DEFAULT_SETTINGS.copy()
    if hasattr(user, "settings") and user.settings:
        current_settings.update(user.settings)
    
    if settings_update.notification_preferences:
        current_settings["notification_preferences"].update(settings_update.notification_preferences)
    if settings_update.display_preferences:
        current_settings["display_preferences"].update(settings_update.display_preferences)
    if settings_update.dashboard_preferences:
        current_settings["dashboard_preferences"].update(settings_update.dashboard_preferences)
    
    if not hasattr(user, "settings"):
        user.settings = {}
    user.settings = current_settings
    await db.commit()
    await db.refresh(user)
    
    await log_action(
        db=db,
        user_id=current_user.id,
        action="settings_updated",
        details={"updated_sections": list(settings_update.model_dump(exclude_none=True).keys())},
    )
    
    return SettingsResponse(
        settings=current_settings,
        user_id=current_user.id,
    )
