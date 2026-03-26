export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  FORGOT_PASSWORD: '/forgot-password',
  DASHBOARD: '/dashboard',
  TRAFFIC: '/traffic',
  FORECASTING: '/forecasting',
  SIMULATION: '/simulation',
  SITES: '/sites',
  MONITORING: '/monitoring',
  REPORTS: '/reports',
  AI_ASSISTANT: '/ai-assistant',
  ADMIN: '/admin',
  PROFILE: '/profile',
  USER_MANAGEMENT: '/admin/users',
} as const

export type RouteKey = keyof typeof ROUTES
export type RoutePath = (typeof ROUTES)[RouteKey]
