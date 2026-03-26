"""
Simulation Router - API endpoints for infrastructure simulation
"""
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.simulation import SimulationScenario, Simulation
from app.schemas.simulation import (
    SimulationScenarioCreate,
    SimulationScenarioUpdate,
    SimulationScenarioResponse,
    SimulationScenarioListResponse,
    SimulationCreate,
    SimulationResponse,
    SimulationListResponse,
    SimulationStatusResponse,
    SimulationResultsResponse,
    ScenarioComparisonRequest,
    ScenarioComparisonResponse,
    AIRecommendationRequest,
    AIRecommendationResponse,
    CostEstimationRequest,
    CostEstimationResponse,
    AIChatRequest,
    AIChatResponse,
)
from app.services.simulation import simulation_service

router = APIRouter(prefix="/simulations", tags=["simulation"])


@router.get("/scenarios", response_model=SimulationScenarioListResponse)
async def list_scenarios(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    scenario_type: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scenarios, total = await simulation_service.list_scenarios(
        db, page=page, page_size=page_size, scenario_type=scenario_type
    )
    return SimulationScenarioListResponse(
        scenarios=[SimulationScenarioResponse.model_validate(s) for s in scenarios],
        total=total,
        page=page,
        page_size=page_size,
    )


async def _get_scenario_eager(db: AsyncSession, scenario_id: uuid.UUID) -> SimulationScenario | None:
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    stmt = select(SimulationScenario).options(
        selectinload(SimulationScenario.simulations).selectinload(Simulation.result)
    ).where(SimulationScenario.id == scenario_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def _get_simulation_eager(db: AsyncSession, simulation_id: uuid.UUID) -> Simulation | None:
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    stmt = select(Simulation).options(
        selectinload(Simulation.result),
        selectinload(Simulation.scenario)
    ).where(Simulation.id == simulation_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


@router.post("/scenarios", response_model=SimulationScenarioResponse)
async def create_scenario(
    scenario_data: SimulationScenarioCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scenario = await simulation_service.create_scenario(
        db, scenario_data, user_id=current_user.id
    )
    loaded_scenario = await _get_scenario_eager(db, scenario.id)
    return SimulationScenarioResponse.model_validate(loaded_scenario)


@router.get("/scenarios/{scenario_id}", response_model=SimulationScenarioResponse)
async def get_scenario(
    scenario_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scenario = await _get_scenario_eager(db, scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return SimulationScenarioResponse.model_validate(scenario)


@router.put("/scenarios/{scenario_id}", response_model=SimulationScenarioResponse)
async def update_scenario(
    scenario_id: uuid.UUID,
    scenario_data: SimulationScenarioUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scenario = await db.get(SimulationScenario, scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    update_data = scenario_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(scenario, key, value)
    scenario.updated_at = datetime.utcnow()
    await db.commit()
    loaded_scenario = await _get_scenario_eager(db, scenario_id)
    return SimulationScenarioResponse.model_validate(loaded_scenario)


@router.delete("/scenarios/{scenario_id}")
async def delete_scenario(
    scenario_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scenario = await db.get(SimulationScenario, scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    scenario.is_active = False
    await db.commit()
    return {"message": "Scenario deactivated successfully"}


@router.get("", response_model=SimulationListResponse)
async def list_simulations(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    scenario_id: uuid.UUID | None = None,
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import select, func
    from sqlalchemy.orm import selectinload
    
    query = select(Simulation).options(
        selectinload(Simulation.result),
        selectinload(Simulation.scenario)
    )
    if scenario_id:
        query = query.where(Simulation.scenario_id == scenario_id)
    if status:
        query = query.where(Simulation.status == status)
    query = query.order_by(Simulation.created_at.desc())
    offset = (page - 1) * page_size
    result = await db.execute(query.offset(offset).limit(page_size))
    simulations = list(result.scalars().all())
    
    count_query = select(func.count(Simulation.id))
    if scenario_id:
        count_query = count_query.where(Simulation.scenario_id == scenario_id)
    if status:
        count_query = count_query.where(Simulation.status == status)
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    return SimulationListResponse(
        simulations=[SimulationResponse.model_validate(s) for s in simulations],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/run", response_model=SimulationResponse)
async def create_and_run_simulation(
    simulation_data: SimulationCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    simulation = await simulation_service.create_simulation(db, simulation_data)
    background_tasks.add_task(run_simulation_task, simulation.id)
    loaded_simulation = await _get_simulation_eager(db, simulation.id)
    return SimulationResponse.model_validate(loaded_simulation)


async def run_simulation_task(simulation_id: uuid.UUID):
    from app.database import async_session_maker
    async with async_session_maker() as db:
        try:
            await simulation_service.run_simulation(db, simulation_id)
        except Exception as e:
            print(f"Simulation task failed: {e}")


@router.get("/{simulation_id}/status", response_model=SimulationStatusResponse)
async def get_simulation_status(
    simulation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    simulation = await db.get(Simulation, simulation_id)
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    scenario = await db.get(SimulationScenario, simulation.scenario_id)
    return SimulationStatusResponse(
        simulation_id=simulation.id,
        scenario_id=simulation.scenario_id,
        scenario_name=scenario.name if scenario else "Unknown",
        status=simulation.status,
        progress_percentage=simulation.progress_percentage,
        started_at=simulation.started_at,
        completed_at=simulation.completed_at,
        estimated_completion=None,
        current_step=f"Processing {simulation.status}",
    )


@router.get("/{simulation_id}/results", response_model=SimulationResultsResponse)
async def get_simulation_results(
    simulation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = await simulation_service.get_simulation_results(db, simulation_id)
    if not results:
        raise HTTPException(status_code=404, detail="Simulation results not found")
    return results


@router.post("/compare", response_model=ScenarioComparisonResponse)
async def compare_scenarios(
    request: ScenarioComparisonRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if len(request.scenario_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 scenarios required for comparison")
    if len(request.scenario_ids) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 scenarios can be compared")
    return await simulation_service.compare_scenarios(db, request, user_id=current_user.id)


@router.post("/recommend", response_model=AIRecommendationResponse)
async def get_ai_recommendation(
    request: AIRecommendationRequest,
    current_user: User = Depends(get_current_user),
):
    return await simulation_service.get_ai_recommendation(request)


@router.post("/estimate-cost", response_model=CostEstimationResponse)
async def estimate_cost(
    request: CostEstimationRequest,
    current_user: User = Depends(get_current_user),
):
    return await simulation_service.estimate_cost(request)


@router.post("/chat", response_model=AIChatResponse)
async def ai_chat(
    request: AIChatRequest,
    current_user: User = Depends(get_current_user),
):
    return await simulation_service.chat(request)
