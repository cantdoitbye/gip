import api from './api'

export interface TrafficData {
  id: string
  location_name: string
  latitude: number
  longitude: number
  vehicle_count: number
  avg_speed: number
  congestion_level: string
  timestamp: string
}

export interface TrafficListResponse {
  items: TrafficData[]
  total: number
  page: number
  page_size: number
  has_more: boolean
}

export interface HeatmapPoint {
  lat: number
  lng: number
  intensity: number
  location_name: string
}

export interface CongestionScore {
  location: string
  level: string
  score: number
  color: string
  latitude: number
  longitude: number
  vehicle_count: number
}

export interface Hotspot {
  id: string
  lat: number
  lng: number
  incident_count: number
  risk_score: number
  risk_level: string
  location_name: string
  incident_types: string[]
}

export interface TrafficInsight {
  type: string
  title: string
  description: string
  confidence: number
  recommendation: string
}

export interface TrafficAnalysisResponse {
  insights: TrafficInsight[]
  summary: string
  recommendations: string[]
}

export const trafficService = {
  async getTrafficData(params: {
    page?: number
    page_size?: number
    location?: string
    min_congestion?: string
    date_from?: string
    date_to?: string
  } = {}): Promise<TrafficListResponse> {
    const response = await api.get('/traffic/data', { params })
    return response.data
  },

  async getHeatmapData(): Promise<HeatmapPoint[]> {
    const response = await api.get('/traffic/heatmap')
    return response.data
  },

  async getCongestionScores(): Promise<CongestionScore[]> {
    const response = await api.get('/traffic/congestion')
    return response.data
  },

  async getHotspots(): Promise<Hotspot[]> {
    const response = await api.get('/traffic/hotspots')
    return response.data
  },

  async analyzeTraffic(data: TrafficData[]): Promise<TrafficAnalysisResponse> {
    const response = await api.post('/traffic/analyze', { data })
    return response.data
  },

  async exportReport(format: 'pdf' | 'excel'): Promise<Blob> {
    const response = await api.get(`/traffic/export?format=${format}`, {
      responseType: 'blob',
    })
    return response.data
  },
}

export default trafficService
