import random
from datetime import datetime
from typing import Any


class EconomicAPIStub:
    """
    Stub service for economic indicators API.
    Simulates government economic data API responses.
    """

    def __init__(self):
        self.regional_data = {
            "vijayawada": {
                "gdp_per_capita": 185000,
                "gdp_growth_rate": 8.2,
                "inflation_rate": 5.4,
                "fdi_investment_cr": 2500,
                "industrial_output_growth": 7.5,
            },
            "guntur": {
                "gdp_per_capita": 142000,
                "gdp_growth_rate": 7.1,
                "inflation_rate": 5.2,
                "fdi_investment_cr": 1200,
                "industrial_output_growth": 6.8,
            },
            "visakhapatnam": {
                "gdp_per_capita": 215000,
                "gdp_growth_rate": 9.5,
                "inflation_rate": 5.6,
                "fdi_investment_cr": 4500,
                "industrial_output_growth": 8.9,
            },
            "tirupati": {
                "gdp_per_capita": 128000,
                "gdp_growth_rate": 8.8,
                "inflation_rate": 5.1,
                "fdi_investment_cr": 800,
                "industrial_output_growth": 7.2,
            },
            "kakinada": {
                "gdp_per_capita": 135000,
                "gdp_growth_rate": 7.8,
                "inflation_rate": 5.3,
                "fdi_investment_cr": 1800,
                "industrial_output_growth": 8.1,
            },
            "nellore": {
                "gdp_per_capita": 138000,
                "gdp_growth_rate": 7.4,
                "inflation_rate": 5.2,
                "fdi_investment_cr": 950,
                "industrial_output_growth": 6.5,
            },
            "kurnool": {
                "gdp_per_capita": 98000,
                "gdp_growth_rate": 6.2,
                "inflation_rate": 5.0,
                "fdi_investment_cr": 400,
                "industrial_output_growth": 5.8,
            },
            "rajahmundry": {
                "gdp_per_capita": 125000,
                "gdp_growth_rate": 6.9,
                "inflation_rate": 5.1,
                "fdi_investment_cr": 650,
                "industrial_output_growth": 6.4,
            },
            "anantapur": {
                "gdp_per_capita": 105000,
                "gdp_growth_rate": 7.6,
                "inflation_rate": 5.0,
                "fdi_investment_cr": 1100,
                "industrial_output_growth": 9.2,
            },
            "kadapa": {
                "gdp_per_capita": 92000,
                "gdp_growth_rate": 6.5,
                "inflation_rate": 4.9,
                "fdi_investment_cr": 350,
                "industrial_output_growth": 5.5,
            },
        }

    def get_economic_indicators(self, location: str) -> dict[str, Any]:
        location_key = location.lower().replace(" ", "_")
        if location_key not in self.regional_data:
            location_key = "vijayawada"
        data = self.regional_data[location_key].copy()
        data["location"] = location
        data["data_source"] = "Economic Survey 2024 (Stub)"
        data["last_updated"] = datetime.utcnow().isoformat()
        return data

    def get_gdp_projection(
        self, location: str, years_ahead: int = 10
    ) -> dict[str, Any]:
        base_data = self.get_economic_indicators(location)
        current_gdp = base_data["gdp_per_capita"]
        growth_rate = base_data["gdp_growth_rate"]
        projected_gdp = int(current_gdp * ((1 + growth_rate / 100) ** years_ahead))
        year_by_year = []
        for i in range(years_ahead + 1):
            year_gdp = int(current_gdp * ((1 + growth_rate / 100) ** i))
            year_by_year.append(
                {
                    "year": datetime.now().year + i,
                    "gdp_per_capita": year_gdp,
                    "growth_from_base": round(
                        ((year_gdp - current_gdp) / current_gdp) * 100, 2
                    ),
                }
            )
        return {
            "location": location,
            "base_year": datetime.now().year,
            "projection_years": years_ahead,
            "base_gdp_per_capita": current_gdp,
            "projected_gdp_per_capita": projected_gdp,
            "annual_growth_rate_percent": growth_rate,
            "total_growth_percent": round(
                ((projected_gdp - current_gdp) / current_gdp) * 100, 2
            ),
            "year_by_year_projection": year_by_year,
            "data_source": "Economic Projection Model (Stub)",
        }

    def get_investment_trends(self, location: str) -> dict[str, Any]:
        base_data = self.get_economic_indicators(location)
        return {
            "location": location,
            "total_fdi_investment_cr": base_data["fdi_investment_cr"],
            "investment_growth_yoy": random.uniform(8, 15),
            "sectors": {
                "manufacturing": {
                    "investment_cr": int(base_data["fdi_investment_cr"] * 0.35),
                    "growth": random.uniform(5, 12),
                },
                "it_services": {
                    "investment_cr": int(base_data["fdi_investment_cr"] * 0.25),
                    "growth": random.uniform(10, 20),
                },
                "infrastructure": {
                    "investment_cr": int(base_data["fdi_investment_cr"] * 0.20),
                    "growth": random.uniform(8, 15),
                },
                "pharma": {
                    "investment_cr": int(base_data["fdi_investment_cr"] * 0.12),
                    "growth": random.uniform(6, 14),
                },
                "other": {
                    "investment_cr": int(base_data["fdi_investment_cr"] * 0.08),
                    "growth": random.uniform(4, 10),
                },
            },
            "upcoming_projects": random.randint(15, 50),
            "data_source": "Investment Survey 2024 (Stub)",
        }

    def get_vehicle_growth_data(self, location: str) -> dict[str, Any]:
        base_data = self.get_economic_indicators(location)
        base_vehicles = random.randint(150000, 500000)
        growth_rate = random.uniform(6, 12)
        return {
            "location": location,
            "total_vehicles": base_vehicles,
            "annual_growth_rate": growth_rate,
            "vehicle_types": {
                "two_wheeler": {
                    "count": int(base_vehicles * 0.65),
                    "growth_rate": growth_rate + 1.5,
                    "percentage": 65,
                },
                "car_jeep": {
                    "count": int(base_vehicles * 0.18),
                    "growth_rate": growth_rate + 2.5,
                    "percentage": 18,
                },
                "three_wheeler": {
                    "count": int(base_vehicles * 0.08),
                    "growth_rate": growth_rate - 1.0,
                    "percentage": 8,
                },
                "bus": {
                    "count": int(base_vehicles * 0.02),
                    "growth_rate": growth_rate - 2.0,
                    "percentage": 2,
                },
                "goods_vehicle": {
                    "count": int(base_vehicles * 0.05),
                    "growth_rate": growth_rate + 0.5,
                    "percentage": 5,
                },
                "other": {
                    "count": int(base_vehicles * 0.02),
                    "growth_rate": growth_rate - 0.5,
                    "percentage": 2,
                },
            },
            "projection_5_years": int(base_vehicles * ((1 + growth_rate / 100) ** 5)),
            "projection_10_years": int(base_vehicles * ((1 + growth_rate / 100) ** 10)),
            "data_source": "Transport Statistics 2024 (Stub)",
        }

    def get_construction_cost_index(self, location: str) -> dict[str, Any]:
        base_index = 150 + random.randint(-20, 20)
        return {
            "location": location,
            "current_index": base_index,
            "base_year_index": 100,
            "base_year": 2015,
            "yoy_change_percent": random.uniform(4, 8),
            "material_costs": {
                "steel_per_ton": 75000 + random.randint(-5000, 5000),
                "cement_per_bag": 380 + random.randint(-20, 20),
                "sand_per_cft": 55 + random.randint(-10, 10),
                "aggregate_per_cft": 45 + random.randint(-8, 8),
                "labor_per_day": 850 + random.randint(-50, 50),
            },
            "trend_last_5_years": [
                {"year": datetime.now().year - 5 + i, "index": base_index - 25 + i * 5}
                for i in range(5)
            ],
            "data_source": "Construction Cost Index 2024 (Stub)",
        }


economic_api_stub = EconomicAPIStub()
