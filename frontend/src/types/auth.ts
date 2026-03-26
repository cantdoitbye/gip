export type UserRole = 'admin' | 'planner' | 'viewer'

export interface User {
  id: string
  email: string
  fullName: string
  role: UserRole
  isActive: boolean
  createdAt: string
  updatedAt: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  fullName: string
}

export interface AuthTokens {
  accessToken: string
  refreshToken: string
  tokenType: string
  user?: User
}

export interface ApiErrorResponse {
  detail: string
  message?: string
}
