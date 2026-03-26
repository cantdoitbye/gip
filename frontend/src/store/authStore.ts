import { create } from 'zustand'
import type { User, AuthTokens } from '../types/auth'

interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  login: (tokens: AuthTokens) => void
  logout: () => void
  setUser: (user: User) => void
  setTokens: (tokens: AuthTokens) => void
  initializeAuth: () => Promise<void>
}

const STORAGE_KEYS = {
  ACCESS_TOKEN: 'accessToken',
  REFRESH_TOKEN: 'refreshToken',
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  accessToken: null,
  refreshToken: null,
  isAuthenticated: false,

  login: (tokens: AuthTokens) => {
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, tokens.accessToken)
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, tokens.refreshToken)
    set({
      user: tokens.user,
      accessToken: tokens.accessToken,
      refreshToken: tokens.refreshToken,
      isAuthenticated: true,
    })
  },

  logout: () => {
    localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN)
    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN)
    set({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
    })
  },

  setUser: (user: User) => {
    set({ user })
  },

  setTokens: (tokens: AuthTokens) => {
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, tokens.accessToken)
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, tokens.refreshToken)
    set({
      accessToken: tokens.accessToken,
      refreshToken: tokens.refreshToken,
    })
  },

  initializeAuth: async () => {
    const accessToken = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN)
    const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN)

    if (accessToken && refreshToken) {
      set({
        accessToken,
        refreshToken,
        isAuthenticated: true,
      })
      
      try {
        const { default: authService } = await import('../services/auth')
        const user = await authService.getProfile()
        set({ user })
      } catch (e) {
        localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN)
        localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN)
        set({
           user: null, 
           accessToken: null, 
           refreshToken: null, 
           isAuthenticated: false 
        })
      }
    }
  },
}))
