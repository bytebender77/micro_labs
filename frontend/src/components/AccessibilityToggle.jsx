import { useState, useEffect } from 'react'
import { FaTextHeight, FaTextWidth } from 'react-icons/fa'
import './AccessibilityToggle.css'

function AccessibilityToggle() {
  const [isLargeText, setIsLargeText] = useState(() => {
    return localStorage.getItem('largeText') === 'true'
  })

  useEffect(() => {
    // Apply large text mode to document
    if (isLargeText) {
      document.documentElement.classList.add('large-text-mode')
      localStorage.setItem('largeText', 'true')
    } else {
      document.documentElement.classList.remove('large-text-mode')
      localStorage.setItem('largeText', 'false')
    }
  }, [isLargeText])

  const toggleLargeText = () => {
    setIsLargeText(!isLargeText)
  }

  return (
    <button
      className="accessibility-toggle"
      onClick={toggleLargeText}
      aria-label={isLargeText ? 'Disable large text mode' : 'Enable large text mode'}
      title={isLargeText ? 'Disable large text mode' : 'Enable large text mode'}
    >
      {isLargeText ? <FaTextWidth /> : <FaTextHeight />}
    </button>
  )
}

export default AccessibilityToggle

