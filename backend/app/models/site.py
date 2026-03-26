import uuid
import enum
from datetime import datetime
from sqlalchemy import String, DateTime, Float, Integer, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class RiskType(str, enum.Enum):
    flood = "flood"
    seismic = "seismic"
    landslide = "landslide"
    industrial = "industrial"
    environmental = "environmental"


class SiteStatus(str, enum.Enum):
    pending = "pending"
    analyzing = "analyzing"
    analyzed = "analyzed"
    approved = "approved"
    rejected = "rejected"


class SiteType(str, enum.Enum):
    proposed_flyover = "proposed_flyover"
    proposed_bridge = "proposed_bridge"
    road_widening = "road_widening"
    intersection_improvement = "intersection_improvement"
    mixed_development = "mixed_development"


class Site(Base):
    __tablename__ = "sites"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    site_type: Mapped[str] = mapped_column(
        String(50), default=SiteType.proposed_flyover.value, nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(50), default=SiteStatus.pending.value, nullable=False
    )
    location_name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    area_sqkm: Mapped[float | None] = mapped_column(Float, nullable=True)
    land_use_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    land_cost_per_sqft: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_land_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    population_density: Mapped[int | None] = mapped_column(Integer, nullable=True)
    employment_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    road_connectivity_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    transit_access_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    utility_availability: Mapped[str | None] = mapped_column(String(100), nullable=True)
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    ai_recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)
    risk_assessment: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    suitability_factors: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    factors: Mapped[list["SiteFactor"]] = relationship(
        "SiteFactor", back_populates="site", cascade="all, delete-orphan"
    )


class SiteFactor(Base):
    __tablename__ = "site_factors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False
    )
    factor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    factor_type: Mapped[str] = mapped_column(String(100), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    value: Mapped[float | None] = mapped_column(Float, nullable=True)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    site: Mapped["Site"] = relationship("Site", back_populates="factors")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class RiskZone(Base):
    __tablename__ = "risk_zones"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False
    )
    risk_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False)
    probability: Mapped[float] = mapped_column(Float, nullable=True)
    impact_score: Mapped[float] = mapped_column(Float, nullable=True)
    mitigation_measures: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )


class SiteAnalysis(Base):
    __tablename__ = "site_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False
    )
    analyzed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    overall_suitability_score: Mapped[float] = mapped_column(Float, nullable=True)
    land_suitability_score: Mapped[float] = mapped_column(Float, nullable=True)
    connectivity_score: Mapped[float] = mapped_column(Float, nullable=True)
    infrastructure_score: Mapped[float] = mapped_column(Float, nullable=True)
    environmental_score: Mapped[float] = mapped_column(Float, nullable=True)
    economic_score: Mapped[float] = mapped_column(Float, nullable=True)
    social_score: Mapped[float] = mapped_column(Float, nullable=True)
    risk_score: Mapped[float] = mapped_column(Float, nullable=True)
    recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    detailed_factors: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
