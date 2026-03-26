import api from './api'

export interface SimulationScenario {
  id: string
  name: string
  description: string | null
  scenario_type: string
  location_name: string
  latitude: number
  longitude: number
  estimated_cost: number | null
  estimated_duration_months: number | null
  priority: string
  is_active: boolean
  parameters: Record<string, unknown> | null
  created_by: string | null
  created_at: string
  updated_at: string
  simulations: Simulation[]
}

export interface SimulationScenarioListResponse {
  scenarios: SimulationScenario[]
  total: number
  page: number
  page_size: number
}

export interface SimulationScenarioCreate {
  name: string
  description?: string
  scenario_type?: string
  location_name: string
  latitude: number
  longitude: number
  estimated_cost?: number
  estimated_duration_months?: number
  priority?: string
  parameters?: Record<string, unknown>
}

export interface SimulationResult {
  id: string
  simulation_id: string
  traffic_improvement_percent: number | null
  congestion_reduction_percent: number | null
  travel_time_savings_min: number | null
  safety_score: number | null
  safety_improvement_percent: number | null
  environmental_impact_score: number | null
  cost_benefit_ratio: number | null
  roi_percent: number | null
  npv: number | null
  irr: number | null
  overall_score: number | null
  recommendation: string | null
  ai_analysis: string | null
  detailed_metrics: Record<string, unknown> | null
  created_at: string
}

export interface Simulation {
  id: string
  scenario_id: string
  status: string
  progress_percentage: number
  started_at: string | null
  completed_at: string | null
  result: SimulationResult | null
  created_at: string
  updated_at: string
}

export interface SimulationListResponse {
  simulations: Simulation[]
  total: number
  page: number
  page_size: number
}

export interface SimulationStatusResponse {
  simulation_id: string
  scenario_id: string
  scenario_name: string
  status: string
  progress_percentage: number
  started_at: string | null
  completed_at: string | null
  estimated_completion: string | null
  current_step: string | null
}

export interface SimulationResultsResponse {
  simulation_id: string
  scenario: SimulationScenario
  result: SimulationResult | null
  comparison_baseline: Record<string, unknown> | null
}

export interface ScenarioComparisonRequest {
  name: string
  scenario_ids: string[]
  comparison_criteria?: Record<string, number>
}

export interface ScenarioComparisonResult {
  scenario_id: string
  scenario_name: string
  scenario_type: string
  estimated_cost: number
  overall_score: number
  traffic_improvement_percent: number
  safety_improvement_percent: number
  cost_benefit_ratio: number
  roi_percent: number
  rank: number
}

export interface ScenarioComparisonResponse {
  id: string
  name: string
  scenarios: ScenarioComparisonResult[]
  ranking_criteria: Record<string, unknown>
  ai_recommendation: string | null
  best_scenario_id: string | null
  created_at: string
}

export interface AIRecommendationRequest {
  location_name: string
  latitude: number
  longitude: number
  current_traffic_volume: number
  current_congestion_level: string
  budget_range?: { min: number; max: number }
  priorities?: string[]
  constraints?: Record<string, unknown>
}

export interface AIRecommendationResponse {
  recommended_scenario_type: string
  recommended_scenario_name: string
  confidence_score: number
  estimated_cost: number
  estimated_duration_months: number
  expected_traffic_improvement: number
  expected_safety_improvement: number
  cost_benefit_ratio: number
  roi_percent: number
  rationale: string
  alternatives: {
    type: string
    estimated_cost: number
    traffic_improvement: number
    safety_improvement: number
    cost_benefit_ratio: number
  }[]
  key_considerations: string[]
  risk_factors: string[]
}

export interface CostEstimationRequest {
  scenario_type: string
  location_name: string
  length_km?: number
  width_m?: number
  lanes?: number
  special_features?: string[]
}

export interface CostEstimationResponse {
  scenario_type: string
  location_name: string
  base_cost: number
  land_acquisition_cost: number
  construction_cost: number
  contingency_percent: number
  total_estimated_cost: number
  cost_per_km: number | null
  timeline_months: number
  cost_breakdown: Record<string, number>
}

export interface AIChatRequest {
  message: string
  context?: Record<string, unknown>
}

export interface AIChatResponse {
  response: string
  sources_used: string[]
  confidence: number
  is_ai_generated: boolean
}

export const simulationService = {
  async listScenarios(params: {
    page?: number
    page_size?: number
    scenario_type?: string
  } = {}): Promise<SimulationScenarioListResponse> {
    const response = await api.get('/simulations/scenarios', { params })
    return response.data
  },

  async createScenario(data: SimulationScenarioCreate): Promise<SimulationScenario> {
    const response = await api.post('/simulations/scenarios', data)
    return response.data
  },

  async getScenario(id: string): Promise<SimulationScenario> {
    const response = await api.get(`/simulations/scenarios/${id}`)
    return response.data
  },

  async updateScenario(id: string, data: Partial<SimulationScenarioCreate>): Promise<SimulationScenario> {
    const response = await api.put(`/simulations/scenarios/${id}`, data)
    return response.data
  },

  async deleteScenario(id: string): Promise<void> {
    await api.delete(`/simulations/scenarios/${id}`)
  },

  async listSimulations(params: {
    page?: number
    page_size?: number
    scenario_id?: string
    status?: string
  } = {}): Promise<SimulationListResponse> {
    const response = await api.get('/simulations', { params })
    return response.data
  },

  async runSimulation(scenarioId: string): Promise<Simulation> {
    const response = await api.post('/simulations/run', { scenario_id: scenarioId })
    return response.data
  },

  async getSimulationStatus(id: string): Promise<SimulationStatusResponse> {
    const response = await api.get(`/simulations/${id}/status`)
    return response.data
  },

  async getSimulationResults(id: string): Promise<SimulationResultsResponse> {
    const response = await api.get(`/simulations/${id}/results`)
    return response.data
  },

  async compareScenarios(data: ScenarioComparisonRequest): Promise<ScenarioComparisonResponse> {
    const response = await api.post('/simulations/compare', data)
    return response.data
  },

  async getAIRecommendation(data: AIRecommendationRequest): Promise<AIRecommendationResponse> {
    const response = await api.post('/simulations/recommend', data)
    return response.data
  },

  async estimateCost(data: CostEstimationRequest): Promise<CostEstimationResponse> {
    const response = await api.post('/simulations/estimate-cost', data)
    return response.data
  },

  async chat(data: AIChatRequest): Promise<AIChatResponse> {
    const response = await api.post('/simulations/chat', data)
    return response.data
  },
}

export default simulationService
