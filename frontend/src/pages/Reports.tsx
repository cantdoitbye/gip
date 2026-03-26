import { useState } from 'react'
import Card from '../components/common/Card'
import Button from '../components/common/Button'
import { trafficService } from '../services/traffic'
import { forecastService } from '../services/forecast'
import { siteService } from '../services/site'

interface ReportHistoryItem {
  id: string
  name: string
  type: 'traffic' | 'forecast' | 'site_analysis'
  format: 'pdf' | 'excel'
  generatedAt: Date
  size: string
  status: 'completed' | 'failed'
}

const reportHistory: ReportHistoryItem[] = [
  { id: '1', name: 'Traffic Report - March 2024', type: 'traffic', format: 'pdf', generatedAt: new Date('2024-03-20'), size: '2.4 MB', status: 'completed' },
  { id: '2', name: 'Forecast Analysis - Q1 2024', type: 'forecast', format: 'excel', generatedAt: new Date('2024-03-18'), size: '1.8 MB', status: 'completed' },
  { id: '3', name: 'Site Analysis - Highway 16', type: 'site_analysis', format: 'pdf', generatedAt: new Date('2024-03-15'), size: '3.2 MB', status: 'completed' },
  { id: '4', name: 'Traffic Hotspot Report', type: 'traffic', format: 'excel', generatedAt: new Date('2024-03-12'), size: '1.1 MB', status: 'completed' },
  { id: '5', name: 'Infrastructure Forecast - 2025', type: 'forecast', format: 'pdf', generatedAt: new Date('2024-03-10'), size: '4.5 MB', status: 'failed' },
]

