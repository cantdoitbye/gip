"""
Site Analysis Service - Business logic for infrastructure site analysis
"""
import uuid
from datetime import datetime
from typing import Any
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config import settings
from app.models.site import Site, SiteFactor, RiskZone, SiteAnalysis, SiteStatus, SiteType
from app.schemas.site import (
    SiteCreate,
    SiteUpdate,
    SiteResponse,
    SiteListResponse,
    SiteFactorResponse,
    RiskZoneResponse,
    SiteAnalysisResponse,
    AISiteAnalysisRequest,
    AISiteAnalysisResponse,
)
from app.stubs.gis_api import gis_api_stub
from app.stubs.population_api import population_api_stub
from app.stubs.economic_api import economic_api_stub
from app.stubs.land_use_api import land_use_api_stub


class SiteAnalysisService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.utility_scores = {
            "electricity": 8.5,
            "water": 7.2,
            "gas": 6.8,
        }
        self._data_source_note = "(Simulated Data - Stub API)"

    async def create_site(
        self, db: AsyncSession, site_data: SiteCreate, user_id: uuid.UUID | None = None
    ) -> Site:
        site = Site(
            name=site_data.name,
            description=site_data.description,
            site_type=site_data.site_type or SiteType.proposed_flyover.value,
            status=SiteStatus.pending.value,
            location_name=site_data.location_name,
            address=site_data.address,
            latitude=site_data.latitude,
            longitude=site_data.longitude,
            area_sqkm=site_data.area_sqkm,
            created_by=user_id,
        )
        db.add(site)
        await db.flush()
        factors = await self._gather_factors_from_stubs(site.location_name, site.latitude, site.longitude)
        for factor_data in factors:
            factor = SiteFactor(
                site_id=site.id,
                factor_name=factor_data["name"],
                factor_type=factor_data["type"],
                score=factor_data["score"],
                weight=factor_data["weight"],
                value=factor_data.get("value"),
                unit=factor_data.get("unit"),
                source=factor_data.get("source"),
            )
            db.add(factor)
        await db.commit()
        await db.refresh(site)
        return site

    async def _gather_factors_from_stubs(self, location: str, latitude: float = 16.5, longitude: float = 80.6) -> list[dict[str, Any]]:
        factors = []
        terrain_data = gis_api_stub.get_terrain_data(latitude, longitude)
        terrain_score = self._calculate_terrain_score(terrain_data)
        factors.append({
            "name": "Terrain Suitability",
            "type": "environmental",
            "score": terrain_score,
            "weight": 0.15,
            "value": terrain_data["elevation_m"],
            "unit": "meters",
            "source": f"GIS API {self._data_source_note}",
            "details": {
                "soil_type": terrain_data["soil_type"],
                "slope_degrees": terrain_data["slope_degrees"],
                "ground_water_depth_m": terrain_data["ground_water_depth_m"],
            },
        })
        env_data = gis_api_stub.get_environmental_data(latitude, longitude)
        env_score = self._calculate_environmental_score(env_data)
        factors.append({
            "name": "Environmental Quality",
            "type": "environmental",
            "score": env_score,
            "weight": 0.10,
            "value": env_data["air_quality_index"],
            "unit": "AQI",
            "source": f"Environmental Survey {self._data_source_note}",
            "details": {
                "noise_level_db": round(env_data["noise_level_db"], 1),
                "water_quality_index": round(env_data["water_quality_index"], 1),
                "green_cover_percent": round(env_data["green_cover_percent"], 1),
            },
        })
        risks = gis_api_stub.get_risk_assessment(latitude, longitude)
        risk_score = self._calculate_risk_score(risks)
        factors.append({
            "name": "Risk Assessment",
            "type": "risk",
            "score": risk_score,
            "weight": 0.15,
            "value": risk_score,
            "unit": "score",
            "source": f"GIS API {self._data_source_note}",
            "details": {
                "risk_count": len(risks.get("risks", [])),
                "overall_risk_score": round(risks.get("overall_risk_score", 0), 2),
            },
        })
        pop_data = population_api_stub.get_population_data(location)
        pop_score = min(pop_data["density_per_sqkm"] / 1000, 10.0)
        factors.append({
            "name": "Population Density",
            "type": "demographic",
            "score": pop_score,
            "weight": 0.10,
            "value": pop_data["density_per_sqkm"],
            "unit": "per sq km",
            "source": f"Census API {self._data_source_note}",
            "details": {
                "current_population": pop_data["current_population"],
                "growth_rate": pop_data["growth_rate"],
                "households": pop_data["households"],
            },
        })
        employment_data = population_api_stub.get_employment_data(location)
        employment_score = employment_data["employment_rate"] / 10
        factors.append({
            "name": "Employment Rate",
            "type": "demographic",
            "score": employment_score,
            "weight": 0.05,
            "value": employment_data["employment_rate"],
            "unit": "percent",
            "source": f"Employment Statistics {self._data_source_note}",
            "details": {
                "unemployment_rate": employment_data["unemployment_rate"],
                "services_sector_percent": employment_data["sectors"]["services"],
            },
        })
        econ_data = economic_api_stub.get_economic_indicators(location)
        econ_score = min(econ_data["gdp_growth_rate"] / 10, 10.0)
        factors.append({
            "name": "Economic Activity",
            "type": "economic",
            "score": econ_score,
            "weight": 0.10,
            "value": econ_data["gdp_per_capita"],
            "unit": "INR",
            "source": f"Economic Survey {self._data_source_note}",
            "details": {
                "gdp_growth_rate": econ_data["gdp_growth_rate"],
                "unemployment_rate": econ_data["unemployment_rate"],
            },
        })
        land_data = land_use_api_stub.get_land_use_data(location)
        land_score = self._calculate_land_use_score(land_data)
        factors.append({
            "name": "Land Use Compatibility",
            "type": "planning",
            "score": land_score,
            "weight": 0.10,
            "value": land_data["commercial_percent"],
            "unit": "percent",
            "source": f"Land Records {self._data_source_note}",
            "details": {
                "urban_area_percent": land_data["urban_area_percent"],
                "industrial_percent": land_data["industrial_percent"],
                "avg_land_price_per_sqft": land_data["avg_land_price_per_sqft"],
            },
        })
        zoning_data = land_use_api_stub.get_zoning_info(location)
        zoning_score = self._calculate_zoning_score(zoning_data)
        factors.append({
            "name": "Zoning Compliance",
            "type": "planning",
            "score": zoning_score,
            "weight": 0.05,
            "value": zoning_score,
            "unit": "score",
            "source": f"Zoning Regulations {self._data_source_note}",
            "details": {
                "max_fsi_cbd": zoning_data["zones"]["central_business_district"]["max_fsi"],
                "min_road_width_m": zoning_data["infrastructure_requirements"]["minimum_road_width_m"],
            },
        })
        infra_data = gis_api_stub.get_infrastructure_data(latitude, longitude)
        infra_score = self._calculate_infrastructure_score(infra_data)
        factors.append({
            "name": "Infrastructure Access",
            "type": "infrastructure",
            "score": infra_score,
            "weight": 0.10,
            "value": infra_score,
            "unit": "score",
            "source": f"Infrastructure Survey {self._data_source_note}",
            "details": {
                "nearest_highway_km": round(infra_data["nearest_highway_km"], 1),
                "nearest_railway_km": round(infra_data["nearest_railway_km"], 1),
                "power_substation_km": round(infra_data["power_substation_km"], 1),
            },
        })
        access_data = gis_api_stub.get_accessibility_data(latitude, longitude)
        access_score = self._calculate_accessibility_score(access_data)
        factors.append({
            "name": "Accessibility",
            "type": "infrastructure",
            "score": access_score,
            "weight": 0.05,
            "value": access_score,
            "unit": "score",
            "source": f"Accessibility Survey {self._data_source_note}",
            "details": {
                "hospitals_within_5km": access_data["hospitals_within_5km"],
                "schools_within_2km": access_data["schools_within_2km"],
                "public_transit_stops": access_data["public_transit_stops_within_500m"],
            },
        })
        utility_costs = gis_api_stub.get_utility_costs(location)
        utility_score = self._calculate_utility_cost_score(utility_costs)
        factors.append({
            "name": "Utility Costs",
            "type": "economic",
            "score": utility_score,
            "weight": 0.05,
            "value": utility_costs["electricity_per_unit"],
            "unit": "per unit",
            "source": f"Utility Tariffs {self._data_source_note}",
            "details": {
                "water_per_kl": utility_costs["water_per_kl"],
                "internet_monthly": utility_costs["internet_monthly"],
            },
        })
        return factors

    def _calculate_risk_score(self, risks: dict[str, Any]) -> float:
        if not risks:
            return 10.0
        risk_list = risks.get("risks", [])
        if not risk_list:
            return 10.0
        total_score = 0.0
        for risk in risk_list:
            prob = risk.get("probability", 0)
            total_score += prob
        avg_score = total_score / max(len(risk_list), 1)
        return max(10.0 - avg_score * 10, 0.0)

    async def analyze_site(
        self, db: AsyncSession, site_id: uuid.UUID, run_analysis: bool = True
    ) -> Site:
        site = await db.get(Site, site_id)
        if not site:
            raise ValueError("Site not found")
        site.status = SiteStatus.analyzing.value
        await db.commit()
        try:
            terrain_data = gis_api_stub.get_terrain_data(site.latitude, site.longitude)
            env_data = gis_api_stub.get_environmental_data(site.latitude, site.longitude)
            risks = gis_api_stub.get_risk_assessment(site.latitude, site.longitude)
            infra_data = gis_api_stub.get_infrastructure_data(site.latitude, site.longitude)
            access_data = gis_api_stub.get_accessibility_data(site.latitude, site.longitude)
            utility_costs = gis_api_stub.get_utility_costs(site.location_name)
            pop_data = population_api_stub.get_population_data(site.location_name)
            employment_data = population_api_stub.get_employment_data(site.location_name)
            econ_data = economic_api_stub.get_economic_indicators(site.location_name)
            land_data = land_use_api_stub.get_land_use_data(site.location_name)
            zoning_data = land_use_api_stub.get_zoning_info(site.location_name)
            road_data = land_use_api_stub.get_road_network_data(site.location_name)
            comprehensive_data = {
                "terrain": terrain_data,
                "environmental": env_data,
                "risks": risks,
                "infrastructure": infra_data,
                "accessibility": access_data,
                "utility_costs": utility_costs,
                "population": pop_data,
                "employment": employment_data,
                "economic": econ_data,
                "land_use": land_data,
                "zoning": zoning_data,
                "road_network": road_data,
            }
            overall_score = self._calculate_comprehensive_score(comprehensive_data)
            site.overall_score = overall_score
            site.ai_recommendation = await self._generate_ai_recommendation(
                site, comprehensive_data, overall_score
            )
            site.status = SiteStatus.analyzed.value
            await db.commit()
            await db.refresh(site)
            return site
        except Exception as e:
            site.status = SiteStatus.pending.value
            site.ai_recommendation = f"Analysis failed: {str(e)}"
            await db.commit()
            raise

    def _calculate_comprehensive_score(self, data: dict[str, Any]) -> float:
        scores = {
            "terrain": self._calculate_terrain_score(data["terrain"]),
            "environmental": self._calculate_environmental_score(data["environmental"]),
            "risk": self._calculate_risk_score(data["risks"]),
            "infrastructure": self._calculate_infrastructure_score(data["infrastructure"]),
            "accessibility": self._calculate_accessibility_score(data["accessibility"]),
            "population": min(data["population"]["density_per_sqkm"] / 1000, 10.0),
            "employment": data["employment"]["employment_rate"] / 10,
            "economy": min(data["economic"]["gdp_growth_rate"] / 10, 10.0),
            "landUse": self._calculate_land_use_score(data["land_use"]),
            "zoning": self._calculate_zoning_score(data["zoning"]),
            "roadNetwork": min(data["road_network"]["connectivity_score"], 10.0),
        }
        weights = {
            "terrain": 0.10,
            "environmental": 0.08,
            "risk": 0.12,
            "infrastructure": 0.12,
            "accessibility": 0.08,
            "population": 0.08,
            "employment": 0.05,
            "economy": 0.10,
            "landUse": 0.10,
            "zoning": 0.07,
            "roadNetwork": 0.10,
        }
        total = 0.0
        for key in scores:
            total += scores[key] * weights.get(key, 0.05)
        return round(min(total, 10.0), 2)

    def _calculate_terrain_score(self, terrain_data: dict[str, Any]) -> float:
        score = 8.0
        if terrain_data.get("slope_degrees", 0) > 10:
            score -= 2.0
        elif terrain_data.get("slope_degrees", 0) > 5:
            score -= 1.0
        if terrain_data.get("flood_risk") == "high":
            score -= 2.0
        elif terrain_data.get("flood_risk") == "moderate":
            score -= 1.0
        if terrain_data.get("ground_water_depth_m", 20) > 30:
            score -= 1.0
        return max(score, 1.0)

    def _calculate_environmental_score(self, env_data: dict[str, Any]) -> float:
        score = 10.0
        aqi = env_data.get("air_quality_index", 100)
        if aqi > 150:
            score -= 2.0
        elif aqi > 100:
            score -= 1.0
        noise = env_data.get("noise_level_db", 60)
        if noise > 70:
            score -= 1.0
        elif noise > 60:
            score -= 0.5
        green_cover = env_data.get("green_cover_percent", 20)
        if green_cover < 15:
            score -= 1.0
        protected_areas = env_data.get("protected_areas_within_5km", 0)
        if protected_areas > 3:
            score -= 1.0
        return max(score, 1.0)

    def _calculate_infrastructure_score(self, infra_data: dict[str, Any]) -> float:
        score = 10.0
        if infra_data.get("nearest_highway_km", 5) > 10:
            score -= 1.5
        elif infra_data.get("nearest_highway_km", 5) > 5:
            score -= 0.5
        if infra_data.get("power_substation_km", 3) > 5:
            score -= 1.0
        if infra_data.get("water_supply") != "available":
            score -= 2.0
        if infra_data.get("electricity_grid") != "available":
            score -= 2.0
        return max(score, 1.0)

    def _calculate_accessibility_score(self, access_data: dict[str, Any]) -> float:
        score = 10.0
        if access_data.get("hospitals_within_5km", 3) < 1:
            score -= 1.5
        if access_data.get("schools_within_2km", 5) < 2:
            score -= 1.0
        if access_data.get("public_transit_stops_within_500m", 5) < 2:
            score -= 1.0
        return max(score, 1.0)

    def _calculate_land_use_score(self, land_data: dict[str, Any]) -> float:
        score = 8.0
        commercial = land_data.get("commercial_percent", 10)
        industrial = land_data.get("industrial_percent", 10)
        if commercial > 15:
            score += 1.0
        elif commercial > 10:
            score += 0.5
        if industrial > 15:
            score += 0.5
        return min(score, 10.0)

    def _calculate_zoning_score(self, zoning_data: dict[str, Any]) -> float:
        score = 7.5
        cbd_fsi = zoning_data.get("zones", {}).get("central_business_district", {}).get("max_fsi", 3.0)
        if cbd_fsi >= 4.0:
            score += 1.5
        elif cbd_fsi >= 3.0:
            score += 1.0
        infra_req = zoning_data.get("infrastructure_requirements", {})
        if infra_req.get("rainwater_harvesting"):
            score += 0.5
        return min(score, 10.0)

    def _calculate_utility_cost_score(self, utility_costs: dict[str, Any]) -> float:
        score = 10.0
        elec_cost = utility_costs.get("electricity_per_unit", 0.006)
        if elec_cost > 0.008:
            score -= 1.5
        elif elec_cost > 0.006:
            score -= 0.5
        water_cost = utility_costs.get("water_per_kl", 50)
        if water_cost > 60:
            score -= 1.0
        return max(score, 1.0)

    def _calculate_overall_score(
        self,
        terrain_data: dict[str, Any],
        risks: dict[str, Any],
        pop_data: dict[str, Any],
        econ_data: dict[str, Any],
        land_data: dict[str, Any],
    ) -> float:
        risk_score = self._calculate_risk_score(risks)
        scores = {
            "terrain": self._calculate_terrain_score(terrain_data),
            "risk": risk_score,
            "population": min(pop_data["density_per_sqkm"] / 1000, 10.0),
            "economy": min(econ_data["gdp_growth_rate"] / 10, 10.0),
            "landUse": self._calculate_land_use_score(land_data),
        }
        weights = {
            "terrain": 0.20,
            "risk": 0.25,
            "population": 0.15,
            "economy": 0.20,
            "landUse": 0.20,
        }
        total = 0.0
        for key in scores:
            total += scores[key] * weights[key]
        return min(total, 10.0)

    async def _generate_ai_recommendation(
        self,
        site: Site | None,
        comprehensive_data: dict[str, Any],
        overall_score: float,
    ) -> str:
        if not self.client:
            return self._generate_mock_recommendation(site, comprehensive_data, overall_score)
        site_name = site.name if site else "Unknown Location"
        location_name = site.location_name if site else "Unknown"
        site_type = site.site_type if site else "infrastructure"
        latitude = site.latitude if site else 0.0
        longitude = site.longitude if site else 0.0
        
        terrain = comprehensive_data.get("terrain", {})
        env_data = comprehensive_data.get("environmental", {})
        risks = comprehensive_data.get("risks", {})
        pop_data = comprehensive_data.get("population", {})
        econ_data = comprehensive_data.get("economic", {})
        land_data = comprehensive_data.get("land_use", {})
        infra_data = comprehensive_data.get("infrastructure", {})
        employment_data = comprehensive_data.get("employment", {})
        
        prompt = f"""
Analyze the site for infrastructure development:

Site: {site_name}
Location: {location_name}
Type: {site_type}
Coordinates: ({latitude}, {longitude})

Terrain & Environmental Factors:
- Elevation: {terrain.get('elevation_m', 'N/A')}m
- Soil Type: {terrain.get('soil_type', 'N/A')}
- Slope: {terrain.get('slope_degrees', 'N/A')}°
- Flood Risk: {terrain.get('flood_risk', 'N/A')}
- Air Quality Index: {round(env_data.get('air_quality_index', 0), 1)}
- Green Cover: {round(env_data.get('green_cover_percent', 0), 1)}%

Risk Assessment:
- Risk Score: {self._calculate_risk_score(risks):.1f}/10
- Active Risks: {len(risks.get('risks', []))}

Demographics:
- Population Density: {pop_data.get('density_per_sqkm', 'N/A')} per sq km
- Growth Rate: {pop_data.get('growth_rate', 'N/A')}%
- Employment Rate: {employment_data.get('employment_rate', 'N/A')}%

Economic Factors:
- GDP Growth: {econ_data.get('gdp_growth_rate', 'N/A')}%
- GDP per Capita: ₹{econ_data.get('gdp_per_capita', 'N/A'):,}

Land Use:
- Commercial: {land_data.get('commercial_percent', 'N/A')}%
- Industrial: {land_data.get('industrial_percent', 'N/A')}%
- Avg Land Price: ₹{land_data.get('avg_land_price_per_sqft', 'N/A')}/sq ft

Infrastructure:
- Nearest Highway: {round(infra_data.get('nearest_highway_km', 0), 1)} km
- Power Substation: {round(infra_data.get('power_substation_km', 0), 1)} km
- Water Supply: {infra_data.get('water_supply', 'N/A')}

Overall Score: {overall_score:.1f}/10

Provide a comprehensive recommendation (max 200 words) covering:
1. Site viability assessment
2. Key advantages
3. Potential challenges and mitigation strategies
4. Development recommendations
"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an infrastructure planning expert with deep knowledge of site analysis, urban planning, and risk assessment."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=300,
            )
            return response.choices[0].message.content or self._generate_mock_recommendation(
                site, comprehensive_data, overall_score
            )
        except Exception:
            return self._generate_mock_recommendation(site, comprehensive_data, overall_score)

    def _generate_mock_recommendation(
        self,
        site: Site | None,
        comprehensive_data: dict[str, Any],
        overall_score: float,
    ) -> str:
        site_name = site.name if site else "Unknown Location"
        location_name = site.location_name if site else "Unknown"
        site_type = site.site_type if site else "infrastructure"
        risk_level = "low" if overall_score >= 7 else "moderate" if overall_score >= 5 else "high"
        terrain = comprehensive_data.get("terrain", {})
        env_data = comprehensive_data.get("environmental", {})
        risks = comprehensive_data.get("risks", {})
        pop_data = comprehensive_data.get("population", {})
        infra_data = comprehensive_data.get("infrastructure", {})
        risk_types = [r.get("type", "unknown") for r in risks.get("risks", [])]
        risk_str = ", ".join(risk_types) if risk_types else "None identified"
        return f"""Site Analysis Report for {site_name} {self._data_source_note}

