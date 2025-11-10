import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './LLMProviderSelector.css'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function LLMProviderSelector({ provider, onProviderChange }) {
  const [providers, setProviders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchProviders()
  }, [])

  const fetchProviders = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/llm-providers`)
      setProviders(response.data.providers || [])
      
      // Set default provider if not already set
      if (!provider && response.data.default) {
        onProviderChange(response.data.default)
      }
    } catch (error) {
      console.error('Error fetching LLM providers:', error)
      // Fallback to default providers
      setProviders([
        { id: 'openai', name: 'OpenAI (GPT-4o Mini)', available: true },
        { id: 'gemini', name: 'Google Gemini 2.0 Flash', available: true }
      ])
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="llm-provider-selector">
        <label>AI Model: </label>
        <select disabled className="llm-provider-select">
          <option>Loading...</option>
        </select>
      </div>
    )
  }

  return (
    <div className="llm-provider-selector">
      <label>AI Model: </label>
      <select 
        value={provider || 'openai'} 
        onChange={(e) => onProviderChange(e.target.value)}
        className="llm-provider-select"
      >
        {providers.map(prov => (
          <option 
            key={prov.id} 
            value={prov.id}
            disabled={!prov.available}
          >
            {prov.name} {!prov.available ? '(Not Available)' : ''}
          </option>
        ))}
      </select>
    </div>
  )
}

export default LLMProviderSelector