export default function Reports() {
  const [generatingReport, setGeneratingReport] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)
  const [siteLocation, setSiteLocation] = useState<string>('Vijayawada')

  const handleTrafficExport = async (format: 'pdf' | 'excel') => {
    try {
      setGeneratingReport(`traffic-${format}`)
      setError(null)
      const blob = await trafficService.exportReport(format)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `traffic_report.${format === 'pdf' ? 'pdf' : 'xlsx'}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
      setSuccessMessage(`Traffic report downloaded successfully as ${format.toUpperCase()}`)
      setTimeout(() => setSuccessMessage(null), 3000)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to export traffic report')
    } finally {
      setGeneratingReport(null)
    }
  }

  const handleForecastExport = async (format: 'pdf' | 'excel') => {
    try {
      setGeneratingReport(`forecast-${format}`)
      setError(null)
      await forecastService.exportForecast(format)
      setSuccessMessage(`Forecast report downloaded successfully as ${format.toUpperCase()}`)
      setTimeout(() => setSuccessMessage(null), 3000)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to export forecast report')
    } finally {
      setGeneratingReport(null)
    }
  }

  const handleSiteAnalysisExport = async (format: 'pdf' | 'excel') => {
    try {
      setGeneratingReport(`site_analysis-${format}`)
      setError(null)
      if (!siteLocation.trim()) {
        setError('Please enter a location for site analysis')
        return
      }
      await siteService.exportSiteAnalysis(siteLocation, format)
      setSuccessMessage(`Site Analysis report for "${siteLocation}" downloaded successfully as ${format.toUpperCase()}`)
      setTimeout(() => setSuccessMessage(null), 3000)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to export site analysis report')
    } finally {
      setGeneratingReport(null)
    }
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'traffic':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400'
      case 'forecast':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400'
      case 'site_analysis':
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
    }
  }

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'traffic':
        return 'Traffic'
      case 'forecast':
        return 'Forecast'
      case 'site_analysis':
        return 'Site Analysis'
      default:
        return type
    }
  }

  const isGenerating = (reportType: string, format: string) => generatingReport === `${reportType}-${format}`

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Reports</h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Generate reports and analytics on infrastructure planning
          </p>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
          <p className="text-red-700 dark:text-red-400">{error}</p>
          <button onClick={() => setError(null)} className="mt-2 text-sm text-red-600 dark:text-red-400 hover:underline">
            Dismiss
          </button>
        </div>
      )}

      {successMessage && (
        <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
          <p className="text-green-700 dark:text-green-400">{successMessage}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-accent-100 text-accent-600 dark:bg-accent-900/30 dark:text-accent-400">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Generated Reports</p>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">45</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-primary-100 text-primary-600 dark:bg-primary-900/30 dark:text-primary-400">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Downloads</p>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">128</p>
            </div>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card title="Traffic Report">
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="p-3 rounded-lg bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400">
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <div>
                <h4 className="font-medium text-gray-900 dark:text-white">Traffic Analysis</h4>
                <p className="text-sm text-gray-500 dark:text-gray-400">Vehicle flow, congestion, hotspots</p>
              </div>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Comprehensive traffic data analysis including vehicle counts, speed patterns, 
              congestion levels, and identified hotspots for infrastructure planning.
            </p>
            <div className="flex gap-2">
              <Button
                variant="primary"
                size="sm"
                onClick={() => handleTrafficExport('pdf')}
                disabled={generatingReport !== null}
                isLoading={isGenerating('traffic', 'pdf')}
                leftIcon={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m0 3l3-3m2 8V7a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                }
              >
                PDF
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => handleTrafficExport('excel')}
                disabled={generatingReport !== null}
                isLoading={isGenerating('traffic', 'excel')}
                leftIcon={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                }
              >
                Excel
              </Button>
            </div>
          </div>
        </Card>

        <Card title="Forecast Report">
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="p-3 rounded-lg bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400">
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div>
                <h4 className="font-medium text-gray-900 dark:text-white">Demand Forecast</h4>
                <p className="text-sm text-gray-500 dark:text-gray-400">Predictive infrastructure needs</p>
              </div>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              AI-powered forecasting of infrastructure demands based on traffic trends, 
              population growth, and urban development patterns.
            </p>
            <div className="flex gap-2">
              <Button
                variant="primary"
                size="sm"
                onClick={() => handleForecastExport('pdf')}
                disabled={generatingReport !== null}
                isLoading={isGenerating('forecast', 'pdf')}
                leftIcon={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m0 3l3-3m2 8V7a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                }
              >
                PDF
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => handleForecastExport('excel')}
                disabled={generatingReport !== null}
                isLoading={isGenerating('forecast', 'excel')}
                leftIcon={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                }
              >
                Excel
              </Button>
            </div>
          </div>
        </Card>

        <Card title="Site Analysis Report">
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="p-3 rounded-lg bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400">
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <h4 className="font-medium text-gray-900 dark:text-white">Site Analysis</h4>
                <p className="text-sm text-gray-500 dark:text-gray-400">Location feasibility studies</p>
              </div>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Detailed analysis of proposed infrastructure sites including geological 
              surveys, environmental impact, and cost-benefit assessments.
            </p>
            <div>
              <label htmlFor="site-location" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Location
              </label>
              <input
                type="text"
                id="site-location"
                value={siteLocation}
                onChange={(e) => setSiteLocation(e.target.value)}
                placeholder="Enter location (e.g., Vijayawada)"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white text-sm"
              />
            </div>
            <div className="flex gap-2">
              <Button
                variant="primary"
                size="sm"
                onClick={() => handleSiteAnalysisExport('pdf')}
                disabled={generatingReport !== null}
                isLoading={isGenerating('site_analysis', 'pdf')}
                leftIcon={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m0 3l3-3m2 8V7a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                }
              >
                PDF
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => handleSiteAnalysisExport('excel')}
                disabled={generatingReport !== null}
                isLoading={isGenerating('site_analysis', 'excel')}
                leftIcon={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                }
              >
                Excel
              </Button>
            </div>
          </div>
        </Card>
      </div>

      <Card title="Recent Reports">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Report Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Format</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Size</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Generated</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
              {reportHistory.map((report) => (
                <tr key={report.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700">
                        <svg className="w-4 h-4 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                      <span className="text-sm font-medium text-gray-900 dark:text-white">{report.name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getTypeColor(report.type)}`}>
                      {getTypeLabel(report.type)}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="text-sm text-gray-600 dark:text-gray-400 uppercase">
                      {report.format}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="text-sm text-gray-600 dark:text-gray-400">{report.size}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {report.generatedAt.toLocaleDateString()}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      report.status === 'completed' 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                        : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                    }`}>
                      {report.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <button
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg bg-blue-100 text-blue-700 hover:bg-blue-200 dark:bg-blue-900/30 dark:text-blue-400 dark:hover:bg-blue-900/50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                      disabled={report.status === 'failed'}
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                      </svg>
                      Download
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}
