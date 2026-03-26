import uuid
import enum
from datetime import datetime
from sqlalchemy import String, DateTime, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class CongestionLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    severe = "severe"


class IncidentType(str, enum.Enum):
    accident = "accident"
    construction = "construction"
    event = "event"
    congestion = "congestion"
    roadwork = "roadwork"


class IncidentSeverity(str, enum.Enum):
    minor = "minor"
    moderate = "moderate"
    severe = "severe"


class TrafficData(Base):
    __tablename__ = "traffic_data"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    location_name: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    flow_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    vehicle_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    avg_speed: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    congestion_level: Mapped[str] = mapped_column(
        String(50), default=CongestionLevel.low.value, nullable=False
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class TrafficIncident(Base):
    __tablename__ = "traffic_incidents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    location_name: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    incident_type: Mapped[str] = mapped_column(
        String(50), default=IncidentType.accident.value, nullable=False
    )
    severity: Mapped[str] = mapped_column(
        String(50), default=IncidentSeverity.minor.value, nullable=False
    )
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    is_resolved: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class TrafficPattern(Base):
    __tablename__ = "traffic_patterns"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    location_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("traffic_data.id", ondelete="CASCADE"), nullable=False
    )
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)
    hour: Mapped[int] = mapped_column(Integer, nullable=False)
    avg_flow: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    avg_speed: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
