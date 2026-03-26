# Make System Dynamic with Stubs and OpenAI Integration Spec

## Why
The Reports module has static mock data for Forecast and Site Analysis reports. The AI Assistant can leverage OpenAI more effectively. The system should use the existing stub infrastructure (traffic, GIS, population, land use, economic) consistently across all modules, with OpenAI enhancing analysis capabilities.

## What Changes
- Connect Reports module to use existing stubs and backend APIs
- Enhance AI Assistant to use OpenAI for all queries (already configured)
- Create forecast export endpoint for dynamic report generation
- Create site analysis export endpoint for dynamic report generation
- Ensure all services use appropriate stubs with clear documentation for future government API integration
- Document real government APIs that will replace stubs

## Impact
- Affected specs: Phase 3-4 Dashboard & Traffic Module, MVP Demo Plan
- Affected code:
  - Backend: `/backend/app/routers/forecasts.py` - add export endpoint
  - Backend: `/backend/app/routers/sites.py` - add export endpoint
  - Backend: `/backend/app/services/forecasting.py` - use OpenAI for analysis
  - Backend: `/backend/app/services/site_analysis.py` - use existing stubs
  - Frontend: `/frontend/src/pages/Reports.tsx` - connect to real APIs
  - Frontend: `/frontend/src/services/forecast.ts` - add export function
  - Frontend: `/frontend/src/services/site.ts` - add export function

## Government APIs Research (Future Integration)

### India Government APIs (Will Replace Stubs)
| Data Type | API/Source | Approval Authority |
|-----------|------------|-------------------|
| **Traffic Data** | Hyderabad Traffic Police API, NIC Traffic Portal | State Traffic Department |
| **GIS/Terrain** | Survey of India, ISRO Bhuvan API | Survey of India / ISRO |
| **Population** | Census of India API | Registrar General of India |
| **Land Records** | Dharani (Telangana), Bhoomi Portal | State Revenue Department |
| **Economic Data** | Ministry of Statistics (MoSPI), RBI | Central Government |
| **Weather** | IMD (India Meteorological Department) | IMD |
| **Environmental** | CPCB, State Pollution Control Board | CPCB |
| **Roads** | NHAI, State PWD | NHAI / State PWD |

## ADDED Requirements

### Requirement: Dynamic Forecast Report Generation
The system SHALL generate forecast reports using stub data and OpenAI analysis.

#### Scenario: Generate forecast report
- **WHEN** user clicks "Forecast Report" button
- **THEN** system fetches forecast data from stubs
- **AND** uses OpenAI to generate insights
- **AND** generates PDF/Excel file for download

### Requirement: Dynamic Site Analysis Report Generation
The system SHALL generate site analysis reports using GIS, population, and land use stubs.

#### Scenario: Generate site analysis report
- **WHEN** user clicks "Site Analysis Report" button
- **THEN** system fetches data from GIS, population, land use stubs
- **AND** uses OpenAI for site recommendations
- **AND** generates PDF/Excel file for download

### Requirement: Enhanced AI Assistant with OpenAI
The AI Assistant SHALL use OpenAI for all queries when API key is configured.

#### Scenario: AI Assistant query with OpenAI
- **WHEN** user asks a question
- **THEN** system uses OpenAI GPT-4 with infrastructure planning context
- **AND** enriches response with stub data
- **AND** returns actionable recommendations

### Requirement: Consistent Stub Usage
All modules SHALL use the existing stub infrastructure for government API simulation.

#### Scenario: Use stubs for data
- **WHEN** any module needs government data
- **THEN** system uses appropriate stub (traffic, GIS, population, land use, economic)
- **AND** data is clearly marked as stub/simulated
- **AND** real API integration points are documented

## MODIFIED Requirements

### Requirement: Reports Page
The Reports page SHALL generate all reports dynamically using backend APIs and stubs.

**Previous**: Forecast and Site Analysis reports were static mock text
**Updated**: All reports use real backend APIs with stub data and OpenAI analysis
