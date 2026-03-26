from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Any


class ForecastFactorBase(BaseModel):
    factor_name: str
    factor_type: str
    current_value: float
    projected_value: float | None = None
    weight: float = 1.0
    growth_rate: float | None = None
    unit: str | None = None
    source: str | None = None


class ForecastFactorCreate(ForecastFactorBase):
    pass


class ForecastFactorUpdate(BaseModel):
    factor_name: str | None = None
    factor_type: str | None = None
    current_value: float | None = None
    projected_value: float | None = None
    weight: float | None = None
    growth_rate: float | None = None
    unit: str | None = None
    source: str | None = None


class ForecastFactorResponse(ForecastFactorBase):
    id: UUID
    forecast_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ForecastScenarioBase(BaseModel):
    name: str
    scenario_type: str = "baseline"
    description: str | None = None
    adjustments: dict[str, Any] | None = None


class ForecastScenarioCreate(ForecastScenarioBase):
    pass


class ForecastScenarioUpdate(BaseModel):
    name: str | None = None
    scenario_type: str | None = None
    description: str | None = None
    adjustments: dict[str, Any] | None = None
    predicted_volume: int | None = None
    predicted_growth: float | None = None
    demand_gap: float | None = None
    confidence: float | None = None


class ForecastScenarioResponse(ForecastScenarioBase):
    id: UUID
    forecast_id: UUID
    predicted_volume: int | None = None
    predicted_growth: float | None = None
    demand_gap: float | None = None
    confidence: float | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ForecastBase(BaseModel):
    name: str
    description: str | None = None
    forecast_type: str = "traffic_demand"
    location_name: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    start_year: int
    end_year: int
    base_traffic_volume: int = 0
    road_capacity: int | None = None


class ForecastCreate(ForecastBase):
    factors: list[ForecastFactorCreate] | None = None


class ForecastUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    forecast_type: str | None = None
    location_name: str | None = None
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    start_year: int | None = None
    end_year: int | None = None
    base_traffic_volume: int | None = None
    road_capacity: int | None = None
    status: str | None = None
    predicted_traffic_volume: int | None = None
    growth_rate: float | None = None
    confidence_score: float | None = None
    demand_capacity_gap: float | None = None
    ai_insights: str | None = None


class ForecastResponse(ForecastBase):
    id: UUID
    status: str
    predicted_traffic_volume: int | None = None
    growth_rate: float | None = None
    confidence_score: float | None = None
    demand_capacity_gap: float | None = None
    ai_insights: str | None = None
    created_by: UUID | None = None
    created_at: datetime
    updated_at: datetime
    factors: list[ForecastFactorResponse] = []
    scenarios: list[ForecastScenarioResponse] = []

    model_config = {"from_attributes": True}


class ForecastListResponse(BaseModel):
    forecasts: list[ForecastResponse]
    total: int
    page: int
    page_size: int


class DemandCapacityGapResponse(BaseModel):
    forecast_id: UUID
    location_name: str
    base_year: int
    target_year: int
    current_capacity: int
    current_demand: int
    projected_demand: int
    demand_capacity_gap: float
    gap_percentage: float
    capacity_utilization: float
    recommended_capacity_increase: int
    priority: str


class TrendAnalysisResponse(BaseModel):
    location_name: str
    period_start: int
    period_end: int
    data_points: list[dict[str, Any]]
    trend_direction: str
    average_growth_rate: float
    volatility: float
    seasonality_detected: bool
    forecast_adjustment_recommended: float


class AIForecastRequest(BaseModel):
    location_name: str
    latitude: float
    longitude: float
    base_year: int
    target_year: int
    base_traffic_volume: int
    road_capacity: int | None = None
    additional_factors: dict[str, Any] | None = None


class AIForecastResponse(BaseModel):
    forecast_id: UUID | None = None
    location_name: str
    predicted_traffic_volume: int
    growth_rate: float
    confidence_score: float
    demand_capacity_gap: float | None = None
    key_factors: list[dict[str, Any]]
    ai_insights: str
    recommendations: list[str]
    yearly_projections: list[dict[str, Any]]


class HistoricalTrendBase(BaseModel):
    location_name: str
    year: int
    traffic_volume: int
    population: int | None = None
    vehicle_count: int | None = None
    gdp_growth: float | None = None


class HistoricalTrendCreate(HistoricalTrendBase):
    pass


class HistoricalTrendResponse(HistoricalTrendBase):
    id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class HistoricalTrendListResponse(BaseModel):
    trends: list[HistoricalTrendResponse]
    total: int
