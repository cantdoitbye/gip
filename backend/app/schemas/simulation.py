from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Any


class SimulationScenarioBase(BaseModel):
    name: str
    description: str | None = None
    scenario_type: str = "flyover"
    location_name: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    estimated_cost: float | None = None
    estimated_duration_months: int | None = None
    priority: str = "medium"
    parameters: dict[str, Any] | None = None


class SimulationScenarioCreate(SimulationScenarioBase):
    pass


class SimulationScenarioUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    scenario_type: str | None = None
    location_name: str | None = None
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    estimated_cost: float | None = None
    estimated_duration_months: int | None = None
    priority: str | None = None
    is_active: bool | None = None
    parameters: dict[str, Any] | None = None


class SimulationResultResponse(BaseModel):
    id: UUID
    simulation_id: UUID
    traffic_improvement_percent: float | None = None
    congestion_reduction_percent: float | None = None
    travel_time_savings_min: float | None = None
    safety_score: float | None = None
    safety_improvement_percent: float | None = None
    environmental_impact_score: float | None = None
    cost_benefit_ratio: float | None = None
    roi_percent: float | None = None
    npv: float | None = None
    irr: float | None = None
    overall_score: float | None = None
    recommendation: str | None = None
    ai_analysis: str | None = None
    detailed_metrics: dict[str, Any] | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class SimulationBase(BaseModel):
    scenario_id: UUID


class SimulationCreate(SimulationBase):
    pass


class SimulationResponse(BaseModel):
    id: UUID
    scenario_id: UUID
    status: str
    progress_percentage: int
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: SimulationResultResponse | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SimulationScenarioResponse(SimulationScenarioBase):
    id: UUID
    is_active: bool
    created_by: UUID | None = None
    created_at: datetime
    updated_at: datetime
    simulations: list[SimulationResponse] = []

    model_config = {"from_attributes": True}


class SimulationScenarioListResponse(BaseModel):
    scenarios: list[SimulationScenarioResponse]
    total: int
    page: int
    page_size: int


class SimulationListResponse(BaseModel):
    simulations: list[SimulationResponse]
    total: int
    page: int
    page_size: int


class SimulationStatusResponse(BaseModel):
    simulation_id: UUID
    scenario_id: UUID
    scenario_name: str
    status: str
    progress_percentage: int
    started_at: datetime | None = None
    completed_at: datetime | None = None
    estimated_completion: datetime | None = None
    current_step: str | None = None


class SimulationResultsResponse(BaseModel):
    simulation_id: UUID
    scenario: SimulationScenarioResponse
    result: SimulationResultResponse
    comparison_baseline: dict[str, Any] | None = None


class ScenarioComparisonRequest(BaseModel):
    name: str
    scenario_ids: list[UUID]
    comparison_criteria: dict[str, float] | None = None


class ScenarioComparisonResult(BaseModel):
    scenario_id: UUID
    scenario_name: str
    scenario_type: str
    estimated_cost: float
    overall_score: float
    traffic_improvement_percent: float
    safety_improvement_percent: float
    cost_benefit_ratio: float
    roi_percent: float
    rank: int


class ScenarioComparisonResponse(BaseModel):
    id: UUID
    name: str
    scenarios: list[ScenarioComparisonResult]
    ranking_criteria: dict[str, Any]
    ai_recommendation: str | None = None
    best_scenario_id: UUID | None = None
    created_at: datetime


class AIRecommendationRequest(BaseModel):
    location_name: str
    latitude: float
    longitude: float
    current_traffic_volume: int
    current_congestion_level: str
    budget_range: dict[str, float] | None = None
    priorities: list[str] | None = None
    constraints: dict[str, Any] | None = None


class AIRecommendationResponse(BaseModel):
    recommended_scenario_type: str
    recommended_scenario_name: str
    confidence_score: float
    estimated_cost: float
    estimated_duration_months: int
    expected_traffic_improvement: float
    expected_safety_improvement: float
    cost_benefit_ratio: float
    roi_percent: float
    rationale: str
    alternatives: list[dict[str, Any]]
    key_considerations: list[str]
    risk_factors: list[str]


class CostEstimationRequest(BaseModel):
    scenario_type: str
    location_name: str
    length_km: float | None = None
    width_m: float | None = None
    lanes: int | None = None
    special_features: list[str] | None = None


class CostEstimationResponse(BaseModel):
    scenario_type: str
    location_name: str
    base_cost: float
    land_acquisition_cost: float
    construction_cost: float
    contingency_percent: float
    total_estimated_cost: float
    cost_per_km: float | None = None


class AIChatRequest(BaseModel):
    message: str
    context: dict[str, Any] | None = None


class AIChatResponse(BaseModel):
    response: str
    sources_used: list[str] = []
    confidence: float = 0.85
    is_ai_generated: bool = True