Location: {location_name}
Type: {site_type}
Overall Score: {overall_score:.1f}/10
Risk Level: {risk_level}

=== TERRAIN & ENVIRONMENT ===
- Elevation: {terrain.get('elevation_m', 'N/A')}m
- Soil Type: {terrain.get('soil_type', 'N/A')}
- Air Quality Index: {round(env_data.get('air_quality_index', 0), 1)}
- Green Cover: {round(env_data.get('green_cover_percent', 0), 1)}%

=== RISK ASSESSMENT ===
- Identified Risks: {risk_str}
- Overall Risk Score: {self._calculate_risk_score(risks):.1f}/10

=== DEMOGRAPHICS ===
- Population Density: {pop_data.get('density_per_sqkm', 'N/A')} per sq km
- Growth Rate: {pop_data.get('growth_rate', 'N/A')}%

=== INFRASTRUCTURE ===
- Highway Access: {round(infra_data.get('nearest_highway_km', 0), 1)} km
- Water Supply: {infra_data.get('water_supply', 'N/A')}
- Power Grid: {infra_data.get('electricity_grid', 'N/A')}

=== RECOMMENDATION ===
This site is classified as {risk_level} risk for infrastructure development.
{"Proceed with standard planning and environmental assessments." if risk_level == "low" else "Conduct detailed feasibility studies before proceeding." if risk_level == "moderate" else "Significant mitigation measures required. Consider alternative sites."}

