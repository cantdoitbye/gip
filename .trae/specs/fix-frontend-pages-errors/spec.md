# Fix Frontend Pages Errors Spec

## Why
The frontend pages (Forecasting.tsx, Simulation.tsx, Sites.tsx) have syntax errors and type mismatches that prevent the application from compiling and running correctly. These need to be fixed before we can test the complete system.

## What Changes
- Fix JSX syntax errors in Sites.tsx (missing braces, unclosed div tags, broken elements)
- Fix type definitions in Forecasting.tsx to properly use AIForecastResponse type
- Fix type definitions in Simulation.tsx to properly use AIRecommendationResponse type
- Ensure all imports are correctly used

## Impact
- Affected specs: Phase 5-7 Frontend Implementation
- Affected code: 
  - `/frontend/src/pages/Forecasting.tsx`
  - `/frontend/src/pages/Simulation.tsx`
  - `/frontend/src/pages/Sites.tsx`

## ADDED Requirements

### Requirement: JSX Syntax Correctness
All frontend pages SHALL have valid JSX syntax with properly closed tags and correct element structure.

#### Scenario: Sites.tsx renders without errors
- **WHEN** the Sites page is loaded
- **THEN** the page renders correctly with all Cards displaying statistics
- **AND** no JSX syntax errors occur

### Requirement: Type Safety
All frontend pages SHALL use correct TypeScript types from service definitions.

#### Scenario: AI prediction types match service response
- **WHEN** AI prediction or recommendation is called
- **THEN** the response type matches the service-defined interface
- **AND** TypeScript compilation succeeds

## Specific Fixes

### Sites.tsx Fixes
1. Line 139: Add missing `{` before `sites.filter(s => s.status === 'pending').length`
2. Lines 128, 141, 153: Add missing `</div>` closing tags inside Card components
3. Line 157: Fix broken `<div className="overflow-x-auto">` element
4. Add missing `</div>` to close the grid container after the statistics Cards

### Forecasting.tsx Fixes
1. Update `aiResult` state type to use `AIForecastResponse` type from service (or keep inline type but ensure compatibility)

### Simulation.tsx Fixes
1. Update `aiResult` state type to use `AIRecommendationResponse` type from service (or keep inline type but ensure compatibility)
