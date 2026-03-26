"""
Forecasting Router - API endpoints for traffic forecasting
"""
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.database import get_db  # type: ignore
from app.middleware.auth import get_current_user, get_current_user_optional  # type: ignore
from app.models.user import User  # type: ignore
from app.models.forecast import Forecast  # type: ignore
from app.schemas.forecast import (  # type: ignore
    ForecastCreate,
    ForecastUpdate,
    ForecastResponse,
    ForecastListResponse,
    ForecastFactorResponse,
    ForecastScenarioResponse,
    AIForecastRequest,
    AIForecastResponse,
    DemandCapacityGapResponse,
    TrendAnalysisResponse,
    HistoricalTrendListResponse,
    HistoricalTrendResponse,
)
from app.services.forecasting import forecasting_service  # type: ignore

router = APIRouter(prefix="/forecasts", tags=["forecasting"])


@router.get("", response_model=ForecastListResponse)
async def list_forecasts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    location: str | None = None,
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Forecast).options(
        selectinload(Forecast.factors),
        selectinload(Forecast.scenarios)
    )
    if location:
        query = query.where(Forecast.location_name.ilike(f"%{location}%"))
    if status:
        query = query.where(Forecast.status == status)
    query = query.order_by(Forecast.created_at.desc())
    offset = (page - 1) * page_size
    result = await db.execute(query.offset(offset).limit(page_size))
    forecasts = list(result.scalars().all())
    
    count_query = select(func.count(Forecast.id))
    if location:
        count_query = count_query.where(Forecast.location_name.ilike(f"%{location}%"))
    if status:
        count_query = count_query.where(Forecast.status == status)
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    return ForecastListResponse(
        forecasts=[ForecastResponse.model_validate(f) for f in forecasts],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/export")
async def export_forecast_report(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    format: str = Query("pdf", pattern="^(pdf|excel|xlsx)$"),
    location: str | None = None,
    status: str | None = None,
) -> StreamingResponse:
    query = select(Forecast).options(
        selectinload(Forecast.factors),
        selectinload(Forecast.scenarios)
    )
    if location:
        query = query.where(Forecast.location_name.ilike(f"%{location}%"))
    if status:
        query = query.where(Forecast.status == status)
    query = query.order_by(Forecast.created_at.desc())
    result = await db.execute(query)
    forecasts = list(result.scalars().all())
    
    forecast_data = []
    for f in forecasts:
        forecast_data.append({
            "id": str(f.id),
            "name": f.name,
            "description": f.description,
            "forecast_type": f.forecast_type,
            "location_name": f.location_name,
            "latitude": f.latitude,
            "longitude": f.longitude,
            "start_year": f.start_year,
            "end_year": f.end_year,
            "base_traffic_volume": f.base_traffic_volume,
            "road_capacity": f.road_capacity,
            "predicted_traffic_volume": f.predicted_traffic_volume,
            "growth_rate": f.growth_rate,
            "confidence_score": f.confidence_score,
            "demand_capacity_gap": f.demand_capacity_gap,
            "status": f.status,
            "ai_insights": f.ai_insights,
            "created_at": f.created_at.isoformat() if f.created_at else None,
            "updated_at": f.updated_at.isoformat() if f.updated_at else None,
        })
    
    if format == "pdf":
        from app.services.export import generate_forecast_pdf_report
        pdf_content = generate_forecast_pdf_report(forecast_data)
        return StreamingResponse(
            iter([pdf_content]),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=forecast_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            },
        )
    else:
        from app.services.export import generate_forecast_excel_report
        excel_content = generate_forecast_excel_report(forecast_data)
        return StreamingResponse(
            iter([excel_content]),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=forecast_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            },
        )


