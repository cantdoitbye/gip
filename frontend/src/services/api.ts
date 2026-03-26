import axios, { type AxiosError, type InternalAxiosRequestConfig } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

let isRefreshing = false
let failedQueue: Array<{
  resolve: (token: string) => void
  reject: (error: Error) => void
}> = []

const processQueue = (error: Error | null, token: string | null = null) => {
  failedQueue.forEach((promise) => {
    if (error) {
      promise.reject(error)
    } else if (token) {
      promise.resolve(token)
    }
  })
  failedQueue = []
}

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean }

    if (error.response) {
      const { status, data } = error.response
      const message = (data as { detail?: string; message?: string })?.detail || 
                      (data as { detail?: string; message?: string })?.message || 
                      'An error occurred'

      if (status === 401 && originalRequest && !originalRequest._retry) {
        if (isRefreshing) {
          return new Promise((resolve, reject) => {
            failedQueue.push({ resolve, reject })
          })
            .then((token) => {
              originalRequest.headers.Authorization = `Bearer ${token}`
              return api(originalRequest)
            })
            .catch((err) => Promise.reject(err))
        }

        originalRequest._retry = true
        isRefreshing = true

        const refreshToken = localStorage.getItem('refreshToken')

        if (!refreshToken) {
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
          window.location.href = '/login'
          return Promise.reject(new Error('No refresh token available'))
        }

        try {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refreshToken,
          })

          const { accessToken, refreshToken: newRefreshToken } = response.data
          localStorage.setItem('accessToken', accessToken)
          localStorage.setItem('refreshToken', newRefreshToken)
          
          api.defaults.headers.common.Authorization = `Bearer ${accessToken}`
          originalRequest.headers.Authorization = `Bearer ${accessToken}`
          
          processQueue(null, accessToken)
          
          return api(originalRequest)
        } catch (refreshError) {
          processQueue(refreshError as Error, null)
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
          window.location.href = '/login'
          return Promise.reject(refreshError)
        } finally {
          isRefreshing = false
        }
      }

      return Promise.reject(new Error(message))
    }

    if (error.request) {
      return Promise.reject(new Error('Network error. Please check your connection.'))
    }

    return Promise.reject(error)
  }
)

export default api
