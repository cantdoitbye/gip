from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Any


class SiteFactorBase(BaseModel):
    factor_name: str
    factor_type: str
    score: float = Field(..., ge=0, le=10)
    weight: float = Field(default=1.0, ge=0, le=1)
    value: float | None = None
    unit: str | None = None
    source: str | None = None


class SiteFactorCreate(SiteFactorBase):
    pass


class SiteFactorResponse(SiteFactorBase):
    id: UUID
    site_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class SiteBase(BaseModel):
    name: str
    description: str | None = None
    site_type: str = "proposed_flyover"
    location_name: str
    address: str | None = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    area_sqkm: float | None = None
    land_use_type: str | None = None
    land_cost_per_sqft: float | None = None
    total_land_cost: float | None = None
    population_density: int | None = None
    employment_rate: float | None = None
    road_connectivity_score: float | None = None
    transit_access_score: float | None = None
    utility_availability: str | None = None
    overall_score: float | None = None
    ai_recommendation: str | None = None
    risk_assessment: dict[str, Any] | None = None
    suitability_factors: dict[str, Any] | None = None


class SiteCreate(SiteBase):
    pass


class SiteUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    site_type: str | None = None
    location_name: str | None = None
    address: str | None = None
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    area_sqkm: float | None = None
    land_use_type: str | None = None
    status: str | None = None
    land_cost_per_sqft: float | None = None
    total_land_cost: float | None = None
    population_density: int | None = None
    employment_rate: float | None = None
    road_connectivity_score: float | None = None
    transit_access_score: float | None = None
    utility_availability: str | None = None
    overall_score: float | None = None
    ai_recommendation: str | None = None
    risk_assessment: dict[str, Any] | None = None
    suitability_factors: dict[str, Any] | None = None


class SiteResponse(SiteBase):
    id: UUID
    status: str
    created_by: UUID | None = None
    created_at: datetime
    updated_at: datetime
    factors: list[SiteFactorResponse] = []
    model_config = {"from_attributes": True}


class SiteListResponse(BaseModel):
    sites: list[SiteResponse]
    total: int
    page: int
    page_size: int


class RiskZoneResponse(BaseModel):
    id: UUID
    site_id: UUID
    risk_type: str
    severity: str
    probability: float | None = None
    impact_score: float | None = None
    mitigation_measures: str | None = None
    data_source: str | None = None
    created_at: datetime
    model_config = {"from_attributes": True}


class SiteAnalysisResponse(BaseModel):
    id: UUID
    site_id: UUID
    overall_suitability_score: float | None = None
    land_suitability_score: float | None = None
    connectivity_score: float | None = None
    infrastructure_score: float | None = None
    environmental_score: float | None = None
    economic_score: float | None = None
    social_score: float | None = None
    risk_score: float | None = None
    recommendation: str | None = None
    ai_analysis: str | None = None
    detailed_factors: dict[str, Any] | None = None
    created_at: datetime
    model_config = {"from_attributes": True}


class AISiteAnalysisRequest(BaseModel):
    location_name: str
    latitude: float
    longitude: float
    site_type: str | None = "proposed_flyover"
    area_hectares: float | None = None
    budget_range: dict[str, float] | None = None
    priorities: list[str] | None = None
    constraints: dict[str, Any] | None = None


class AISiteAnalysisResponse(BaseModel):
    site_id: UUID | None = None
    location_name: str
    latitude: float
    longitude: float
    overall_suitability_score: float
    land_suitability_score: float
    connectivity_score: float
    infrastructure_score: float
    environmental_score: float
    economic_score: float
    social_score: float
    risk_score: float
    recommendation: str
    ai_analysis: str
    detailed_factors: dict[str, Any]

    model_config = {"from_attributes": True}
