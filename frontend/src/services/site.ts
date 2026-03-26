import api from './api'

export interface SiteFactor {
  id: string
  site_id: string
  factor_name: string
  factor_type: string
  score: number
  weight: number
  value: number | null
  unit: string | null
  source: string | null
  created_at: string
  updated_at: string
}

export interface RiskZone {
  id: string
  site_id: string
  zone_type: string
  severity: string
  description: string | null
  latitude: number
  longitude: number
  radius_meters: number
  created_at: string
}

export interface Site {
  id: string
  name: string
  description: string | null
  site_type: string
  status: string
  location_name: string
  address: string | null
  latitude: number
  longitude: number
  area_sqkm: number | null
  overall_score: number | null
  ai_recommendation: string | null
  created_by: string | null
  created_at: string
  updated_at: string
  factors: SiteFactor[]
  risk_zones: RiskZone[]
}

export interface SiteListResponse {
  sites: Site[]
  total: number
  page: number
  page_size: number
}

export interface SiteCreate {
  name: string
  description?: string
  site_type?: string
  location_name: string
  address?: string
  latitude: number
  longitude: number
  area_sqkm?: number
}

export interface SiteUpdate {
  name?: string
  description?: string
  site_type?: string
  location_name?: string
  address?: string
  latitude?: number
  longitude?: number
  area_sqkm?: number
}

export interface AISiteAnalysisRequest {
  location_name: string
  latitude: number
  longitude: number
  area_sqkm?: number
}

export interface AISiteAnalysisResponse {
  site_id: string | null
  location_name: string
  latitude: number
  longitude: number
  overall_suitability_score: number
  land_suitability_score: number
  connectivity_score: number
  infrastructure_score: number
  environmental_score: number
  economic_score: number
  social_score: number
  risk_score: number
  recommendation: string
  ai_analysis: string
  detailed_factors: Record<string, unknown>
}

export const siteService = {
  async listSites(params: {
    page?: number
    page_size?: number
    site_type?: string
    status?: string
  } = {}): Promise<SiteListResponse> {
    const response = await api.get('/sites', { params })
    return response.data
  },

  async createSite(data: SiteCreate): Promise<Site> {
    const response = await api.post('/sites', data)
    return response.data
  },

  async getSite(id: string): Promise<Site> {
    const response = await api.get(`/sites/${id}`)
    return response.data
  },

  async updateSite(id: string, data: SiteUpdate): Promise<Site> {
    const response = await api.put(`/sites/${id}`, data)
    return response.data
  },

  async deleteSite(id: string): Promise<void> {
    await api.delete(`/sites/${id}`)
  },

  async analyzeSite(id: string): Promise<Site> {
    const response = await api.post(`/sites/${id}/analyze`)
    return response.data
  },

  async aiAnalyzeSite(data: AISiteAnalysisRequest): Promise<AISiteAnalysisResponse> {
    const response = await api.post('/sites/ai-analyze', data)
    return response.data
  },

  async exportSiteAnalysis(location: string, format: 'pdf' | 'excel' = 'pdf'): Promise<void> {
    const response = await api.get(`/sites/export`, {
      params: { location, format },
      responseType: 'blob',
    })
    const blob = new Blob([response.data], {
      type: format === 'pdf' ? 'application/pdf' : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    const sanitizedLocation = location.replace(/[^a-zA-Z0-9]/g, '_')
    link.download = `site-analysis-${sanitizedLocation}.${format === 'pdf' ? 'pdf' : 'xlsx'}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  },
}

export default siteService
