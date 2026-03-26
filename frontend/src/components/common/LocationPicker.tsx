/// <reference types="google.maps" />
import { useState, useEffect, useRef, useCallback } from 'react'

declare global {
  interface Window {
    google: typeof google
    initGoogleMaps: () => void
  }
}

interface LocationPickerProps {
  latitude: number
  longitude: number
  locationName?: string
  onLocationChange: (lat: number, lng: number, address?: string) => void
  onLocationNameChange?: (name: string) => void
}

const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''

export default function LocationPicker({
  latitude,
  longitude,
  locationName = '',
  onLocationChange,
  onLocationNameChange,
}: LocationPickerProps) {
  const mapRef = useRef<HTMLDivElement>(null)
  const [mapLoaded, setMapLoaded] = useState(false)
  const [mapError, setMapError] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState(locationName)
  const mapInstanceRef = useRef<google.maps.Map | null>(null)
  const markerRef = useRef<google.maps.Marker | null>(null)
  const autocompleteRef = useRef<google.maps.places.Autocomplete | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (!GOOGLE_MAPS_API_KEY) {
      setMapError('Google Maps API key not configured. Using manual coordinate entry.')
      return
    }

    if (window.google && window.google.maps) {
      setMapLoaded(true)
      return
    }

    const existingScript = document.getElementById('google-maps-script')
    if (existingScript) {
      existingScript.remove()
    }

    window.initGoogleMaps = () => {
      setMapLoaded(true)
    }

    const script = document.createElement('script')
    script.id = 'google-maps-script'
    script.src = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}&libraries=places&callback=initGoogleMaps`
    script.async = true
    script.defer = true
    script.onerror = () => {
      setMapError('Failed to load Google Maps. Please check your API key.')
    }
    document.head.appendChild(script)

    return () => {
      const scriptEl = document.getElementById('google-maps-script')
      if (scriptEl) {
        scriptEl.remove()
      }
    }
  }, [])

  useEffect(() => {
    if (!mapLoaded || !mapRef.current || mapInstanceRef.current) return

    const defaultCenter = { lat: latitude || 16.5061, lng: longitude || 80.6460 }
    
    const map = new google.maps.Map(mapRef.current, {
      center: defaultCenter,
      zoom: 12,
      mapTypeControl: false,
      streetViewControl: false,
      fullscreenControl: false,
    })

    const marker = new google.maps.Marker({
      position: defaultCenter,
      map: map,
      draggable: true,
      title: 'Site Location',
    })

    marker.addListener('dragend', () => {
      const position = marker.getPosition()
      if (position) {
        const lat = position.lat()
        const lng = position.lng()
        onLocationChange(lat, lng)
        
        const geocoder = new google.maps.Geocoder()
        geocoder.geocode({ location: { lat, lng } }, (results, status) => {
          if (status === 'OK' && results && results[0]) {
            const address = results[0].formatted_address
            if (onLocationNameChange) {
              onLocationNameChange(address)
              setSearchQuery(address)
            }
          }
        })
      }
    })

    map.addListener('click', (e: google.maps.MapMouseEvent) => {
      if (e.latLng) {
        const lat = e.latLng.lat()
        const lng = e.latLng.lng()
        marker.setPosition({ lat, lng })
        onLocationChange(lat, lng)
        
        const geocoder = new google.maps.Geocoder()
        geocoder.geocode({ location: { lat, lng } }, (results, status) => {
          if (status === 'OK' && results && results[0]) {
            const address = results[0].formatted_address
            if (onLocationNameChange) {
              onLocationNameChange(address)
              setSearchQuery(address)
            }
          }
        })
      }
    })

    mapInstanceRef.current = map
    markerRef.current = marker

    if (inputRef.current) {
      const autocomplete = new google.maps.places.Autocomplete(inputRef.current, {
        types: ['geocode', 'establishment'],
        componentRestrictions: { country: 'in' },
      })

      autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace()
        if (place.geometry && place.geometry.location) {
          const lat = place.geometry.location.lat()
          const lng = place.geometry.location.lng()
          const address = place.formatted_address || place.name || ''
          
          map.setCenter({ lat, lng })
          marker.setPosition({ lat, lng })
          onLocationChange(lat, lng, address)
          if (onLocationNameChange) {
            onLocationNameChange(address)
          }
        }
      })

      autocompleteRef.current = autocomplete
    }
  }, [mapLoaded, latitude, longitude, onLocationChange, onLocationNameChange])

  const handleSearch = useCallback(() => {
    if (!searchQuery || !mapInstanceRef.current || !markerRef.current) return

    const geocoder = new google.maps.Geocoder()
    geocoder.geocode({ address: searchQuery + ', India' }, (results, status) => {
      if (status === 'OK' && results && results[0].geometry) {
        const location = results[0].geometry.location
        const lat = location.lat()
        const lng = location.lng()
        const address = results[0].formatted_address
        
        mapInstanceRef.current?.setCenter({ lat, lng })
        mapInstanceRef.current?.setZoom(15)
        markerRef.current?.setPosition({ lat, lng })
        onLocationChange(lat, lng, address)
        if (onLocationNameChange) {
          onLocationNameChange(address)
        }
      }
    })
  }, [searchQuery, onLocationChange, onLocationNameChange])

  const handleManualLatChange = (value: number) => {
    onLocationChange(value, longitude)
    if (mapInstanceRef.current && markerRef.current) {
      markerRef.current.setPosition({ lat: value, lng: longitude })
      mapInstanceRef.current.panTo({ lat: value, lng: longitude })
    }
  }

  const handleManualLngChange = (value: number) => {
    onLocationChange(latitude, value)
    if (mapInstanceRef.current && markerRef.current) {
      markerRef.current.setPosition({ lat: latitude, lng: value })
      mapInstanceRef.current.panTo({ lat: latitude, lng: value })
    }
  }

  return (
    <div className="space-y-4">
      {mapError ? (
        <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
          <p className="text-sm text-yellow-700 dark:text-yellow-300">{mapError}</p>
          <p className="text-xs text-yellow-600 dark:text-yellow-400 mt-1">
            Add VITE_GOOGLE_MAPS_API_KEY to your .env file to enable map picker.
          </p>
        </div>
      ) : (
        <>
          <div className="flex gap-2">
            <input
              ref={inputRef}
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Search for a location..."
              className="flex-1 rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            />
            <button
              type="button"
              onClick={handleSearch}
              className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
            >
              Search
            </button>
          </div>

          {!mapLoaded ? (
            <div className="h-64 flex items-center justify-center bg-gray-100 dark:bg-gray-800 rounded-lg">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            </div>
          ) : (
            <div
              ref={mapRef}
              className="h-64 rounded-lg border border-gray-300 dark:border-gray-600"
            />
          )}

          <p className="text-xs text-gray-500 dark:text-gray-400">
            Click on the map or drag the marker to set the exact location.
          </p>
        </>
      )}

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Latitude
          </label>
          <input
            type="number"
            step="0.000001"
            value={latitude}
            onChange={(e) => handleManualLatChange(parseFloat(e.target.value) || 0)}
            className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Longitude
          </label>
          <input
            type="number"
            step="0.000001"
            value={longitude}
            onChange={(e) => handleManualLngChange(parseFloat(e.target.value) || 0)}
            className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-gray-900 dark:text-white focus:outline-none focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
      </div>
    </div>
  )
}
