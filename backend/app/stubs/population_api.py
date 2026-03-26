import random
from datetime import datetime, timedelta
from typing import Any


class PopulationAPIStub:
    """
    Stub service for population and demographic data API.
    Simulates government census API responses.
    """

    def __init__(self):
        self.locations = {
            "vijayawada": {
                "current_population": 1184000,
                "growth_rate": 2.1,
                "density_per_sqkm": 11500,
                "households": 296000,
                "avg_household_size": 4.0,
            },
            "guntur": {
                "current_population": 743654,
                "growth_rate": 1.9,
                "density_per_sqkm": 8900,
                "households": 185913,
                "avg_household_size": 4.0,
            },
            "visakhapatnam": {
                "current_population": 2035622,
                "growth_rate": 2.4,
                "density_per_sqkm": 12400,
                "households": 508905,
                "avg_household_size": 4.0,
            },
            "tirupati": {
                "current_population": 374260,
                "growth_rate": 2.8,
                "density_per_sqkm": 6800,
                "households": 93565,
                "avg_household_size": 4.0,
            },
            "kakinada": {
                "current_population": 376861,
                "growth_rate": 1.7,
                "density_per_sqkm": 7200,
                "households": 94215,
                "avg_household_size": 4.0,
            },
            "nellore": {
                "current_population": 600869,
                "growth_rate": 2.0,
                "density_per_sqkm": 8100,
                "households": 150217,
                "avg_household_size": 4.0,
            },
            "kurnool": {
                "current_population": 460184,
                "growth_rate": 1.6,
                "density_per_sqkm": 5400,
                "households": 115046,
                "avg_household_size": 4.0,
            },
            "rajahmundry": {
                "current_population": 341831,
                "growth_rate": 1.8,
                "density_per_sqkm": 6100,
                "households": 85457,
                "avg_household_size": 4.0,
            },
            "anantapur": {
                "current_population": 388723,
                "growth_rate": 1.5,
                "density_per_sqkm": 4800,
                "households": 97180,
                "avg_household_size": 4.0,
            },
            "kadapa": {
                "current_population": 344893,
                "growth_rate": 1.7,
                "density_per_sqkm": 5200,
                "households": 86223,
                "avg_household_size": 4.0,
            },
        }

    def get_population_data(self, location: str) -> dict[str, Any]:
        location_key = location.lower().replace(" ", "_")
        if location_key not in self.locations:
            location_key = "vijayawada"
        data = self.locations[location_key].copy()
        data["location"] = location
        data["data_source"] = "Census 2024 (Stub)"
        data["last_updated"] = datetime.utcnow().isoformat()
        return data

    def get_population_projection(
        self, location: str, years_ahead: int = 10
    ) -> dict[str, Any]:
        base_data = self.get_population_data(location)
        current_pop = base_data["current_population"]
        growth_rate = base_data["growth_rate"]
        projected_pop = int(current_pop * ((1 + growth_rate / 100) ** years_ahead))
        year_by_year = []
        for i in range(years_ahead + 1):
            year_pop = int(current_pop * ((1 + growth_rate / 100) ** i))
            year_by_year.append(
                {
                    "year": datetime.now().year + i,
                    "population": year_pop,
                    "growth_from_base": round(
                        ((year_pop - current_pop) / current_pop) * 100, 2
                    ),
                }
            )
        return {
            "location": location,
            "base_year": datetime.now().year,
            "projection_years": years_ahead,
            "base_population": current_pop,
            "projected_population": projected_pop,
            "growth_rate_percent": growth_rate,
            "total_growth_percent": round(
                ((projected_pop - current_pop) / current_pop) * 100, 2
            ),
            "year_by_year_projection": year_by_year,
            "data_source": "Census Projection Model (Stub)",
        }

    def get_age_distribution(self, location: str) -> dict[str, Any]:
        base_data = self.get_population_data(location)
        total_pop = base_data["current_population"]
        return {
            "location": location,
            "total_population": total_pop,
            "age_groups": {
                "0-14": {"count": int(total_pop * 0.24), "percentage": 24.0},
                "15-29": {"count": int(total_pop * 0.26), "percentage": 26.0},
                "30-44": {"count": int(total_pop * 0.22), "percentage": 22.0},
                "45-59": {"count": int(total_pop * 0.16), "percentage": 16.0},
                "60+": {"count": int(total_pop * 0.12), "percentage": 12.0},
            },
            "working_age_population": int(total_pop * 0.64),
            "dependency_ratio": 0.56,
            "data_source": "Demographic Survey 2024 (Stub)",
        }

    def get_employment_data(self, location: str) -> dict[str, Any]:
        base_data = self.get_population_data(location)
        working_pop = int(base_data["current_population"] * 0.64)
        return {
            "location": location,
            "working_age_population": working_pop,
            "employed": int(working_pop * 0.72),
            "unemployed": int(working_pop * 0.05),
            "not_in_labor_force": int(working_pop * 0.23),
            "employment_rate": 72.0,
            "unemployment_rate": 5.0,
            "sectors": {
                "agriculture": 18,
                "manufacturing": 22,
                "services": 42,
                "construction": 10,
                "other": 8,
            },
            "data_source": "Employment Statistics 2024 (Stub)",
        }

    def get_migration_data(self, location: str) -> dict[str, Any]:
        base_data = self.get_population_data(location)
        return {
            "location": location,
            "net_migration_rate": random.uniform(1.5, 4.5),
            "in_migrants_per_year": random.randint(8000, 25000),
            "out_migrants_per_year": random.randint(5000, 15000),
            "migration_reasons": {
                "employment": 45,
                "education": 20,
                "family": 25,
                "other": 10,
            },
            "origin_states": {
                "telangana": 35,
                "karnataka": 20,
                "tamil_nadu": 15,
                "maharashtra": 10,
                "other": 20,
            },
            "data_source": "Migration Survey 2024 (Stub)",
        }


population_api_stub = PopulationAPIStub()
