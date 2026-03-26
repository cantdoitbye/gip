import { useEffect, useState } from 'react'
import Card from '../components/common/Card'
import healthService, { type DetailedHealthResponse } from '../services/health'
import dashboardService from '../services/dashboard'
import type { DashboardMetrics, ActivityItem } from '../types/dashboard'

export default function Dashboard() {
  const [healthData, setHealthData] = useState<DetailedHealthResponse | null>(null)
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null)
  const [activities, setActivities] = useState<ActivityItem[]>([])
  const [loading, setLoading] = useState(true)
  const [metricsLoading, setMetricsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [metricsError, setMetricsError] = useState<string | null>(null)

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        setLoading(true)
        setError(null)
        const data = await healthService.checkDetailedHealth()
        setHealthData(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch health status')
      } finally {
        setLoading(false)
      }
    }

    fetchHealth()
  }, [])

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setMetricsLoading(true)
        setMetricsError(null)
        const [metricsData, activityData] = await Promise.all([
          dashboardService.getMetrics(),
          dashboardService.getActivity(10)
        ])
        setMetrics(metricsData)
        setActivities(activityData)
      } catch (err) {
        setMetricsError(err instanceof Error ? err.message : 'Failed to fetch dashboard data')
      } finally {
        setMetricsLoading(false)
      }
    }

    fetchDashboardData()
  }, [])

  const getStatusIndicator = (status: string) => {
    if (loading) {
      return { color: 'bg-warning-400 animate-pulse', text: 'Checking...' }
    }
    if (status === 'healthy' || status === 'connected') {
      return { color: 'bg-success-400', text: 'Connected' }
    }
    return { color: 'bg-error-400', text: 'Disconnected' }
  }

  const apiStatus = healthData?.status === 'healthy' ? 'healthy' : 'unhealthy'
  const apiIndicator = getStatusIndicator(apiStatus)
  const dbIndicator = loading 
    ? { color: 'bg-warning-400 animate-pulse', text: 'Checking...' }
    : healthData 
      ? getStatusIndicator(healthData.services?.database ?? 'unhealthy') 
      : { color: 'bg-error-400', text: 'Disconnected' }
  const redisIndicator = loading 
    ? { color: 'bg-warning-400 animate-pulse', text: 'Checking...' }
    : healthData 
      ? getStatusIndicator(healthData.services?.redis ?? 'unhealthy') 
      : { color: 'bg-error-400', text: 'Disconnected' }

  const getEntityTypeIcon = (type: ActivityItem['entityType']) => {
    switch (type) {
      case 'project':
        return (
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        )
      case 'site':
        return (
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        )
      case 'report':
        return (
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        )
      case 'simulation':
        return (
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        )
      case 'forecast':
        return (
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        )
    }
  }

  const formatTimeAgo = (dateString: string) => {
    if (!dateString) return 'Unknown'
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return 'Unknown'
    const now = new Date()
    const seconds = Math.floor((now.getTime() - date.getTime()) / 1000)

    if (seconds < 0) return 'Just now'
    if (seconds < 60) return 'Just now'
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
    if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`
    return date.toLocaleDateString()
  }

  const LoadingSkeleton = () => (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-16"></div>
      <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-24 mt-2"></div>
    </div>
  )

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Overview of infrastructure planning system
        </p>
      </div>

      {metricsError && (
        <div className="p-4 bg-error-50 border border-error-200 rounded-lg">
          <p className="text-sm text-error-600">{metricsError}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          {metricsLoading ? (
            <LoadingSkeleton />
          ) : (
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-primary-100 text-primary-600">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Projects</p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">{metrics?.projectsCount ?? 0}</p>
              </div>
            </div>
          )}
        </Card>

        <Card>
          {metricsLoading ? (
            <LoadingSkeleton />
          ) : (
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-warning-100 text-warning-600">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Pending</p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">{metrics?.pendingItems ?? 0}</p>
              </div>
            </div>
          )}
        </Card>

        <Card>
          {metricsLoading ? (
            <LoadingSkeleton />
          ) : (
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-success-100 text-success-600">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Completed</p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">{metrics?.completedItems ?? 0}</p>
              </div>
            </div>
          )}
        </Card>

        <Card>
          {metricsLoading ? (
            <LoadingSkeleton />
          ) : (
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-accent-100 text-accent-600">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Active Sites</p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">{metrics?.activeSites ?? 0}</p>
              </div>
            </div>
          )}
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="System Health">
          <div className="space-y-4">
            {error && (
              <div className="p-3 bg-error-50 border border-error-200 rounded-lg">
                <p className="text-sm text-error-600">{error}</p>
              </div>
            )}
            <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div className="flex items-center gap-3">
                <div className={`w-3 h-3 ${apiIndicator.color} rounded-full`}></div>
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Backend API</span>
              </div>
              <span className="text-sm text-gray-500 dark:text-gray-400">{apiIndicator.text}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div className="flex items-center gap-3">
                <div className={`w-3 h-3 ${dbIndicator.color} rounded-full`}></div>
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Database</span>
              </div>
              <span className="text-sm text-gray-500 dark:text-gray-400">{dbIndicator.text}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div className="flex items-center gap-3">
                <div className={`w-3 h-3 ${redisIndicator.color} rounded-full`}></div>
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Cache (Redis)</span>
              </div>
              <span className="text-sm text-gray-500 dark:text-gray-400">{redisIndicator.text}</span>
            </div>
            {healthData && (
              <div className="pt-2 border-t border-gray-200 dark:border-gray-700">
                <p className="text-xs text-gray-400 dark:text-gray-500">API Version: {healthData.version}</p>
              </div>
            )}
          </div>
        </Card>

        <Card title="Recent Activity">
          <div className="space-y-4">
            {metricsLoading ? (
              <div className="space-y-3">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="animate-pulse flex items-start gap-3">
                    <div className="w-8 h-8 bg-gray-200 dark:bg-gray-700 rounded-full"></div>
                    <div className="flex-1">
                      <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
                      <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mt-2"></div>
                    </div>
                  </div>
                ))}
              </div>
            ) : activities.length === 0 ? (
              <p className="text-sm text-gray-500 dark:text-gray-400 text-center py-4">
                No recent activity to display
              </p>
            ) : (
              <div className="space-y-3">
                {activities.map((activity) => (
                  <div key={activity.id} className="flex items-start gap-3 p-2 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg transition-colors">
                    <div className="w-8 h-8 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center text-primary-600 flex-shrink-0">
                      {getEntityTypeIcon(activity.entityType)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-gray-900 dark:text-white truncate">{activity.description}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                        {activity.userName} · {formatTimeAgo(activity.createdAt)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  )
}
