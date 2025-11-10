import React from 'react'
import './Disclaimer.css'

const DISCLAIMER_TEXT = {
  en: "I am an AI assistant, not a medical professional. My advice is for informational purposes only and is not a substitute for professional medical diagnosis or treatment. Always consult a human doctor for serious symptoms.",
  hi: "मैं एक AI सहायक हूं, चिकित्सा पेशेवर नहीं। मेरी सलाह केवल सूचनात्मक उद्देश्यों के लिए है और यह पेशेवर चिकित्सा निदान या उपचार का विकल्प नहीं है। गंभीर लक्षणों के लिए हमेशा एक मानव चिकित्सक से परामर्श करें।",
  es: "Soy un asistente de IA, no un profesional médico. Mi consejo es solo para fines informativos y no sustituye el diagnóstico o tratamiento médico profesional. Siempre consulte a un médico humano para síntomas graves."
}

function Disclaimer({ onAccept, language = 'en' }) {
  const text = DISCLAIMER_TEXT[language] || DISCLAIMER_TEXT.en

  return (
    <div className="disclaimer-overlay">
      <div className="disclaimer-modal">
        <div className="disclaimer-icon">⚠️</div>
        <h2>Important Disclaimer</h2>
        <p>{text}</p>
        <button className="disclaimer-button" onClick={onAccept}>
          I Understand
        </button>
      </div>
    </div>
  )
}

export default Disclaimer

