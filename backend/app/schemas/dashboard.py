from datetime import datetime
from typing import Any
from pydantic import BaseModel


class TrafficSummary(BaseModel):
    total_vehicles: int
    avg_speed: float
    congestion_level: str


class AlertCounts(BaseModel):
    critical_alerts: int
    warnings: int
    info_alerts: int


class DashboardMetrics(BaseModel):
    projects_count: int
    pending_items: int
    completed_items: int
    active_sites: int
    traffic_summary: TrafficSummary
    alert_counts: AlertCounts


class ActivityItem(BaseModel):
    id: str
    action: str
    description: str
    user_name: str | None
    timestamp: datetime
    details: dict[str, Any] | None
    
    model_config = {"from_attributes": True}


class ActivityListResponse(BaseModel):
    items: list[ActivityItem]
    total: int
    page: int
    page_size: int
    has_more: bool
    
    model_config = {"from_attributes": True}
