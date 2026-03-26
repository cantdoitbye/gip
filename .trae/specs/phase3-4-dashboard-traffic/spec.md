# Phase 3 & 4: Core Dashboard & Traffic Analysis Module

## Why
Phase 3 establishes the main dashboard interface with metrics, notifications, and navigation that serves as the central hub for the application. Phase 4 implements the first functional module - Traffic Analysis - which provides interactive traffic data visualization, AI-powered insights, congestion analysis, and hotspot detection.

## What Changes
- Dashboard metrics API with summary statistics
- Activity feed and notification system
- File upload service for documents/images
- Settings API for user preferences
- Traffic data models and database schema
- Traffic API stub service (mock government data)
- Heatmap generation for traffic visualization
- AI traffic insights using OpenAI
- Congestion scoring algorithm
- Accident hotspot detection
- Traffic report export (PDF/Excel)
- Dashboard UI with metrics widgets
- Navigation sidebar with module links
- Notification center component
- File upload component
- Settings page
- Traffic dashboard with interactive map
- Traffic data tables with filtering
- AI insights panel for traffic analysis

## Impact
- Affected specs: Phase 2 (auth integration for protected endpoints)
- Affected code: 
  - Backend: new routers (dashboard, traffic, notifications, settings, upload), models (traffic), services (traffic, ai), stubs (traffic_api)
  - Frontend: new pages (enhanced Dashboard, enhanced Traffic), components (Map, Chart, FileUpload, Notification), services (dashboard, traffic), types (traffic)

## ADDED Requirements

### Requirement: Dashboard Metrics API
The system SHALL provide a metrics API that returns summary statistics for the dashboard.

#### Scenario: Get dashboard metrics
- **WHEN** authenticated user requests GET /api/v1/dashboard/metrics
- **THEN** system returns JSON with project counts, traffic summary, alert counts

### Requirement: Activity Feed API
The system SHALL provide an activity feed showing recent system events.

#### Scenario: Get recent activity
- **WHEN** authenticated user requests GET /api/v1/dashboard/activity
- **THEN** system returns paginated list of recent activities with timestamps

### Requirement: Notification System
The system SHALL provide in-app notifications for users.

#### Scenario: Get notifications
- **WHEN** authenticated user requests GET /api/v1/notifications
- **THEN** system returns list of notifications for current user

#### Scenario: Mark notification read
- **WHEN** user requests POST /api/v1/notifications/:id/read
- **THEN** system marks notification as read

### Requirement: File Upload Service
The system SHALL allow file uploads for documents and images.

#### Scenario: Upload file
- **WHEN** authenticated user uploads file via POST /api/v1/upload
- **THEN** system stores file and returns file URL and metadata

### Requirement: Settings API
The system SHALL provide user preference settings.

#### Scenario: Get settings
- **WHEN** user requests GET /api/v1/settings
- **THEN** system returns user preferences

#### Scenario: Update settings
- **WHEN** user updates settings via PUT /api/v1/settings
- **THEN** system saves preferences and returns updated settings

### Requirement: Traffic Data Model
The system SHALL store traffic data including flow, incidents, and patterns.

#### Scenario: Traffic data structure
- **GIVEN** the database
- **THEN** traffic_data table exists with id, location, flow_rate, timestamp, vehicle_count, congestion_level, incident_type, coordinates

### Requirement: Traffic API Stub Service
The system SHALL provide mock traffic data simulating government APIs.

#### Scenario: Fetch mock traffic data
- **WHEN** traffic service requests data from stub
- **THEN** stub returns realistic traffic data with flow rates, incidents, timestamps

### Requirement: Traffic Heatmap Generation
The system SHALL generate coordinate-based heatmap data for visualization.

#### Scenario: Get heatmap data
- **WHEN** user requests GET /api/v1/traffic/heatmap with bounds
- **THEN** system returns array of coordinates with intensity values

### Requirement: AI Traffic Insights
The system SHALL provide AI-powered traffic analysis using OpenAI.

#### Scenario: Analyze traffic data
- **WHEN** user requests POST /api/v1/traffic/analyze with traffic data
- **THEN** system returns AI-generated insights about patterns, anomalies, recommendations

### Requirement: Congestion Analysis
The system SHALL calculate and return congestion scores for locations.

#### Scenario: Get congestion score
- **WHEN** user requests GET /api/v1/traffic/congestion
- **THEN** system returns locations with congestion levels (low, medium, high, severe)

### Requirement: Accident Hotspot Detection
The system SHALL identify traffic incident hotspots.

#### Scenario: Get hotspots
- **WHEN** user requests GET /api/v1/traffic/hotspots
- **THEN** system returns locations with high incident frequency and risk scores

### Requirement: Traffic Report Export
The system SHALL export traffic reports in PDF and Excel formats.

#### Scenario: Export PDF report
- **WHEN** user requests GET /api/v1/traffic/export?format=pdf
- **THEN** system generates and returns PDF file with traffic analysis

#### Scenario: Export Excel report
- **WHEN** user requests GET /api/v1/traffic/export?format=excel
- **THEN** system generates and returns Excel file with traffic data

### Requirement: Dashboard UI
The frontend SHALL display a dashboard with metrics widgets and activity feed.

#### Scenario: View dashboard
- **WHEN** authenticated user navigates to /dashboard
- **THEN** page displays metrics cards, system health, recent activity

### Requirement: Navigation Sidebar
The frontend SHALL provide navigation to all modules.

#### Scenario: Navigate modules
- **WHEN** user views sidebar
- **THEN** links to Dashboard, Traffic, Forecasting, Simulation, Sites, Monitoring, Reports, AI Assistant, Admin are visible

### Requirement: Notification Center
The frontend SHALL display notifications in header dropdown.

#### Scenario: View notifications
- **WHEN** user clicks notification bell
- **THEN** dropdown shows recent notifications with unread count

### Requirement: File Upload Component
The frontend SHALL provide drag-drop file upload.

#### Scenario: Upload file via UI
- **WHEN** user drags file to upload area
- **THEN** file uploads with progress indicator and success/error feedback

### Requirement: Settings Page
The frontend SHALL allow users to view and edit preferences.

#### Scenario: Edit settings
- **WHEN** user navigates to settings and changes preferences
- **THEN** settings save and confirmation displays

### Requirement: Traffic Dashboard
The frontend SHALL display traffic analysis interface.

#### Scenario: View traffic module
- **WHEN** user navigates to /traffic
- **THEN** page displays traffic map, stats cards, filters, data table

### Requirement: Interactive Heatmap
The frontend SHALL display interactive traffic heatmap.

#### Scenario: View heatmap
- **WHEN** user views traffic map
- **THEN** Leaflet map displays heatmap overlay with traffic intensity

### Requirement: Traffic Data Table
The frontend SHALL display filterable traffic data grid.

#### Scenario: Filter traffic data
- **WHEN** user applies date range and area filters
- **THEN** table updates with filtered results

### Requirement: AI Insights Panel
The frontend SHALL display AI-generated traffic insights.

#### Scenario: View AI insights
- **WHEN** traffic data is loaded
- **THEN** panel displays AI analysis with key findings and recommendations

### Requirement: Traffic Export UI
The frontend SHALL provide export buttons for reports.

#### Scenario: Export report
- **WHEN** user clicks export button and selects format
- **THEN** file downloads to user's device
