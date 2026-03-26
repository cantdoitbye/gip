# Government API Integration Guide

This document provides comprehensive guidance for integrating real government APIs to replace the stub services in the Ooumph GIP (Government Infrastructure Planning) application.

## Table of Contents

1. [Overview](#overview)
2. [Current Stub Architecture](#current-stub-architecture)
3. [API Mappings and Real Equivalents](#api-mappings-and-real-equivalents)
4. [Approval Authorities and Requirements](#approval-authorities-and-requirements)
5. [API Integration Guide](#api-integration-guide)
6. [Code Examples](#code-examples)
7. [Migration Strategy](#migration-strategy)

---

## Overview

The application currently uses five stub services to simulate government API responses. These stubs provide realistic mock data for development and demonstration purposes. This guide documents how to replace each stub with real government API integrations.

### Current Stub Files Location
```
backend/app/stubs/
├── traffic_api.py      # Traffic flow and incident data
├── gis_api.py          # Geographic and environmental data
├── population_api.py   # Census and demographic data
├── land_use_api.py     # Land records and zoning data
└── economic_api.py     # Economic indicators and statistics
```

---

## Current Stub Architecture

### Stub Methods Summary

| Stub | Methods | Data Types |
|------|---------|------------|
| `traffic_api_stub` | `get_all_traffic_data()`, `get_incidents()`, `get_heatmap_data()` | Traffic flow, incidents, congestion |
| `gis_api_stub` | `get_terrain_data()`, `get_environmental_data()`, `get_risk_assessment()`, `get_infrastructure_data()`, `get_accessibility_data()`, `get_utility_costs()` | GIS, terrain, environmental, infrastructure |
| `population_api_stub` | `get_population_data()`, `get_population_projection()`, `get_age_distribution()`, `get_employment_data()`, `get_migration_data()` | Census, demographics, employment |
| `land_use_api_stub` | `get_land_use_data()`, `get_available_parcels()`, `get_zoning_info()`, `get_development_potential()`, `get_road_network_data()` | Land records, zoning, development |
| `economic_api_stub` | `get_economic_indicators()`, `get_gdp_projection()`, `get_investment_trends()`, `get_vehicle_growth_data()`, `get_construction_cost_index()` | GDP, investment, vehicle stats |

---

## API Mappings and Real Equivalents

### 1. Traffic API Stub → Real APIs

#### Current Stub: `traffic_api_stub`
**File:** [backend/app/stubs/traffic_api.py](../backend/app/stubs/traffic_api.py)

#### Real API Equivalents

##### A. Hyderabad Traffic Police API
- **Purpose:** Real-time traffic data for Hyderabad/Telangana region
- **Base URL:** Contact Hyderabad Traffic Police IT Cell
- **Coverage:** Hyderabad Metropolitan Area
- **Data Available:**
  - Real-time traffic flow
  - Congestion levels
  - Traffic incidents
  - Signal timing data

##### B. NIC Traffic Portal (National Informatics Centre)
- **Purpose:** National traffic data aggregation
- **Base URL:** `https://parivahan.gov.in/` (Contact NIC for API access)
- **Coverage:** Pan-India
- **Data Available:**
  - Vehicle registration data
  - Traffic violations
  - Road safety statistics
  - National highway traffic data

##### C. Indian Roads Congress (IRC) Data Portal
- **Purpose:** Road traffic studies and surveys
- **Website:** `https://irc.nic.in/`
- **Data Available:**
  - Traffic volume studies
  - Road capacity data
  - Traffic forecasting models

#### Stub Method → Real API Mapping

| Stub Method | Real API Endpoint | Data Format |
|-------------|-------------------|-------------|
| `get_all_traffic_data()` | `/api/v1/traffic/flow` | JSON |
| `get_incidents()` | `/api/v1/traffic/incidents` | JSON |
| `get_heatmap_data()` | `/api/v1/traffic/heatmap` | GeoJSON |

---

### 2. GIS API Stub → Real APIs

#### Current Stub: `gis_api_stub`
**File:** [backend/app/stubs/gis_api.py](../backend/app/stubs/gis_api.py)

#### Real API Equivalents

##### A. Survey of India
- **Purpose:** Official mapping and geospatial data
- **Website:** `https://surveyofindia.gov.in/`
- **Contact:** Open Series Map (OSM) Division
- **Data Available:**
  - Topographical maps
  - Digital Elevation Models (DEM)
  - Administrative boundaries
  - Land survey records
- **Approval Authority:** Surveyor General of India

##### B. ISRO Bhuvan API
- **Purpose:** Indian satellite imagery and geospatial services
- **Base URL:** `https://bhuvan.nrsc.gov.in/`
- **API Portal:** `https://bhuvan.nrsc.gov.in/bhuvan_api/`
- **Coverage:** Pan-India
- **Data Available:**
  - Satellite imagery
  - Terrain data (SRTM/ASTER)
  - Land use/land cover
  - Watershed boundaries
  - Disaster management data
- **Authentication:** API Key + IP Whitelisting

##### C. Geological Survey of India (GSI)
- **Purpose:** Geological and geohazard data
- **Website:** `https://www.gsi.gov.in/`
- **Data Available:**
  - Seismic zone maps
  - Geological surveys
  - Landslide hazard zones
  - Groundwater surveys

##### D. National Remote Sensing Centre (NRSC)
- **Purpose:** Remote sensing data
- **Website:** `https://www.nrsc.gov.in/`
- **Data Available:**
  - Satellite imagery (Resourcesat, Cartosat)
  - Environmental monitoring
  - Flood inundation maps

#### Stub Method → Real API Mapping

| Stub Method | Real API Endpoint | Data Format |
|-------------|-------------------|-------------|
| `get_terrain_data()` | Bhuvan `/dem/terrain` | GeoJSON |
| `get_environmental_data()` | Bhuvan `/environment/assessment` | JSON |
| `get_risk_assessment()` | GSI `/geohazard/assess` | JSON |
| `get_infrastructure_data()` | Survey of India `/infrastructure` | GeoJSON |
| `get_accessibility_data()` | Bhuvan `/accessibility/analyze` | JSON |
| `get_utility_costs()` | State Electricity Board APIs | JSON |

---

### 3. Population API Stub → Real APIs

#### Current Stub: `population_api_stub`
**File:** [backend/app/stubs/population_api.py](../backend/app/stubs/population_api.py)

#### Real API Equivalents

##### A. Census of India API
- **Purpose:** Official population and demographic data
- **Website:** `https://censusindia.gov.in/`
- **Open Data Portal:** `https://data.gov.in/`
- **Coverage:** Pan-India (latest: 2011 Census, with projections)
- **Data Available:**
  - Population by district/mandal/village
  - Age distribution
  - Literacy rates
  - Workforce participation
  - Migration data
- **Approval Authority:** Registrar General & Census Commissioner of India
- **Authentication:** Data.gov.in API Key

##### B. National Population Register (NPR)
- **Purpose:** Citizen registration database
- **Authority:** Office of the Registrar General
- **Access:** Restricted (Government use only)

##### C. State Statistical Handbooks
- **Purpose:** State-level demographic data
- **Example:** Andhra Pradesh Economic and Statistical Organization
- **Website:** `https://des.ap.gov.in/`

#### Stub Method → Real API Mapping

| Stub Method | Real API Endpoint | Data Format |
|-------------|-------------------|-------------|
| `get_population_data()` | Census `/population/{district}` | JSON |
| `get_population_projection()` | Census `/projection/{location}/{years}` | JSON |
| `get_age_distribution()` | Census `/demographics/age/{district}` | JSON |
| `get_employment_data()` | Census `/employment/{district}` | JSON |
| `get_migration_data()` | Census `/migration/{district}` | JSON |

---

### 4. Land Use API Stub → Real APIs

#### Current Stub: `land_use_api_stub`
**File:** [backend/app/stubs/land_use_api.py](../backend/app/stubs/land_use_api.py)

#### Real API Equivalents

##### A. Dharani Portal (Telangana)
- **Purpose:** Integrated land records management
- **Website:** `https://dharani.telangana.gov.in/`
- **Coverage:** Telangana State
- **Data Available:**
  - Land ownership records (pahani)
  - Land parcels
  - Mutation history
  - Encumbrance certificates
- **Approval Authority:** Commissioner of Land Revenue, Telangana
- **Access:** Government API (requires official approval)

##### B. Bhoomi Portal (Karnataka)
- **Purpose:** Karnataka land records
- **Website:** `https://bhoomi.karnataka.gov.in/`
- **Coverage:** Karnataka State

##### C. Mee Bhoomi (Andhra Pradesh)
- **Purpose:** AP land records portal
- **Website:** `https://meebhoomi.ap.gov.in/`
- **Coverage:** Andhra Pradesh State
- **Data Available:**
  - Adangal/Pahani
  - 1B extracts
  - Village maps
  - FMB sketches

##### D. National Land Record Modernisation Programme (NLRMP)
- **Purpose:** Unified land records across India
- **Website:** `https://dolr.gov.in/`
- **Coverage:** Pan-India (progressive)

##### E. Master Plan/Zoning Data
- **Source:** State Town and Country Planning Departments
- **Example:** Andhra Pradesh Capital Region Development Authority (CRDA)
- **Data Available:**
  - Zoning regulations
  - FSI/FAR limits
  - Building bylaws
  - Development potential

#### Stub Method → Real API Mapping

| Stub Method | Real API Endpoint | Data Format |
|-------------|-------------------|-------------|
| `get_land_use_data()` | Mee Bhoomi `/land/use/{survey}` | JSON |
| `get_available_parcels()` | Dharani `/parcels/search` | JSON |
| `get_zoning_info()` | CRDA `/zoning/{zone}` | JSON |
| `get_development_potential()` | Town Planning `/development/{area}` | JSON |
| `get_road_network_data()` | NHAI/R&B `/roads/network` | GeoJSON |

---

### 5. Economic API Stub → Real APIs

#### Current Stub: `economic_api_stub`
**File:** [backend/app/stubs/economic_api.py](../backend/app/stubs/economic_api.py)

#### Real API Equivalents

##### A. Ministry of Statistics and Programme Implementation (MoSPI)
- **Purpose:** Official economic statistics
- **Website:** `https://mospi.gov.in/`
- **Data Portal:** `https://mospi.nic.in/`
- **Data Available:**
  - GDP data (national and state)
  - Consumer Price Index (CPI)
  - Wholesale Price Index (WPI)
  - Index of Industrial Production (IIP)
  - National Accounts Statistics

##### B. Reserve Bank of India (RBI) API
- **Purpose:** Financial and monetary data
- **Website:** `https://www.rbi.org.in/`
- **Data Portal:** `https://dbie.rbi.org.in/`
- **Data Available:**
  - Interest rates
  - Inflation data
  - Foreign investment statistics
  - Banking statistics
  - Exchange rates

##### C. NITI Aayog Data Portal
- **Purpose:** Development indicators
- **Website:** `https://www.niti.gov.in/`
- **Data Available:**
  - SDG indicators
  - State development indices
  - Economic forecasts

##### D. State Economic Surveys
- **Purpose:** State-level economic data
- **Example:** Andhra Pradesh Economic Survey (published annually)
- **Source:** State Planning Department

##### E. Transport Statistics
- **Source:** Ministry of Road Transport and Highways (MoRTH)
- **Website:** `https://morth.nic.in/`
- **Data Available:**
  - Vehicle registration statistics
  - Road length data
  - Accident statistics
  - Freight and passenger movement

#### Stub Method → Real API Mapping

| Stub Method | Real API Endpoint | Data Format |
|-------------|-------------------|-------------|
| `get_economic_indicators()` | MoSPI `/economy/indicators/{state}` | JSON |
| `get_gdp_projection()` | RBI `/projections/gdp` | JSON |
| `get_investment_trends()` | RBI `/fdi/trends/{state}` | JSON |
| `get_vehicle_growth_data()` | MoRTH `/transport/vehicles/{state}` | JSON |
| `get_construction_cost_index()` | CPWD `/cost-index/{city}` | JSON |

---

## Approval Authorities and Requirements

### Summary Table

| API Category | Primary Authority | Approval Type | Typical Timeline |
|--------------|-------------------|---------------|------------------|
| Traffic Data | Hyderabad Traffic Police / NIC | MoU + Security Clearance | 2-4 weeks |
| GIS Data | Survey of India / ISRO NRSC | License Agreement | 4-8 weeks |
| Population Data | Registrar General of India | Data Access Request | 2-4 weeks |
| Land Records | State Revenue Department | Government Order | 4-12 weeks |
| Economic Data | MoSPI / RBI | Registration + Agreement | 2-4 weeks |

### Detailed Requirements

#### 1. Traffic API Access

**Hyderabad Traffic Police**
- **Authority:** Additional Commissioner of Police (Traffic)
- **Requirements:**
  - Official request letter on organization letterhead
  - Project proposal document
  - Data usage agreement
  - IP address whitelisting
  - Security audit clearance
  - Annual renewal required

**NIC Parivahan**
- **Authority:** National Informatics Centre
- **Requirements:**
  - Registration on data.gov.in
  - API key application
  - Purpose statement
  - Data protection undertaking

#### 2. GIS API Access

**ISRO Bhuvan**
- **Authority:** National Remote Sensing Centre (NRSC)
- **Requirements:**
  - User registration at Bhuvan portal
  - API key request form
  - Project documentation
  - IP whitelisting for production
  - Usage limits acknowledgment
- **Contact:** `bhuvan@nrsc.gov.in`

**Survey of India**
- **Authority:** Surveyor General of India
- **Requirements:**
  - Official request through proper channel
  - Security clearance (for restricted data)
  - License fee payment
  - Usage agreement
- **Contact:** Open Series Map Division

#### 3. Population/Census API Access

**Census of India**
- **Authority:** Registrar General & Census Commissioner
- **Requirements:**
  - Registration on data.gov.in
  - API key for open data
  - For restricted data: Official request + clearance
- **Open Data:** Most census tables are available through data.gov.in API

#### 4. Land Records API Access

**Dharani (Telangana) / Mee Bhoomi (AP)**
- **Authority:** State Revenue Department
- **Requirements:**
  - Government Order (GO) for API access
  - Integration agreement
  - Data security compliance
  - Audit trail maintenance
  - Annual compliance report
- **Note:** Typically restricted to government departments and authorized agencies

#### 5. Economic Data API Access

**MoSPI**
- **Authority:** Chief Statistician of India
- **Requirements:**
  - Registration on mospi.gov.in
  - Data usage agreement
  - Attribution in publications

**RBI DBIE (Database on Indian Economy)**
- **Authority:** Reserve Bank of India
- **Requirements:**
  - User registration
  - API key for automated access
  - Rate limiting compliance
- **Contact:** `dbie@rbi.org.in`

---

## API Integration Guide

### Authentication Requirements

#### 1. API Key Based Authentication

Most government APIs use API key authentication:

```python
# Environment variables to configure
GOV_API_KEY=your_api_key_here
BHUAVAN_API_KEY=bhuvan_api_key
CENSUS_API_KEY=census_api_key
MOSPI_API_KEY=mospi_api_key
```

#### 2. OAuth 2.0 (Some Modern APIs)

```python
# OAuth configuration
AUTH_URL=https://api.example.gov.in/oauth/token
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
SCOPE=read:data
```

#### 3. IP Whitelisting

Many government APIs require IP whitelisting:
- Submit static IP addresses to the API provider
- Ensure server IPs are registered
- Update IPs when infrastructure changes

#### 4. Digital Signature Certificate (DSC)

Some APIs may require DSC for request signing:
- Obtain Class 3 DSC from authorized CA
- Register public key with API provider
- Sign API requests programmatically

### Data Format Expectations

#### Standard Response Format

```json
{
  "status": "success",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    // Response data
  },
  "metadata": {
    "source": "api_name",
    "version": "1.0",
    "cache_hit": false
  }
}
```

#### Error Response Format

```json
{
  "status": "error",
  "error_code": "INVALID_REQUEST",
  "message": "Invalid location parameter",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Coordinate Systems

| API | Coordinate System | Notes |
|-----|-------------------|-------|
| Bhuvan | EPSG:4326 (WGS84) | Default |
| Survey of India | EPSG:7755 (WGS84/India) | Transform required |
| State APIs | Varies | Check documentation |

### Rate Limits

| API Provider | Rate Limit | Burst Limit | Notes |
|--------------|------------|-------------|-------|
| Bhuvan | 1000 req/day | 100 req/min | Varies by plan |
| data.gov.in | 10000 req/day | 100 req/min | Open data |
| RBI DBIE | 5000 req/day | 50 req/min | Registered users |
| MoSPI | 5000 req/day | 50 req/min | Standard access |

### Rate Limiting Implementation

```python
import asyncio
from functools import wraps
import time

class RateLimiter:
    def __init__(self, calls_per_minute: int):
        self.calls_per_minute = calls_per_minute
        self.min_interval = 60.0 / calls_per_minute
        self.last_call = 0.0
        self.lock = asyncio.Lock()
    
    async def acquire(self):
        async with self.lock:
            now = time.time()
            time_since_last = now - self.last_call
            if time_since_last < self.min_interval:
                await asyncio.sleep(self.min_interval - time_since_last)
            self.last_call = time.time()

rate_limiter = RateLimiter(calls_per_minute=50)
```

---

## Code Examples

### Creating a Real API Client

#### Example 1: Traffic API Client

```python
# backend/app/clients/traffic_api_client.py

import httpx
from typing import Any
from datetime import datetime
from app.config import settings


class TrafficAPIClient:
    """
    Real implementation for Hyderabad Traffic Police API.
    Replace traffic_api_stub with this client in production.
    """
    
    def __init__(self):
        self.base_url = settings.TRAFFIC_API_URL
        self.api_key = settings.TRAFFIC_API_KEY
        self.timeout = httpx.Timeout(30.0)
    
    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Request-ID": datetime.utcnow().isoformat(),
        }
    
    async def get_all_traffic_data(self) -> list[dict[str, Any]]:
        """
        Fetch real-time traffic data from Hyderabad Traffic Police API.
        
        Endpoint: GET /api/v1/traffic/flow
        Response format matches stub format for seamless integration.
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/api/v1/traffic/flow",
                headers=self._get_headers(),
                params={"city": "hyderabad"}
            )
            response.raise_for_status()
            
            data = response.json()
            return self._transform_traffic_response(data)
    
    def _transform_traffic_response(self, data: dict) -> list[dict[str, Any]]:
        """Transform API response to match stub format."""
        return [
            {
                "location_name": item["location"],
                "latitude": item["coordinates"]["lat"],
                "longitude": item["coordinates"]["lng"],
                "flow_rate": item["flow"]["vehicles_per_hour"],
                "vehicle_count": item["flow"]["total_count"],
                "avg_speed": item["flow"]["average_speed_kmph"],
                "congestion_level": item["congestion"]["level"],
                "timestamp": datetime.fromisoformat(item["timestamp"]),
            }
            for item in data["traffic_points"]
        ]
    
    async def get_incidents(self, limit: int = 10) -> list[dict[str, Any]]:
        """
        Fetch traffic incidents.
        
        Endpoint: GET /api/v1/traffic/incidents
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/api/v1/traffic/incidents",
                headers=self._get_headers(),
                params={"limit": limit, "status": "active"}
            )
            response.raise_for_status()
            
            data = response.json()
            return self._transform_incidents_response(data)
    
    def _transform_incidents_response(self, data: dict) -> list[dict[str, Any]]:
        """Transform incidents API response to match stub format."""
        return [
            {
                "location_name": item["location"],
                "latitude": item["coordinates"]["lat"],
                "longitude": item["coordinates"]["lng"],
                "incident_type": item["type"],
                "severity": item["severity"],
                "description": item["description"],
                "timestamp": datetime.fromisoformat(item["reported_at"]),
            }
            for item in data["incidents"]
        ]
    
    async def get_heatmap_data(self) -> list[dict[str, Any]]:
        """
        Fetch heatmap data for visualization.
        
        Endpoint: GET /api/v1/traffic/heatmap
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/api/v1/traffic/heatmap",
                headers=self._get_headers(),
                params={"format": "json"}
            )
            response.raise_for_status()
            
            data = response.json()
            return self._transform_heatmap_response(data)
    
    def _transform_heatmap_response(self, data: dict) -> list[dict[str, Any]]:
        """Transform heatmap API response to match stub format."""
        return [
            {
                "location_name": item["location"],
                "lat": item["coordinates"]["lat"],
                "lng": item["coordinates"]["lng"],
                "intensity": item["congestion_index"],
            }
            for item in data["heatmap_points"]
        ]


traffic_api_client = TrafficAPIClient()
```

#### Example 2: GIS API Client (Bhuvan)

```python
# backend/app/clients/gis_api_client.py

import httpx
from typing import Any
from app.config import settings
from app.utils.cache import cache


class GISAPIClient:
    """
    Real implementation for ISRO Bhuvan API.
    Replace gis_api_stub with this client in production.
    """
    
    def __init__(self):
        self.base_url = settings.BHUVAN_API_URL
        self.api_key = settings.BHUVAN_API_KEY
        self.timeout = httpx.Timeout(60.0)
    
    def _get_headers(self) -> dict[str, str]:
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        }
    
    @cache(ttl=3600)
    async def get_terrain_data(
        self, latitude: float, longitude: float
    ) -> dict[str, Any]:
        """
        Fetch terrain data from Bhuvan DEM API.
        
        Endpoint: GET /dem/terrain
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/dem/terrain",
                headers=self._get_headers(),
                params={
                    "lat": latitude,
                    "lon": longitude,
                    "buffer": 1000
                }
            )
            response.raise_for_status()
            
            data = response.json()
            return self._transform_terrain_response(data, latitude, longitude)
    
    def _transform_terrain_response(
        self, data: dict, lat: float, lon: float
    ) -> dict[str, Any]:
        """Transform Bhuvan terrain response to match stub format."""
        return {
            "latitude": lat,
            "longitude": lon,
            "elevation_m": data["elevation"]["value"],
            "soil_type": data["soil"]["type"],
            "flood_risk": data["hazards"]["flood_risk"],
            "seismic_zone": data["hazards"]["seismic_zone"],
            "ground_water_depth_m": data["groundwater"]["depth"],
            "slope_degrees": data["terrain"]["slope"],
            "data_source": "ISRO Bhuvan API",
        }
    
    @cache(ttl=3600)
    async def get_environmental_data(
        self, latitude: float, longitude: float
    ) -> dict[str, Any]:
        """
        Fetch environmental data.
        
        Endpoint: GET /environment/assessment
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/environment/assessment",
                headers=self._get_headers(),
                params={"lat": latitude, "lon": longitude}
            )
            response.raise_for_status()
            
            data = response.json()
            return self._transform_environmental_response(data, latitude, longitude)
    
    def _transform_environmental_response(
        self, data: dict, lat: float, lon: float
    ) -> dict[str, Any]:
        """Transform environmental response to match stub format."""
        return {
            "latitude": lat,
            "longitude": lon,
            "air_quality_index": data["air_quality"]["aqi"],
            "noise_level_db": data["noise"]["level_db"],
            "water_quality_index": data["water"]["quality_index"],
            "green_cover_percent": data["land_cover"]["green_percent"],
            "protected_areas_within_5km": data["protected_areas"]["count"],
            "industrial_areas_within_2km": data["industrial"]["count"],
            "wetlands_within_5km": data["wetlands"]["count"],
            "data_source": "ISRO Bhuvan API",
        }
    
    async def get_risk_assessment(
        self, latitude: float, longitude: float
    ) -> dict[str, Any]:
        """
        Fetch risk assessment data (combines multiple sources).
        """
        terrain = await self.get_terrain_data(latitude, longitude)
        
        risks = []
        
        if terrain["flood_risk"] in ["moderate", "high"]:
            risks.append({
                "type": "flood",
                "probability": 0.5 if terrain["flood_risk"] == "moderate" else 0.8,
                "severity": terrain["flood_risk"],
                "mitigation": "Adequate drainage system required",
            })
        
        seismic_map = {"zone_1": 0.1, "zone_2": 0.3, "zone_3": 0.5, "zone_4": 0.7, "zone_5": 0.9}
        seismic_prob = seismic_map.get(terrain["seismic_zone"], 0.3)
        if seismic_prob > 0.2:
            risks.append({
                "type": "seismic",
                "probability": seismic_prob,
                "severity": "high" if seismic_prob > 0.4 else "moderate",
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
            "data_source": "ISRO Bhuvan + GSI API",
        }


gis_api_client = GISAPIClient()
```

#### Example 3: Population API Client (Census)

```python
# backend/app/clients/population_api_client.py

import httpx
from typing import Any
from datetime import datetime
from app.config import settings
from app.utils.cache import cache


class PopulationAPIClient:
    """
    Real implementation for Census of India API via data.gov.in.
    Replace population_api_stub with this client in production.
    """
    
    def __init__(self):
        self.base_url = settings.CENSUS_API_URL
        self.api_key = settings.CENSUS_API_KEY
        self.timeout = httpx.Timeout(30.0)
    
    def _get_headers(self) -> dict[str, str]:
        return {
            "X-API-Key": self.api_key,
            "Accept": "application/json",
        }
    
    @cache(ttl=86400)
    async def get_population_data(self, location: str) -> dict[str, Any]:
        """
        Fetch population data from Census API.
        
        Endpoint: GET /census/population
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/census/population",
                headers=self._get_headers(),
                params={
                    "location": location,
                    "year": 2011,
                    "include_projections": True
                }
            )
            response.raise_for_status()
            
            data = response.json()
            return self._transform_population_response(data, location)
    
    def _transform_population_response(
        self, data: dict, location: str
    ) -> dict[str, Any]:
        """Transform Census API response to match stub format."""
        records = data.get("records", [])
        if not records:
            raise ValueError(f"No population data found for {location}")
        
        record = records[0]
        return {
            "location": location,
            "current_population": record["projected_population_2024"],
            "growth_rate": record["decadal_growth_rate"] / 10,
            "density_per_sqkm": record["population_density"],
            "households": record["total_households"],
            "avg_household_size": record["household_size"],
            "data_source": "Census of India + Projections",
            "last_updated": datetime.utcnow().isoformat(),
        }
    
    async def get_population_projection(
        self, location: str, years_ahead: int = 10
    ) -> dict[str, Any]:
        """
        Calculate population projection based on Census data.
        """
        base_data = await self.get_population_data(location)
        current_pop = base_data["current_population"]
        growth_rate = base_data["growth_rate"]
        
        projected_pop = int(current_pop * ((1 + growth_rate / 100) ** years_ahead))
        
        year_by_year = []
        for i in range(years_ahead + 1):
            year_pop = int(current_pop * ((1 + growth_rate / 100) ** i))
            year_by_year.append({
                "year": datetime.now().year + i,
                "population": year_pop,
                "growth_from_base": round(((year_pop - current_pop) / current_pop) * 100, 2),
            })
        
        return {
            "location": location,
            "base_year": datetime.now().year,
            "projection_years": years_ahead,
            "base_population": current_pop,
            "projected_population": projected_pop,
            "growth_rate_percent": growth_rate,
            "total_growth_percent": round(((projected_pop - current_pop) / current_pop) * 100, 2),
            "year_by_year_projection": year_by_year,
            "data_source": "Census Projection Model",
        }
    
    async def get_employment_data(self, location: str) -> dict[str, Any]:
        """
        Fetch employment data from Census API.
        
        Endpoint: GET /census/employment
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/census/employment",
                headers=self._get_headers(),
                params={"location": location}
            )
            response.raise_for_status()
            
            data = response.json()
            return self._transform_employment_response(data, location)
    
    def _transform_employment_response(
        self, data: dict, location: str
    ) -> dict[str, Any]:
        """Transform employment response to match stub format."""
        records = data.get("records", [])
        if not records:
            raise ValueError(f"No employment data found for {location}")
        
        record = records[0]
        working_pop = record["working_population"]
        
        return {
            "location": location,
            "working_age_population": working_pop,
            "employed": record["main_workers"] + record["marginal_workers"],
            "unemployed": record["non_workers"] - record["students"] - record["dependents"],
            "not_in_labor_force": record["non_workers"],
            "employment_rate": round((record["main_workers"] / working_pop) * 100, 1),
            "unemployment_rate": round((record["seeking_work"] / working_pop) * 100, 1),
            "sectors": {
                "agriculture": record["cultivators_percent"],
                "manufacturing": record["household_industry_percent"],
                "services": record["other_workers_percent"],
                "construction": 10,
                "other": 8,
            },
            "data_source": "Census Employment Data",
        }


population_api_client = PopulationAPIClient()
```

#### Example 4: Land Use API Client

```python
# backend/app/clients/land_use_api_client.py

import httpx
from typing import Any
from datetime import datetime
from app.config import settings
from app.utils.cache import cache


class LandUseAPIClient:
    """
    Real implementation for land records APIs (Dharani/Mee Bhoomi).
    Replace land_use_api_stub with this client in production.
    """
    
    def __init__(self):
        self.base_url = settings.LAND_RECORDS_API_URL
        self.api_key = settings.LAND_RECORDS_API_KEY
        self.timeout = httpx.Timeout(30.0)
    
    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    @cache(ttl=86400)
    async def get_land_use_data(self, location: str) -> dict[str, Any]:
        """
        Fetch land use data from state land records API.
        
        Endpoint: GET /land/use/summary
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/land/use/summary",
                headers=self._get_headers(),
                params={"mandal": location}
            )
            response.raise_for_status()
            
            data = response.json()
            return self._transform_land_use_response(data, location)
    
    def _transform_land_use_response(
        self, data: dict, location: str
    ) -> dict[str, Any]:
        """Transform land records response to match stub format."""
        summary = data.get("summary", {})
        
        return {
            "location": location,
            "total_area_sqkm": summary["total_geographical_area_ha"] / 100,
            "urban_area_percent": summary["urban_area_percent"],
            "commercial_percent": summary["land_use"]["commercial_percent"],
            "industrial_percent": summary["land_use"]["industrial_percent"],
            "residential_percent": summary["land_use"]["residential_percent"],
            "agricultural_percent": summary["land_use"]["agricultural_percent"],
            "open_spaces_percent": summary["land_use"]["open_spaces_percent"],
            "avg_land_price_per_sqft": summary["market_value"]["avg_per_sqft"],
            "data_source": "State Land Records Portal",
            "last_updated": datetime.utcnow().isoformat(),
        }
    
    async def get_zoning_info(self, location: str) -> dict[str, Any]:
        """
        Fetch zoning information from Town Planning API.
        
        Endpoint: GET /zoning/regulations
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/zoning/regulations",
                headers=self._get_headers(),
                params={"area": location}
            )
            response.raise_for_status()
            
            data = response.json()
            return self._transform_zoning_response(data, location)
    
    def _transform_zoning_response(
        self, data: dict, location: str
    ) -> dict[str, Any]:
        """Transform zoning response to match stub format."""
        zones = data.get("zones", {})
        
        return {
            "location": location,
            "zones": {
                "central_business_district": {
                    "max_fsi": zones["cbd"]["fsi_max"],
                    "max_height_m": zones["cbd"]["height_max_m"],
                    "setbacks_m": zones["cbd"]["setbacks_m"],
                    "permitted_uses": zones["cbd"]["permitted_uses"],
                },
                "commercial_zone": {
                    "max_fsi": zones["commercial"]["fsi_max"],
                    "max_height_m": zones["commercial"]["height_max_m"],
                    "setbacks_m": zones["commercial"]["setbacks_m"],
                    "permitted_uses": zones["commercial"]["permitted_uses"],
                },
                "industrial_zone": {
                    "max_fsi": zones["industrial"]["fsi_max"],
                    "max_height_m": zones["industrial"]["height_max_m"],
                    "setbacks_m": zones["industrial"]["setbacks_m"],
                    "permitted_uses": zones["industrial"]["permitted_uses"],
                },
                "residential_zone": {
                    "max_fsi": zones["residential"]["fsi_max"],
                    "max_height_m": zones["residential"]["height_max_m"],
                    "setbacks_m": zones["residential"]["setbacks_m"],
                    "permitted_uses": zones["residential"]["permitted_uses"],
                },
            },
            "infrastructure_requirements": data["infrastructure_requirements"],
            "data_source": "Town Planning Department",
        }


land_use_api_client = LandUseAPIClient()
```

#### Example 5: Economic API Client

```python
# backend/app/clients/economic_api_client.py

import httpx
from typing import Any
from datetime import datetime
from app.config import settings
from app.utils.cache import cache


class EconomicAPIClient:
    """
    Real implementation for MoSPI and RBI APIs.
    Replace economic_api_stub with this client in production.
    """
    
    def __init__(self):
        self.mospi_url = settings.MOSPI_API_URL
        self.rbi_url = settings.RBI_API_URL
        self.api_key = settings.ECONOMIC_API_KEY
        self.timeout = httpx.Timeout(30.0)
    
    def _get_headers(self) -> dict[str, str]:
        return {
            "X-API-Key": self.api_key,
            "Accept": "application/json",
        }
    
    @cache(ttl=86400)
    async def get_economic_indicators(self, location: str) -> dict[str, Any]:
        """
        Fetch economic indicators from MoSPI API.
        
        Endpoint: GET /economy/indicators
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.mospi_url}/economy/indicators",
                headers=self._get_headers(),
                params={"state": location, "year": "latest"}
            )
            response.raise_for_status()
            
            data = response.json()
            return self._transform_economic_response(data, location)
    
    def _transform_economic_response(
        self, data: dict, location: str
    ) -> dict[str, Any]:
        """Transform MoSPI response to match stub format."""
        indicators = data.get("indicators", {})
        
        return {
            "location": location,
            "gdp_per_capita": indicators["nsdp_per_capita"],
            "gdp_growth_rate": indicators["gsva_growth_rate"],
            "inflation_rate": indicators["cpi_inflation"],
            "fdi_investment_cr": indicators["fdi_inflows_cr"],
            "industrial_output_growth": indicators["iip_growth"],
            "data_source": "MoSPI Economic Survey",
            "last_updated": datetime.utcnow().isoformat(),
        }
    
    async def get_vehicle_growth_data(self, location: str) -> dict[str, Any]:
        """
        Fetch vehicle statistics from MoRTH API.
        
        Endpoint: GET /transport/vehicles
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.mospi_url}/transport/vehicles",
                headers=self._get_headers(),
                params={"state": location}
            )
            response.raise_for_status()
            
            data = response.json()
            return self._transform_vehicle_response(data, location)
    
    def _transform_vehicle_response(
        self, data: dict, location: str
    ) -> dict[str, Any]:
        """Transform vehicle statistics response."""
        vehicles = data.get("vehicles", {})
        total = sum(v["count"] for v in vehicles["by_type"].values())
        
        return {
            "location": location,
            "total_vehicles": total,
            "annual_growth_rate": vehicles["growth_rate_yoy"],
            "vehicle_types": {
                vtype: {
                    "count": vdata["count"],
                    "growth_rate": vdata["growth_rate"],
                    "percentage": round((vdata["count"] / total) * 100, 1),
                }
                for vtype, vdata in vehicles["by_type"].items()
            },
            "projection_5_years": int(total * ((1 + vehicles["growth_rate_yoy"] / 100) ** 5)),
            "projection_10_years": int(total * ((1 + vehicles["growth_rate_yoy"] / 100) ** 10)),
            "data_source": "MoRTH Transport Statistics",
        }


economic_api_client = EconomicAPIClient()
```

---

## Migration Strategy

### Step 1: Configuration

Add API configuration to environment:

```python
# backend/app/config.py additions

class Settings(BaseSettings):
    # Existing settings...
    
    # Government API Configuration
    TRAFFIC_API_URL: str = "https://traffic-api.gov.in"
    TRAFFIC_API_KEY: str = ""
    
    BHUVAN_API_URL: str = "https://bhuvan.nrsc.gov.in/api"
    BHUVAN_API_KEY: str = ""
    
    CENSUS_API_URL: str = "https://data.gov.in/api/census"
    CENSUS_API_KEY: str = ""
    
    LAND_RECORDS_API_URL: str = "https://landrecords.gov.in/api"
    LAND_RECORDS_API_KEY: str = ""
    
    MOSPI_API_URL: str = "https://mospi.gov.in/api"
    RBI_API_URL: str = "https://dbie.rbi.org.in/api"
    ECONOMIC_API_KEY: str = ""
    
    # Feature flag for using real APIs
    USE_REAL_APIS: bool = False
```

### Step 2: Create API Client Factory

```python
# backend/app/clients/api_factory.py

from app.config import settings
from app.stubs.traffic_api import traffic_api_stub
from app.stubs.gis_api import gis_api_stub
from app.stubs.population_api import population_api_stub
from app.stubs.land_use_api import land_use_api_stub
from app.stubs.economic_api import economic_api_stub

from app.clients.traffic_api_client import traffic_api_client
from app.clients.gis_api_client import gis_api_client
from app.clients.population_api_client import population_api_client
from app.clients.land_use_api_client import land_use_api_client
from app.clients.economic_api_client import economic_api_client


class APIFactory:
    """
    Factory to provide either stub or real API clients
    based on configuration.
    """
    
    @staticmethod
    def get_traffic_api():
        if settings.USE_REAL_APIS and settings.TRAFFIC_API_KEY:
            return traffic_api_client
        return traffic_api_stub
    
    @staticmethod
    def get_gis_api():
        if settings.USE_REAL_APIS and settings.BHUVAN_API_KEY:
            return gis_api_client
        return gis_api_stub
    
    @staticmethod
    def get_population_api():
        if settings.USE_REAL_APIS and settings.CENSUS_API_KEY:
            return population_api_client
        return population_api_stub
    
    @staticmethod
    def get_land_use_api():
        if settings.USE_REAL_APIS and settings.LAND_RECORDS_API_KEY:
            return land_use_api_client
        return land_use_api_stub
    
    @staticmethod
    def get_economic_api():
        if settings.USE_REAL_APIS and settings.ECONOMIC_API_KEY:
            return economic_api_client
        return economic_api_stub


api_factory = APIFactory()
```

### Step 3: Update Service Layer

```python
# backend/app/services/site_analysis.py updates

from app.clients.api_factory import api_factory

class SiteAnalysisService:
    def __init__(self):
        self.gis_api = api_factory.get_gis_api()
        self.population_api = api_factory.get_population_api()
        self.economic_api = api_factory.get_economic_api()
        self.land_use_api = api_factory.get_land_use_api()
    
    async def analyze_site(self, db: AsyncSession, site_id: uuid.UUID) -> Site:
        site = await db.get(Site, site_id)
        if not site:
            raise ValueError("Site not found")
        
        terrain_data = self.gis_api.get_terrain_data(site.latitude, site.longitude)
        env_data = self.gis_api.get_environmental_data(site.latitude, site.longitude)
        pop_data = self.population_api.get_population_data(site.location_name)
        econ_data = self.economic_api.get_economic_indicators(site.location_name)
        land_data = self.land_use_api.get_land_use_data(site.location_name)
        
        # ... rest of the method
```

### Step 4: Environment Variables

```bash
# .env additions for production

USE_REAL_APIS=true

TRAFFIC_API_URL=https://hyderabad-traffic-api.gov.in
TRAFFIC_API_KEY=your_traffic_api_key

BHUAVAN_API_URL=https://bhuvan.nrsc.gov.in/api
BHUAVAN_API_KEY=your_bhuvan_api_key

CENSUS_API_URL=https://data.gov.in/api/census
CENSUS_API_KEY=your_census_api_key

LAND_RECORDS_API_URL=https://meebhoomi.ap.gov.in/api
LAND_RECORDS_API_KEY=your_land_api_key

MOSPI_API_URL=https://mospi.gov.in/api
RBI_API_URL=https://dbie.rbi.org.in/api
ECONOMIC_API_KEY=your_economic_api_key
```

### Step 5: Gradual Migration Checklist

- [ ] Obtain API keys for each government API
- [ ] Implement rate limiting middleware
- [ ] Add circuit breaker for API failures
- [ ] Set up monitoring and alerting
- [ ] Configure caching (Redis recommended)
- [ ] Test each API client individually
- [ ] Run parallel testing (stub vs real)
- [ ] Enable feature flag for production
- [ ] Monitor data quality and consistency
- [ ] Document any data transformation issues

---

## Appendix: Contact Information

### Government API Contacts

| Organization | Contact | Email |
|--------------|---------|-------|
| ISRO Bhuvan | NRSC Helpdesk | bhuvan@nrsc.gov.in |
| Survey of India | Open Series Map Division | osm@sosurvey.gov.in |
| Census of India | Data Dissemination Unit | data@censusindia.gov.in |
| MoSPI | Statistical Data Division | support@mospi.gov.in |
| RBI DBIE | Database Support | dbie@rbi.org.in |
| NIC | API Support | support@nic.in |
| Hyderabad Traffic Police | IT Cell | traffic-hyd@telangana.gov.in |

### Useful Links

- [Data.gov.in Open Data Portal](https://data.gov.in/)
- [ISRO Bhuvan](https://bhuvan.nrsc.gov.in/)
- [Census of India](https://censusindia.gov.in/)
- [MoSPI](https://mospi.gov.in/)
- [RBI DBIE](https://dbie.rbi.org.in/)
- [NIC eGov APIs](https://egovernance.nic.in/)

---

*Last Updated: March 2026*
*Document Version: 1.0*
