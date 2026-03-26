# Implement Reports and AI Assistant Pages,

## Why
The Reports page shows "coming soon" and the AI Assistant page shows "coming soon" for The Dashboard shows no data because the `/dashboard/metrics` endpoint returns empty results (projectsCount=0, pendingItems=0, completedItems 0, activeSites all show 0). System health shows "Disconnected" for all services because the health check endpoint returns incorrect structure - `DetailedHealthResponse` has `services` object but should frontend expects `services.database` but backend returns `database` directly.

## What Changes
- Implement Reports page with report generation from existing traffic/forecast/simulation data
- Implement AI Assistant page with chat interface using simulation recommendation API
- Fix Dashboard metrics endpoint to return stub data
- Fix health endpoint response schema to align frontend expectations

## Impact
- Affected specs: Phase 3-4 Dashboard & Traffic Module
- Affected code:
  - Backend: `/backend/app/routers/dashboard.py` - fix metrics endpoint
  - Backend: `/backend/app/routers/health.py` - fix health response schema
  - Backend: `/backend/app/schemas/health.py` - update schema
  - Frontend: `/frontend/src/pages/Reports.tsx` - implement report generation
  - Frontend: `/frontend/src/pages/AiAssistant.tsx` - implement chat interface

## ADDED Requirements

### Requirement: Reports Page
The system SHALL provide report generation functionality with export options.

#### Scenario: Generate traffic report
- **WHEN** user clicks "Traffic Report" button
- **THEN** system generates PDF/Excel report from traffic data
- **AND** report downloads automatically

#### Scenario: Generate forecast report
- **WHEN** user clicks "Forecast Report" button
- **THEN** system generates forecast analysis report
- **AND** report downloads automatically

### Requirement: AI Assistant Page
The system SHALL provide AI-powered chat interface for infrastructure planning assistance.

#### Scenario: Ask question via chat
- **WHEN** user types a question and- **THEN** system calls simulation recommendation API
- **AND** displays AI response with recommendations

### Requirement: Dashboard Metrics
The dashboard metrics endpoint SHALL return meaningful stub data.

#### Scenario: Get dashboard metrics
- **WHEN** authenticated user requests GET /api/v1/dashboard/metrics
- **THEN** system returns non-zero values for projectsCount, pendingItems, completedItems, activeSites
- **AND** includes traffic summary and alert counts

### Requirement: Health Check Response
The health check endpoint SHALL return correct response structure.

#### Scenario: Get detailed health
- **WHEN** user requests GET /api/v1/health/detailed
- **THEN** system returns response with `services` object containing `database` and `redis` keys
- **AND** response structure matches frontend expectations
