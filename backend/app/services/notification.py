import uuid
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate

async def create_notification(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_id: uuid.UUID,
    notification: NotificationCreate,
) -> Notification:
    db_notification = Notification(
        user_id=user_id,
        title=notification.title,
        message=notification.message,
        type=notification.type.value,
        is_read=notification.is_read,
    )
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    return db_notification

async def mark_as_read(
    db: Annotated[AsyncSession, Depends(get_db)],
    notification_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Notification | None:
    result = await db.execute(
        select(Notification)
        .where(Notification.id == notification_id)
        .where(Notification.user_id == user_id)
    )
    notification = result.scalar_one_or_none()
    
    if not notification:
        return None
    
    notification.is_read = True
    await db.commit()
    await db.refresh(notification)
    return notification
