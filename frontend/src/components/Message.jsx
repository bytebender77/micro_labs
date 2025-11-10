import React from 'react'
import './Message.css'

function Message({ message }) {
  const isUser = message.role === 'user'
  const isEmergency = message.content.includes('URGENT') || message.content.includes('emergency')

  return (
    <div className={`message ${message.role} ${isEmergency ? 'emergency' : ''}`}>
      <div className="message-content">
        {isEmergency && (
          <div className="emergency-badge">⚠️ URGENT</div>
        )}
        <div className="message-text">
          {message.content.split('\n').map((line, index) => (
            <p key={index}>{line}</p>
          ))}
        </div>
        <div className="message-time">
          {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  )
}

export default Message

