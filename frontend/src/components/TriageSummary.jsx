import React from 'react'
import './TriageSummary.css'

const TRIAGE_LEVELS = {
  EMERGENCY: { color: '#dc3545', label: 'Emergency', icon: '🚨' },
  URGENT: { color: '#ff9800', label: 'Urgent', icon: '⚠️' },
  SELF_CARE: { color: '#28a745', label: 'Self-Care', icon: '✅' },
  FOLLOW_UP: { color: '#17a2b8', label: 'Follow-Up', icon: '📋' }
}

function TriageSummary({ triageResult }) {
  if (!triageResult) return null

  const level = TRIAGE_LEVELS[triageResult.triage_level] || TRIAGE_LEVELS.FOLLOW_UP

  return (
    <div className="triage-summary" style={{ borderColor: level.color }}>
      <div className="triage-header" style={{ backgroundColor: level.color }}>
        <span className="triage-icon">{level.icon}</span>
        <span className="triage-label">{level.label}</span>
      </div>
      <div className="triage-content">
        <h3>Summary</h3>
        <p>{triageResult.summary}</p>
        
        {triageResult.recommended_next_steps && triageResult.recommended_next_steps.length > 0 && (
          <>
            <h3>Recommended Next Steps</h3>
            <ul>
              {triageResult.recommended_next_steps.map((step, index) => (
                <li key={index}>{step}</li>
              ))}
            </ul>
          </>
        )}

        {triageResult.escalate && (
          <div className="escalate-warning">
            ⚠️ Please consult with a healthcare provider or seek emergency care.
          </div>
        )}
      </div>
    </div>
  )
}

export default TriageSummary

