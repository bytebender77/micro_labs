// frontend/src/App.jsx
import React, { useState, useEffect } from 'react'
import ChatBot from './components/ChatBot'
import Disclaimer from './components/Disclaimer'
import LanguageSelector from './components/LanguageSelector'
import LLMProviderSelector from './components/LLMProviderSelector'
import SymptomSelector from './components/SymptomSelector'
import TemperatureChart from './components/TemperatureChart'
import ThemeToggle from './components/ThemeToggle'
import AccessibilityToggle from './components/AccessibilityToggle'
import QuickActions from './components/QuickActions'
import './App.css'

function App() {
  const [language, setLanguage] = useState('en')
  const [llmProvider, setLlmProvider] = useState('openai')
  const [showDisclaimer, setShowDisclaimer] = useState(true)

  // Optional: pass selected symptoms into ChatBot as a prefill message
  const [prefillMessage, setPrefillMessage] = useState('')
  const [symptomData, setSymptomData] = useState(null)
  const [sessionId, setSessionId] = useState(null)

  useEffect(() => {
    const disclaimerShown = localStorage.getItem('disclaimerShown')
    if (disclaimerShown) setShowDisclaimer(false)
  }, [])

  const handleDisclaimerAccept = () => {
    setShowDisclaimer(false)
    localStorage.setItem('disclaimerShown', 'true')
  }

  const handleSymptomsSubmit = (payload, summaryText) => {
    // Store structured symptom data for backend processing
    setSymptomData(payload)
    // Also create a prefill message for the chat
    setPrefillMessage(
      `${summaryText}\n\nPlease assess these symptoms for fever triage. Language: ${language.toUpperCase()}`
    )
  }

  const handleQuickAction = (action) => {
    // Handle quick actions
    switch (action) {
      case 'fever':
        setPrefillMessage('I have a fever. Can you help me assess my symptoms?')
        break
      case 'emergency':
        setPrefillMessage('EMERGENCY: I need immediate medical attention. Please help me find emergency care.')
        break
      case 'find-doctor':
        // Trigger provider search
        setPrefillMessage('I need to find a nearby doctor or healthcare provider.')
        break
      default:
        break
    }
  }

  return (
    <div className="App">
      <div className="app-container">
        <header className="app-header">
          <div className="header-top">
            <h1>🌡️ HealthGuide</h1>
            <div className="header-actions">
              <ThemeToggle />
              <AccessibilityToggle />
            </div>
          </div>
          <p className="subtitle">Fever Helpline - Your AI Health Assistant</p>
          <div className="header-controls">
            <LanguageSelector language={language} onLanguageChange={setLanguage} />
            <LLMProviderSelector provider={llmProvider} onProviderChange={setLlmProvider} />
          </div>
        </header>

        {showDisclaimer && (
          <Disclaimer onAccept={handleDisclaimerAccept} language={language} />
        )}

        {/* Quick Actions */}
        <QuickActions onAction={handleQuickAction} language={language} />

        {/* New Symptom Selector */}
        <SymptomSelector onSubmit={handleSymptomsSubmit} language={language} />

        {/* Temperature Chart */}
        {sessionId && <TemperatureChart sessionId={sessionId} />}

        {/* Pass prefillMessage and symptomData to ChatBot */}
        <ChatBot 
          language={language} 
          llmProvider={llmProvider} 
          prefillMessage={prefillMessage}
          symptomData={symptomData}
          onSessionIdChange={setSessionId}
        />
      </div>
    </div>
  )
}

export default App