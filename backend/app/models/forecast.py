import uuid
import enum
from datetime import datetime
from sqlalchemy import String, DateTime, Float, Integer, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class ForecastType(str, enum.Enum):
    traffic_demand = "traffic_demand"
    population_growth = "population_growth"
    economic_growth = "economic_growth"
    vehicle_growth = "vehicle_growth"


class ForecastStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class ScenarioType(str, enum.Enum):
    baseline = "baseline"
    optimistic = "optimistic"
    pessimistic = "pessimistic"
    custom = "custom"


class Forecast(Base):
    __tablename__ = "forecasts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    forecast_type: Mapped[str] = mapped_column(
        String(50), default=ForecastType.traffic_demand.value, nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(50), default=ForecastStatus.pending.value, nullable=False
    )
    location_name: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    start_year: Mapped[int] = mapped_column(Integer, nullable=False)
    end_year: Mapped[int] = mapped_column(Integer, nullable=False)
    base_traffic_volume: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    predicted_traffic_volume: Mapped[int] = mapped_column(Integer, nullable=True)
    growth_rate: Mapped[float] = mapped_column(Float, nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=True)
    demand_capacity_gap: Mapped[float] = mapped_column(Float, nullable=True)
    road_capacity: Mapped[int] = mapped_column(Integer, nullable=True)
    ai_insights: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    factors: Mapped[list["ForecastFactor"]] = relationship(
        "ForecastFactor", back_populates="forecast", cascade="all, delete-orphan"
    )
    scenarios: Mapped[list["ForecastScenario"]] = relationship(
        "ForecastScenario", back_populates="forecast", cascade="all, delete-orphan"
    )


class ForecastFactor(Base):
    __tablename__ = "forecast_factors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    forecast_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("forecasts.id", ondelete="CASCADE"), nullable=False
    )
    factor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    factor_type: Mapped[str] = mapped_column(String(100), nullable=False)
    current_value: Mapped[float] = mapped_column(Float, nullable=False)
    projected_value: Mapped[float] = mapped_column(Float, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    growth_rate: Mapped[float] = mapped_column(Float, nullable=True)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    forecast: Mapped["Forecast"] = relationship("Forecast", back_populates="factors")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class ForecastScenario(Base):
    __tablename__ = "forecast_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    forecast_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("forecasts.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario_type: Mapped[str] = mapped_column(
        String(50), default=ScenarioType.baseline.value, nullable=False
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    adjustments: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    predicted_volume: Mapped[int] = mapped_column(Integer, nullable=True)
    predicted_growth: Mapped[float] = mapped_column(Float, nullable=True)
    demand_gap: Mapped[float] = mapped_column(Float, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=True)
    forecast: Mapped["Forecast"] = relationship("Forecast", back_populates="scenarios")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class HistoricalTrend(Base):
    __tablename__ = "historical_trends"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    location_name: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    traffic_volume: Mapped[int] = mapped_column(Integer, nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=True)
    vehicle_count: Mapped[int] = mapped_column(Integer, nullable=True)
    gdp_growth: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
