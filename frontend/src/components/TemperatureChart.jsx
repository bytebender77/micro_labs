import { useState, useEffect } from 'react'
import axios from 'axios'
import './TemperatureChart.css'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const TemperatureChart = ({ sessionId }) => {
  const [tempData, setTempData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (sessionId) {
      fetchTemperatureHistory(sessionId)
    }
  }, [sessionId])

  const fetchTemperatureHistory = async (sessionId) => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_BASE_URL}/api/temperature/${sessionId}`)
      // Reverse to show chronological order (oldest to newest)
      const temperatures = (response.data.temperatures || []).reverse()
      setTempData(temperatures)
    } catch (error) {
      console.error('Error fetching temperature history:', error)
      setTempData([])
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="temperature-chart-loading">Loading temperature data...</div>
  }

  if (tempData.length === 0) {
    return (
      <div className="temperature-chart-empty">
        <p>No temperature data recorded yet.</p>
        <p className="hint">Record your temperature to see a chart here.</p>
      </div>
    )
  }

  // Simple chart using CSS (can be enhanced with Chart.js later)
  const maxTemp = Math.max(...tempData.map(d => d.temperature))
  const minTemp = Math.min(...tempData.map(d => d.temperature))
  const range = maxTemp - minTemp || 1

  return (
    <div className="temperature-chart">
      <h3 className="chart-title">Temperature Trend</h3>
      <div className="chart-container">
        <div className="chart-y-axis">
          <span className="y-label">{Math.ceil(maxTemp)}°F</span>
          <span className="y-label">{Math.floor(minTemp)}°F</span>
        </div>
        <div className="chart-area">
          <div className="fever-threshold" style={{ bottom: `${((100 - minTemp) / range) * 100}%` }}>
            <span className="threshold-label">Fever (100°F)</span>
          </div>
          <svg className="chart-svg" viewBox="0 0 400 200">
            <polyline
              fill="none"
              stroke="#667eea"
              strokeWidth="2"
              points={tempData.map((d, i) => {
                const x = (i / (tempData.length - 1 || 1)) * 400
                const y = 200 - ((d.temperature - minTemp) / range) * 200
                return `${x},${y}`
              }).join(' ')}
            />
            {tempData.map((d, i) => {
              const x = (i / (tempData.length - 1 || 1)) * 400
              const y = 200 - ((d.temperature - minTemp) / range) * 200
              return (
                <circle
                  key={i}
                  cx={x}
                  cy={y}
                  r="4"
                  fill="#667eea"
                />
              )
            })}
          </svg>
          <div className="chart-x-axis">
            {tempData.map((d, i) => (
              <span key={i} className="x-label">
                {new Date(d.recorded_at).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}
              </span>
            ))}
          </div>
        </div>
      </div>
      <div className="chart-stats">
        <div className="stat">
          <span className="stat-label">Latest:</span>
          <span className="stat-value">{tempData[tempData.length - 1]?.temperature}°F</span>
        </div>
        <div className="stat">
          <span className="stat-label">Highest:</span>
          <span className="stat-value">{maxTemp}°F</span>
        </div>
        <div className="stat">
          <span className="stat-label">Lowest:</span>
          <span className="stat-value">{minTemp}°F</span>
        </div>
      </div>
    </div>
  )
}

export default TemperatureChart
