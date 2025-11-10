import { FaExclamationTriangle, FaStethoscope, FaHospital } from 'react-icons/fa'
import './QuickActions.css'

function QuickActions({ onAction, language = 'en' }) {
  const actions = {
    en: {
      fever: { label: 'I have fever', icon: FaStethoscope, action: 'fever' },
      emergency: { label: 'Emergency', icon: FaExclamationTriangle, action: 'emergency' },
      findDoctor: { label: 'Find Doctor', icon: FaHospital, action: 'find-doctor' }
    },
    hi: {
      fever: { label: 'मुझे बुखार है', icon: FaStethoscope, action: 'fever' },
      emergency: { label: 'आपातकाल', icon: FaExclamationTriangle, action: 'emergency' },
      findDoctor: { label: 'डॉक्टर खोजें', icon: FaHospital, action: 'find-doctor' }
    },
    ta: {
      fever: { label: 'எனக்கு காய்ச்சல்', icon: FaStethoscope, action: 'fever' },
      emergency: { label: 'அவசரம்', icon: FaExclamationTriangle, action: 'emergency' },
      findDoctor: { label: 'மருத்துவரைக் கண்டுபிடி', icon: FaHospital, action: 'find-doctor' }
    },
    te: {
      fever: { label: 'నాకు జ్వరం', icon: FaStethoscope, action: 'fever' },
      emergency: { label: 'అత్యవసరం', icon: FaExclamationTriangle, action: 'emergency' },
      findDoctor: { label: 'డాక్టర్ కనుగొనండి', icon: FaHospital, action: 'find-doctor' }
    },
    bn: {
      fever: { label: 'আমার জ্বর আছে', icon: FaStethoscope, action: 'fever' },
      emergency: { label: 'জরুরি', icon: FaExclamationTriangle, action: 'emergency' },
      findDoctor: { label: 'ডাক্তার খুঁজুন', icon: FaHospital, action: 'find-doctor' }
    }
  }

  const currentActions = actions[language] || actions.en

  const handleClick = (action) => {
    if (onAction) {
      onAction(action)
    }
  }

  return (
    <div className="quick-actions">
      <h3 className="quick-actions-title">Quick Actions</h3>
      <div className="quick-actions-grid">
        {Object.values(currentActions).map((item, index) => {
          const Icon = item.icon
          return (
            <button
              key={index}
              className={`quick-action-btn ${item.action}`}
              onClick={() => handleClick(item.action)}
              aria-label={item.label}
            >
              <Icon className="quick-action-icon" />
              <span className="quick-action-label">{item.label}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}

export default QuickActions

