# Tasks - Phase 3 & 4: Dashboard & Traffic Analysis

## Phase 3: Core Dashboard & Navigation

### Backend Tasks

- [ ] Task 1: Create dashboard router and endpoints
  - [ ] SubTask 1.1: Create /api/v1/dashboard/router.py with metrics endpoint
  - [ ] SubTask 1.2: Create /api/v1/dashboard/metrics endpoint returning summary stats
  - [ ] SubTask 1.3: Create /api/v1/dashboard/activity endpoint for recent actions
  - [ ] SubTask 1.4: Add router to main.py

- [ ] Task 2: Create notification model and API
  - [ ] SubTask 2.1: Create Notification model in models/notification.py
  - [ ] SubTask 2.2: Create notification schemas in schemas/notification.py
  - [ ] SubTask 2.3: Create /api/v1/notifications router with CRUD endpoints
  - [ ] SubTask 2.4: Implement notification service for creating/marking read

- [ ] Task 3: Create file upload service
  - [ ] SubTask 3.1: Create /api/v1/upload router with POST endpoint
  - [ ] SubTask 3.2: Implement file validation (size, type)
  - [ ] SubTask 3.3: Configure upload directory and static file serving
  - [ ] SubTask 3.4: Create upload schemas and response format

- [ ] Task 4: Create settings API
  - [ ] SubTask 4.1: Create UserSettings model or use JSON field on User
  - [ ] SubTask 4.2: Create settings schemas in schemas/settings.py
  - [ ] SubTask 4.3: Create /api/v1/settings router with GET/PUT endpoints
  - [ ] SubTask 4.4: Implement settings service for preference management

- [ ] Task 5: Create database migration for Phase 3
  - [ ] SubTask 5.1: Create migration for notifications table
  - [ ] SubTask 5.2: Add settings column to users table if needed

### Frontend Tasks - Phase 3

- [ ] Task 6: Enhance Dashboard page
  - [ ] SubTask 6.1: Add metrics cards showing projects, pending, completed, sites counts
  - [ ] SubTask 6.2: Add activity feed component showing recent actions
  - [ ] SubTask 6.3: Connect to /api/v1/dashboard/metrics endpoint
  - [ ] SubTask 6.4: Add loading states and error handling

- [ ] Task 7: Create notification system
  - [ ] SubTask 7.1: Create notification types in types/notification.ts
  - [ ] SubTask 7.2: Create notification service in services/notification.ts
  - [ ] SubTask 7.3: Add notification bell to Header with unread badge
  - [ ] SubTask 7.4: Create notification dropdown component
  - [ ] SubTask 7.5: Implement mark-as-read functionality

- [ ] Task 8: Create file upload component
  - [ ] SubTask 8.1: Create FileUpload component with drag-drop support
  - [ ] SubTask 8.2: Add file type validation and size limits
  - [ ] SubTask 8.3: Show upload progress indicator
  - [ ] SubTask 8.4: Handle success/error states

- [ ] Task 9: Create settings page
  - [ ] SubTask 9.1: Create Settings page with preference sections
  - [ ] SubTask 9.2: Create settings service for API calls
  - [ ] SubTask 9.3: Add form for notification preferences
  - [ ] SubTask 9.4: Add theme/display preferences section
  - [ ] SubTask 9.5: Connect to /api/v1/settings endpoint

- [ ] Task 10: Update Sidebar navigation
  - [ ] SubTask 10.1: Add all module links with icons
  - [ ] SubTask 10.2: Highlight active route
  - [ ] SubTask 10.3: Add collapse/expand functionality

## Phase 4: Traffic Analysis Module

### Backend Tasks - Phase 4

- [ ] Task 11: Create traffic data models
  - [ ] SubTask 11.1: Create TrafficData model with location, flow, timestamp fields
  - [ ] SubTask 11.2: Create TrafficIncident model for accidents/events
  - [ ] SubTask 11.3: Create TrafficPattern model for historical patterns
  - [ ] SubTask 11.4: Add GIS coordinate fields using PostGIS

- [ ] Task 12: Create traffic schemas
  - [ ] SubTask 12.1: Create TrafficDataCreate, TrafficDataResponse schemas
  - [ ] SubTask 12.2: Create TrafficFilter schema for query params
  - [ ] SubTask 12.3: Create HeatmapPoint schema for visualization
  - [ ] SubTask 12.4: Create CongestionScore schema
  - [ ] SubTask 12.5: Create Hotspot schema with risk assessment

- [ ] Task 13: Create traffic API stub service
  - [ ] SubTask 13.1: Create stubs/traffic_api.py with mock data generator
  - [ ] SubTask 13.2: Generate realistic traffic flow data
  - [ ] SubTask 13.3: Generate mock incident data
  - [ ] SubTask 13.4: Implement data refresh simulation

- [ ] Task 14: Create traffic router and endpoints
  - [ ] SubTask 14.1: Create /api/v1/traffic router
  - [ ] SubTask 14.2: GET /api/v1/traffic/data - list traffic data with filters
  - [ ] SubTask 14.3: GET /api/v1/traffic/heatmap - return heatmap coordinates
  - [ ] SubTask 14.4: GET /api/v1/traffic/congestion - return congestion scores
  - [ ] SubTask 14.5: GET /api/v1/traffic/hotspots - return incident hotspots
  - [ ] SubTask 14.6: GET /api/v1/traffic/export - export report as PDF/Excel

