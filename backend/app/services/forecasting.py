"""
Forecasting Service - Business logic for traffic forecasting
"""
import os
import uuid
import json
from typing import Any
from datetime import datetime
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config import settings
from app.models.forecast import Forecast, ForecastFactor, ForecastScenario, HistoricalTrend
from app.schemas.forecast import (
    ForecastCreate,
    ForecastResponse,
    AIForecastRequest,
    AIForecastResponse,
    DemandCapacityGapResponse,
    TrendAnalysisResponse,
)
from app.stubs.population_api import population_api_stub
from app.stubs.economic_api import economic_api_stub
from app.stubs.land_use_api import land_use_api_stub


class ForecastingService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    async def create_forecast(
        self, db: AsyncSession, forecast_data: ForecastCreate, user_id: uuid.UUID | None = None
    ) -> Forecast:
        forecast = Forecast(
            name=forecast_data.name,
            description=forecast_data.description,
            forecast_type=forecast_data.forecast_type,
            location_name=forecast_data.location_name,
            latitude=forecast_data.latitude,
            longitude=forecast_data.longitude,
            start_year=forecast_data.start_year,
            end_year=forecast_data.end_year,
            base_traffic_volume=forecast_data.base_traffic_volume,
            road_capacity=forecast_data.road_capacity,
            status="pending",
            created_by=user_id,
        )
        db.add(forecast)
        await db.flush()
        if forecast_data.factors:
            for factor_data in forecast_data.factors:
                factor = ForecastFactor(
                    forecast_id=forecast.id,
                    factor_name=factor_data.factor_name,
                    factor_type=factor_data.factor_type,
                    current_value=factor_data.current_value,
                    projected_value=factor_data.projected_value,
                    weight=factor_data.weight,
                    growth_rate=factor_data.growth_rate,
                    unit=factor_data.unit,
                    source=factor_data.source,
                )
                db.add(factor)
        await db.commit()
        await db.refresh(forecast)
        return forecast

    async def run_forecast(self, db: AsyncSession, forecast_id: uuid.UUID) -> Forecast:
        forecast = await db.get(Forecast, forecast_id)
        if not forecast:
            raise ValueError("Forecast not found")
        forecast.status = "processing"
        await db.commit()
        try:
            factors = await self._gather_factors_from_stubs(forecast.location_name)
            for factor_data in factors:
                factor = ForecastFactor(
                    forecast_id=forecast.id,
                    factor_name=factor_data["name"],
                    factor_type=factor_data["type"],
                    current_value=factor_data["current"],
                    projected_value=factor_data["projected"],
                    weight=factor_data["weight"],
                    growth_rate=factor_data["growth_rate"],
                    unit=factor_data["unit"],
                    source=factor_data["source"],
                )
                db.add(factor)
            await db.flush()
            result = await self._calculate_forecast(db, forecast)
            forecast.predicted_traffic_volume = result["predicted_volume"]
            forecast.growth_rate = result["growth_rate"]
            forecast.confidence_score = result["confidence"]
            forecast.demand_capacity_gap = result["demand_gap"]
            forecast.ai_insights = result["ai_insights"]
            forecast.status = "completed"
        except Exception as e:
            forecast.status = "failed"
            forecast.ai_insights = f"Forecast failed: {str(e)}"
        await db.commit()
        await db.refresh(forecast)
        return forecast

    async def _gather_factors_from_stubs(self, location: str) -> list[dict[str, Any]]:
        factors = []
        pop_data = population_api_stub.get_population_projection(location, 10)
        factors.append({
            "name": "Population",
            "type": "demographic",
            "current": pop_data["base_population"],
            "projected": pop_data["projected_population"],
            "weight": 0.25,
            "growth_rate": pop_data["growth_rate_percent"],
            "unit": "persons",
            "source": "Census API (Stub)",
        })
        econ_data = economic_api_stub.get_economic_indicators(location)
        factors.append({
            "name": "GDP Per Capita",
            "type": "economic",
            "current": econ_data["gdp_per_capita"],
            "projected": econ_data["gdp_per_capita"] * (1 + econ_data["gdp_growth_rate"] / 100),
            "weight": 0.20,
            "growth_rate": econ_data["gdp_growth_rate"],
            "unit": "INR",
            "source": "Economic Survey (Stub)",
        })
        vehicle_data = economic_api_stub.get_vehicle_growth_data(location)
        factors.append({
            "name": "Vehicle Count",
            "type": "transport",
            "current": vehicle_data["total_vehicles"],
            "projected": vehicle_data["projection_10_years"],
            "weight": 0.30,
            "growth_rate": vehicle_data["annual_growth_rate"],
            "unit": "vehicles",
            "source": "Transport Statistics (Stub)",
        })
        land_data = land_use_api_stub.get_land_use_data(location)
        factors.append({
            "name": "Urbanization Rate",
            "type": "land_use",
            "current": land_data["urban_area_percent"],
            "projected": land_data["urban_area_percent"] * 1.15,
            "weight": 0.15,
            "growth_rate": 1.5,
            "unit": "percent",
            "source": "Land Records (Stub)",
        })
        factors.append({
            "name": "Employment Rate",
            "type": "economic",
            "current": 72.0,
            "projected": 75.0,
            "weight": 0.10,
            "growth_rate": 0.3,
            "unit": "percent",
            "source": "Employment Survey (Stub)",
        })
        return factors

    async def _calculate_forecast(
        self, db: AsyncSession, forecast: Forecast
    ) -> dict[str, Any]:
        result = await self._get_factors_for_forecast(db, forecast.id)
        factors = result
        base_volume = forecast.base_traffic_volume
        years = forecast.end_year - forecast.start_year
        weighted_growth = 0.0
        total_weight = 0.0
        for factor in factors:
            weighted_growth += factor.growth_rate * factor.weight
            total_weight += factor.weight
        avg_growth_rate = weighted_growth / max(total_weight, 1)
        predicted_volume = int(base_volume * ((1 + avg_growth_rate / 100) ** years))
        demand_gap = None
        if forecast.road_capacity:
            demand_gap = ((predicted_volume - forecast.road_capacity) / forecast.road_capacity) * 100
        confidence = min(0.95, 0.6 + (0.05 * len(factors)))
        ai_insights = await self._generate_ai_insights(forecast, factors, predicted_volume, confidence)
        return {
            "predicted_volume": predicted_volume,
            "growth_rate": avg_growth_rate,
            "confidence": confidence,
            "demand_gap": demand_gap,
            "ai_insights": ai_insights,
        }

    async def _get_factors_for_forecast(
        self, db: AsyncSession, forecast_id: uuid.UUID
    ) -> list[ForecastFactor]:
        result = await db.execute(
            select(ForecastFactor).where(ForecastFactor.forecast_id == forecast_id)
        )
        return list(result.scalars().all())

    async def _generate_ai_insights(
        self, forecast: Forecast, factors: list[ForecastFactor], predicted_volume: int, confidence: float
    ) -> str:
        if not self.client:
            return self._generate_mock_insights(forecast, factors, predicted_volume, confidence)
        factor_summary = "\n".join([
            f"- {f.factor_name}: {f.current_value} -> {f.projected_value} ({f.growth_rate}% growth)"
            for f in factors
        ])
        prompt = f"""
        Analyze the following traffic forecast for {forecast.location_name}:
        
        Forecast Period: {forecast.start_year} to {forecast.end_year} ({forecast.end_year - forecast.start_year} years)
        Base Traffic Volume: {forecast.base_traffic_volume} vehicles/day
        Predicted Volume: {predicted_volume} vehicles/day
        Growth Rate: {((predicted_volume / max(forecast.base_traffic_volume, 1)) - 1) * 100:.1f}%
        Confidence: {confidence * 100:.0f}%
        
        Key Factors:
        {factor_summary}
        
        Provide:
        1. Summary of the forecast
        2. Key drivers of growth
        3. Potential risks and uncertainties
        4. Infrastructure recommendations
        Keep the response concise (max 300 words).
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a traffic planning expert. Provide clear, actionable insights."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=400,
            )
            return response.choices[0].message.content or "AI analysis not available"
        except Exception:
            return self._generate_mock_insights(forecast, factors, predicted_volume, confidence)

    def _generate_mock_insights(
        self, forecast: Forecast, factors: list[ForecastFactor], predicted_volume: int, confidence: float
    ) -> str:
        growth_pct = ((predicted_volume / max(forecast.base_traffic_volume, 1)) - 1) * 100
        return f"""
        Traffic Forecast Analysis for {forecast.location_name}:
        
        Over the {forecast.end_year - forecast.start_year}-year period, traffic is expected to grow by {growth_pct:.1f}%.
        The predicted daily traffic volume of {predicted_volume:,} vehicles represents a significant increase 
        from the current {forecast.base_traffic_volume:,} vehicles.
        
        Key Growth Drivers:
        - Population growth and urbanization
        - Economic development and employment opportunities
        - Vehicle ownership increase
        
        Infrastructure Recommendations:
        - Capacity expansion may be needed to accommodate growth
        - Consider multi-modal transport options
        - Plan for phased infrastructure development
        
        Confidence Level: {confidence * 100:.0f}%
        
        (Mock analysis - OpenAI API key not configured)
        """

    async def ai_predict(self, request: AIForecastRequest) -> AIForecastResponse:
        factors = await self._gather_factors_from_stubs(request.location_name)
        weighted_growth = 0.0
        total_weight = 0.0
        key_factors = []
        for factor in factors:
            weighted_growth += factor["growth_rate"] * factor["weight"]
            total_weight += factor["weight"]
            key_factors.append({
                "name": factor["name"],
                "type": factor["type"],
                "current_value": factor["current"],
                "projected_value": factor["projected"],
                "growth_rate": factor["growth_rate"],
                "weight": factor["weight"],
            })
        avg_growth = weighted_growth / max(total_weight, 1)
        years = request.target_year - request.base_year
        predicted_volume = int(request.base_traffic_volume * ((1 + avg_growth / 100) ** years))
        demand_gap = None
        if request.road_capacity:
            demand_gap = ((predicted_volume - request.road_capacity) / request.road_capacity) * 100
        confidence = min(0.95, 0.6 + (0.05 * len(factors)))
        yearly_projections = []
        for i in range(years + 1):
            year_vol = int(request.base_traffic_volume * ((1 + avg_growth / 100) ** i))
            yearly_projections.append({
                "year": request.base_year + i,
                "volume": year_vol,
                "growth_from_base": ((year_vol / max(request.base_traffic_volume, 1)) - 1) * 100,
            })
        ai_insights = await self._generate_ai_insights_simple(
            request, predicted_volume, avg_growth, confidence, key_factors
        )
        recommendations = self._generate_recommendations(predicted_volume, request.road_capacity, avg_growth)
        return AIForecastResponse(
            forecast_id=None,
            location_name=request.location_name,
            predicted_traffic_volume=predicted_volume,
            growth_rate=avg_growth,
            confidence_score=confidence,
            demand_capacity_gap=demand_gap,
            key_factors=key_factors,
            ai_insights=ai_insights,
            recommendations=recommendations,
            yearly_projections=yearly_projections,
        )

    async def _generate_ai_insights_simple(
        self, request: AIForecastRequest, predicted: int, growth: float, confidence: float, factors: list
    ) -> str:
        if not self.client:
            return f"Predicted {growth:.1f}% growth over {request.target_year - request.base_year} years. Key drivers: population growth, economic development, and vehicle ownership increase."
        prompt = f"""
        Traffic forecast for {request.location_name}:
        - Period: {request.base_year} to {request.target_year}
        - Base volume: {request.base_traffic_volume} vehicles/day
        - Predicted: {predicted} vehicles/day
        - Growth rate: {growth:.1f}%
        
        Provide a brief insight (max 100 words) on this forecast.
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
            )
            return response.choices[0].message.content or "AI insight not available"
        except Exception:
            return f"Predicted {growth:.1f}% growth. Monitor key factors for accuracy."

    def _generate_recommendations(
        self, predicted: int, capacity: int | None, growth: float
    ) -> list[str]:
        recommendations = []
        if capacity and predicted > capacity:
            gap_pct = ((predicted - capacity) / capacity) * 100
            recommendations.append(f"Capacity expansion required - predicted demand exceeds current capacity by {gap_pct:.0f}%")
        if growth > 5:
            recommendations.append("High growth rate detected - consider phased infrastructure development")
        recommendations.append("Regular monitoring of growth factors recommended for forecast accuracy")
        recommendations.append("Consider multi-modal transport options to manage demand")
        return recommendations

    async def calculate_demand_capacity_gap(
        self, db: AsyncSession, forecast_id: uuid.UUID
    ) -> DemandCapacityGapResponse:
        forecast = await db.get(Forecast, forecast_id)
        if not forecast:
            raise ValueError("Forecast not found")
        if not forecast.road_capacity:
            raise ValueError("Road capacity not set for this forecast")
        current_demand = forecast.base_traffic_volume
        projected_demand = forecast.predicted_traffic_volume or current_demand
        capacity = forecast.road_capacity
        gap = projected_demand - capacity
        gap_pct = (gap / capacity) * 100 if capacity else 0
        utilization = (current_demand / capacity) * 100 if capacity else 0
        recommended_increase = max(0, int(gap * 1.2))
        priority = "low"
        if gap_pct > 30:
            priority = "critical"
        elif gap_pct > 15:
            priority = "high"
        elif gap_pct > 5:
            priority = "medium"
        return DemandCapacityGapResponse(
            forecast_id=forecast_id,
            location_name=forecast.location_name,
            base_year=forecast.start_year,
            target_year=forecast.end_year,
            current_capacity=capacity,
            current_demand=current_demand,
            projected_demand=projected_demand,
            demand_capacity_gap=gap_pct,
            gap_percentage=gap_pct,
            capacity_utilization=utilization,
            recommended_capacity_increase=recommended_increase,
            priority=priority,
        )

    async def get_trend_analysis(
        self, db: AsyncSession, location: str, start_year: int, end_year: int
    ) -> TrendAnalysisResponse:
        result = await db.execute(
            select(HistoricalTrend)
            .where(HistoricalTrend.location_name == location)
            .where(HistoricalTrend.year >= start_year)
            .where(HistoricalTrend.year <= end_year)
            .order_by(HistoricalTrend.year)
        )
        trends = list(result.scalars().all())
        if not trends:
            trends = await self._generate_mock_historical_trends(location, start_year, end_year)
        data_points = [
            {
                "year": t.year,
                "traffic_volume": t.traffic_volume,
                "population": t.population,
                "vehicle_count": t.vehicle_count,
            }
            for t in trends
        ]
        volumes = [t.traffic_volume for t in trends]
        avg_growth = 0
        if len(volumes) > 1:
            total_growth = ((volumes[-1] - volumes[0]) / max(volumes[0], 1)) * 100
            avg_growth = total_growth / (len(volumes) - 1)
        trend_dir = "increasing" if avg_growth > 0 else "decreasing" if avg_growth < 0 else "stable"
        return TrendAnalysisResponse(
            location_name=location,
            period_start=start_year,
            period_end=end_year,
            data_points=data_points,
            trend_direction=trend_dir,
            average_growth_rate=avg_growth,
            volatility=2.5,
            seasonality_detected=True,
            forecast_adjustment_recommended=avg_growth * 0.1,
        )

    async def _generate_mock_historical_trends(
        self, location: str, start_year: int, end_year: int
    ) -> list[HistoricalTrend]:
        base_volume = 50000
        trends = []
        for year in range(start_year, end_year + 1):
            growth = (year - start_year) * 0.05
            volume = int(base_volume * (1 + growth))
            trends.append(HistoricalTrend(
                location_name=location,
                year=year,
                traffic_volume=volume,
                population=int(500000 * (1 + growth * 0.8)),
                vehicle_count=int(100000 * (1 + growth * 1.2)),
                gdp_growth=6.5 + (year % 3),
            ))
        return trends


forecasting_service = ForecastingService()
