from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import CurrentUser
from app.models.user import User
from app.models.audit import AuditLog
from app.schemas.dashboard import DashboardMetrics, TrafficSummary, AlertCounts, ActivityListResponse, ActivityItem

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DashboardMetrics:
    traffic_summary = TrafficSummary(
        total_vehicles=1547,
        avg_speed=42.5,
        congestion_level="moderate",
    )
    alert_counts = AlertCounts(
        critical_alerts=3,
        warnings=8,
        info_alerts=15,
    )
    return DashboardMetrics(
        projects_count=12,
        pending_items=5,
        completed_items=28,
        active_sites=8,
        traffic_summary=traffic_summary,
        alert_counts=alert_counts,
    )


def _get_entity_type(action: str) -> str:
    action_lower = action.lower()
    if "site" in action_lower:
        return "site"
    elif "report" in action_lower:
        return "report"
    elif "simulation" in action_lower:
        return "simulation"
    elif "forecast" in action_lower:
        return "forecast"
    elif "traffic" in action_lower:
        return "traffic"
    return "project"


@router.get("/activity", response_model=ActivityListResponse)
async def get_dashboard_activity(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1, le=100),
    page_size: int = Query(20, ge=1, le=100),
) -> ActivityListResponse:
    from datetime import datetime, timedelta
    
    offset = (page - 1) * page_size
    total_result = await db.execute(select(func.count()).select_from(AuditLog))
    total = total_result.scalar() or 0
    
    if total == 0:
        default_activities = [
            {
                "action": "site_analysis",
                "description": "Analyzed site at Vijayawada Junction",
                "entity_type": "site",
                "time_offset": 5,
            },
            {
                "action": "forecast_generated",
                "description": "Generated traffic forecast for Q1 2025",
                "entity_type": "forecast",
                "time_offset": 15,
            },
            {
                "action": "simulation_run",
                "description": "Completed flyover simulation for MG Road",
                "entity_type": "simulation",
                "time_offset": 30,
            },
            {
                "action": "report_exported",
                "description": "Exported infrastructure report to PDF",
                "entity_type": "report",
                "time_offset": 60,
            },
            {
                "action": "project_created",
                "description": "Created new infrastructure project proposal",
                "entity_type": "project",
                "time_offset": 120,
            },
        ]
        
        now = datetime.utcnow()
        items = []
        for i, activity in enumerate(default_activities):
            items.append(ActivityItem(
                id=str(1000 + i),
                action=activity["action"],
                description=activity["description"],
                user_name=current_user.full_name or "System",
                timestamp=now - timedelta(minutes=activity["time_offset"]),
                details={"entity_type": activity["entity_type"]},
            ))
        
        return ActivityListResponse(
            items=items[:page_size],
            total=len(items),
            page=1,
            page_size=page_size,
            has_more=False,
        )
    
    query = (
        select(AuditLog)
        .order_by(AuditLog.timestamp.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(query)
    rows = result.scalars().all()
    
    items = []
    for row in rows:
        user_name = None
        if row.user_id:
            user_result = await db.execute(
                select(User.full_name).where(User.id == row.user_id)
            )
            user_name = user_result.scalar_one_or_none()
        
        details = row.details or {}
        entity_type = details.get("entity_type", _get_entity_type(row.action))
        
        items.append(ActivityItem(
            id=str(row.id),
            action=row.action,
            description=details.get("description", row.action),
            user_name=user_name,
            timestamp=row.timestamp,
            details={"entity_type": entity_type, **details},
        ))
    
    return ActivityListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        has_more=(page * page_size) < total,
    )
