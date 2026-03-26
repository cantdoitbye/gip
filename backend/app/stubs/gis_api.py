import random
from datetime import datetime
from typing import Any


class GISAPIStub:
    """
    Stub service for GIS and environmental data API.
    Simulates government GIS API responses.
    """

    def __init__(self):
        self.locations = {
            "vijayawada": {
                "elevation": 12,
                "soil_type": "alluvial",
                "flood_zone": "low",
                "seismic_zone": "zone_2",
                "ground_water_depth": 15,
                "slope_degrees": 2,
            },
            "guntur": {
                "elevation": 33,
                "soil_type": "black_cotton",
                "flood_zone": "moderate",
                "seismic_zone": "zone_2",
                "ground_water_depth": 20,
                "slope_degrees": 1,
            },
            "visakhapatnam": {
                "elevation": 45,
                "soil_type": "laterite",
                "flood_zone": "low",
                "seismic_zone": "zone_3",
                "ground_water_depth": 12,
                "slope_degrees": 5,
            },
            "tirupati": {
                "elevation": 162,
                "soil_type": "red_sandy",
                "flood_zone": "low",
                "seismic_zone": "zone_2",
                "ground_water_depth": 25,
                "slope_degrees": 8,
            },
            "kakinada": {
                "elevation": 2,
                "soil_type": "alluvial",
                "flood_zone": "moderate",
                "seismic_zone": "zone_2",
                "ground_water_depth": 8,
                "slope_degrees": 0,
            },
            "nellore": {
                "elevation": 18,
                "soil_type": "red_loam",
                "flood_zone": "low",
                "seismic_zone": "zone_2",
                "ground_water_depth": 18,
                "slope_degrees": 1,
            },
            "kurnool": {
                "elevation": 285,
                "soil_type": "black_soil",
                "flood_zone": "low",
                "seismic_zone": "zone_2",
                "ground_water_depth": 35,
                "slope_degrees": 3,
            },
            "rajahmundry": {
                "elevation": 14,
                "soil_type": "alluvial",
                "flood_zone": "moderate",
                "seismic_zone": "zone_2",
                "ground_water_depth": 12,
                "slope_degrees": 1,
            },
            "anantapur": {
                "elevation": 335,
                "soil_type": "red_sandy",
                "flood_zone": "low",
                "seismic_zone": "zone_2",
                "ground_water_depth": 40,
                "slope_degrees": 2,
            },
            "kadapa": {
                "elevation": 138,
                "soil_type": "red_loam",
                "flood_zone": "low",
                "seismic_zone": "zone_2",
                "ground_water_depth": 30,
                "slope_degrees": 4,
            },
        }

    def get_terrain_data(self, latitude: float, longitude: float) -> dict[str, Any]:
        location_key = self._find_nearest_location(latitude, longitude)
        data = self.locations.get(location_key, self.locations["vijayawada"]).copy()
        return {
            "latitude": latitude,
            "longitude": longitude,
            "elevation_m": data["elevation"],
            "soil_type": data["soil_type"],
            "flood_risk": data["flood_zone"],
            "seismic_zone": data["seismic_zone"],
            "ground_water_depth_m": data["ground_water_depth"],
            "slope_degrees": data["slope_degrees"],
            "data_source": "GIS Survey (Stub)",
        }

    def _find_nearest_location(self, lat: float, lon: float) -> str:
        min_dist = float("inf")
        min_loc = None
        min_dist = float("inf")
        for name, data in self.locations.items():
            loc_lat = 16.5 + random.uniform(-0.5, 0.5)
            loc_lon = 80.6 + random.uniform(-0.5, 0.5)
            dist = abs(lat - loc_lat) + abs(lon - loc_lon)
            if min_dist is None or dist < min_dist:
                min_dist = dist
                min_loc = name
        return min_loc or "vijayawada"

    def get_environmental_data(self, latitude: float, longitude: float) -> dict[str, Any]:
        base_data = self.get_terrain_data(latitude, longitude)
        return {
            "latitude": latitude,
            "longitude": longitude,
            "air_quality_index": random.uniform(50, 150),
            "noise_level_db": random.uniform(45, 75),
            "water_quality_index": random.uniform(60, 95),
            "green_cover_percent": random.uniform(15, 35),
            "protected_areas_within_5km": random.randint(0, 5),
            "industrial_areas_within_2km": random.uniform(0, 3),
            "wetlands_within_5km": random.uniform(0, 2),
            "data_source": "Environmental Survey (Stub)",
        }

    def get_risk_assessment(self, latitude: float, longitude: float) -> dict[str, Any]:
        terrain = self.get_terrain_data(latitude, longitude)
        risks = []
        flood_risk = self._assess_flood_risk(terrain)
        if flood_risk > 0.3:
            risks.append({
                "type": "flood",
                "probability": flood_risk,
                "severity": "high" if flood_risk > 0.6 else "moderate",
                "mitigation": "Adequate drainage system required",
            })
        seismic_risk = self._assess_seismic_risk(terrain)
        if seismic_risk > 0.2:
            risks.append({
                "type": "seismic",
                "probability": seismic_risk,
                "severity": "high" if seismic_risk > 0.4 else "moderate",
                "mitigation": "Seismic-resistant construction required",
            })
        if terrain["slope_degrees"] > 5:
            risks.append({
                "type": "landslide",
                "probability": min(terrain["slope_degrees"] / 10, 0.9),
                "severity": "moderate",
                "mitigation": "Slope stabilization measures needed",
            })
        return {
            "latitude": latitude,
            "longitude": longitude,
            "overall_risk_score": sum(r["probability"] for r in risks) / max(len(risks), 1) if risks else 0,
            "risks": risks,
            "recommendations": [
                "Conduct detailed geotechnical survey",
                "Implement risk mitigation measures",
                "Regular monitoring and maintenance",
            ],
            "data_source": "Risk Assessment (Stub)",
        }

    def _assess_flood_risk(self, terrain: dict) -> float:
        zone_scores = {"low": 0.2, "moderate": 0.5, "high": 0.8}
        return zone_scores.get(terrain.get("flood_zone", "low"), 0.2)

    def _assess_seismic_risk(self, terrain: dict) -> float:
        zone_scores = {"zone_1": 0.1, "zone_2": 0.3, "zone_3": 0.5, "zone_4": 0.7, "zone_5": 0.9}
        return zone_scores.get(terrain.get("seismic_zone", "zone_2"), 0.3)

    def get_infrastructure_data(self, latitude: float, longitude: float) -> dict[str, Any]:
        return {
            "latitude": latitude,
            "longitude": longitude,
            "nearest_highway_km": random.uniform(0.5, 5),
            "nearest_railway_km": random.uniform(1, 15),
            "nearest_airport_km": random.uniform(10, 50),
            "power_substation_km": random.uniform(0.5, 3),
            "water_supply": "available",
            "electricity_grid": "available",
            "gas_pipeline": random.choice([True, False]),
            "sewage_system": "available",
            "telecom_infrastructure": "fiber_available",
            "data_source": "Infrastructure Survey (Stub)",
        }

    def get_accessibility_data(self, latitude: float, longitude: float) -> dict[str, Any]:
        return {
            "latitude": latitude,
            "longitude": longitude,
            "major_roads_within_1km": random.randint(2, 8),
            "public_transit_stops_within_500m": random.randint(1, 10),
            "hospitals_within_5km": random.randint(1, 5),
            "schools_within_2km": random.randint(2, 10),
            "markets_within_2km": random.randint(1, 5),
            "banks_within_3km": random.randint(1, 8),
            "police_stations_within_5km": random.randint(1, 3),
            "fire_stations_within_5km": random.randint(1, 3),
            "data_source": "Accessibility Survey (Stub)",
        }

    def get_utility_costs(self, location: str) -> dict[str, Any]:
        base_cost = random.randint(5000, 15000)
        return {
            "location": location,
            "electricity_per_unit": round(base_cost * 0.001 + random.uniform(-0.0002, 0.0002), 4),
            "water_per_kl": round(base_cost * 0.05 + random.uniform(-0.005, 0.005), 2),
            "gas_per_unit": round(base_cost * 0.002 + random.uniform(-0.0002, 0.0002), 4),
            "internet_monthly": round(base_cost * 0.5 + random.uniform(-50, 50), 2),
            "data_source": "Utility Tariffs (Stub)",
        }


gis_api_stub = GISAPIStub()
