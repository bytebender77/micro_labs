import React, { useState } from 'react'
import axios from 'axios'
import './ProvidersButton.css'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function ProvidersButton({ show, onToggle }) {
  const [providers, setProviders] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFindProviders = async () => {
    setLoading(true)
    setError(null)

    try {
      // Get user's location (mock for now - in production, use geolocation API)
      const mockLocation = {
        latitude: 37.7749,
        longitude: -122.4194,
        radius: 10
      }

      const response = await axios.post(`${API_BASE_URL}/api/providers`, mockLocation)
      setProviders(response.data)
      onToggle()
    } catch (err) {
      console.error('Error fetching providers:', err)
      setError('Unable to fetch providers. Please try again later.')
    } finally {
      setLoading(false)
    }
  }

  if (!show) return null

  return (
    <div className="providers-container">
      <button 
        className="providers-button"
        onClick={handleFindProviders}
        disabled={loading}
      >
        {loading ? 'Loading...' : '📍 Find Nearby Healthcare Providers'}
      </button>

      {error && (
        <div className="providers-error">{error}</div>
      )}

      {providers.length > 0 && (
        <div className="providers-list">
          <h3>Nearby Healthcare Providers</h3>
          {providers.map(provider => (
            <div key={provider.id} className="provider-card">
              <h4>{provider.name}</h4>
              <p className="provider-type">{provider.type}</p>
              <p className="provider-address">{provider.address}</p>
              <p className="provider-phone">{provider.phone}</p>
              {provider.distance && (
                <p className="provider-distance">📍 {provider.distance} km away</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default ProvidersButton

