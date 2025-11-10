// frontend/src/components/SymptomSelector.jsx
import React, { useMemo, useState } from 'react'
import { CATEGORIES } from '../data/symptoms'
import { FaStethoscope, FaBrain, FaLungs, FaUtensils, FaDumbbell, FaAllergies, FaHeartbeat, FaTint, FaExclamationTriangle, FaSearch, FaTimes } from 'react-icons/fa'
import './SymptomSelector.css'

const ICONS = {
  general: FaStethoscope,
  neuro: FaBrain,
  resp: FaLungs,
  gi: FaUtensils,
  msk: FaDumbbell,
  skin: FaAllergies,
  cardio: FaHeartbeat,
  urinary: FaTint,
  emergency: FaExclamationTriangle,
}

function normalizeKey(text) {
  return text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '')
}

export default function SymptomSelector({ onSubmit, language = 'en' }) {
  const [category, setCategory] = useState('all')
  const [query, setQuery] = useState('')
  const [selected, setSelected] = useState(new Map())

  const flatSymptoms = useMemo(() => {
    const items = []
    for (const cat of CATEGORIES) {
      for (const label of cat.symptoms) {
        const key = `${cat.id}:${normalizeKey(label)}`
        items.push({
          key,
          label,
          categoryId: cat.id,
          categoryLabel: cat.label,
        })
      }
    }
    return items
  }, [])

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    return flatSymptoms.filter((s) => {
      const matchCat = category === 'all' || s.categoryId === category
      const matchQuery = !q || s.label.toLowerCase().includes(q)
      return matchCat && matchQuery
    })
  }, [flatSymptoms, query, category])

  const emergencySelected = useMemo(
    () => Array.from(selected.values()).some((s) => s.categoryId === 'emergency'),
    [selected]
  )

  const toggleSymptom = (item) => {
    setSelected((prev) => {
      const next = new Map(prev)
      if (next.has(item.key)) next.delete(item.key)
      else next.set(item.key, item)
      return next
    })
  }

  const clearAll = () => setSelected(new Map())

  const handleSubmit = () => {
    const selectedArr = Array.from(selected.values())
    const byCategory = selectedArr.reduce((acc, s) => {
      acc[s.categoryLabel] = acc[s.categoryLabel] || []
      acc[s.categoryLabel].push(s.label)
      return acc
    }, {})

    const payload = {
      symptoms: selectedArr.map((s) => s.label),
      byCategory,
      emergencyDetected: emergencySelected,
      totalSelected: selectedArr.length,
      language,
    }

    const summaryText = [
      'Symptoms selected:',
      ...Object.entries(byCategory).map(([cat, list]) => `- ${cat}: ${list.join(', ')}`),
    ].join('\n')

    onSubmit?.(payload, summaryText)
  }

  return (
    <section className="selector-card" aria-label="Symptom selector">
      <div className="selector-header">
        <h2>Select your symptoms</h2>
        <p className="selector-subtitle">
          Choose a category, search, and select one or more symptoms below.
        </p>
      </div>

      <div className="selector-controls">
        <div className="control">
          <label htmlFor="category" className="control-label">Category</label>
          <div className="select-wrap">
            <select
              id="category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              aria-label="Symptom category"
            >
              <option value="all">All categories</option>
              {CATEGORIES.map((c) => (
                <option key={c.id} value={c.id}>{c.label}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="control control-search">
          <label htmlFor="search" className="control-label">Search</label>
          <div className="search-wrap">
            <FaSearch className="search-icon" />
            <input
              id="search"
              type="text"
              placeholder="Type to filter symptoms..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              aria-label="Search symptoms"
            />
          </div>
        </div>
      </div>

      {emergencySelected && (
        <div className="emergency-banner" role="note" aria-live="polite">
          <FaExclamationTriangle />
          You selected one or more emergency symptoms. Consider urgent medical attention.
        </div>
      )}

      <div className="symptom-grid" role="group" aria-label="Symptoms">
        {filtered.map((item) => {
          const checked = selected.has(item.key)
          const Icon = ICONS[item.categoryId] || FaStethoscope
          return (
            <label
              key={item.key}
              className={`symptom-item ${checked ? 'checked' : ''} ${item.categoryId === 'emergency' ? 'emergency' : ''}`}
            >
              <input
                type="checkbox"
                checked={checked}
                onChange={() => toggleSymptom(item)}
                aria-checked={checked}
                aria-label={`${item.label} (${item.categoryLabel})`}
              />
              <span className="symptom-icon"><Icon /></span>
              <span className="symptom-text">{item.label}</span>
              <span className="symptom-tag">{item.categoryLabel}</span>
            </label>
          )
        })}
        {filtered.length === 0 && (
          <div className="empty-state">No symptoms match your search.</div>
        )}
      </div>

      {selected.size > 0 && (
        <div className="selected-chips" aria-label="Selected symptoms">
          {Array.from(selected.values()).map((s) => (
            <span key={s.key} className={`chip ${s.categoryId === 'emergency' ? 'chip-emergency' : ''}`}>
              {s.label}
              <button
                className="chip-remove"
                onClick={() => toggleSymptom(s)}
                aria-label={`Remove ${s.label}`}
                title="Remove"
              >
                <FaTimes />
              </button>
            </span>
          ))}
        </div>
      )}

      <div className="selector-footer">
        <button className="btn ghost" onClick={clearAll} disabled={selected.size === 0}>
          Clear
        </button>
        <button className="btn primary" onClick={handleSubmit} disabled={selected.size === 0}>
          Add to triage
        </button>
      </div>
    </section>
  )
}