(Mock analysis - OpenAI API key not configured)"""

    async def ai_analyze_site(self, request: AISiteAnalysisRequest) -> AISiteAnalysisResponse:
        terrain_data = gis_api_stub.get_terrain_data(request.latitude, request.longitude)
        env_data = gis_api_stub.get_environmental_data(request.latitude, request.longitude)
        risks = gis_api_stub.get_risk_assessment(request.latitude, request.longitude)
        infra_data = gis_api_stub.get_infrastructure_data(request.latitude, request.longitude)
        access_data = gis_api_stub.get_accessibility_data(request.latitude, request.longitude)
        utility_costs = gis_api_stub.get_utility_costs(request.location_name)
        pop_data = population_api_stub.get_population_data(request.location_name)
        employment_data = population_api_stub.get_employment_data(request.location_name)
        econ_data = economic_api_stub.get_economic_indicators(request.location_name)
        land_data = land_use_api_stub.get_land_use_data(request.location_name)
        zoning_data = land_use_api_stub.get_zoning_info(request.location_name)
        road_data = land_use_api_stub.get_road_network_data(request.location_name)
        comprehensive_data = {
            "terrain": terrain_data,
            "environmental": env_data,
            "risks": risks,
            "infrastructure": infra_data,
            "accessibility": access_data,
            "utility_costs": utility_costs,
            "population": pop_data,
            "employment": employment_data,
            "economic": econ_data,
            "land_use": land_data,
            "zoning": zoning_data,
            "road_network": road_data,
        }
        overall_score = self._calculate_comprehensive_score(comprehensive_data)
        recommendation = await self._generate_ai_recommendation(
            None, comprehensive_data, overall_score
        )
        return AISiteAnalysisResponse(
            site_id=None,
            location_name=request.location_name,
            latitude=request.latitude,
            longitude=request.longitude,
            overall_suitability_score=overall_score,
            land_suitability_score=self._calculate_terrain_score(terrain_data),
            connectivity_score=road_data.get("connectivity_score", 7.0),
            infrastructure_score=self._calculate_infrastructure_score(infra_data),
            environmental_score=self._calculate_environmental_score(env_data),
            economic_score=min(econ_data.get("gdp_growth_rate", 5) / 10, 10.0),
            social_score=min(pop_data.get("density_per_sqkm", 0) / 1000, 10.0),
            risk_score=self._calculate_risk_score(risks),
            recommendation=recommendation,
            ai_analysis=recommendation,
            detailed_factors={
                "terrain": {**terrain_data, "_source": f"GIS API {self._data_source_note}"},
                "environmental": {**env_data, "_source": f"Environmental Survey {self._data_source_note}"},
                "risks": {**risks, "_source": f"Risk Assessment {self._data_source_note}"},
                "infrastructure": {**infra_data, "_source": f"Infrastructure Survey {self._data_source_note}"},
                "accessibility": {**access_data, "_source": f"Accessibility Survey {self._data_source_note}"},
                "population": {**pop_data, "_source": f"Census API {self._data_source_note}"},
                "employment": {**employment_data, "_source": f"Employment Statistics {self._data_source_note}"},
                "economy": {**econ_data, "_source": f"Economic Survey {self._data_source_note}"},
                "land_use": {**land_data, "_source": f"Land Records {self._data_source_note}"},
                "zoning": {**zoning_data, "_source": f"Zoning Regulations {self._data_source_note}"},
                "road_network": {**road_data, "_source": f"Road Statistics {self._data_source_note}"},
            },
        )

    async def get_site(self, db: AsyncSession, site_id: uuid.UUID) -> Site | None:
        return await db.get(Site, site_id)

    async def list_sites(
        self,
        db: AsyncSession,
        page: int = 1,
        page_size: int = 10,
        site_type: str | None = None,
        status: str | None = None,
    ) -> tuple[list[Site], int]:
        from sqlalchemy.orm import selectinload
        query = select(Site).options(selectinload(Site.factors))
        if site_type:
            query = query.where(Site.site_type == site_type)
        if status:
            query = query.where(Site.status == status)
        query = query.order_by(Site.created_at.desc())
        offset = (page - 1) * page_size
        result = await db.execute(query.offset(offset).limit(page_size))
        sites = list(result.scalars().all())
        count_query = select(Site)
        if site_type:
            count_query = count_query.where(Site.site_type == site_type)
        if status:
            count_query = count_query.where(Site.status == status)
        count_result = await db.execute(count_query)
        total = len(list(count_result.scalars().all()))
        return sites, total


site_analysis_service = SiteAnalysisService()
