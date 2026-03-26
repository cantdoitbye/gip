# Tasks

- [ ] Task 1: Fix Sites.tsx JSX syntax errors
  - [ ] SubTask 1.1: Fix line 139 - Add missing `{` before `sites.filter`
  - [ ] SubTask 1.2: Add missing `</div>` closing tags for Card components (lines 128, 141, 153)
  - [ ] SubTask 1.3: Fix broken `<div className="overflow-x-auto">` element on line 157
  - [ ] SubTask 1.4: Add missing `</div>` to close grid container

- [ ] Task 2: Fix Forecasting.tsx type issues
  - [ ] SubTask 2.1: Import `AIForecastResponse` type from forecast service
  - [ ] SubTask 2.2: Update `aiResult` state to use `AIForecastResponse | null` type

- [ ] Task 3: Fix Simulation.tsx type issues
  - [ ] SubTask 3.1: Import `AIRecommendationResponse` type from simulation service
  - [ ] SubTask 3.2: Update `aiResult` state to use `AIRecommendationResponse | null` type

- [ ] Task 4: Verify TypeScript compilation
  - [ ] SubTask 4.1: Run TypeScript compiler to verify no errors

- [ ] Task 5: Test all three pages work correctly
  - [ ] SubTask 5.1: Start frontend dev server
  - [ ] SubTask 5.2: Verify pages load without errors

# Task Dependencies
- [Task 4] depends on [Task 1, Task 2, Task 3]
- [Task 5] depends on [Task 4]