- [ ] Task 15: Create traffic service with AI integration
  - [ ] SubTask 15.1: Create services/traffic.py with business logic
  - [ ] SubTask 15.2: Implement heatmap data generation algorithm
  - [ ] SubTask 15.3: Implement congestion scoring algorithm
  - [ ] SubTask 15.4: Implement hotspot detection algorithm
  - [ ] SubTask 15.5: Create POST /api/v1/traffic/analyze for AI insights
  - [ ] SubTask 15.6: Integrate OpenAI for traffic analysis

- [ ] Task 16: Create AI traffic insights service
  - [ ] SubTask 16.1: Create ai/traffic_analyzer.py
  - [ ] SubTask 16.2: Implement prompt templates for traffic analysis
  - [ ] SubTask 16.3: Parse AI response into structured insights
  - [ ] SubTask 16.4: Add confidence scoring for AI recommendations

- [ ] Task 17: Create traffic export service
  - [ ] SubTask 17.1: Implement PDF report generation using WeasyPrint
  - [ ] SubTask 17.2: Implement Excel export using OpenPyXL
  - [ ] SubTask 17.3: Create report templates with charts
  - [ ] SubTask 17.4: Add export endpoint with format selection

- [ ] Task 18: Create database migration for traffic
  - [ ] SubTask 18.1: Create migration for traffic_data table
  - [ ] SubTask 18.2: Create migration for traffic_incidents table
  - [ ] SubTask 18.3: Add spatial indexes for GIS queries

### Frontend Tasks - Phase 4

- [ ] Task 19: Create traffic types and service
  - [ ] SubTask 19.1: Create types/traffic.ts with all interfaces
  - [ ] SubTask 19.2: Create services/traffic.ts with API calls
  - [ ] SubTask 19.3: Add traffic store with Zustand for state management

- [ ] Task 20: Enhance Traffic page layout
  - [ ] SubTask 20.1: Add stats cards for traffic volume, peak hours, incidents
  - [ ] SubTask 20.2: Add filter controls (date range, area, type)
  - [ ] SubTask 20.3: Add export buttons (PDF, Excel)
  - [ ] SubTask 20.4: Create responsive grid layout

- [ ] Task 21: Create Map component
  - [ ] SubTask 21.1: Install Leaflet and react-leaflet packages
  - [ ] SubTask 21.2: Create Map component with Leaflet integration
  - [ ] SubTask 21.3: Add heatmap layer using leaflet.heat
  - [ ] SubTask 21.4: Add marker clustering for incidents
  - [ ] SubTask 21.5: Connect to /api/v1/traffic/heatmap endpoint

- [ ] Task 22: Create traffic data table
  - [ ] SubTask 22.1: Create Table component with sorting/filtering
  - [ ] SubTask 22.2: Display traffic data with columns (location, flow, time, level)
  - [ ] SubTask 22.3: Add pagination controls
  - [ ] SubTask 22.4: Connect to /api/v1/traffic/data endpoint

- [ ] Task 23: Create congestion visualizer
  - [ ] SubTask 23.1: Create color-coded congestion display (green/yellow/orange/red)
  - [ ] SubTask 23.2: Add congestion legend
  - [ ] SubTask 23.3: Show real-time congestion status
  - [ ] SubTask 23.4: Connect to /api/v1/traffic/congestion endpoint

- [ ] Task 24: Create incident markers on map
  - [ ] SubTask 24.1: Add custom markers for incidents
  - [ ] SubTask 24.2: Create incident popup with details
  - [ ] SubTask 24.3: Filter incidents by type and date
  - [ ] SubTask 24.4: Connect to hotspot data

- [ ] Task 25: Create AI insights panel
  - [ ] SubTask 25.1: Create insights panel component
  - [ ] SubTask 25.2: Display key findings from AI analysis
  - [ ] SubTask 25.3: Show recommendations with confidence scores
  - [ ] SubTask 25.4: Add refresh analysis button
  - [ ] SubTask 25.5: Connect to POST /api/v1/traffic/analyze endpoint

- [ ] Task 26: Create traffic filters component
  - [ ] SubTask 26.1: Add date range picker
  - [ ] SubTask 26.2: Add area/location selector
  - [ ] SubTask 26.3: Add traffic type filter
  - [ ] SubTask 26.4: Apply filters to all traffic views

- [ ] Task 27: Wire export functionality
  - [ ] SubTask 27.1: Add PDF export button with download handling
  - [ ] SubTask 27.2: Add Excel export button with download handling
  - [ ] SubTask 27.3: Show export progress indicator
  - [ ] SubTask 27.4: Handle export errors gracefully

## Task Dependencies
- [Task 5] depends on [Task 2, Task 4]
- [Task 6] depends on [Task 1]
- [Task 7] depends on [Task 2]
- [Task 9] depends on [Task 4]
- [Task 14] depends on [Task 11, Task 12, Task 13]
- [Task 15] depends on [Task 14]
- [Task 16] depends on [Task 15]
- [Task 17] depends on [Task 15]
- [Task 18] depends on [Task 11]
- [Task 20] depends on [Task 19]
- [Task 21] depends on [Task 19]
- [Task 22] depends on [Task 19]
- [Task 25] depends on [Task 16]
- [Task 27] depends on [Task 17]

## Parallelizable Work
- Backend Tasks 1-4 can run in parallel
- Backend Tasks 11-13 can run in parallel
- Frontend Tasks 6-10 can run in parallel after backend is ready
- Frontend Tasks 20-27 can run in parallel after backend is ready
