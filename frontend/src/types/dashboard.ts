export interface DashboardMetrics {
  projectsCount: number
  pendingItems: number
  completedItems: number
  activeSites: number
}

export interface ActivityItem {
  id: string
  action: string
  description: string
  entityType: 'project' | 'site' | 'report' | 'simulation' | 'forecast'
  entityId?: string
  userId: string
  userName: string
  createdAt: string
}

export interface DashboardData {
  metrics: DashboardMetrics
  recentActivity: ActivityItem[]
}
