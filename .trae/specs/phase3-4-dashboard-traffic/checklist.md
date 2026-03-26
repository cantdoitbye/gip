# Checklist - Phase 3 & 4: Dashboard & Traffic Analysis

## Phase 3: Backend Checklist

- [ ] Dashboard router exists at /api/v1/dashboard
- [ ] GET /api/v1/dashboard/metrics returns summary statistics
- [ ] GET /api/v1/dashboard/activity returns recent actions
- [ ] Notification model exists with required fields
- [ ] GET /api/v1/notifications returns user notifications
- [ ] POST /api/v1/notifications creates new notification
- [ ] PUT /api/v1/notifications/:id/read marks as read
- [ ] File upload endpoint accepts valid files
- [ ] File upload rejects invalid types/sizes
- [ ] Uploaded files are accessible via static URL
- [ ] Settings model or fields exist
- [ ] GET /api/v1/settings returns user preferences
- [ ] PUT /api/v1/settings updates user preferences
- [ ] Database migration includes notifications table

## Phase 3: Frontend Checklist

- [ ] Dashboard page displays metrics cards
- [ ] Dashboard page shows activity feed
- [ ] Dashboard connects to metrics API
- [ ] Dashboard shows loading states
- [ ] Notification bell in header displays unread count
- [ ] Notification dropdown shows recent notifications
- [ ] Mark as read works in notification dropdown
- [ ] FileUpload component accepts drag-drop
- [ ] FileUpload shows upload progress
- [ ] FileUpload handles errors gracefully
- [ ] Settings page displays user preferences
- [ ] Settings page saves changes successfully
- [ ] Sidebar has all module navigation links
- [ ] Sidebar highlights active route

## Phase 4: Backend Checklist

- [ ] TrafficData model exists with location, flow, timestamp fields
- [ ] TrafficIncident model exists with type, severity, coordinates
- [ ] TrafficPattern model exists for historical data
- [ ] Traffic schemas created (Create, Response, Filter)
- [ ] HeatmapPoint schema defined
- [ ] CongestionScore schema defined
- [ ] Hotspot schema with risk assessment
- [ ] Traffic API stub generates realistic mock data
- [ ] GET /api/v1/traffic/data returns filtered traffic data
- [ ] GET /api/v1/traffic/heatmap returns coordinate array with intensity
- [ ] GET /api/v1/traffic/congestion returns congestion levels
- [ ] GET /api/v1/traffic/hotspots returns incident hotspots
- [ ] POST /api/v1/traffic/analyze returns AI-generated insights
- [ ] GET /api/v1/traffic/export generates PDF report
- [ ] GET /api/v1/traffic/export?format=xlsx generates Excel report
- [ ] Congestion scoring algorithm works correctly
- [ ] Hotspot detection identifies high-risk areas
- [ ] AI analysis uses OpenAI API
- [ ] AI insights include confidence scores
- [ ] Database migration includes traffic tables
- [ ] Spatial indexes exist for GIS queries

## Phase 4: Frontend Checklist

- [ ] Traffic types defined in types/traffic.ts
- [ ] Traffic service calls all traffic endpoints
- [ ] Traffic page displays stats cards
- [ ] Traffic page has filter controls (date, area, type)
- [ ] Map component displays with Leaflet
- [ ] Heatmap layer shows traffic intensity
- [ ] Incident markers display on map
- [ ] Incident popups show details
- [ ] Traffic data table displays with pagination
- [ ] Table sorting works
- [ ] Table filtering works
- [ ] Congestion visualizer shows color-coded levels
- [ ] Congestion legend displays
- [ ] AI insights panel displays analysis
- [ ] AI insights show confidence scores
- [ ] Refresh analysis button works
- [ ] PDF export downloads file
- [ ] Excel export downloads file
- [ ] Export shows progress indicator
- [ ] All filters apply to map, table, and insights

## Integration Checklist

- [ ] Dashboard metrics load after login
- [ ] Notifications appear for relevant events
- [ ] Traffic page requires authentication
- [ ] Traffic data loads from API
- [ ] Heatmap renders on map
- [ ] AI analysis returns meaningful insights
- [ ] Export generates valid files
- [ ] Settings persist across sessions
- [ ] File uploads are associated with user
