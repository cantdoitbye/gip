import api from './api'

export interface ForecastFactor {
  id: string
  forecast_id: string
  factor_name: string
  factor_type: string
  current_value: number
  projected_value: number | null
  weight: number
  growth_rate: number | null
  unit: string | null
  source: string | null
  created_at: string
  updated_at: string
}

export interface ForecastScenario {
  id: string
  forecast_id: string
  name: string
  scenario_type: string
  description: string | null
  adjustments: Record<string, unknown> | null
  predicted_volume: number | null
  predicted_growth: number | null
  demand_gap: number | null
  confidence: number | null
  created_at: string
  updated_at: string
}

export interface Forecast {
  id: string
  name: string
  description: string | null
  forecast_type: string
  status: string
  location_name: string
  latitude: number
  longitude: number
  start_year: number
  end_year: number
  base_traffic_volume: number
  predicted_traffic_volume: number | null
  growth_rate: number | null
  confidence_score: number | null
  demand_capacity_gap: number | null
  road_capacity: number | null
  ai_insights: string | null
  created_by: string | null
  created_at: string
  updated_at: string
  factors: ForecastFactor[]
  scenarios: ForecastScenario[]
}

export interface ForecastListResponse {
  forecasts: Forecast[]
  total: number
  page: number
  page_size: number
}

export interface ForecastCreate {
  name: string
  description?: string
  forecast_type?: string
  location_name: string
  latitude: number
  longitude: number
  start_year: number
  end_year: number
  base_traffic_volume: number
  road_capacity?: number
  factors?: {
    factor_name: string
    factor_type: string
    current_value: number
    projected_value?: number
    weight?: number
    growth_rate?: number
    unit?: string
    source?: string
  }[]
}

export interface AIForecastRequest {
  location_name: string
  latitude: number
  longitude: number
  base_year: number
  target_year: number
  base_traffic_volume: number
  road_capacity?: number
  additional_factors?: Record<string, unknown>
}

export interface AIForecastResponse {
  forecast_id: string | null
  location_name: string
  predicted_traffic_volume: number
  growth_rate: number
  confidence_score: number
  demand_capacity_gap: number | null
  key_factors: {
    name: string
    type: string
    current_value: number
    projected_value: number
    growth_rate: number
    weight: number
  }[]
  ai_insights: string
  recommendations: string[]
  yearly_projections: {
    year: number
    volume: number
    growth_from_base: number
  }[]
}

export interface DemandCapacityGapResponse {
  forecast_id: string
  location_name: string
  base_year: number
  target_year: number
  current_capacity: number
  current_demand: number
  projected_demand: number
  demand_capacity_gap: number
  gap_percentage: number
  capacity_utilization: number
  recommended_capacity_increase: number
  priority: string
}

export interface TrendAnalysisResponse {
  location_name: string
  period_start: number
  period_end: number
  data_points: {
    year: number
    traffic_volume: number
    population?: number
    vehicle_count?: number
  }[]
  trend_direction: string
  average_growth_rate: number
  volatility: number
  seasonality_detected: boolean
  forecast_adjustment_recommended: number
}

export const forecastService = {
  async listForecasts(params: {
    page?: number
    page_size?: number
    location?: string
    status?: string
  } = {}): Promise<ForecastListResponse> {
    const response = await api.get('/forecasts', { params })
    return response.data
  },

  async createForecast(data: ForecastCreate): Promise<Forecast> {
    const response = await api.post('/forecasts', data)
    return response.data
  },

  async getForecast(id: string): Promise<Forecast> {
    const response = await api.get(`/forecasts/${id}`)
    return response.data
  },

  async updateForecast(id: string, data: Partial<ForecastCreate>): Promise<Forecast> {
    const response = await api.put(`/forecasts/${id}`, data)
    return response.data
  },

  async deleteForecast(id: string): Promise<void> {
    await api.delete(`/forecasts/${id}`)
  },

  async runForecast(id: string): Promise<Forecast> {
    const response = await api.post(`/forecasts/${id}/run`)
    return response.data
  },

  async getDemandCapacityGap(id: string): Promise<DemandCapacityGapResponse> {
    const response = await api.get(`/forecasts/${id}/gap`)
    return response.data
  },

  async getForecastFactors(id: string): Promise<ForecastFactor[]> {
    const response = await api.get(`/forecasts/${id}/factors`)
    return response.data
  },

  async getForecastScenarios(id: string): Promise<ForecastScenario[]> {
    const response = await api.get(`/forecasts/${id}/scenarios`)
    return response.data
  },

  async getTrendAnalysis(location: string, startYear: number, endYear: number): Promise<TrendAnalysisResponse> {
    const response = await api.get('/forecasts/trends', {
      params: { location, start_year: startYear, end_year: endYear }
    })
    return response.data
  },

  async aiPredict(data: AIForecastRequest): Promise<AIForecastResponse> {
    const response = await api.post('/forecasts/ai-predict', data)
    return response.data
  },

  async exportForecast(format: 'pdf' | 'excel' = 'pdf'): Promise<void> {
    const response = await api.get(`/forecasts/export?format=${format}`, {
      responseType: 'blob',
    })
    const blob = new Blob([response.data], {
      type: format === 'pdf' ? 'application/pdf' : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `forecast-report.${format === 'pdf' ? 'pdf' : 'xlsx'}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  },
}

export default forecastService
