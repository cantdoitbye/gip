import { api } from './api'

export interface HealthResponse {
  status: string
  version: string
}

export interface DetailedHealthResponse {
  status: string
  version: string
  services: {
    database: string
    redis: string
  }
}

interface BackendDetailedHealth {
  status: string
  version: string
  services: {
    database: string
    redis: string
  }
}

export const healthService = {
  async checkHealth(): Promise<HealthResponse> {
    const response = await api.get<HealthResponse>('/health')
    return response.data
  },

  async checkDetailedHealth(): Promise<DetailedHealthResponse> {
    const response = await api.get<BackendDetailedHealth>('/health/detailed')
    return {
      status: response.data.status,
      version: response.data.version,
      services: {
        database: response.data.services?.database || 'unhealthy',
        redis: response.data.services?.redis || 'unhealthy',
      },
    }
  },
}

export default healthService
