import uuid
from typing import Annotated, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.middleware.auth import CurrentUser
from app.models.traffic import TrafficData, TrafficIncident, TrafficPattern, CongestionLevel
from app.schemas.traffic import (
    TrafficDataCreate,
    TrafficDataResponse,
    TrafficDataListResponse,
    TrafficFilter,
    HeatmapPoint,
    CongestionScore,
    Hotspot,
    TrafficAnalysisResponse,
    TrafficInsight,
)
from app.services.traffic import TrafficService
from app.services.audit import log_action
from app.stubs.traffic_api import traffic_api_stub

router = APIRouter(prefix="/traffic", tags=["traffic"])
traffic_service = TrafficService()


@router.get("/data", response_model=TrafficDataListResponse)
async def get_traffic_data(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    location: Optional[str] = Query(None),
    min_congestion: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> TrafficDataListResponse:
    stub_data = traffic_api_stub.get_all_traffic_data()
    
    if location:
        stub_data = [d for d in stub_data if location.lower() in d["location_name"].lower()]
    if min_congestion:
        stub_data = [d for d in stub_data if d["congestion_level"] == min_congestion]
    if date_from:
        stub_data = [d for d in stub_data if d["timestamp"] >= date_from]
    if date_to:
        stub_data = [d for d in stub_data if d["timestamp"] <= date_to]
    
    total = len(stub_data)
    
    if total > 0:
        stub_data = sorted(stub_data, key=lambda x: x["timestamp"], reverse=True)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_data = stub_data[start_idx:end_idx]
        
        return TrafficDataListResponse(
            items=[TrafficDataResponse(
                id=uuid.uuid4(),
                location_name=d["location_name"],
                latitude=d["latitude"],
                longitude=d["longitude"],
                flow_rate=d["flow_rate"],
                vehicle_count=d["vehicle_count"],
                avg_speed=d["avg_speed"],
                congestion_level=d["congestion_level"],
                timestamp=d["timestamp"],
                created_at=d["timestamp"],
            ) for d in paginated_data],
            total=total,
            page=page,
            page_size=page_size,
            has_more=(page * page_size) < total,
        )
    
    db_query = select(TrafficData)
    
    if location:
        db_query = db_query.where(TrafficData.location_name.ilike(f"%{location}%"))
    if min_congestion:
        db_query = db_query.where(TrafficData.congestion_level == min_congestion)
    if date_from:
        db_query = db_query.where(TrafficData.timestamp >= date_from)
    if date_to:
        db_query = db_query.where(TrafficData.timestamp <= date_to)
    
    total_result = await db.execute(select(func.count()).select_from(db_query.subquery()))
    db_total = total_result.scalar() or 0
    
    db_query = db_query.order_by(TrafficData.timestamp.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(db_query)
    traffic_data = result.scalars().all()
    
    return TrafficDataListResponse(
        items=[TrafficDataResponse.model_validate(td) for td in traffic_data],
        total=db_total,
        page=page,
        page_size=page_size,
        has_more=(page * page_size) < db_total,
    )


@router.get("/heatmap", response_model=list[HeatmapPoint])
async def get_heatmap_data(
    current_user: CurrentUser,
) -> list[HeatmapPoint]:
    stub_data = traffic_api_stub.get_heatmap_data()
    return [HeatmapPoint(**point) for point in stub_data]


@router.get("/congestion", response_model=list[CongestionScore])
async def get_congestion_scores(
    current_user: CurrentUser,
) -> list[CongestionScore]:
    stub_data = traffic_api_stub.get_all_traffic_data()
    congestion_scores = []
    colors = {
        CongestionLevel.low.value: "#22c55e",
        CongestionLevel.medium.value: "#f59e0b",
        CongestionLevel.high.value: "#ff9800",
        CongestionLevel.severe.value: "#ef4444",
    }
    for data in stub_data:
        score = (data["vehicle_count"] / max(data["avg_speed"], 1)) * 25
        congestion_scores.append(CongestionScore(
            location=data["location_name"],
            level=data["congestion_level"],
            score=min(score, 100),
            color=colors.get(data["congestion_level"], "#6b7280"),
            latitude=data["latitude"],
            longitude=data["longitude"],
            vehicle_count=data["vehicle_count"],
        ))
    
    return congestion_scores


@router.get("/hotspots", response_model=list[Hotspot])
async def get_hotspots(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[Hotspot]:
    incidents = traffic_api_stub.get_incidents()
    hotspots_dict = {}
    
    for incident in incidents:
        key = (round(incident["latitude"], 4), round(incident["longitude"], 4))
        if key not in hotspots_dict:
            hotspots_dict[key] = {
                "lat": incident["latitude"],
                "lng": incident["longitude"],
                "incident_count": 1,
                "incidents": [incident],
                "location_name": incident["location_name"],
            }
        else:
            hotspots_dict[key]["incident_count"] += 1
            hotspots_dict[key]["incidents"].append(incident)
    
    hotspots = []
    for key, data in hotspots_dict.items():
        risk_score = min((data["incident_count"] / 3) * 100, 100)
        if risk_score < 30:
            risk_level = "low"
        elif risk_score < 60:
            risk_level = "medium"
        elif risk_score < 80:
            risk_level = "high"
        else:
            risk_level = "critical"
        
        hotspots.append(Hotspot(
            id=uuid.uuid4(),
            lat=data["lat"],
            lng=data["lng"],
            incident_count=data["incident_count"],
            risk_score=risk_score,
            risk_level=risk_level,
            location_name=data["location_name"],
            incident_types=list(set(i["incident_type"] for i in data["incidents"])),
        ))
    
    return hotspots


@router.post("/analyze", response_model=TrafficAnalysisResponse)
async def analyze_traffic(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    traffic_data: list[TrafficDataCreate],
) -> TrafficAnalysisResponse:
    insights = await traffic_service.analyze_traffic_data(traffic_data)
    
    await log_action(
        db=db,
        user_id=current_user.id,
        action="traffic_analyzed",
        details={"data_points": len(traffic_data)},
    )
    
    return insights


@router.get("/export")
async def export_traffic_report(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    format: str = Query("pdf", pattern="^(pdf|excel|xlsx)$"),
) -> StreamingResponse:
    report_data = traffic_api_stub.get_all_traffic_data()
    
    if format == "pdf":
        from app.services.export import generate_pdf_report
        pdf_content = generate_pdf_report(report_data)
        return StreamingResponse(
            iter([pdf_content]),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=traffic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            },
        )
    else:
        from app.services.export import generate_excel_report
        excel_content = generate_excel_report(report_data)
        return StreamingResponse(
            iter([excel_content]),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=traffic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            },
        )
