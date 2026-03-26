"""
Simulation Service - Business logic for infrastructure simulation
"""
import uuid
import json
import random
from typing import Any
from datetime import datetime
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config import settings
from app.models.simulation import (
    SimulationScenario,
    Simulation,
    SimulationResult,
    ScenarioComparison,
    SimulationStatus,
)
from app.schemas.simulation import (
    SimulationScenarioCreate,
    SimulationScenarioResponse,
    SimulationCreate,
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
from app.stubs.economic_api import economic_api_stub


class SimulationService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.cost_factors = {
            "flyover": {"base_per_km": 150000000, "multiplier": 1.0},
            "road_widening": {"base_per_km": 50000000, "multiplier": 0.8},
            "traffic_signals": {"base_per_unit": 5000000, "multiplier": 0.5},
            "underpass": {"base_per_km": 200000000, "multiplier": 1.3},
            "roundabout": {"base_per_unit": 25000000, "multiplier": 0.6},
            "bridge": {"base_per_km": 180000000, "multiplier": 1.2},
        }

    async def create_scenario(
        self, db: AsyncSession, scenario_data: SimulationScenarioCreate, user_id: uuid.UUID | None = None
    ) -> SimulationScenario:
        scenario = SimulationScenario(
            name=scenario_data.name,
            description=scenario_data.description,
            scenario_type=scenario_data.scenario_type,
            location_name=scenario_data.location_name,
            latitude=scenario_data.latitude,
            longitude=scenario_data.longitude,
            estimated_cost=scenario_data.estimated_cost,
            estimated_duration_months=scenario_data.estimated_duration_months,
            priority=scenario_data.priority,
            parameters=scenario_data.parameters or {},
            created_by=user_id,
        )
        db.add(scenario)
        await db.commit()
        await db.refresh(scenario)
        return scenario

    async def get_scenario(self, db: AsyncSession, scenario_id: uuid.UUID) -> SimulationScenario | None:
        return await db.get(SimulationScenario, scenario_id)

    async def list_scenarios(
        self, db: AsyncSession, page: int = 1, page_size: int = 10, scenario_type: str | None = None
    ) -> tuple[list[SimulationScenario], int]:
        from sqlalchemy.orm import selectinload
        query = select(SimulationScenario).options(
            selectinload(SimulationScenario.simulations).selectinload(Simulation.result)
        ).where(SimulationScenario.is_active == True)
        if scenario_type:
            query = query.where(SimulationScenario.scenario_type == scenario_type)
        query = query.order_by(SimulationScenario.created_at.desc())
        offset = (page - 1) * page_size
        result = await db.execute(query.offset(offset).limit(page_size))
        scenarios = list(result.scalars().all())
        count_query = select(SimulationScenario).where(SimulationScenario.is_active == True)
        if scenario_type:
            count_query = count_query.where(SimulationScenario.scenario_type == scenario_type)
        count_result = await db.execute(count_query)
        total = len(list(count_result.scalars().all()))
        return scenarios, total

    async def create_simulation(
        self, db: AsyncSession, simulation_data: SimulationCreate
    ) -> Simulation:
        scenario = await db.get(SimulationScenario, simulation_data.scenario_id)
        if not scenario:
            raise ValueError("Scenario not found")
        simulation = Simulation(
            scenario_id=simulation_data.scenario_id,
            status=SimulationStatus.pending.value,
            progress_percentage=0,
        )
        db.add(simulation)
        await db.commit()
        await db.refresh(simulation)
        return simulation

    async def run_simulation(self, db: AsyncSession, simulation_id: uuid.UUID) -> Simulation:
        simulation = await db.get(Simulation, simulation_id)
        if not simulation:
            raise ValueError("Simulation not found")
        simulation.status = SimulationStatus.running.value
        simulation.started_at = datetime.utcnow()
        simulation.progress_percentage = 10
        await db.commit()
        try:
            scenario = await db.get(SimulationScenario, simulation.scenario_id)
            if not scenario:
                raise ValueError("Scenario not found")
            simulation.progress_percentage = 30
            await db.commit()
            traffic_improvement = self._calculate_traffic_improvement(scenario)
            congestion_reduction = self._calculate_congestion_reduction(scenario)
            travel_time_savings = self._calculate_travel_time_savings(scenario)
            safety_improvement = self._calculate_safety_improvement(scenario)
            env_impact = self._calculate_environmental_impact(scenario)
            cost_benefit = self._calculate_cost_benefit_ratio(scenario)
            roi = self._calculate_roi(scenario)
            npv = self._calculate_npv(scenario)
            irr = self._calculate_irr(scenario)
            simulation.progress_percentage = 60
            await db.commit()
            overall_score = self._calculate_overall_score(
                traffic_improvement, congestion_reduction, safety_improvement, cost_benefit
            )
            ai_analysis = await self._generate_ai_analysis(scenario, {
                "traffic_improvement": traffic_improvement,
                "congestion_reduction": congestion_reduction,
                "safety_improvement": safety_improvement,
                "cost_benefit": cost_benefit,
                "roi": roi,
            })
            recommendation = self._generate_recommendation(overall_score, scenario)
            simulation.progress_percentage = 80
            await db.commit()
            result = SimulationResult(
                simulation_id=simulation.id,
                traffic_improvement_percent=traffic_improvement,
                congestion_reduction_percent=congestion_reduction,
                travel_time_savings_min=travel_time_savings,
                safety_score=7.5 + random.uniform(-1, 1),
                safety_improvement_percent=safety_improvement,
                environmental_impact_score=env_impact,
                cost_benefit_ratio=cost_benefit,
                roi_percent=roi,
                npv=npv,
                irr=irr,
                overall_score=overall_score,
                recommendation=recommendation,
                ai_analysis=ai_analysis,
                detailed_metrics={
                    "scenario_type": scenario.scenario_type,
                    "estimated_cost": scenario.estimated_cost,
                    "duration_months": scenario.estimated_duration_months,
                },
            )
            db.add(result)
            simulation.status = SimulationStatus.completed.value
            simulation.completed_at = datetime.utcnow()
            simulation.progress_percentage = 100
            await db.commit()
        except Exception as e:
            simulation.status = SimulationStatus.failed.value
            await db.commit()
            raise
        await db.refresh(simulation)
        return simulation

    def _calculate_traffic_improvement(self, scenario: SimulationScenario) -> float:
        base_improvements = {
            "flyover": 35,
            "road_widening": 25,
            "traffic_signals": 15,
            "underpass": 40,
            "roundabout": 20,
            "bridge": 30,
        }
        base = base_improvements.get(scenario.scenario_type, 20)
        variance = random.uniform(-5, 5)
        return round(base + variance, 2)

    def _calculate_congestion_reduction(self, scenario: SimulationScenario) -> float:
        base_reductions = {
            "flyover": 45,
            "road_widening": 35,
            "traffic_signals": 20,
            "underpass": 50,
            "roundabout": 30,
            "bridge": 40,
        }
        base = base_reductions.get(scenario.scenario_type, 25)
        variance = random.uniform(-5, 5)
        return round(base + variance, 2)

    def _calculate_travel_time_savings(self, scenario: SimulationScenario) -> float:
        base_savings = {
            "flyover": 12,
            "road_widening": 8,
            "traffic_signals": 5,
            "underpass": 15,
            "roundabout": 6,
            "bridge": 10,
        }
        base = base_savings.get(scenario.scenario_type, 7)
        variance = random.uniform(-2, 2)
        return round(base + variance, 2)

    def _calculate_safety_improvement(self, scenario: SimulationScenario) -> float:
        base_improvements = {
            "flyover": 30,
            "road_widening": 25,
            "traffic_signals": 40,
            "underpass": 35,
            "roundabout": 45,
            "bridge": 28,
        }
        base = base_improvements.get(scenario.scenario_type, 25)
        variance = random.uniform(-5, 5)
        return round(base + variance, 2)

    def _calculate_environmental_impact(self, scenario: SimulationScenario) -> float:
        scores = {
            "flyover": 6.5,
            "road_widening": 5.5,
            "traffic_signals": 7.5,
            "underpass": 6.0,
            "roundabout": 7.0,
            "bridge": 5.8,
        }
        base = scores.get(scenario.scenario_type, 6.0)
        variance = random.uniform(-0.5, 0.5)
        return round(base + variance, 2)

    def _calculate_cost_benefit_ratio(self, scenario: SimulationScenario) -> float:
        if not scenario.estimated_cost:
            return 1.5 + random.uniform(-0.2, 0.2)
        cost = scenario.estimated_cost
        annual_benefit = cost * 0.15
        ratio = (annual_benefit * 20) / cost
        return round(ratio + random.uniform(-0.2, 0.2), 2)

    def _calculate_roi(self, scenario: SimulationScenario) -> float:
        base_rois = {
            "flyover": 18,
            "road_widening": 15,
            "traffic_signals": 25,
            "underpass": 16,
            "roundabout": 22,
            "bridge": 17,
        }
        base = base_rois.get(scenario.scenario_type, 18)
        variance = random.uniform(-3, 3)
        return round(base + variance, 2)

    def _calculate_npv(self, scenario: SimulationScenario) -> float:
        if not scenario.estimated_cost:
            return 50000000 + random.uniform(-5000000, 5000000)
        cost = scenario.estimated_cost
        annual_benefit = cost * 0.12
        npv = (annual_benefit * 10) - cost
        return round(npv + random.uniform(-cost * 0.1, cost * 0.1), 2)

    def _calculate_irr(self, scenario: SimulationScenario) -> float:
        base_irrs = {
            "flyover": 14,
            "road_widening": 12,
            "traffic_signals": 18,
            "underpass": 13,
            "roundabout": 16,
            "bridge": 13.5,
        }
        base = base_irrs.get(scenario.scenario_type, 14)
        variance = random.uniform(-2, 2)
        return round(base + variance, 2)

    def _calculate_overall_score(
        self, traffic: float, congestion: float, safety: float, cost_benefit: float
    ) -> float:
        score = (
            (traffic * 0.25) +
            (congestion * 0.25) +
            (safety * 0.25) +
            (cost_benefit * 10 * 0.25)
        )
        return round(min(10, max(1, score / 10)), 2)

    async def _generate_ai_analysis(
        self, scenario: SimulationScenario, metrics: dict[str, float]
    ) -> str:
        if not self.client:
            return self._generate_mock_analysis(scenario, metrics)
        prompt = f"""
        Analyze this infrastructure simulation for {scenario.location_name}:
        
        Scenario: {scenario.name}
        Type: {scenario.scenario_type}
        Description: {scenario.description or 'N/A'}
        Estimated Cost: ₹{scenario.estimated_cost:,.0f} if {scenario.estimated_cost} else 'Not specified'
        Duration: {scenario.estimated_duration_months} months
        
        Key Metrics:
        - Traffic Improvement: {metrics['traffic_improvement']}%
        - Congestion Reduction: {metrics['congestion_reduction']}%
        - Safety Improvement: {metrics['safety_improvement']}%
        - Cost-Benefit Ratio: {metrics['cost_benefit']}
        - ROI: {metrics['roi']}%
        
        Provide a brief analysis (max 200 words) covering:
        1. Overall viability
        2. Key benefits
        3. Potential risks
        4. Recommendation
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an infrastructure planning expert. Provide clear, actionable analysis."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=300,
            )
            return response.choices[0].message.content or "AI analysis not available"
        except Exception:
            return self._generate_mock_analysis(scenario, metrics)

    def _generate_mock_analysis(
        self, scenario: SimulationScenario, metrics: dict[str, float]
    ) -> str:
        return f"""
        Simulation Analysis for {scenario.name}:
        
        The {scenario.scenario_type.replace('_', ' ').title()} project at {scenario.location_name} shows promising results.
        
        Key Findings:
        - Traffic flow improvement of {metrics['traffic_improvement']:.0f}% expected
        - Congestion reduction of {metrics['congestion_reduction']:.0f}% projected
        - Safety improvements of {metrics['safety_improvement']:.0f}% anticipated
        - Strong cost-benefit ratio of {metrics['cost_benefit']:.2f}
        
        The project is {"highly recommended" if metrics['cost_benefit'] > 1.5 else "recommended"} for implementation.
        Consider phased execution to manage costs and minimize disruption.
        
        (Mock analysis - OpenAI API key not configured)
        """

    def _generate_recommendation(self, score: float, scenario: SimulationScenario) -> str:
        if score >= 8:
            return f"Highly Recommended: This {scenario.scenario_type} project shows excellent potential with strong benefits across all metrics."
        elif score >= 6:
            return f"Recommended: This {scenario.scenario_type} project is viable with good expected outcomes."
        elif score >= 4:
            return f"Conditional: This {scenario.scenario_type} project requires careful consideration of costs vs benefits."
        else:
            return f"Not Recommended: This {scenario.scenario_type} project may not provide sufficient return on investment."

    async def get_simulation_results(
        self, db: AsyncSession, simulation_id: uuid.UUID
    ) -> SimulationResultsResponse | None:
        simulation = await db.get(Simulation, simulation_id)
        if not simulation:
            return None
        scenario = await db.get(SimulationScenario, simulation.scenario_id)
        if not scenario:
            return None
        result = None
        if simulation.result:
            result = simulation.result
        from app.schemas.simulation import SimulationScenarioResponse, SimulationResultResponse
        scenario_resp = SimulationScenarioResponse.model_validate(scenario)
        result_resp = SimulationResultResponse.model_validate(result) if result else None
        return SimulationResultsResponse(
            simulation_id=simulation.id,
            scenario=scenario_resp,
            result=result_resp,
            comparison_baseline=None,
        )

    async def compare_scenarios(
        self, db: AsyncSession, request: ScenarioComparisonRequest, user_id: uuid.UUID | None = None
    ) -> ScenarioComparisonResponse:
        scenarios_data = []
        for scenario_id in request.scenario_ids:
            scenario = await db.get(SimulationScenario, scenario_id)
            if scenario:
                result = await self._get_or_create_result(db, scenario)
                scenarios_data.append({
                    "scenario": scenario,
                    "result": result,
                })
        criteria = request.comparison_criteria or {
            "traffic_improvement": 0.3,
            "safety_improvement": 0.25,
            "cost_benefit": 0.25,
            "roi": 0.2,
        }
        scored_scenarios = []
        for data in scenarios_data:
            scenario = data["scenario"]
            result = data["result"]
            score = self._calculate_comparison_score(result, criteria)
            scored_scenarios.append((scenario, result, score))
        scored_scenarios.sort(key=lambda x: x[2], reverse=True)
        comparison_results = []
        for rank, (scenario, result, score) in enumerate(scored_scenarios, 1):
            from app.schemas.simulation import ScenarioComparisonResult
            comparison_results.append(ScenarioComparisonResult(
                scenario_id=scenario.id,
                scenario_name=scenario.name,
                scenario_type=scenario.scenario_type,
                estimated_cost=scenario.estimated_cost or 0,
                overall_score=result.overall_score if result else 0,
                traffic_improvement_percent=result.traffic_improvement_percent if result else 0,
                safety_improvement_percent=result.safety_improvement_percent if result else 0,
                cost_benefit_ratio=result.cost_benefit_ratio if result else 0,
                roi_percent=result.roi_percent if result else 0,
                rank=rank,
            ))
        ai_recommendation = await self._generate_comparison_ai_analysis(comparison_results)
        best_id = comparison_results[0].scenario_id if comparison_results else None
        comparison = ScenarioComparison(
            name=request.name,
            scenario_ids=[str(sid) for sid in request.scenario_ids],
            comparison_metrics=criteria,
            ranking={str(r.scenario_id): r.rank for r in comparison_results},
            ai_recommendation=ai_recommendation,
            created_by=user_id,
        )
        db.add(comparison)
        await db.commit()
        await db.refresh(comparison)
        return ScenarioComparisonResponse(
            id=comparison.id,
            name=request.name,
            scenarios=comparison_results,
            ranking_criteria=criteria,
            ai_recommendation=ai_recommendation,
            best_scenario_id=best_id,
            created_at=comparison.created_at,
        )

    async def _get_or_create_result(
        self, db: AsyncSession, scenario: SimulationScenario
    ) -> SimulationResult | None:
        result = await db.execute(
            select(Simulation)
            .where(Simulation.scenario_id == scenario.id)
            .where(Simulation.status == SimulationStatus.completed.value)
        )
        simulation = result.scalar_one_or_none()
        if simulation and simulation.result:
            return simulation.result
        return None

    def _calculate_comparison_score(
        self, result: SimulationResult | None, criteria: dict[str, float]
    ) -> float:
        if not result:
            return 0
        score = 0
        score += (result.traffic_improvement_percent or 0) * criteria.get("traffic_improvement", 0.25)
        score += (result.safety_improvement_percent or 0) * criteria.get("safety_improvement", 0.25)
        score += (result.cost_benefit_ratio or 0) * 10 * criteria.get("cost_benefit", 0.25)
        score += (result.roi_percent or 0) * criteria.get("roi", 0.25)
        return score

    async def _generate_comparison_ai_analysis(
        self, results: list[Any]
    ) -> str:
        if not results:
            return "No scenarios to compare."
        best = results[0]
        if not self.client:
            return f"""
            Comparison Analysis:
            
            Based on the evaluation criteria, {best.scenario_name} ranks as the best option.
            
            Top performer across key metrics:
            - Traffic Improvement: {best.traffic_improvement_percent}%
            - Safety Improvement: {best.safety_improvement_percent}%
            - Cost-Benefit Ratio: {best.cost_benefit_ratio}
            - ROI: {best.roi_percent}%
            
            Recommendation: Proceed with {best.scenario_name} implementation.
            
            (Mock analysis - OpenAI API key not configured)
            """
        prompt = f"""
        Compare the following infrastructure scenarios and recommend the best option:
        
        {json.dumps([r.model_dump() for r in results], indent=2, default=str)}
        
        Provide a brief comparison analysis and recommendation (max 150 words).
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
            )
            return response.choices[0].message.content or "Comparison analysis not available"
        except Exception:
            return f"Based on the evaluation, {best.scenario_name} is recommended as the top choice."

    async def get_ai_recommendation(
        self, request: AIRecommendationRequest
    ) -> AIRecommendationResponse:
        best_type = self._determine_best_scenario_type(request)
        cost_estimate = self._estimate_cost(best_type, request)
        duration = self._estimate_duration(best_type)
        metrics = self._estimate_metrics(best_type)
        if self.client:
            ai_rationale = await self._get_ai_rationale(request, best_type, metrics)
        else:
            ai_rationale = self._generate_mock_rationale(request, best_type, metrics)
        alternatives = self._generate_alternatives(best_type, request)
        return AIRecommendationResponse(
            recommended_scenario_type=best_type,
            recommended_scenario_name=f"Recommended {best_type.replace('_', ' ').title()} at {request.location_name}",
            confidence_score=0.82,
            estimated_cost=cost_estimate,
            estimated_duration_months=duration,
            expected_traffic_improvement=metrics["traffic"],
            expected_safety_improvement=metrics["safety"],
            cost_benefit_ratio=metrics["cost_benefit"],
            roi_percent=metrics["roi"],
            rationale=ai_rationale,
            alternatives=alternatives,
            key_considerations=[
                "Traffic volume and growth projections",
                "Available budget and timeline",
                "Environmental impact",
                "Community impact during construction",
            ],
            risk_factors=[
                "Construction delays",
                "Cost overruns",
                "Traffic disruption during construction",
                "Regulatory approvals",
            ],
        )

    def _determine_best_scenario_type(self, request: AIRecommendationRequest) -> str:
        congestion = request.current_congestion_level.lower()
        if congestion in ["severe", "high"]:
            return "flyover"
        elif congestion in ["medium"]:
            return "road_widening"
        else:
            return "traffic_signals"

    def _estimate_cost(self, scenario_type: str, request: AIRecommendationRequest) -> float:
        base_costs = {
            "flyover": 250000000,
            "road_widening": 100000000,
            "traffic_signals": 15000000,
            "underpass": 300000000,
            "roundabout": 30000000,
            "bridge": 200000000,
        }
        base = base_costs.get(scenario_type, 100000000)
        if request.budget_range:
            max_budget = request.budget_range.get("max", base * 2)
            if base > max_budget:
                base = max_budget * 0.8
        return base + random.uniform(-base * 0.1, base * 0.1)

    def _estimate_duration(self, scenario_type: str) -> int:
        durations = {
            "flyover": 24,
            "road_widening": 18,
            "traffic_signals": 6,
            "underpass": 30,
            "roundabout": 12,
            "bridge": 36,
        }
        return durations.get(scenario_type, 18)

    def _estimate_metrics(self, scenario_type: str) -> dict[str, float]:
        metrics = {
            "flyover": {"traffic": 35, "safety": 30, "cost_benefit": 1.8, "roi": 18},
            "road_widening": {"traffic": 25, "safety": 25, "cost_benefit": 1.6, "roi": 15},
            "traffic_signals": {"traffic": 15, "safety": 40, "cost_benefit": 2.2, "roi": 25},
            "underpass": {"traffic": 40, "safety": 35, "cost_benefit": 1.7, "roi": 16},
            "roundabout": {"traffic": 20, "safety": 45, "cost_benefit": 2.0, "roi": 22},
            "bridge": {"traffic": 30, "safety": 28, "cost_benefit": 1.6, "roi": 17},
        }
        base = metrics.get(scenario_type, metrics["flyover"])
        return {
            "traffic": base["traffic"] + random.uniform(-3, 3),
            "safety": base["safety"] + random.uniform(-3, 3),
            "cost_benefit": base["cost_benefit"] + random.uniform(-0.2, 0.2),
            "roi": base["roi"] + random.uniform(-2, 2),
        }

    async def _get_ai_rationale(
        self, request: AIRecommendationRequest, scenario_type: str, metrics: dict
    ) -> str:
        prompt = f"""
        Recommend infrastructure solution for {request.location_name}:
        
        Current conditions:
        - Traffic volume: {request.current_traffic_volume} vehicles/day
        - Congestion level: {request.current_congestion_level}
        
        Recommended: {scenario_type.replace('_', ' ').title()}
        Expected improvements:
        - Traffic: {metrics['traffic']:.0f}%
        - Safety: {metrics['safety']:.0f}%
        - ROI: {metrics['roi']:.0f}%
        
        Provide a brief rationale (max 100 words).
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
            )
            return response.choices[0].message.content or "Recommendation based on traffic analysis."
        except Exception:
            return self._generate_mock_rationale(request, scenario_type, metrics)

    def _generate_mock_rationale(
        self, request: AIRecommendationRequest, scenario_type: str, metrics: dict
    ) -> str:
        return f"""
        Based on the current traffic volume of {request.current_traffic_volume} vehicles/day 
        and {request.current_congestion_level} congestion at {request.location_name}, 
        a {scenario_type.replace('_', ' ')} is recommended.
        
        Expected benefits include {metrics['traffic']:.0f}% traffic improvement and 
        {metrics['safety']:.0f}% safety enhancement with an ROI of {metrics['roi']:.0f}%.
        
        (Mock analysis - OpenAI API key not configured)
        """

    def _generate_alternatives(
        self, best_type: str, request: AIRecommendationRequest
    ) -> list[dict[str, Any]]:
        all_types = ["flyover", "road_widening", "traffic_signals", "underpass", "roundabout"]
        alternatives = []
        for t in all_types:
            if t != best_type:
                metrics = self._estimate_metrics(t)
                alternatives.append({
                    "type": t,
                    "estimated_cost": self._estimate_cost(t, request),
                    "traffic_improvement": metrics["traffic"],
                    "safety_improvement": metrics["safety"],
                    "cost_benefit_ratio": metrics["cost_benefit"],
                })
        return alternatives[:3]

    async def estimate_cost(self, request: CostEstimationRequest) -> CostEstimationResponse:
        cost_data = economic_api_stub.get_construction_cost_index(request.location_name)
        base_costs = {
            "flyover": 150000000,
            "road_widening": 50000000,
            "traffic_signals": 5000000,
            "underpass": 200000000,
            "roundabout": 25000000,
            "bridge": 180000000,
        }
        base_per_km = base_costs.get(request.scenario_type, 100000000)
        length = request.length_km or 1.0
        construction_cost = base_per_km * length * (cost_data["current_index"] / 100)
        land_cost = construction_cost * 0.3
        total = construction_cost + land_cost
        contingency = total * 0.1
        breakdown = {
            "materials": construction_cost * 0.45,
            "labor": construction_cost * 0.30,
            "equipment": construction_cost * 0.15,
            "overhead": construction_cost * 0.10,
            "land_acquisition": land_cost,
            "contingency": contingency,
        }
        return CostEstimationResponse(
            scenario_type=request.scenario_type,
            location_name=request.location_name,
            base_cost=base_per_km * length,
            land_acquisition_cost=land_cost,
            construction_cost=construction_cost,
            contingency_percent=10,
            total_estimated_cost=total + contingency,
            cost_per_km=(total + contingency) / length if length else None,
            timeline_months=self._estimate_duration(request.scenario_type),
            cost_breakdown=breakdown,
        )

    async def chat(self, request: "AIChatRequest") -> "AIChatResponse":
        if self.client:
            return await self._ai_chat(request)
        return self._mock_chat(request)

    async def _ai_chat(self, request: "AIChatRequest") -> "AIChatResponse":
        try:
            system_prompt = """You are an expert infrastructure planning assistant for Ooumph GIP (Government Infrastructure Planning) platform. 
            You help users with:
            - Traffic analysis and forecasting
            - Site analysis for infrastructure projects
            - Simulation recommendations for roads, flyovers, traffic signals
            - Cost estimation and ROI analysis
            - Environmental and demographic considerations
            
            Provide detailed, actionable advice based on infrastructure planning best practices.
            Always be helpful, professional, and provide specific recommendations when possible.
            If you don't have enough information, ask clarifying questions."""
            
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": request.message},
                ],
                temperature=0.7,
                max_tokens=1500,
            )
            
            return AIChatResponse(
                response=response.choices[0].message.content or "I apologize, I couldn't generate a response.",
                sources_used=["OpenAI GPT-4"],
                confidence=0.9,
                is_ai_generated=True,
            )
        except Exception as e:
            return self._mock_chat(request)

    def _mock_chat(self, request: "AIChatRequest") -> "AIChatResponse":
        message_lower = request.message.lower()
        
        if "traffic" in message_lower:
            response = """Based on my analysis of traffic patterns, here are my recommendations:

**Traffic Analysis Summary:**
- Current traffic volume in the area is estimated at 2,500-3,500 vehicles/hour during peak times
- Congestion level is moderate to high, especially during morning (8-10 AM) and evening (5-8 PM) rush hours

**Recommendations:**
1. **Short-term**: Optimize traffic signal timing at key intersections
2. **Medium-term**: Consider road widening on major arterials
3. **Long-term**: Evaluate feasibility of a flyover at the most congested intersection

**Expected Improvements:**
- Traffic flow improvement: 25-35%
- Travel time reduction: 15-20 minutes during peak hours
- Safety improvement: 20-30%

Would you like me to provide more specific analysis for any particular location or scenario?"""
        elif "site" in message_lower or "location" in message_lower:
            response = """**Site Analysis Recommendations:**

**Key Factors to Consider:**
1. **Terrain**: Evaluate elevation, slope, and soil conditions
2. **Accessibility**: Proximity to major roads and public transport
3. **Demographics**: Population density and growth projections
4. **Land Use**: Current zoning and future development plans
5. **Environmental**: Flood risk, seismic activity, environmental clearances

**Recommended Steps:**
1. Conduct detailed topographical survey
2. Review land acquisition requirements and costs
3. Assess utility relocation needs
4. Evaluate environmental impact assessment requirements
5. Engage with local stakeholders and communities

**Estimated Timeline:**
- Site analysis and surveys: 2-3 months
- Clearances and approvals: 6-12 months
- Land acquisition: 12-24 months

Would you like specific analysis for a particular site location?"""
        elif "forecast" in message_lower or "predict" in message_lower:
            response = """**Infrastructure Demand Forecast:**

**Methodology:**
- Historical traffic data analysis
- Population growth projections
- Economic development trends
- Urban expansion patterns

**Key Projections (5-year horizon):**
- Traffic volume growth: 15-25% annually
- Peak hour congestion: Expected to increase by 30-40%
- Infrastructure capacity: Current roads operating at 85-95% capacity

**Recommendations:**
1. Begin planning for capacity expansion now
2. Implement smart traffic management systems
3. Consider multi-modal transport options
4. Plan for future connectivity corridors

Would you like me to generate a detailed forecast report for a specific corridor or area?"""
        else:
            response = f"""Thank you for your question about infrastructure planning.

I can help you with:
- **Traffic Analysis**: Analyze current traffic patterns and recommend improvements
- **Site Analysis**: Evaluate locations for new infrastructure projects
- **Forecasting**: Predict future infrastructure demands
- **Cost Estimation**: Estimate costs for different infrastructure scenarios
- **Simulation**: Compare different infrastructure options

Could you please provide more details about what specific analysis or information you need? For example:
- A specific location or area
- Type of infrastructure (road, flyover, traffic signals, etc.)
- Budget constraints
- Timeline requirements

I'll provide detailed, actionable recommendations based on your requirements."""

        return AIChatResponse(
            response=response,
            sources_used=["Mock Data (OpenAI API key not configured)"],
            confidence=0.75,
            is_ai_generated=False,
        )


simulation_service = SimulationService()
