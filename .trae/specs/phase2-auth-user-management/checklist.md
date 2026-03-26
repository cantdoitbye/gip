# Checklist - Phase 2: Authentication & User Management

## Backend Checklist

- [ ] User model exists with all required fields (id, email, hashed_password, full_name, role, is_active, created_at, updated_at)
- [ ] UserRole enum defined (admin, planner, viewer)
- [ ] User schemas created (UserCreate, UserUpdate, UserResponse, UserLogin)
- [ ] Auth schemas created (Token, TokenPayload, LoginRequest, RegisterRequest)
- [ ] Password hashing implemented with bcrypt
- [ ] JWT token creation functions exist
- [ ] JWT token validation/decoding works
- [ ] Token blacklist in Redis implemented
- [ ] Auth service with register, login, logout, refresh functions
- [ ] get_current_user dependency works
- [ ] require_role decorator enforces RBAC
- [ ] POST /api/v1/auth/register returns tokens
- [ ] POST /api/v1/auth/login returns tokens on success
- [ ] POST /api/v1/auth/login returns 401 on invalid credentials
- [ ] POST /api/v1/auth/refresh returns new tokens
- [ ] POST /api/v1/auth/logout invalidates tokens
- [ ] GET /api/v1/users returns paginated user list (admin only)
- [ ] GET /api/v1/users/me returns current user
- [ ] PUT /api/v1/users/me updates own profile
- [ ] GET /api/v1/users/:id returns user details
- [ ] PUT /api/v1/users/:id updates user (admin or self)
- [ ] DELETE /api/v1/users/:id deactivates user (admin only)
- [ ] AuditLog model exists
- [ ] Audit logging integrated into auth endpoints
- [ ] Database migration created and applied

## Frontend Checklist

- [ ] Auth types defined (User, LoginCredentials, RegisterData, AuthTokens)
- [ ] Auth service with login, register, logout, refresh functions
- [ ] Auth store with user, tokens, isAuthenticated state
- [ ] Token persistence in localStorage
- [ ] API client attaches Authorization header
- [ ] API client handles 401 responses
- [ ] Automatic token refresh implemented
- [ ] ProtectedRoute component created
- [ ] Role-based route protection works
- [ ] Login page calls auth API
- [ ] Login page shows errors
- [ ] Login page redirects after success
- [ ] Register page calls auth API
- [ ] Register page auto-logins after success
- [ ] ForgotPassword page has placeholder
- [ ] Profile page displays user info
- [ ] Profile page allows editing
- [ ] UserManagement page shows user list (admin)
- [ ] User edit modal works
- [ ] Role change functionality works
- [ ] User deactivation works
- [ ] Protected routes in App.tsx
- [ ] /profile route added
- [ ] /admin/users route added
- [ ] Header shows user dropdown
- [ ] Logout works from header
- [ ] Profile link in header

## Integration Checklist

- [ ] Login flow works end-to-end
- [ ] Registration flow works end-to-end
- [ ] Token refresh works automatically
- [ ] Logout invalidates session
- [ ] Admin can view users
- [ ] Admin can change roles
- [ ] Admin can deactivate users
- [ ] Non-admin cannot access user management
- [ ] Protected routes redirect to login when unauthenticated