async def _get_forecast_eager(db: AsyncSession, forecast_id: uuid.UUID) -> Forecast | None:
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    stmt = select(Forecast).options(
        selectinload(Forecast.factors),
        selectinload(Forecast.scenarios)
    ).where(Forecast.id == forecast_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

@router.post("", response_model=ForecastResponse)
async def create_forecast(
    forecast_data: ForecastCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    forecast = await forecasting_service.create_forecast(
        db, forecast_data, user_id=current_user.id
    )
    background_tasks.add_task(run_forecast_task, forecast.id)
    loaded_forecast = await _get_forecast_eager(db, forecast.id)
    return ForecastResponse.model_validate(loaded_forecast)


async def run_forecast_task(forecast_id: uuid.UUID):
    from app.database import async_session_maker  # type: ignore
    async with async_session_maker() as db:
        try:
            await forecasting_service.run_forecast(db, forecast_id)
        except Exception as e:
            print(f"Forecast task failed: {e}")


@router.get("/trends", response_model=TrendAnalysisResponse)
async def get_trend_analysis(
    location: str = Query(...),
    start_year: int = Query(...),
    end_year: int = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await forecasting_service.get_trend_analysis(db, location, start_year, end_year)


@router.post("/ai-predict", response_model=AIForecastResponse)
async def ai_predict_forecast(
    request: AIForecastRequest,
    current_user: User = Depends(get_current_user),
):
    return await forecasting_service.ai_predict(request)


@router.get("/{forecast_id}", response_model=ForecastResponse)
async def get_forecast(
    forecast_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    forecast = await _get_forecast_eager(db, forecast_id)
    if not forecast:
        raise HTTPException(status_code=404, detail="Forecast not found")
    return ForecastResponse.model_validate(forecast)


@router.put("/{forecast_id}", response_model=ForecastResponse)
async def update_forecast(
    forecast_id: uuid.UUID,
    forecast_data: ForecastUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    forecast = await db.get(Forecast, forecast_id)
    if not forecast:
        raise HTTPException(status_code=404, detail="Forecast not found")
    update_data = forecast_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(forecast, key, value)
    forecast.updated_at = datetime.utcnow()
    await db.commit()
    loaded_forecast = await _get_forecast_eager(db, forecast_id)
    return ForecastResponse.model_validate(loaded_forecast)


@router.delete("/{forecast_id}")
async def delete_forecast(
    forecast_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    forecast = await db.get(Forecast, forecast_id)
    if not forecast:
        raise HTTPException(status_code=404, detail="Forecast not found")
    await db.delete(forecast)
    await db.commit()
    return {"message": "Forecast deleted successfully"}


@router.post("/{forecast_id}/run", response_model=ForecastResponse)
async def run_forecast(
    forecast_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    forecast = await forecasting_service.run_forecast(db, forecast_id)
    loaded_forecast = await _get_forecast_eager(db, forecast.id)
    return ForecastResponse.model_validate(loaded_forecast)


@router.get("/{forecast_id}/gap", response_model=DemandCapacityGapResponse)
async def get_demand_capacity_gap(
    forecast_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await forecasting_service.calculate_demand_capacity_gap(db, forecast_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{forecast_id}/factors", response_model=list[ForecastFactorResponse])
async def get_forecast_factors(
    forecast_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import select
    from app.models.forecast import ForecastFactor  # type: ignore
    forecast = await db.get(Forecast, forecast_id)
    if not forecast:
        raise HTTPException(status_code=404, detail="Forecast not found")
    result = await db.execute(
        select(ForecastFactor).where(ForecastFactor.forecast_id == forecast_id)
    )
    factors = list(result.scalars().all())
    return [ForecastFactorResponse.model_validate(f) for f in factors]


@router.get("/{forecast_id}/scenarios", response_model=list[ForecastScenarioResponse])
async def get_forecast_scenarios(
    forecast_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import select
    from app.models.forecast import ForecastScenario  # type: ignore
    forecast = await db.get(Forecast, forecast_id)
    if not forecast:
        raise HTTPException(status_code=404, detail="Forecast not found")
    result = await db.execute(
        select(ForecastScenario).where(ForecastScenario.forecast_id == forecast_id)
    )
    scenarios = list(result.scalars().all())
    return [ForecastScenarioResponse.model_validate(s) for s in scenarios]
