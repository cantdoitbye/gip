# Phase 2: Authentication & User Management Spec

## Why
The AI-Powered Infrastructure Planning System requires a secure authentication system to control access to sensitive infrastructure data. Users need to be authenticated with role-based permissions to ensure only authorized personnel can access, planning, monitoring, and administrative features.

## What Changes
- Create User model with SQLAlchemy for PostgreSQL
- Implement JWT-based authentication with access and refresh tokens
- Add role-based access control (RBAC) with Admin, Planner, and Viewer roles
- Create password hashing using bcrypt
- Implement session management with token refresh and logout
- Build User CRUD APIs for user management
- Add audit logging for user actions
- Wire frontend login/register pages to backend APIs
- Implement protected routes with auth guards
- Create user profile and user management UI

## Impact
- Affected specs: Depends on Phase 1 Foundation
- Affected code: 
  - Backend: app/models/user.py, app/routers/auth.py, app/routers/users.py, app/services/auth.py, app/middleware/auth.py
  - Frontend: src/pages/Login.tsx, src/pages/Register.tsx, src/store/authStore.ts, src/services/auth.ts

---

## ADDED Requirements

### Requirement: User Model
The system SHALL have a User model with the following fields:
- id: UUID primary key
- email: unique string, indexed
- hashed_password: string
- full_name: string
- role: enum (admin, planner, viewer)
- is_active: boolean, default true
- created_at: datetime
- updated_at: datetime

#### Scenario: User created in database
- **WHEN** a new user registers
- **THEN** user record is created with hashed password
- **AND** default role is "viewer"

### Requirement: JWT Authentication
The system SHALL implement JWT-based authentication:
- Access tokens expire in 30 minutes
- Refresh tokens expire in 7 days
- Tokens signed with SECRET_KEY from environment
- Token payload includes: user_id, email, role

#### Scenario: User logs in successfully
- **WHEN** user submits valid email and password
- **THEN** access_token and refresh_token are returned
- **AND** response code is 200

#### Scenario: User login fails with invalid credentials
- **WHEN** user submits invalid email or password
- **THEN** error message "Invalid credentials" is returned
- **AND** response code is 401

### Requirement: Role-Based Access Control
The system SHALL enforce role-based permissions:
- admin: Full access to all features including user management
- planner: Access to planning modules (traffic, forecasting, simulation, site analysis)
- viewer: Read-only access to view dashboards and reports

#### Scenario: Admin accesses user management
- **WHEN** user with admin role calls GET /api/v1/users
- **THEN** list of all users is returned

#### Scenario: Non-admin denied user management
- **WHEN** user with planner or viewer role calls GET /api/v1/users
- **THEN** 403 Forbidden is returned

### Requirement: Password Security
The system SHALL securely handle passwords:
- Passwords hashed using bcrypt with salt
- Minimum password length of 8 characters
- Password never returned in API responses

#### Scenario: Password stored securely
- **WHEN** user registers with password "myPassword123"
- **THEN** only bcrypt hash is stored in database
- **AND** plain text password is never logged or stored

### Requirement: Token Refresh
The system SHALL support token refresh:
- POST /api/v1/auth/refresh accepts refresh_token
- Returns new access_token and refresh_token
- Old refresh_token is invalidated

#### Scenario: Token refresh succeeds
- **WHEN** valid refresh_token is submitted
- **THEN** new token pair is returned
- **AND** old refresh_token cannot be reused

### Requirement: User Registration
The system SHALL allow user registration:
- POST /api/v1/auth/register with email, password, full_name
- Email must be unique
- Password validated for minimum requirements

#### Scenario: Registration succeeds
- **WHEN** unique email and valid password submitted
- **THEN** user is created with viewer role
- **AND** tokens are returned for immediate login

### Requirement: Logout
The system SHALL support logout:
- POST /api/v1/auth/logout invalidates current session
- Refresh token is blacklisted

#### Scenario: Logout succeeds
- **WHEN** authenticated user calls logout
- **THEN** refresh_token is invalidated
- **AND** user cannot refresh tokens

### Requirement: User CRUD Operations
The system SHALL provide user management APIs:
- GET /api/v1/users - List users (admin only)
- GET /api/v1/users/:id - Get user details (admin or self)
- PUT /api/v1/users/:id - Update user (admin or self)
- DELETE /api/v1/users/:id - Deactivate user (admin only)

#### Scenario: Admin lists users
- **WHEN** admin calls GET /api/v1/users
- **THEN** paginated list of users is returned
- **AND** passwords are not included

### Requirement: Current User Profile
The system SHALL provide profile endpoints:
- GET /api/v1/users/me - Get current user profile
- PUT /api/v1/users/me - Update own profile

#### Scenario: User views own profile
- **WHEN** authenticated user calls GET /api/v1/users/me
- **THEN** user details are returned without password

### Requirement: Audit Logging
The system SHALL log user actions:
- Login attempts (success/failure)
- User creation/modification
- Role changes
- Authentication failures

#### Scenario: Login audit logged
- **WHEN** user attempts login
- **THEN** audit entry created with timestamp, email, IP, success/failure

### Requirement: Frontend Login Flow
The frontend SHALL implement complete login flow:
- Login form calls POST /api/v1/auth/login
- Tokens stored securely (httpOnly cookie or localStorage)
- Protected routes check authentication
- Auto-refresh tokens before expiry

#### Scenario: User logs in via UI
- **WHEN** user enters credentials and submits
- **THEN** API is called
- **AND** on success, redirected to dashboard
- **AND** on failure, error message displayed

### Requirement: Frontend Registration Flow
The frontend SHALL implement registration flow:
- Registration form calls POST /api/v1/auth/register
- Validation errors displayed inline
- Auto-login after successful registration

#### Scenario: User registers via UI
- **WHEN** user fills registration form and submits
- **THEN** API is called
- **AND** on success, redirected to dashboard

### Requirement: Protected Routes
The frontend SHALL protect routes:
- Unauthenticated users redirected to login
- Role-based route protection
- Current route preserved for post-login redirect

#### Scenario: Unauthenticated access blocked
- **WHEN** unauthenticated user navigates to /dashboard
- **THEN** redirected to /login
- **AND** redirect_to parameter set

### Requirement: User Management UI
The frontend SHALL provide admin user management:
- User list table with search and pagination
- User detail/edit modal
- Role change functionality
- User deactivation

#### Scenario: Admin views user list
- **WHEN** admin navigates to /admin/users
- **THEN** table of users is displayed
- **AND** edit/deactivate actions available
