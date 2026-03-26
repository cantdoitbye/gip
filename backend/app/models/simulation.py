import uuid
import enum
from datetime import datetime
from sqlalchemy import String, DateTime, Float, Integer, ForeignKey, Text, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class ScenarioType(str, enum.Enum):
    flyover = "flyover"
    road_widening = "road_widening"
    traffic_signals = "traffic_signals"
    underpass = "underpass"
    roundabout = "roundabout"
    bridge = "bridge"
    mixed = "mixed"


class SimulationStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class PriorityLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class SimulationScenario(Base):
    __tablename__ = "simulation_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    scenario_type: Mapped[str] = mapped_column(
        String(50), default=ScenarioType.flyover.value, nullable=False
    )
    location_name: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=True)
    estimated_duration_months: Mapped[int] = mapped_column(Integer, nullable=True)
    priority: Mapped[str] = mapped_column(
        String(50), default=PriorityLevel.medium.value, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    parameters: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    simulations: Mapped[list["Simulation"]] = relationship(
        "Simulation", back_populates="scenario", cascade="all, delete-orphan"
    )


class Simulation(Base):
    __tablename__ = "simulations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scenario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("simulation_scenarios.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(50), default=SimulationStatus.pending.value, nullable=False
    )
    progress_percentage: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    scenario: Mapped["SimulationScenario"] = relationship("SimulationScenario", back_populates="simulations")
    result: Mapped["SimulationResult | None"] = relationship(
        "SimulationResult", back_populates="simulation", uselist=False, cascade="all, delete-orphan"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class SimulationResult(Base):
    __tablename__ = "simulation_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    simulation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("simulations.id", ondelete="CASCADE"), nullable=False
    )
    traffic_improvement_percent: Mapped[float] = mapped_column(Float, nullable=True)
    congestion_reduction_percent: Mapped[float] = mapped_column(Float, nullable=True)
    travel_time_savings_min: Mapped[float] = mapped_column(Float, nullable=True)
    safety_score: Mapped[float] = mapped_column(Float, nullable=True)
    safety_improvement_percent: Mapped[float] = mapped_column(Float, nullable=True)
    environmental_impact_score: Mapped[float] = mapped_column(Float, nullable=True)
    cost_benefit_ratio: Mapped[float] = mapped_column(Float, nullable=True)
    roi_percent: Mapped[float] = mapped_column(Float, nullable=True)
    npv: Mapped[float] = mapped_column(Float, nullable=True)
    irr: Mapped[float] = mapped_column(Float, nullable=True)
    overall_score: Mapped[float] = mapped_column(Float, nullable=True)
    recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    detailed_metrics: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    simulation: Mapped["Simulation"] = relationship("Simulation", back_populates="result")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )


class ScenarioComparison(Base):
    __tablename__ = "scenario_comparisons"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario_ids: Mapped[list] = mapped_column(JSON, nullable=False)
    comparison_metrics: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    ranking: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    ai_recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
