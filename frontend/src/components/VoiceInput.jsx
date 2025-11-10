import { useState, useEffect, useRef } from 'react'
import { FaMicrophone, FaStop } from 'react-icons/fa'
import './VoiceInput.css'

const VoiceInput = ({ onTranscript, language = 'en-US' }) => {
  const [isListening, setIsListening] = useState(false)
  const [error, setError] = useState(null)
  const recognitionRef = useRef(null)

  useEffect(() => {
    // Check if browser supports speech recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    
    if (!SpeechRecognition) {
      setError('Speech recognition is not supported in your browser')
      return
    }

    // Initialize recognition
    const recognition = new SpeechRecognition()
    recognition.continuous = false
    recognition.interimResults = false
    recognition.lang = language === 'en' ? 'en-US' : language === 'hi' ? 'hi-IN' : 'en-US'

    recognition.onstart = () => {
      setIsListening(true)
      setError(null)
    }

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript
      onTranscript?.(transcript)
      setIsListening(false)
    }

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error)
      setError(`Error: ${event.error}`)
      setIsListening(false)
    }

    recognition.onend = () => {
      setIsListening(false)
    }

    recognitionRef.current = recognition

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }
    }
  }, [language, onTranscript])

  const toggleListening = () => {
    if (!recognitionRef.current) {
      setError('Speech recognition not available')
      return
    }

    if (isListening) {
      recognitionRef.current.stop()
      setIsListening(false)
    } else {
      try {
        recognitionRef.current.start()
      } catch (err) {
        console.error('Error starting recognition:', err)
        setError('Could not start speech recognition')
      }
    }
  }

  if (error && !isListening) {
    return (
      <div className="voice-input-error">
        <span className="error-text">{error}</span>
      </div>
    )
  }

  return (
    <button
      onClick={toggleListening}
      className={`voice-btn ${isListening ? 'listening' : ''}`}
      disabled={!!error}
      aria-label={isListening ? 'Stop recording' : 'Start voice input'}
      title={isListening ? 'Stop recording' : 'Start voice input'}
    >
      {isListening ? <FaStop /> : <FaMicrophone />}
      {isListening && <span className="pulse"></span>}
    </button>
  )
}

export default VoiceInput
