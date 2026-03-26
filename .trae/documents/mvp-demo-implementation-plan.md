# MVP Demo Implementation Plan - AI Infrastructure Planning System

## Goal
Make all features work without errors using stub data (no real government APIs).

## Current Status

### Working
- Backend API with all routers (traffic, forecasts, simulations, sites, etc.)
- Frontend routing and layout
- Authentication flow
- Dashboard page
- Sites page (partial)
- Forecasting page (partial)
- Simulation page (partial)

### Needs Work (Placeholders showing "coming soon")
1. **Traffic page** - Static data, needs real API integration + map
2. **Monitoring page** - Static data, needs real metrics
3. **Reports page** - Static data, needs export functionality
4. **AI Assistant page** - Placeholder chat interface

---

## Implementation Tasks

### Phase 1: Fix Traffic Page
- [ ] Connect to `/traffic/data` API
- [ ] Connect to `/traffic/heatmap` API
- [ ] Connect to `/traffic/congestion` API
- [ ] Add traffic data table with pagination
- [ ] Add congestion indicators
- [ ] Add export buttons (PDF/Excel)

### Phase 2: Fix Monitoring Page
- [ ] Connect to `/health/detailed` API for system status
- [ ] Create monitoring service for project tracking
- [ ] Add mock project data
- [ ] Display alerts from notifications API

### Phase 3: Fix Reports Page
- [ ] Create report generation UI
- [ ] Connect to traffic/export endpoint
- [ ] Add forecast report generation
- [ ] Add site analysis report generation

### Phase 4: Fix AI Assistant Page
- [ ] Create chat interface component
- [ ] Connect to `/simulations/recommend` API
- [ ] Add context-aware AI queries
- [ ] Display AI responses

### Phase 5: Verify All Endpoints
- [ ] Test all API endpoints return data
- [ ] Test all frontend pages load without errors
- [ ] Test all CRUD operations work

---

## Files to Modify

### Frontend Pages
1. `frontend/src/pages/Traffic.tsx` - Full implementation
2. `frontend/src/pages/Monitoring.tsx` - Add real data
3. `frontend/src/pages/Reports.tsx` - Add export functionality
4. `frontend/src/pages/AiAssistant.tsx` - Add chat interface

### Frontend Services (may need updates)
1. `frontend/src/services/traffic.ts` - Ensure all endpoints covered
2. `frontend/src/services/monitoring.ts` - Create if missing

### Backend (if needed)
1. `backend/app/routers/monitoring.py` - Create if missing
2. `backend/app/services/monitoring.py` - Create if missing

---

## Success Criteria
- All pages load without "coming soon" messages
- All API calls return data (from stubs)
- Export buttons generate files
- AI Assistant responds to queries
- No console errors
