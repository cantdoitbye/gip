import { useState, useEffect } from 'react'
import Card from '../components/common/Card'
import Button, { ActionButton } from '../components/common/Button'
import LocationPicker from '../components/common/LocationPicker'
import { siteService, type Site, type SiteCreate } from '../services/site'

export default function Sites() {
  const [sites, setSites] = useState<Site[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [selectedSite, setSelectedSite] = useState<Site | null>(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [formData, setFormData] = useState<SiteCreate>({
    name: '',
    description: '',
    site_type: 'proposed_flyover',
    location_name: '',
    latitude: 16.5,
    longitude: 80.6,
    area_sqkm: 1,
  })

  useEffect(() => {
    loadSites()
  }, [])

  const loadSites = async () => {
    try {
      setLoading(true)
      const response = await siteService.listSites({})
      setSites(response.sites)
    } catch (error) {
      console.error('Failed to load sites:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateSite = async () => {
    try {
      await siteService.createSite(formData)
      setShowCreateModal(false)
      setFormData({
        name: '',
        description: '',
        site_type: 'proposed_flyover',
        location_name: '',
        latitude: 16.5,
        longitude: 80.6,
        area_sqkm: 1,
      })
      loadSites()
    } catch (error) {
      console.error('Failed to create site:', error)
    }
  }

  const handleAnalyzeSite = async (siteId: string) => {
    try {
      setAnalyzing(true)
      await siteService.analyzeSite(siteId)
      loadSites()
    } catch (error) {
      console.error('Failed to analyze site:', error)
    } finally {
      setAnalyzing(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
      case 'analyzing':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400'
      case 'analyzed':
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'proposed_bridge':
        return 'Bridge'
      case 'proposed_flyover':
        return 'Flyover'
      case 'existing_bridge':
        return 'Bridge'
      case 'existing_flyover':
        return 'Flyover'
      default:
        return type
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Site Analysis</h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Analyze and evaluate infrastructure development sites
          </p>
        </div>
        <Button onClick={() => setShowCreateModal(true)} leftIcon={
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
        }>Add Site</Button>
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
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Sites</p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">{sites.length}</p>
                </div>
              </div>
            </Card>
            <Card>
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-yellow-100 text-yellow-600 dark:bg-yellow-900/30 dark:text-yellow-400">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Pending</p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">{sites.filter(s => s.status === 'pending').length}</p>
                </div>
              </div>
            </Card>
            <Card>
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Analyzed</p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">{sites.filter(s => s.status === 'analyzed').length}</p>
                </div>
              </div>
            </Card>
          </div>

          <Card title="Sites List">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Name
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Type
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Location
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Score
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                  {sites.map((site) => (
                    <tr key={site.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900 dark:text-white">{site.name}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300">
                          {getTypeIcon(site.site_type)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900 dark:text-gray-100">{site.location_name}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(site.status)}`}>
                          {site.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900 dark:text-gray-100">
                          {site.overall_score ? site.overall_score.toFixed(1) : '-'}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          <ActionButton variant="view" onClick={() => setSelectedSite(site)}>
                            View
                          </ActionButton>
                          <ActionButton variant="analyze" onClick={() => handleAnalyzeSite(site.id)} disabled={analyzing}>
                            {analyzing ? 'Analyzing...' : 'Analyze'}
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
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Add New Site</h3>
              <form onSubmit={handleCreateSite} className="space-y-4">
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
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Site Type</label>
                  <select
                    value={formData.site_type}
                    onChange={(e) => setFormData({ ...formData, site_type: e.target.value })}
                    className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  >
                    <option value="proposed_bridge">Proposed Bridge</option>
                    <option value="proposed_flyover">Proposed Flyover</option>
                    <option value="existing_bridge">Existing Bridge</option>
                    <option value="existing_flyover">Existing Flyover</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Location Name</label>
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
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Area (sq km)</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.area_sqkm}
                    onChange={(e) => setFormData({ ...formData, area_sqkm: parseFloat(e.target.value) })}
                    className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div className="flex justify-end space-x-3 pt-4">
                  <Button variant="secondary" onClick={() => setShowCreateModal(false)}>
                    Cancel
                  </Button>
                  <Button type="submit">Create Site</Button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {selectedSite && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center px-4 pt-4">
            <div className="fixed inset-0 bg-black/50" onClick={() => setSelectedSite(null)}></div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto p-6 relative z-10">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-gray-900 dark:text-white">{selectedSite.name}</h3>
                <button onClick={() => setSelectedSite(null)} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Type</p>
                    <p className="font-medium text-gray-900 dark:text-white">{selectedSite.site_type}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Status</p>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(selectedSite.status)}`}>
                      {selectedSite.status}
                    </span>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Location</p>
                    <p className="font-medium text-gray-900 dark:text-white">{selectedSite.location_name}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Coordinates</p>
                    <p className="font-medium text-gray-900 dark:text-white">{selectedSite.latitude}, {selectedSite.longitude}</p>
                  </div>
                </div>
                {selectedSite.description && (
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-4">Description</p>
                    <p className="font-medium text-gray-900 dark:text-white">{selectedSite.description}</p>
                  </div>
                )}
                {selectedSite.overall_score && (
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-4">Overall Score</p>
                    <div className="flex items-center mt-1">
                      <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full"
                          style={{ width: `${selectedSite.overall_score * 10}%` }}
                        ></div>
                      </div>
                      <span className="ml-2 text-sm font-medium text-gray-900 dark:text-white">{selectedSite.overall_score.toFixed(1)}/10</span>
                    </div>
                  </div>
                )}
                {selectedSite.ai_recommendation && (
                  <div className="mt-4">
                    <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">AI Recommendation</p>
                    <div className="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                      {selectedSite.ai_recommendation}
                    </div>
                  </div>
                )}
              </div>
              <div className="mt-6 flex justify-end">
                <Button variant="secondary" onClick={() => setSelectedSite(null)}>
                  Close
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
