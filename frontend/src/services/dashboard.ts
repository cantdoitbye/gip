import { api } from './api'
import type { DashboardMetrics, ActivityItem, DashboardData } from '../types/dashboard'

interface BackendMetrics {
  projects_count: number
  pending_items: number
  completed_items: number
  active_sites: number
}

interface BackendActivityItem {
  id: string
  action: string
  description: string
  user_name: string | null
  timestamp: string
  details: Record<string, unknown> | null
}

export const dashboardService = {
  async getMetrics(): Promise<DashboardMetrics> {
    const response = await api.get<BackendMetrics>('/dashboard/metrics')
    return {
      projectsCount: response.data.projects_count,
      pendingItems: response.data.pending_items,
      completedItems: response.data.completed_items,
      activeSites: response.data.active_sites,
    }
  },

  async getActivity(limit?: number): Promise<ActivityItem[]> {
    const response = await api.get<{ items: BackendActivityItem[] }>('/dashboard/activity', {
      params: { page_size: limit || 10 }
    })
    return (response.data.items || []).map((item): ActivityItem => {
      let entityType: ActivityItem['entityType'] = 'project'
      const details = item.details || {}
      
      if (details.entity_type && typeof details.entity_type === 'string') {
        const et = details.entity_type as string
        if (['project', 'site', 'report', 'simulation', 'forecast'].includes(et)) {
          entityType = et as ActivityItem['entityType']
        }
      } else {
        const action = item.action.toLowerCase()
        if (action.includes('site')) entityType = 'site'
        else if (action.includes('report')) entityType = 'report'
        else if (action.includes('simulation')) entityType = 'simulation'
        else if (action.includes('forecast')) entityType = 'forecast'
      }
      
      return {
        id: item.id,
        action: item.action,
        description: item.description || item.action,
        entityType,
        userId: '',
        userName: item.user_name || 'System',
        createdAt: item.timestamp,
      }
    })
  },

  async getDashboardData(): Promise<DashboardData> {
    const response = await api.get<DashboardData>('/dashboard')
    return response.data
  },
}

export default dashboardService
