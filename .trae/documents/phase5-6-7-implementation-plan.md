# Phase 5, 6, 7 Implementation Plan - Demo MVP

## Problem Analysis

### Root Cause of Model Failures
The model is repeatedly failing due to **Python syntax errors** in the service file:

1. **Line 78**: `_gather_factors_from_stubs` method is incorrectly indented INSIDE `create_site` method
2. **Line 143**: Invalid condition `if not risks or risks.get("risks"):` - logic error
3. **Line 150-151**: Duplicate return statements causing unreachable code
4. **Line 153-156**: Missing comma between function parameters in `analyze_site`
5. **Line 212**: Invalid for loop syntax `for key, scores:` should be `for key in scores:`

### Why This Keeps Happening
- Large code blocks being written with complex indentation
- F-strings with nested braces causing parsing issues
- Async methods being placed inside other methods
- Missing basic Python syntax (commas, colons)

---

## Implementation Plan

### Phase A: Fix Backend Syntax Errors (Priority: CRITICAL)

#### Task A1: Rewrite site_analysis.py Service
- Fix all indentation issues
- Fix missing comma in function definition
- Fix for loop syntax
- Fix logic error in risk calculation
- Remove duplicate return statements

#### Task A2: Update main.py
- Import sites router
- Include sites router in app

### Phase B: Complete Backend Verification

#### Task B1: Verify All Routers
- Check forecasts router
- Check simulations router  
- Check sites router
- Verify all imports work

#### Task B2: Verify All Stub Services
- GIS API stub
- Population API stub
- Economic API stub
- Land Use API stub

### Phase C: Complete Frontend Services

#### Task C1: Create Site Service
- Create `/frontend/src/services/site.ts`
- CRUD operations for sites
- AI analysis endpoint

#### Task C2: Verify Forecast & Simulation Services
- Already created, verify they work

### Phase D: Create Frontend Pages (Demo MVP)

#### Task D1: Site Analysis Page
- List sites with scores
- Create new site form
- View site analysis details
- AI analysis feature

#### Task D2: Forecast Page  
- List forecasts
- Create forecast
- View forecast results

#### Task D3: Simulation Page
- List simulations
- Create simulation scenario
- Run simulation
- View results

#### Task D4: Update Navigation
- Add routes for new pages
- Update sidebar menu

### Phase E: Integration Testing

#### Task E1: Test Backend Endpoints
- Run backend server
- Test all API endpoints with curl/Postman

#### Task E2: Test Frontend Integration
- Run frontend dev server
- Test all pages load correctly
- Test API calls work

---

## File Changes Summary

### Files to Fix
1. `/backend/app/services/site_analysis.py` - Rewrite with correct syntax
2. `/backend/app/main.py` - Add sites router

### Files to Create
1. `/frontend/src/services/site.ts` - Site API service

### Files to Create (Frontend Pages)
1. `/frontend/src/pages/SitesPage.tsx` - Site listing and management
2. `/frontend/src/pages/ForecastsPage.tsx` - Traffic forecasting
3. `/frontend/src/pages/SimulationsPage.tsx` - Infrastructure simulation

### Files to Update
1. `/frontend/src/App.tsx` - Add routes
2. `/frontend/src/components/Sidebar.tsx` - Add navigation items

---

## Stub Services Status (All Complete)
- ✅ `/backend/app/stubs/gis_api.py` - Terrain, risk, environmental data
- ✅ `/backend/app/stubs/population_api.py` - Census/demographic data
- ✅ `/backend/app/stubs/economic_api.py` - Economic indicators
- ✅ `/backend/app/stubs/land_use_api.py` - Land registry data

## Backend Models Status (All Complete)
- ✅ `/backend/app/models/forecast.py` - Forecast models
- ✅ `/backend/app/models/simulation.py` - Simulation models
- ✅ `/backend/app/models/site.py` - Site analysis models

## Backend Routers Status (All Complete)
- ✅ `/backend/app/routers/forecasts.py` - Forecast endpoints
- ✅ `/backend/app/routers/simulations.py` - Simulation endpoints
- ✅ `/backend/app/routers/sites.py` - Site endpoints

---

## Key Principle
**Write smaller, simpler code. Avoid complex nested structures. Test incrementally.**

## Estimated Tasks
1. Fix site_analysis.py syntax - 1 task
2. Update main.py - 1 task
3. Create site.ts service - 1 task
4. Create SitesPage.tsx - 1 task
5. Create ForecastsPage.tsx - 1 task
6. Create SimulationsPage.tsx - 1 task
7. Update App.tsx routes - 1 task
8. Update Sidebar navigation - 1 task
9. Test backend - 1 task
10. Test frontend - 1 task

**Total: 10 tasks**

---

## User Requirements Recap
> "Create a demo level MVP with all features from plan PDFs with stubs for any government or paid API requirement"

This means:
- All features must be functional
- External APIs are stubbed (already done)
- OpenAI integration for AI features (already implemented)
- Full frontend pages for demo purposes
