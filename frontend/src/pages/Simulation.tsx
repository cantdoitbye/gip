import { useState, useEffect } from 'react'
import Card from '../components/common/Card'
import Button, { ActionButton } from '../components/common/Button'
import LocationPicker from '../components/common/LocationPicker'
import {
  simulationService,
  type SimulationScenario,
  type SimulationScenarioCreate,
  type AIRecommendationRequest,
} from '../services/simulation'

export default function Simulation() {
  const [scenarios, setScenarios] = useState<SimulationScenario[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [selectedScenario, setSelectedScenario] = useState<SimulationScenario | null>(null)
  const [runningSimulation, setRunningSimulation] = useState(false)
  const [showAIModal, setShowAIModal] = useState(false)
  const [formData, setFormData] = useState<SimulationScenarioCreate>({
    name: '',
    description: '',
    scenario_type: 'new_flyover',
    location_name: '',
    latitude: 16.5,
    longitude: 80.6,
    estimated_cost: 50000000,
    estimated_duration_months: 24,
    priority: 'medium',
  })
  const [aiForm, setAIForm] = useState<AIRecommendationRequest>({
    location_name: '',
    latitude: 16.5,
    longitude: 80.6,
    current_traffic_volume: 10000,
    current_congestion_level: 'high',
  })
  const [aiResult, setAIResult] = useState<{
    recommended_scenario_type: string
    estimated_cost: number
    expected_traffic_improvement: number
    rationale: string
  } | null>(null)

  useEffect(() => {
    loadScenarios()
  }, [])

  const loadScenarios = async () => {
    try {
      setLoading(true)
      const response = await simulationService.listScenarios({})
      setScenarios(response.scenarios)
    } catch (error) {
      console.error('Failed to load scenarios:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateScenario = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await simulationService.createScenario(formData)
      setShowCreateModal(false)
      setFormData({
        name: '',
        description: '',
        scenario_type: 'new_flyover',
        location_name: '',
        latitude: 16.5,
        longitude: 80.6,
        estimated_cost: 50000000,
        estimated_duration_months: 24,
        priority: 'medium',
      })
      loadScenarios()
    } catch (error) {
      console.error('Failed to create scenario:', error)
    }
  }

  const handleRunSimulation = async (scenarioId: string) => {
    try {
      setRunningSimulation(true)
      await simulationService.runSimulation(scenarioId)
      loadScenarios()
    } catch (error) {
      console.error('Failed to run simulation:', error)
    } finally {
      setRunningSimulation(false)
    }
  }

  const handleAIRecommendation = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const result = await simulationService.getAIRecommendation(aiForm)
      setAIResult(result)
    } catch (error) {
      console.error('Failed to get AI recommendation:', error)
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
      case 'low':
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
    }
  }

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'new_bridge':
        return 'New Bridge'
      case 'new_flyover':
        return 'New Flyover'
      case 'widening':
        return 'Road Widening'
      case 'intersection_upgrade':
        return 'Intersection'
      default:
        return type
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Infrastructure Simulation</h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Run simulations and analyze infrastructure scenarios
          </p>
        </div>
        <div className="flex space-x-2">
          <Button variant="secondary" onClick={() => setShowAIModal(true)} leftIcon={
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          }>
            AI Recommend
          </Button>
          <Button onClick={() => setShowCreateModal(true)} leftIcon={
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
          }>Create Scenario</Button>
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
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Scenarios</p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">{scenarios.length}</p>
                </div>
              </div>
            </Card>
            <Card>
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Active</p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">{scenarios.filter(s => s.is_active).length}</p>
                </div>
              </div>
            </Card>
            <Card>
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">High Priority</p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">{scenarios.filter(s => s.priority === 'high').length}</p>
                </div>
              </div>
            </Card>
            <Card>
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Cost</p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                    Rs {(scenarios.reduce((acc, s) => acc + (s.estimated_cost || 0), 0) / 10000000).toFixed(0)}Cr
                  </p>
                </div>
              </div>
            </Card>
          </div>

          <Card title="Simulation Scenarios">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Name</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Type</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Location</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Priority</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Est. Cost</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                  {scenarios.map((scenario) => (
                    <tr key={scenario.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900 dark:text-white">{scenario.name}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400">
                          {getTypeLabel(scenario.scenario_type)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900 dark:text-white">{scenario.location_name}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityColor(scenario.priority)}`}>
                          {scenario.priority}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900 dark:text-white">
                          Rs {(scenario.estimated_cost || 0) / 10000000}Cr
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <div className="flex gap-2 justify-end">
                          <ActionButton variant="view" onClick={() => setSelectedScenario(scenario)}>
                            View
                          </ActionButton>
                          <ActionButton
                            variant="run"
                            onClick={() => handleRunSimulation(scenario.id)}
                            disabled={runningSimulation}
                          >
                            Run
                          </ActionButton>
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
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Create New Scenario</h3>
              <form onSubmit={handleCreateScenario} className="space-y-4">
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
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Description</label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Scenario Type</label>
                  <select
                    value={formData.scenario_type}
                    onChange={(e) => setFormData({ ...formData, scenario_type: e.target.value })}
                    className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  >
                    <option value="new_bridge">New Bridge</option>
                    <option value="new_flyover">New Flyover</option>
                    <option value="widening">Road Widening</option>
                    <option value="intersection_upgrade">Intersection Upgrade</option>
                  </select>
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
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Est. Cost (Rs)</label>
                    <input
                      type="number"
                      value={formData.estimated_cost}
                      onChange={(e) => setFormData({ ...formData, estimated_cost: parseInt(e.target.value) })}
                      className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Duration (months)</label>
                    <input
                      type="number"
                      value={formData.estimated_duration_months}
                      onChange={(e) => setFormData({ ...formData, estimated_duration_months: parseInt(e.target.value) })}
                      className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Priority</label>
                  <select
                    value={formData.priority}
                    onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                    className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  >
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                  </select>
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
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">AI Scenario Recommendation</h3>
              <form onSubmit={handleAIRecommendation} className="space-y-4">
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
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Current Traffic</label>
                    <input
                      type="number"
                      required
                      value={aiForm.current_traffic_volume}
                      onChange={(e) => setAIForm({ ...aiForm, current_traffic_volume: parseInt(e.target.value) })}
                      className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Congestion</label>
                    <select
                      value={aiForm.current_congestion_level}
                      onChange={(e) => setAIForm({ ...aiForm, current_congestion_level: e.target.value })}
                      className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                      <option value="critical">Critical</option>
                    </select>
                  </div>
                </div>
                <div className="flex justify-end space-x-3 pt-4">
                  <Button variant="secondary" onClick={() => { setShowAIModal(false); setAIResult(null); }}>Cancel</Button>
                  <Button type="submit">Get Recommendation</Button>
                </div>
              </form>
              {aiResult && (
                <div className="mt-6 p-4 bg-purple-50 dark:bg-purple-900/30 rounded-lg">
                  <h4 className="text-sm font-medium text-purple-900 dark:text-purple-300 mb-2">AI Recommendation</h4>
                  <div className="space-y-2 text-sm text-purple-800 dark:text-purple-300">
                    <p><strong>Scenario Type:</strong> {aiResult.recommended_scenario_type}</p>
                    <p><strong>Est. Cost:</strong> Rs {aiResult.estimated_cost.toLocaleString()}</p>
                    <p><strong>Traffic Improvement:</strong> {aiResult.expected_traffic_improvement}%</p>
                    <p><strong>Rationale:</strong> {aiResult.rationale}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {selectedScenario && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center px-4 pt-4">
            <div className="fixed inset-0 bg-black/50" onClick={() => setSelectedScenario(null)}></div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto p-6 relative z-10">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-gray-900 dark:text-white">{selectedScenario.name}</h3>
                <button onClick={() => setSelectedScenario(null)} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Type</p>
                    <p className="font-medium text-gray-900 dark:text-white">{getTypeLabel(selectedScenario.scenario_type)}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Priority</p>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityColor(selectedScenario.priority)}`}>
                      {selectedScenario.priority}
                    </span>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Location</p>
                    <p className="font-medium text-gray-900 dark:text-white">{selectedScenario.location_name}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Coordinates</p>
                    <p className="font-medium text-gray-900 dark:text-white">{selectedScenario.latitude}, {selectedScenario.longitude}</p>
                  </div>
                </div>
                {selectedScenario.description && (
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-4">Description</p>
                    <p className="font-medium text-gray-900 dark:text-white">{selectedScenario.description}</p>
                  </div>
                )}
                <div className="grid grid-cols-2 gap-4 mt-4">
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Est. Cost</p>
                    <p className="font-medium text-gray-900 dark:text-white">Rs {(selectedScenario.estimated_cost || 1) / 10000000}Cr</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Duration</p>
                    <p className="font-medium text-gray-900 dark:text-white">{selectedScenario.estimated_duration_months || 0} months</p>
                  </div>
                </div>
                {selectedScenario.simulations && selectedScenario.simulations.length > 0 && (
                  <div className="mt-4">
                    <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">Simulation Results</p>
                    <div className="bg-gray-50 dark:bg-gray-900/50 p-4 rounded-lg text-sm text-gray-700 dark:text-gray-300">
                      {selectedScenario.simulations[0].result?.overall_score && (
                        <p>Overall Score: {selectedScenario.simulations[0].result.overall_score.toFixed(1)}/10</p>
                      )}
                      {selectedScenario.simulations[0].result?.recommendation && (
                        <p className="mt-2">{selectedScenario.simulations[0].result.recommendation}</p>
                      )}
                    </div>
                  </div>
                )}
              </div>
              <div className="mt-6 flex justify-end">
                <Button variant="secondary" onClick={() => setSelectedScenario(null)}>Close</Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
