# Fix Traffic Page Data Display Spec

## Why
The Traffic page has blank sections and showing zeros because the `/traffic/data` endpoint queries the database (which is empty) instead of using stub data like the congestion and hotspots endpoints do. The system needs to use stub data for government API simulation and leverage OpenAI API for AI-powered analysis.

## What Changes
- **BREAKING**: Modify `/traffic/data` endpoint to use stub data instead of database queries
- Ensure all traffic endpoints consistently use stubs for government API simulation
- Verify OpenAI API integration is working for traffic analysis
- Add data seeding option for populating database with initial traffic data
- Update frontend to handle stub data properly

## Impact
- Affected specs: Phase 3-4 Dashboard & Traffic Module
- Affected code:
  - Backend: `/backend/app/routers/traffic.py` - modify data endpoint to use stubs
  - Backend: `/backend/app/stubs/traffic_api.py` - ensure complete stub data
  - Backend: `/backend/app/services/traffic.py` - verify OpenAI integration
  - Frontend: `/frontend/src/pages/Traffic.tsx` - verify data display

## ADDED Requirements

### Requirement: Traffic Data Endpoint Uses Stubs
The system SHALL provide traffic data from stub service instead of empty database queries.

#### Scenario: Get traffic data from stubs
- **WHEN** user requests GET /api/v1/traffic/data
- **THEN** system returns traffic data from traffic_api_stub
- **AND** data includes location_name, vehicle_count, avg_speed, congestion_level, timestamp
- **AND** top four cards show non-zero values

### Requirement: Consistent Stub Usage
All traffic endpoints SHALL consistently use stub data for government API simulation.

#### Scenario: All endpoints return stub data
- **WHEN** any traffic endpoint is called (data, heatmap, congestion, hotspots)
- **THEN** all return data from traffic_api_stub
- **AND** no endpoint returns empty results due to missing database records

### Requirement: OpenAI API Integration for Analysis
The system SHALL use OpenAI API for traffic analysis when API key is configured.

#### Scenario: AI traffic analysis with OpenAI
- **WHEN** user requests POST /api/v1/traffic/analyze with valid OpenAI API key
- **THEN** system uses GPT-4 to generate insights
- **AND** returns AI-generated findings and recommendations
- **AND** includes confidence scores

#### Scenario: Fallback to mock insights without OpenAI key
- **WHEN** OpenAI API key is not configured
- **THEN** system returns mock insights with clear indication
- **AND** analysis still provides value to users

### Requirement: Traffic Hotspots Display
The traffic hotspots section SHALL display incident hotspot data.

#### Scenario: View traffic hotspots
- **WHEN** Traffic page loads
- **THEN** hotspots section shows locations with incident counts and risk levels
- **AND** each hotspot displays risk_score and risk_level badge

### Requirement: Traffic Data Table Display
The traffic data table SHALL display traffic records with pagination.

#### Scenario: View traffic data table
- **WHEN** Traffic page loads
- **THEN** table shows at least 10 traffic records
- **AND** each row shows location, vehicles, avg speed, congestion level, timestamp
- **AND** pagination works correctly

## MODIFIED Requirements

### Requirement: Traffic Data Router
The traffic router SHALL use stub data for all read operations while maintaining database capability for future persistence.

**Previous**: Traffic data endpoint queries database directly
**Updated**: Traffic data endpoint uses stub data with option to query database when data exists

## Implementation Notes

1. **Stub Data Flow**: All traffic endpoints should follow the pattern used by `/traffic/congestion` and `/traffic/hotspots` - get data from `traffic_api_stub.get_all_traffic_data()`

2. **Database vs Stubs**: 
   - Current implementation: `/traffic/data` queries database (empty) → returns empty array
   - Required implementation: Use stubs first, optionally merge with database data

3. **OpenAI Integration**: Already implemented in `TrafficService.analyze_traffic_data()` - needs verification that API key is being read from environment

4. **Environment Configuration**: Ensure `.env` file has valid `OPENAI_API_KEY` for production use
