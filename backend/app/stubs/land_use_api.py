import random
from datetime import datetime
from typing import Any


class LandUseAPIStub:
    """
    Stub service for land use and registry data API.
    Simulates government land records API responses.
    """

    def __init__(self):
        self.land_data = {
            "vijayawada": {
                "total_area_sqkm": 103,
                "urban_area_percent": 78,
                "commercial_percent": 12,
                "industrial_percent": 8,
                "residential_percent": 45,
                "agricultural_percent": 15,
                "open_spaces_percent": 12,
                "avg_land_price_per_sqft": 8500,
            },
            "guntur": {
                "total_area_sqkm": 168,
                "urban_area_percent": 62,
                "commercial_percent": 10,
                "industrial_percent": 12,
                "residential_percent": 40,
                "agricultural_percent": 25,
                "open_spaces_percent": 13,
                "avg_land_price_per_sqft": 5200,
            },
            "visakhapatnam": {
                "total_area_sqkm": 540,
                "urban_area_percent": 55,
                "commercial_percent": 15,
                "industrial_percent": 18,
                "residential_percent": 38,
                "agricultural_percent": 15,
                "open_spaces_percent": 14,
                "avg_land_price_per_sqft": 7800,
            },
            "tirupati": {
                "total_area_sqkm": 125,
                "urban_area_percent": 58,
                "commercial_percent": 14,
                "industrial_percent": 6,
                "residential_percent": 42,
                "agricultural_percent": 22,
                "open_spaces_percent": 16,
                "avg_land_price_per_sqft": 4800,
            },
            "kakinada": {
                "total_area_sqkm": 192,
                "urban_area_percent": 52,
                "commercial_percent": 11,
                "industrial_percent": 15,
                "residential_percent": 38,
                "agricultural_percent": 24,
                "open_spaces_percent": 12,
                "avg_land_price_per_sqft": 4500,
            },
            "nellore": {
                "total_area_sqkm": 247,
                "urban_area_percent": 48,
                "commercial_percent": 9,
                "industrial_percent": 10,
                "residential_percent": 40,
                "agricultural_percent": 28,
                "open_spaces_percent": 13,
                "avg_land_price_per_sqft": 3800,
            },
            "kurnool": {
                "total_area_sqkm": 195,
                "urban_area_percent": 42,
                "commercial_percent": 8,
                "industrial_percent": 7,
                "residential_percent": 38,
                "agricultural_percent": 35,
                "open_spaces_percent": 12,
                "avg_land_price_per_sqft": 2800,
            },
            "rajahmundry": {
                "total_area_sqkm": 154,
                "urban_area_percent": 55,
                "commercial_percent": 10,
                "industrial_percent": 8,
                "residential_percent": 42,
                "agricultural_percent": 25,
                "open_spaces_percent": 15,
                "avg_land_price_per_sqft": 4200,
            },
            "anantapur": {
                "total_area_sqkm": 285,
                "urban_area_percent": 38,
                "commercial_percent": 7,
                "industrial_percent": 12,
                "residential_percent": 35,
                "agricultural_percent": 35,
                "open_spaces_percent": 11,
                "avg_land_price_per_sqft": 2500,
            },
            "kadapa": {
                "total_area_sqkm": 164,
                "urban_area_percent": 45,
                "commercial_percent": 8,
                "industrial_percent": 6,
                "residential_percent": 40,
                "agricultural_percent": 30,
                "open_spaces_percent": 16,
                "avg_land_price_per_sqft": 3200,
            },
        }

    def get_land_use_data(self, location: str) -> dict[str, Any]:
        location_key = location.lower().replace(" ", "_")
        if location_key not in self.land_data:
            location_key = "vijayawada"
        data = self.land_data[location_key].copy()
        data["location"] = location
        data["data_source"] = "Land Records 2024 (Stub)"
        data["last_updated"] = datetime.utcnow().isoformat()
        return data

    def get_available_parcels(
        self, location: str, min_area: float = 0, max_area: float = 100000
    ) -> dict[str, Any]:
        parcels = []
        num_parcels = random.randint(5, 15)
        base_data = self.get_land_use_data(location)
        for i in range(num_parcels):
            area = random.uniform(500, 50000)
            if min_area <= area <= max_area:
                parcels.append(
                    {
                        "parcel_id": f"PARCEL-{location[:3].upper()}-{random.randint(1000, 9999)}",
                        "area_sqft": round(area, 2),
                        "land_type": random.choice(
                            ["commercial", "industrial", "residential", "mixed_use"]
                        ),
                        "price_per_sqft": base_data["avg_land_price_per_sqft"]
                        * random.uniform(0.8, 1.3),
                        "total_price": round(
                            area
                            * base_data["avg_land_price_per_sqft"]
                            * random.uniform(0.8, 1.3),
                            2,
                        ),
                        "zone": random.choice(
                            ["central", "north", "south", "east", "west"]
                        ),
                        "road_frontage_m": random.randint(10, 100),
                        "encumbrance_free": random.choice([True, True, True, False]),
                        "latitude": 16.5 + random.uniform(-0.5, 0.5),
                        "longitude": 80.6 + random.uniform(-0.5, 0.5),
                    }
                )
        return {
            "location": location,
            "total_parcels_found": len(parcels),
            "parcels": parcels,
            "data_source": "Land Registry 2024 (Stub)",
        }

    def get_zoning_info(self, location: str) -> dict[str, Any]:
        return {
            "location": location,
            "zones": {
                "central_business_district": {
                    "max_fsi": 4.0,
                    "max_height_m": 50,
                    "setbacks_m": {"front": 6, "side": 3, "rear": 3},
                    "permitted_uses": ["commercial", "mixed_use", "institutional"],
                },
                "commercial_zone": {
                    "max_fsi": 3.0,
                    "max_height_m": 35,
                    "setbacks_m": {"front": 6, "side": 3, "rear": 3},
                    "permitted_uses": ["commercial", "mixed_use"],
                },
                "industrial_zone": {
                    "max_fsi": 2.0,
                    "max_height_m": 25,
                    "setbacks_m": {"front": 9, "side": 6, "rear": 6},
                    "permitted_uses": ["industrial", "warehouse", "logistics"],
                },
                "residential_zone": {
                    "max_fsi": 2.5,
                    "max_height_m": 20,
                    "setbacks_m": {"front": 6, "side": 3, "rear": 3},
                    "permitted_uses": ["residential", "mixed_use_low"],
                },
            },
            "infrastructure_requirements": {
                "minimum_road_width_m": 12,
                "parking_spaces_per_100sqm": 1.5,
                "rainwater_harvesting": True,
                "sewage_treatment": "required_for_large",
            },
            "data_source": "Zoning Regulations 2024 (Stub)",
        }

    def get_development_potential(
        self, location: str, area_sqft: float
    ) -> dict[str, Any]:
        base_data = self.get_land_use_data(location)
        avg_price = base_data["avg_land_price_per_sqft"]
        fsi = 2.5
        return {
            "location": location,
            "input_area_sqft": area_sqft,
            "land_cost": round(area_sqft * avg_price, 2),
            "permissible_fsi": fsi,
            "built_up_area_sqft": round(area_sqft * fsi, 2),
            "estimated_construction_cost": round(area_sqft * fsi * 2200, 2),
            "total_project_cost": round(area_sqft * avg_price + area_sqft * fsi * 2200, 2),
            "infrastructure_development_cost": round(area_sqft * 150, 2),
            "approval_timeline_months": random.randint(6, 18),
            "data_source": "Development Authority 2024 (Stub)",
        }

    def get_road_network_data(self, location: str) -> dict[str, Any]:
        base_data = self.get_land_use_data(location)
        total_length = base_data["total_area_sqkm"] * random.uniform(2.5, 4.0)
        return {
            "location": location,
            "total_road_length_km": round(total_length, 2),
            "road_hierarchy": {
                "national_highways_km": round(total_length * 0.05, 2),
                "state_highways_km": round(total_length * 0.08, 2),
                "major_district_roads_km": round(total_length * 0.12, 2),
                "other_district_roads_km": round(total_length * 0.15, 2),
                "urban_roads_km": round(total_length * 0.35, 2),
                "rural_roads_km": round(total_length * 0.25, 2),
            },
            "road_condition": {
                "good_percent": random.randint(45, 60),
                "fair_percent": random.randint(25, 35),
                "poor_percent": random.randint(10, 25),
            },
            "connectivity_score": random.uniform(6.5, 8.5),
            "average_road_width_m": random.uniform(8, 14),
            "data_source": "Road Statistics 2024 (Stub)",
        }


land_use_api_stub = LandUseAPIStub()
