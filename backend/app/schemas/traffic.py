import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class CongestionLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    severe = "severe"


class IncidentType(str, Enum):
    accident = "accident"
    construction = "construction"
    event = "event"
    congestion = "congestion"
    roadwork = "roadwork"


class IncidentSeverity(str, Enum):
    minor = "minor"
    moderate = "moderate"
    severe = "severe"


class TrafficDataCreate(BaseModel):
    location_name: str = Field(..., min_length=1, max_length=255)
    latitude: float
    longitude: float
    flow_rate: float = Field(default=0.0)
    vehicle_count: int = Field(default=0)
    avg_speed: float = Field(default=0.0)
    congestion_level: CongestionLevel = Field(default=CongestionLevel.low)
    
    model_config = {"from_attributes": True}


class TrafficDataResponse(BaseModel):
    id: uuid.UUID
    location_name: str
    latitude: float
    longitude: float
    flow_rate: float
    vehicle_count: int
    avg_speed: float
    congestion_level: str
    timestamp: datetime
    created_at: datetime
    
    model_config = {"from_attributes": True}


class TrafficFilter(BaseModel):
    location: Optional[str] = None
    min_congestion: Optional[CongestionLevel] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class HeatmapPoint(BaseModel):
    lat: float
    lng: float
    intensity: float = Field(..., ge=0, le=1)


class CongestionScore(BaseModel):
    location: str
    level: str
    score: float = Field(..., ge=0, le=100)
    color: str
    latitude: float
    longitude: float
    vehicle_count: int


class Hotspot(BaseModel):
    id: uuid.UUID
    lat: float
    lng: float
    incident_count: int
    risk_score: float = Field(..., ge=0, le=100)
    risk_level: str
    location_name: str
    incident_types: List[str]


class TrafficInsight(BaseModel):
    finding: str
    recommendation: str
    confidence: float = Field(..., ge=0, le=1)
    category: str
    priority: str


class TrafficAnalysisResponse(BaseModel):
    insights: List[TrafficInsight]
    summary: str
    total_analyzed: int
    confidence_score: float


class TrafficDataListResponse(BaseModel):
    items: List[TrafficDataResponse]
    total: int
    page: int
    page_size: int
    has_more: bool
    
    model_config = {"from_attributes": True}
