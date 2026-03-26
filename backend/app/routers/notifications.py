import uuid
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.middleware.auth import CurrentUser
from app.models.notification import Notification, NotificationType
from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
    NotificationListResponse,
    NotificationType as NotificationTypeSchema,
)

from app.services.audit import log_action

from app.services.notification import create_notification, mark_as_read

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=NotificationListResponse)
async def get_notifications(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    unread_only: bool = Query(False),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    notification_type: Optional[NotificationTypeSchema] = Query(None),
) -> NotificationListResponse:
    query = select(Notification).where(Notification.user_id == current_user.id)
    
    if notification_type:
        query = query.where(Notification.type == notification_type)
    
    if unread_only:
        query = query.where(Notification.is_read == False)
    
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0
    
    query = query.order_by(Notification.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    notifications = result.scalars().all()
    
    return NotificationListResponse(
        items=[NotificationResponse.model_validate(n) for n in notifications],
        total=total,
        page=page,
        page_size=page_size,
        has_more=(page * page_size) < total,
    )


@router.post("", response_model=NotificationResponse, status_code=201)
async def create_notification_endpoint(
    current_user: CurrentUser,
    notification: NotificationCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> NotificationResponse:
    db_notification = Notification(
        user_id=current_user.id,
        title=notification.title,
        message=notification.message,
        type=notification.type,
        is_read=notification.is_read,
    )
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    await log_action(
        db=db,
        user_id=current_user.id,
        action="notification_created",
        details={"title": notification.title, "type": notification.type.value},
    )
    return NotificationResponse.model_validate(db_notification)


@router.put("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> NotificationResponse:
    result = await db.execute(
        select(Notification)
        .where(Notification.id == notification_id)
        .where(Notification.user_id == current_user.id)
    )
    notification = result.scalar_one_or_none()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    await db.commit()
    await db.refresh(notification)
    await log_action(
        db=db,
        user_id=current_user.id,
        action="notification_read",
        details={"notification_id": str(notification_id)},
    )
    return NotificationResponse.model_validate(notification)


@router.get("/unread-count")
async def get_unread_count(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    result = await db.execute(
        select(func.count())
        .select_from(Notification)
        .where(Notification.user_id == current_user.id)
        .where(Notification.is_read == False)
    )
    count = result.scalar() or 0
    return {"unread_count": count}
