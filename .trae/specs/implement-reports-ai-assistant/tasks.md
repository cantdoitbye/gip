# Tasks

## Task 1: Fix Dashboard Metrics Endpoint
- [x] Modify `/backend/app/routers/dashboard.py` to return stub data for metrics
  - [x] Add stub data for projectsCount (e.g., 12)
  - [x] Add stub data for pendingItems (e.g., 5)
  - [x] Add stub data for completedItems (e.g., 28)
  - [x] Add stub data for activeSites (e.g., 8)
  - [x] Add traffic summary with realistic values
  - [x] Add alert counts

## Task 2: Fix Health Check Response Schema
- [x] Update `/backend/app/schemas/health.py` to match frontend expectations
  - [x] Ensure DetailedHealthResponse has `services` object
  - [x] `services` should contain `database` and `redis` keys
- [x] Update `/backend/app/routers/health.py` to use correct schema
  - [x] Return response with nested services structure

## Task 3: Implement Reports Page
- [x] Update `/frontend/src/pages/Reports.tsx` to remove "coming soon"
  - [x] Add report generation buttons (Traffic, Forecast, Site Analysis)
  - [x] Use existing traffic export API for traffic reports
  - [x] Use existing forecast API for forecast reports
  - [x] Add download functionality for PDF/Excel formats
  - [x] Add report history section

## Task 4: Implement AI Assistant Page
- [x] Update `/frontend/src/pages/AiAssistant.tsx` to remove "coming soon"
  - [x] Add chat interface with message input
  - [x] Add message display area with user/assistant messages
  - [x] Connect to simulation recommendations API
  - [x] Add quick action buttons
  - [x] Handle OpenAI responses when configured
  - [x] Show mock responses when OpenAI not configured

## Task 5: Verify Dashboard and Health Integration
- [x] Test dashboard metrics display
- [x] Test system health indicators
- [x] Verify all services show proper status

# Task Dependencies
- [Task 1: Dashboard Metrics] and [Task 2: Health Check] can run in parallel
- [Task 3: Reports Page] and [Task 4: AI Assistant Page] can run in parallel
- [Task 5: Verify Integration] depends on Tasks 1-4 being completed
