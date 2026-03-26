import { api } from './api'
import type { User, LoginCredentials, RegisterData, AuthTokens } from '../types/auth'

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthTokens> {
    const response = await api.post<any>('/auth/login', credentials)
    const tokens = {
      accessToken: response.data.access_token,
      refreshToken: response.data.refresh_token,
      tokenType: response.data.token_type,
    }
    
    // Set headers temporarily to fetch profile
    localStorage.setItem('accessToken', tokens.accessToken)
    api.defaults.headers.common.Authorization = `Bearer ${tokens.accessToken}`
    
    try {
      const userResponse = await api.get<User>('/users/me')
      return { ...tokens, user: userResponse.data }
    } catch (e) {
      localStorage.removeItem('accessToken')
      delete api.defaults.headers.common.Authorization
      throw e
    }
  },

  async register(data: RegisterData): Promise<AuthTokens> {
    const response = await api.post<any>('/auth/register', data)
    const tokens = {
      accessToken: response.data.access_token,
      refreshToken: response.data.refresh_token,
      tokenType: response.data.token_type,
    }
    
    localStorage.setItem('accessToken', tokens.accessToken)
    api.defaults.headers.common.Authorization = `Bearer ${tokens.accessToken}`
    
    try {
      const userResponse = await api.get<User>('/users/me')
      return { ...tokens, user: userResponse.data }
    } catch (e) {
      localStorage.removeItem('accessToken')
      delete api.defaults.headers.common.Authorization
      throw e
    }
  },

  async logout(): Promise<void> {
    await api.post('/auth/logout')
  },

  async refreshTokens(refreshToken: string): Promise<AuthTokens> {
    const response = await api.post<any>('/auth/refresh', { refreshToken })
    return {
      accessToken: response.data.access_token,
      refreshToken: response.data.refresh_token,
      tokenType: response.data.token_type,
    }
  },

  async getProfile(): Promise<User> {
    const response = await api.get<User>('/users/me')
    return response.data
  },

  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await api.patch<User>('/users/me', data)
    return response.data
  },

  async getAllUsers(params?: { search?: string; page?: number; limit?: number }): Promise<{ users: User[]; total: number }> {
    const response = await api.get<{ users: User[]; total: number }>('/users', { params })
    return response.data
  },

  async updateUser(userId: string, data: Partial<User>): Promise<User> {
    const response = await api.patch<User>(`/users/${userId}`, data)
    return response.data
  },

  async deactivateUser(userId: string): Promise<User> {
    const response = await api.patch<User>(`/users/${userId}/deactivate`)
    return response.data
  },

  async activateUser(userId: string): Promise<User> {
    const response = await api.patch<User>(`/users/${userId}/activate`)
    return response.data
  },
}

export default authService
