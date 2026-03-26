# Tasks - Phase 2: Authentication & User Management

## Backend Tasks

- [ ] Task 1: Create User model
  - [ ] Task 1.1: Create app/models/user.py with User SQLAlchemy model (id, email, hashed_password, full_name, role, is_active, created_at, updated_at)
  - [ ] Task 1.2: Create UserRole enum in app/models/user.py
  - [ ] Task 1.3: Add User import to app/models/__init__.py

- [ ] Task 2: Create user schemas
  - [ ] Task 2.1: Create app/schemas/user.py with UserCreate, UserUpdate, UserResponse, UserLogin schemas
  - [ ] Task 2.2: Create app/schemas/auth.py with Token, TokenPayload, LoginRequest, RegisterRequest schemas
  - [ ] Task 2.3: Add schema imports to app/schemas/__init__.py

- [ ] Task 3: Implement password utilities
  - [ ] Task 3.1: Create app/utils/security.py with hash_password, verify_password functions using bcrypt

- [ ] Task 4: Implement JWT utilities
  - [ ] Task 4.1: Create app/utils/jwt.py with create_access_token, create_refresh_token, decode_token functions
  - [ ] Task 4.2: Add token blacklist handling in Redis

- [ ] Task 5: Create auth service
  - [ ] Task 5.1: Create app/services/auth.py with register_user, authenticate_user, create_tokens, refresh_tokens, logout_user functions

- [ ] Task 6: Create auth middleware
  - [ ] Task 6.1: Create app/middleware/auth.py with get_current_user dependency
  - [ ] Task 6.2: Create require_role decorator for RBAC

- [ ] Task 7: Create auth router
  - [ ] Task 7.1: Create app/routers/auth.py with POST /register endpoint
  - [ ] Task 7.2: Add POST /login endpoint
  - [ ] Task 7.3: Add POST /refresh endpoint
  - [ ] Task 7.4: Add POST /logout endpoint
  - [ ] Task 7.5: Wire auth router to main.py

- [ ] Task 8: Create users router
  - [ ] Task 8.1: Create app/routers/users.py with GET / (list users, admin only)
  - [ ] Task 8.2: Add GET /me endpoint (current user profile)
  - [ ] Task 8.3: Add PUT /me endpoint (update own profile)
  - [ ] Task 8.4: Add GET /:id endpoint (get user by ID)
  - [ ] Task 8.5: Add PUT /:id endpoint (update user, admin or self)
  - [ ] Task 8.6: Add DELETE /:id endpoint (deactivate user, admin only)
  - [ ] Task 8.7: Wire users router to main.py

- [ ] Task 9: Create audit log model and service
  - [ ] Task 9.1: Create app/models/audit.py with AuditLog model
  - [ ] Task 9.2: Create app/services/audit.py with log_action function
  - [ ] Task 9.3: Integrate audit logging into auth endpoints

- [ ] Task 10: Create database migration
  - [ ] Task 10.1: Generate Alembic migration for users and audit_logs tables
  - [ ] Task 10.2: Run migration to create tables

## Frontend Tasks

- [ ] Task 11: Create auth types
  - [ ] Task 11.1: Create src/types/auth.ts with User, LoginCredentials, RegisterData, AuthTokens interfaces
  - [ ] Task 11.2: Add UserRole type

- [ ] Task 12: Create auth service
  - [ ] Task 12.1: Create src/services/auth.ts with login, register, logout, refreshTokens, getProfile functions
  - [ ] Task 12.2: Add updateProfile function

- [ ] Task 13: Create auth store
  - [ ] Task 13.1: Create src/store/authStore.ts with user, tokens, isAuthenticated state
  - [ ] Task 13.2: Add login, logout, setUser actions
  - [ ] Task 13.3: Implement token persistence in localStorage

- [ ] Task 14: Update API client for auth
  - [ ] Task 14.1: Update src/services/api.ts to attach Authorization header
  - [ ] Task 14.2: Add response interceptor for 401 handling
  - [ ] Task 14.3: Implement automatic token refresh

- [ ] Task 15: Create protected route component
  - [ ] Task 15.1: Create src/components/auth/ProtectedRoute.tsx with auth check
  - [ ] Task 15.2: Add role-based route protection

- [ ] Task 16: Wire login page
  - [ ] Task 16.1: Update src/pages/Login.tsx to call auth service
  - [ ] Task 16.2: Add form submission handling
  - [ ] Task 16.3: Add error display and loading states
  - [ ] Task 16.4: Add redirect after successful login

- [ ] Task 17: Wire register page
  - [ ] Task 17.1: Update src/pages/Register.tsx to call auth service
  - [ ] Task 17.2: Add form submission handling
  - [ ] Task 17.3: Add auto-login after registration

- [ ] Task 18: Wire forgot password page
  - [ ] Task 18.1: Update src/pages/ForgotPassword.tsx with placeholder functionality

- [ ] Task 19: Create profile page
  - [ ] Task 19.1: Create src/pages/Profile.tsx with user info display
  - [ ] Task 19.2: Add profile edit form

- [ ] Task 20: Create user management page (admin)
  - [ ] Task 20.1: Create src/pages/UserManagement.tsx with user list table
  - [ ] Task 20.2: Add user edit modal
  - [ ] Task 20.3: Add user role change functionality
  - [ ] Task 20.4: Add user deactivation

- [ ] Task 21: Update App routing
  - [ ] Task 21.1: Update src/App.tsx with protected routes
  - [ ] Task 21.2: Add /profile and /admin/users routes
  - [ ] Task 21.3: Wrap protected routes with ProtectedRoute component

- [ ] Task 22: Update Header with user menu
  - [ ] Task 22.1: Update src/components/layout/Header.tsx with user dropdown
  - [ ] Task 22.2: Add logout functionality
  - [ ] Task 22.3: Add profile link

## Task Dependencies
- Task 2 depends on Task 1
- Task 3, Task 4 can run in parallel
- Task 5 depends on Task 3, Task 4
- Task 6 depends on Task 4
- Task 7 depends on Task 5, Task 6
- Task 8 depends on Task 1, Task 6
- Task 9 depends on Task 1
- Task 10 depends on Task 1, Task 9
- Task 12 depends on Task 11
- Task 13 depends on Task 11, Task 12
- Task 14 depends on Task 12, Task 13
- Task 15 depends on Task 13
- Task 16, Task 17, Task 18 can run in parallel after Task 12, Task 13
- Task 19 depends on Task 13
- Task 20 depends on Task 12, Task 13
- Task 21 depends on Task 15, Task 19, Task 20
- Task 22 depends on Task 13

## Parallelizable Work
- Backend Tasks 3 & 4 (password & JWT utils) can run in parallel
- Frontend Tasks 11, 12, 13 can run in parallel with Backend Tasks 1-10
- Frontend Tasks 16, 17, 18 (login/register/forgot password wiring) can run in parallel
