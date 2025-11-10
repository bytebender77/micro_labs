import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import MessageList from './MessageList'
import MessageInput from './MessageInput'
import TriageSummary from './TriageSummary'
import ProvidersButton from './ProvidersButton'
import './ChatBot.css'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function ChatBot({ language, llmProvider, prefillMessage, symptomData, onSessionIdChange }) {
  const [messages, setMessages] = useState([])
  const [sessionId, setSessionId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [conversationComplete, setConversationComplete] = useState(false)
  const [triageResult, setTriageResult] = useState(null)
  const [showProviders, setShowProviders] = useState(false)
  const messagesEndRef = useRef(null)
  const prefillSentRef = useRef(false)

  useEffect(() => {
    // Initialize session
    initializeSession()
    
    // Add welcome message
    const welcomeMessage = {
      role: 'assistant',
      content: "Hello! I'm HealthGuide, your AI assistant for the Fever Helpline. I understand you're concerned about a fever. Can you tell me about your symptoms? What are you experiencing right now?",
      timestamp: new Date().toISOString()
    }
    setMessages([welcomeMessage])
  }, [])

  // Handle prefill message - automatically send when provided
  useEffect(() => {
    if (prefillMessage && prefillMessage.trim() && !prefillSentRef.current && sessionId) {
      prefillSentRef.current = true
      // Small delay to ensure session is initialized
      setTimeout(() => {
        handleSendMessage(prefillMessage, true) // Pass true to indicate this is a prefill message
      }, 500)
    }
  }, [prefillMessage, sessionId])

  useEffect(() => {
    // Scroll to bottom when messages change
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const initializeSession = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/session`)
      const newSessionId = response.data.session_id
      setSessionId(newSessionId)
      // Notify parent component of session ID
      if (onSessionIdChange) {
        onSessionIdChange(newSessionId)
      }
    } catch (error) {
      console.error('Error initializing session:', error)
      // Fallback to local session ID
      const fallbackSessionId = `session-${Date.now()}`
      setSessionId(fallbackSessionId)
      if (onSessionIdChange) {
        onSessionIdChange(fallbackSessionId)
      }
    }
  }

  const handleSendMessage = async (message, isPrefill = false) => {
    if (!message.trim() || loading) return

    // Add user message to UI
    const userMessage = {
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    }
    setMessages(prev => [...prev, userMessage])
    setLoading(true)

    try {
      // Prepare conversation history
      const conversationHistory = messages.map(msg => ({
        role: msg.role,
        content: msg.content
      }))

      // Prepare request payload
      const requestPayload = {
        session_id: sessionId,
        message: message,
        conversation_history: conversationHistory,
        llm_provider: llmProvider || 'openai'
      }

      // Include structured symptom data if available (only for prefill message with symptom data)
      if (symptomData && isPrefill) {
        requestPayload.symptom_data = {
          symptoms: symptomData.symptoms || [],
          by_category: symptomData.byCategory || null,
          emergency_detected: symptomData.emergencyDetected || false,
          total_selected: symptomData.totalSelected || 0,
          language: symptomData.language || language
        }
      }

      // Send to backend
      const response = await axios.post(`${API_BASE_URL}/api/triage`, requestPayload)

      // Add assistant response
      const assistantMessage = {
        role: 'assistant',
        content: response.data.message,
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, assistantMessage])

      // Update triage result
      if (response.data.triage_result) {
        setTriageResult(response.data.triage_result)
        setConversationComplete(response.data.conversation_complete)
      }

      // If red flag detected, show providers immediately
      if (response.data.triage_result?.red_flag_detected) {
        setShowProviders(true)
        setConversationComplete(true)
      }

    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage = {
        role: 'assistant',
        content: "I apologize, but I'm having trouble processing your request. Please try again or contact emergency services if this is urgent.",
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chatbot-container">
      <div className="chatbot-messages">
        <MessageList messages={messages} loading={loading} />
        <div ref={messagesEndRef} />
      </div>

      {conversationComplete && triageResult && (
        <TriageSummary triageResult={triageResult} />
      )}

      {conversationComplete && (
        <ProvidersButton 
          show={showProviders || conversationComplete}
          onToggle={() => setShowProviders(!showProviders)}
        />
      )}

      <MessageInput 
        onSendMessage={handleSendMessage} 
        disabled={loading || conversationComplete}
        placeholder={loading ? "Thinking..." : "Type your message..."}
        language={language}
      />
    </div>
  )
}

export default ChatBot

