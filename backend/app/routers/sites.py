"""
Site Analysis Router - API endpoints for infrastructure site analysis
"""
import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.site import Site, SiteStatus
from app.schemas.site import (
    SiteCreate,
    SiteUpdate,
    SiteResponse,
    SiteListResponse,
    SiteAnalysisResponse,
    AISiteAnalysisRequest,
    AISiteAnalysisResponse,
)
from app.services.site_analysis import site_analysis_service
from app.services.audit import log_action
from app.stubs.gis_api import gis_api_stub
from app.stubs.population_api import population_api_stub
from app.stubs.land_use_api import land_use_api_stub

router = APIRouter(prefix="/sites", tags=["site-analysis"])


async def _get_site_eager(db: AsyncSession, site_id: uuid.UUID) -> Site | None:
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    stmt = select(Site).options(selectinload(Site.factors)).where(Site.id == site_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def analyze_site_task(site_id: str, user_id: str | None = None):
    from app.database import async_session_maker
    async with async_session_maker() as db:
        try:
            site = await site_analysis_service.analyze_site(db, uuid.UUID(site_id))
            await log_action(
                db,
                uuid.UUID(user_id) if user_id else None,
                "site_analysis_completed",
                {
                    "description": f"Site analysis completed for {site.name}",
                    "site_id": str(site_id),
                    "site_name": site.name,
                    "location": site.location_name,
                    "entity_type": "site",
                    "overall_score": site.overall_score,
                }
            )
            await db.commit()
        except Exception as e:
            print(f"Site analysis task failed: {e}")


@router.get("", response_model=SiteListResponse)
async def list_sites(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    site_type: str | None = None,
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sites, total = await site_analysis_service.list_sites(
        db, page=page, page_size=page_size, site_type=site_type, status=status
    )
    return SiteListResponse(
        sites=[SiteResponse.model_validate(s) for s in sites],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/export")
async def export_site_report(
    current_user: User = Depends(get_current_user),
    location: str = Query("Vijayawada", description="Location name for site analysis"),
    latitude: Optional[float] = Query(16.5, description="Latitude coordinate"),
    longitude: Optional[float] = Query(80.6, description="Longitude coordinate"),
    format: str = Query("pdf", pattern="^(pdf|excel|xlsx)$", description="Export format (pdf or excel)"),
    db: AsyncSession = Depends(get_db),
):
    await log_action(
        db,
        current_user.id,
        "report_exported",
        {
            "description": f"Exported site analysis report for {location}",
            "location": location,
            "format": format,
            "entity_type": "report",
        }
    )
    await db.commit()
    
    terrain_data = gis_api_stub.get_terrain_data(latitude, longitude)
    environmental_data = gis_api_stub.get_environmental_data(latitude, longitude)
    risks = gis_api_stub.get_risk_assessment(latitude, longitude)
    population_data = population_api_stub.get_population_data(location)
    land_use_data = land_use_api_stub.get_land_use_data(location)
    zoning_data = land_use_api_stub.get_zoning_info(location)
    infrastructure_data = gis_api_stub.get_infrastructure_data(latitude, longitude)
    
    comprehensive_data = {
        "terrain": terrain_data,
        "environmental": environmental_data,
        "risks": risks,
        "population": population_data,
        "land_use": land_use_data,
        "zoning": zoning_data,
        "infrastructure": infrastructure_data,
    }
    
    overall_score = site_analysis_service._calculate_comprehensive_score(comprehensive_data)
    recommendation = await site_analysis_service._generate_ai_recommendation(
        None, comprehensive_data, overall_score
    )
    
    report_data = {
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
        "generated_at": datetime.now().isoformat(),
        "overall_score": overall_score,
        "terrain": terrain_data,
        "environmental": environmental_data,
        "risks": risks,
        "population": population_data,
        "land_use": land_use_data,
        "zoning": zoning_data,
        "infrastructure": infrastructure_data,
        "recommendation": recommendation,
    }
    
    if format == "pdf":
        from app.services.export import generate_site_pdf_report
        pdf_content = generate_site_pdf_report(report_data)
        return StreamingResponse(
            iter([pdf_content]),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=site_analysis_{location.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            },
        )
    else:
        from app.services.export import generate_site_excel_report
        excel_content = generate_site_excel_report(report_data)
        return StreamingResponse(
            iter([excel_content]),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=site_analysis_{location.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            },
        )


@router.post("/ai-analyze", response_model=AISiteAnalysisResponse)
async def ai_analyze_site(
    request: AISiteAnalysisRequest,
    current_user: User = Depends(get_current_user),
):
    return await site_analysis_service.ai_analyze_site(request)


@router.post("", response_model=SiteResponse)
async def create_site(
    site_data: SiteCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    site = await site_analysis_service.create_site(db, site_data, user_id=current_user.id)
    
    await log_action(
        db,
        current_user.id,
        "site_created",
        {
            "description": f"Created new site: {site.name} at {site.location_name}",
            "site_id": str(site.id),
            "site_name": site.name,
            "location": site.location_name,
            "site_type": site.site_type,
            "entity_type": "site",
        }
    )
    await db.commit()
    
    background_tasks.add_task(analyze_site_task, str(site.id), str(current_user.id))
    loaded_site = await _get_site_eager(db, site.id)
    return SiteResponse.model_validate(loaded_site)


@router.get("/{site_id}", response_model=SiteResponse)
async def get_site(
    site_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    site = await _get_site_eager(db, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return SiteResponse.model_validate(site)


@router.put("/{site_id}", response_model=SiteResponse)
async def update_site(
    site_id: uuid.UUID,
    site_data: SiteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    site = await db.get(Site, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    update_data = site_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(site, key, value)
    site.updated_at = datetime.utcnow()
    
    await log_action(
        db,
        current_user.id,
        "site_updated",
        {
            "description": f"Updated site: {site.name}",
            "site_id": str(site_id),
            "site_name": site.name,
            "entity_type": "site",
        }
    )
    
    await db.commit()
    loaded_site = await _get_site_eager(db, site_id)
    return SiteResponse.model_validate(loaded_site)


@router.delete("/{site_id}")
async def delete_site(
    site_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    site = await db.get(Site, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    site_name = site.name
    
    await log_action(
        db,
        current_user.id,
        "site_deleted",
        {
            "description": f"Deleted site: {site_name}",
            "site_id": str(site_id),
            "site_name": site_name,
            "entity_type": "site",
        }
    )
    
    await db.delete(site)
    await db.commit()
    return {"message": "Site deleted successfully"}


@router.post("/{site_id}/analyze", response_model=SiteResponse)
async def analyze_site(
    site_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    site = await site_analysis_service.analyze_site(db, site_id)
    
    await log_action(
        db,
        current_user.id,
        "site_analyzed",
        {
            "description": f"Analyzed site: {site.name}",
            "site_id": str(site_id),
            "site_name": site.name,
            "entity_type": "site",
            "overall_score": site.overall_score,
        }
    )
    await db.commit()
    
    loaded_site = await _get_site_eager(db, site.id)
    return SiteResponse.model_validate(loaded_site)
