import React, { useState } from 'react'
import VoiceInput from './VoiceInput'
import './MessageInput.css'

function MessageInput({ onSendMessage, disabled, placeholder, language }) {
  const [message, setMessage] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !disabled) {
      onSendMessage(message)
      setMessage('')
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleVoiceTranscript = (transcript) => {
    setMessage(transcript)
    // Optionally auto-send after voice input
    // onSendMessage(transcript)
  }

  return (
    <form className="message-input-form" onSubmit={handleSubmit}>
      <div className="message-input-wrapper">
        <VoiceInput onTranscript={handleVoiceTranscript} language={language} />
        <input
          type="text"
          className="message-input"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={placeholder}
          disabled={disabled}
        />
        <button 
          type="submit" 
          className="send-button"
          disabled={disabled || !message.trim()}
        >
          Send
        </button>
      </div>
    </form>
  )
}

export default MessageInput

