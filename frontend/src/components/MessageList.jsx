import React from 'react'
import Message from './Message'
import './MessageList.css'

function MessageList({ messages, loading }) {
  return (
    <div className="message-list">
      {messages.map((message, index) => (
        <Message key={index} message={message} />
      ))}
      {loading && (
        <div className="message assistant">
          <div className="message-content">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default MessageList

