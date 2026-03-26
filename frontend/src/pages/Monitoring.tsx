import { useState, useEffect } from 'react'
import Card from '../components/common/Card'
import { healthService } from '../services/health'

interface MockProject {
  id: string
  name: string
  location: string
  status: string
  progress: number
  startDate: string
  endDate: string
}

const mockProjects: MockProject[] = [
  { id: '1', name: 'Vijayawada Flyover', location: 'Vijayawada', status: 'in_progress', progress: 65, startDate: '2025-01-01', endDate: '2026-06-30' },
  { id: '2', name: 'Guntur Road Widening', location: 'Guntur', status: 'in_progress', progress: 40, startDate: '2025-02-15', endDate: '2025-12-31' },
  { id: '3', name: 'Amaravati Bridge', location: 'Amaravati', status: 'planning', progress: 10, startDate: '2025-06-01', endDate: '2027-03-31' },
  { id: '4', name: 'Kakinada Intersection', location: 'Kakinada', status: 'completed', progress: 100, startDate: '2024-06-01', endDate: '2025-03-15' },
  { id: '5', name: 'Tirupati Underpass', location: 'Tirupati', status: 'on_hold', progress: 25, startDate: '2025-01-15', endDate: '2025-10-31' },
]

export default function Monitoring() {
  const [systemStatus, setSystemStatus] = useState<'healthy' | 'degraded' | 'down'>('healthy')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchHealth()
  }, [])

  const fetchHealth = async () => {
    try {
      setLoading(true)
      const data = await healthService.checkDetailedHealth()
      setSystemStatus(data.status === 'ok' ? 'healthy' : 'degraded')
    } catch {
      setSystemStatus('degraded')
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800'
      case 'in_progress': return 'bg-blue-100 text-blue-800'
      case 'planning': return 'bg-yellow-100 text-yellow-800'
      case 'on_hold': return 'bg-orange-100 text-orange-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getProgressColor = (progress: number) => {
    if (progress >= 80) return 'bg-green-500'
    if (progress >= 50) return 'bg-blue-500'
    if (progress >= 25) return 'bg-yellow-500'
    return 'bg-gray-300'
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Monitoring</h1>
        <p className="mt-1 text-sm text-gray-500">Real-time monitoring of infrastructure projects</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card>
          <div className="flex items-center">
            <div className={`p-3 rounded-full ${systemStatus === 'healthy' ? 'bg-green-100 text-green-600' : 'bg-yellow-100 text-yellow-600'}`}>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">System Status</p>
              <p className="text-lg font-semibold text-gray-900 capitalize">{systemStatus}</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-primary-100 text-primary-600">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Active Projects</p>
              <p className="text-2xl font-semibold text-gray-900">{mockProjects.filter(p => p.status === 'in_progress').length}</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-warning-100 text-warning-600">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">On Hold</p>
              <p className="text-2xl font-semibold text-gray-900">{mockProjects.filter(p => p.status === 'on_hold').length}</p>
            </div>
          </div>
        </Card>
      </div>

      <Card title="Project Status">
        <div className="space-y-4">
          {mockProjects.map((project) => (
            <div key={project.id} className="p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <div>
                  <h3 className="text-sm font-semibold text-gray-900">{project.name}</h3>
                  <p className="text-xs text-gray-500">{project.location}</p>
                </div>
                <span className={`text-xs px-2 py-1 rounded-full capitalize ${getStatusColor(project.status)}`}>
                  {project.status.replace('_', ' ')}
                </span>
              </div>
              <div className="mt-2">
                <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
                  <span>Progress</span>
                  <span>{project.progress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className={`h-2 rounded-full ${getProgressColor(project.progress)}`} style={{ width: `${project.progress}%` }}></div>
                </div>
              </div>
              <div className="mt-2 flex items-center justify-between text-xs text-gray-500">
                <span>Start: {new Date(project.startDate).toLocaleDateString()}</span>
                <span>End: {new Date(project.endDate).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}
