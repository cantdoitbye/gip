import { useState, useEffect } from 'react'
import Card from '../components/common/Card'
import Button, { ActionButton } from '../components/common/Button'
import LocationPicker from '../components/common/LocationPicker'
import {
  forecastService,
  type Forecast,
  type ForecastCreate,
  type AIForecastRequest,
  type AIForecastResponse,
} from '../services/forecast'

export default function Forecasting() {
  const [forecasts, setForecasts] = useState<Forecast[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [selectedForecast, setSelectedForecast] = useState<Forecast | null>(null)
  const [runningForecast, setRunningForecast] = useState(false)
  const [showAIModal, setShowAIModal] = useState(false)
  const [formData, setFormData] = useState<ForecastCreate>({
    name: '',
    description: '',
    forecast_type: 'traffic_volume',
    location_name: '',
    latitude: 16.5,
    longitude: 80.6,
    start_year: new Date().getFullYear(),
    end_year: new Date().getFullYear() + 5,
    base_traffic_volume: 10000,
    road_capacity: 15000,
  })
  const [aiForm, setAIForm] = useState<AIForecastRequest>({
    location_name: '',
    latitude: 16.5,
    longitude: 80.6,
    base_year: new Date().getFullYear(),
    target_year: new Date().getFullYear() + 5,
    base_traffic_volume: 10000,
    road_capacity: 15000,
  })
  const [aiResult, setAIResult] = useState<AIForecastResponse | null>(null)

  useEffect(() => {
    loadForecasts()
  }, [])

  const loadForecasts = async () => {
    try {
      setLoading(true)
      const response = await forecastService.listForecasts({})
      setForecasts(response.forecasts)
    } catch (error) {
      console.error('Failed to load forecasts:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateForecast = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await forecastService.createForecast(formData)
      setShowCreateModal(false)
      setFormData({
        name: '',
        description: '',
        forecast_type: 'traffic_volume',
        location_name: '',
        latitude: 16.5,
        longitude: 80.6,
        start_year: new Date().getFullYear(),
        end_year: new Date().getFullYear() + 5,
        base_traffic_volume: 10000,
        road_capacity: 15000,
      })
      loadForecasts()
    } catch (error) {
      console.error('Failed to create forecast:', error)
    }
  }

  const handleRunForecast = async (forecastId: string) => {
    try {
      setRunningForecast(true)
      await forecastService.runForecast(forecastId)
      loadForecasts()
    } catch (error) {
      console.error('Failed to run forecast:', error)
    } finally {
      setRunningForecast(false)
    }
  }

  const handleAIPredict = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const result = await forecastService.aiPredict(aiForm)
      setAIResult(result)
    } catch (error) {
      console.error('Failed to get AI prediction:', error)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
      case 'running':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400'
      case 'completed':
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Traffic Forecasting</h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Predict future infrastructure demands and capacity requirements
          </p>
        </div>
        <div className="flex space-x-2">
          <Button variant="secondary" onClick={() => setShowAIModal(true)}>
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            AI Predict
          </Button>
          <Button onClick={() => setShowCreateModal(true)}>
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Create Forecast
          </Button>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card>
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-primary-100 text-primary-600 dark:bg-primary-900/30 dark:text-primary-400">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Forecasts</p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">{forecasts.length}</p>
                </div>
              </div>
            </Card>
            <Card>
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Completed</p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">{forecasts.filter(f => f.status === 'completed').length}</p>
                </div>
              </div>
            </Card>
            <Card>
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-yellow-100 text-yellow-600 dark:bg-yellow-900/30 dark:text-yellow-400">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Pending</p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">{forecasts.filter(f => f.status === 'pending').length}</p>
                </div>
              </div>
            </Card>
            <Card>
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Avg Growth</p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                    {forecasts.length > 0
                      ? (forecasts.reduce((acc, f) => acc + (f.growth_rate || 0), 0) / forecasts.length).toFixed(1) + '%'
                      : '0%'}
                  </p>
                </div>
              </div>
            </Card>
          </div>

          <Card title="Forecasts">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Name</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Location</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Period</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Growth</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                  {forecasts.map((forecast) => (
                    <tr key={forecast.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900 dark:text-white">{forecast.name}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900 dark:text-white">{forecast.location_name}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900 dark:text-white">{forecast.start_year} - {forecast.end_year}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(forecast.status)}`}>
                          {forecast.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900 dark:text-white">
                          {forecast.growth_rate ? `${forecast.growth_rate.toFixed(1)}%` : '-'}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <div className="flex gap-2 justify-end">
                          <ActionButton variant="view" onClick={() => setSelectedForecast(forecast)}>
                            View
                          </ActionButton>
                          {forecast.status === 'pending' && (
                            <ActionButton
                              variant="run"
                              onClick={() => handleRunForecast(forecast.id)}
                              disabled={runningForecast}
                            >
                              Run
                            </ActionButton>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </>
      )}

      {showCreateModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center px-4 pt-4">
            <div className="fixed inset-0 bg-black/50" onClick={() => setShowCreateModal(false)}></div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 relative z-10">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Create New Forecast</h3>
              <form onSubmit={handleCreateForecast} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Name</label>
                  <input
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Location</label>
                  <input
                    type="text"
                    required
                    value={formData.location_name}
                    onChange={(e) => setFormData({ ...formData, location_name: e.target.value })}
                    className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    placeholder="e.g., MG Road Junction, Vijayawada"
                  />
                </div>
                <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Select Location on Map
                  </label>
                  <LocationPicker
                    latitude={formData.latitude}
                    longitude={formData.longitude}
                    locationName={formData.location_name}
                    onLocationChange={(lat, lng) => setFormData({ ...formData, latitude: lat, longitude: lng })}
                    onLocationNameChange={(name) => setFormData({ ...formData, location_name: name })}
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Start Year</label>
                    <input
                      type="number"
                      required
                      value={formData.start_year}
                      onChange={(e) => setFormData({ ...formData, start_year: parseInt(e.target.value) })}
                      className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">End Year</label>
                    <input
                      type="number"
                      required
                      value={formData.end_year}
                      onChange={(e) => setFormData({ ...formData, end_year: parseInt(e.target.value) })}
                      className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Base Traffic Volume</label>
                  <input
                    type="number"
                    required
                    value={formData.base_traffic_volume}
                    onChange={(e) => setFormData({ ...formData, base_traffic_volume: parseInt(e.target.value) })}
                    className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div className="flex justify-end space-x-3 pt-4">
                  <Button variant="secondary" onClick={() => setShowCreateModal(false)}>Cancel</Button>
                  <Button type="submit">Create</Button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {showAIModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center px-4 pt-4">
            <div className="fixed inset-0 bg-black/50" onClick={() => { setShowAIModal(false); setAIResult(null); }}></div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 relative z-10">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">AI Traffic Prediction</h3>
              <form onSubmit={handleAIPredict} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Location</label>
                  <input
                    type="text"
                    required
                    value={aiForm.location_name}
                    onChange={(e) => setAIForm({ ...aiForm, location_name: e.target.value })}
                    className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    placeholder="e.g., MG Road Junction, Vijayawada"
                  />
                </div>
                <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Select Location on Map
                  </label>
                  <LocationPicker
                    latitude={aiForm.latitude}
                    longitude={aiForm.longitude}
                    locationName={aiForm.location_name}
                    onLocationChange={(lat, lng) => setAIForm({ ...aiForm, latitude: lat, longitude: lng })}
                    onLocationNameChange={(name) => setAIForm({ ...aiForm, location_name: name })}
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Base Year</label>
                    <input
                      type="number"
                      required
                      value={aiForm.base_year}
                      onChange={(e) => setAIForm({ ...aiForm, base_year: parseInt(e.target.value) })}
                      className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Target Year</label>
                    <input
                      type="number"
                      required
                      value={aiForm.target_year}
                      onChange={(e) => setAIForm({ ...aiForm, target_year: parseInt(e.target.value) })}
                      className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Base Traffic Volume</label>
                  <input
                    type="number"
                    required
                    value={aiForm.base_traffic_volume}
                    onChange={(e) => setAIForm({ ...aiForm, base_traffic_volume: parseInt(e.target.value) })}
                    className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div className="flex justify-end space-x-3 pt-4">
                  <Button variant="secondary" onClick={() => { setShowAIModal(false); setAIResult(null); }}>Cancel</Button>
                  <Button type="submit">Predict</Button>
                </div>
              </form>
              {aiResult && (
                <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
                  <h4 className="text-sm font-medium text-blue-900 dark:text-blue-300 mb-2">AI Prediction Results</h4>
                  <div className="space-y-2 text-sm text-blue-800 dark:text-blue-300">
                    <p><strong>Predicted Volume:</strong> {aiResult.predicted_traffic_volume.toLocaleString()}</p>
                    <p><strong>Growth Rate:</strong> {aiResult.growth_rate.toFixed(1)}%</p>
                    <p><strong>Confidence:</strong> {aiResult.confidence_score.toFixed(1)}%</p>
                    <p><strong>Insights:</strong> {aiResult.ai_insights}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {selectedForecast && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center px-4 pt-4">
            <div className="fixed inset-0 bg-black/50" onClick={() => setSelectedForecast(null)}></div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto p-6 relative z-10">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-gray-900 dark:text-white">{selectedForecast.name}</h3>
                <button onClick={() => setSelectedForecast(null)} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Location</p>
                    <p className="font-medium text-gray-900 dark:text-white">{selectedForecast.location_name}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Status</p>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(selectedForecast.status)}`}>
                      {selectedForecast.status}
                    </span>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Period</p>
                    <p className="font-medium text-gray-900 dark:text-white">{selectedForecast.start_year} - {selectedForecast.end_year}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Base Volume</p>
                    <p className="font-medium text-gray-900 dark:text-white">{selectedForecast.base_traffic_volume.toLocaleString()}</p>
                  </div>
                </div>
                {selectedForecast.predicted_traffic_volume && (
                  <div className="grid grid-cols-2 gap-4 mt-4">
                    <div>
                      <p className="text-sm text-gray-500 dark:text-gray-400">Predicted Volume</p>
                      <p className="font-medium text-gray-900 dark:text-white">{selectedForecast.predicted_traffic_volume.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500 dark:text-gray-400">Growth Rate</p>
                      <p className="font-medium text-gray-900 dark:text-white">{selectedForecast.growth_rate?.toFixed(1)}%</p>
                    </div>
                  </div>
                )}
                {selectedForecast.ai_insights && (
                  <div className="mt-4">
                    <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">AI Insights</p>
                    <div className="bg-gray-50 dark:bg-gray-900/50 p-4 rounded-lg text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                      {selectedForecast.ai_insights}
                    </div>
                  </div>
                )}
              </div>
              <div className="mt-6 flex justify-end">
                <Button variant="secondary" onClick={() => setSelectedForecast(null)}>Close</Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
