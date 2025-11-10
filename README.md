# HealthGuide - Fever Helpline

A comprehensive AI-powered digital assistant that provides instant, safe, and multilingual help for fever-related concerns through a chatbot interface.

## 🌟 Features

- **AI-Powered Triage**: Intelligent symptom assessment using OpenAI or Google Gemini
- **Red Flag Detection**: Immediate identification of emergency symptoms
- **Multi-language Support**: English, Hindi, and Spanish
- **Healthcare Provider Locator**: Find nearby clinics, hospitals, and pharmacies
- **Conversation Tracking**: Session management and conversation history
- **Responsive UI**: Mobile-friendly chatbot interface
- **Safety First**: Prioritizes user safety with immediate emergency redirection

## 📁 Project Structure

```
fever-helpline-healthguide/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration settings
│   │   ├── models.py            # Pydantic models
│   │   ├── database.py          # Database setup
│   │   ├── llm_service.py       # LLM integration
│   │   ├── red_flags.py         # Red flag detection
│   │   └── providers.py         # Healthcare provider service
│   ├── prompts/
│   │   ├── system_prompt_healthguide.txt
│   │   └── triage_prompt.txt
│   ├── data/
│   │   ├── mock_providers.json
│   │   └── samples/
│   │       └── sample_conversation.json
│   ├── tests/
│   │   ├── test_red_flags.py
│   │   └── test_triage.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatBot.jsx
│   │   │   ├── Message.jsx
│   │   │   ├── MessageList.jsx
│   │   │   ├── MessageInput.jsx
│   │   │   ├── Disclaimer.jsx
│   │   │   ├── LanguageSelector.jsx
│   │   │   ├── TriageSummary.jsx
│   │   │   └── ProvidersButton.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- OpenAI API key OR Google Gemini API key

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

5. **Run the backend server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

4. **Open browser**:
   Navigate to `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
MAPS_API_KEY=your_google_maps_api_key_here

# Database
DATABASE_URL=sqlite:///./healthguide.db

# LLM Provider (openai or gemini)
LLM_PROVIDER=openai

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 📡 API Endpoints

### POST `/api/triage`
Process user message and provide triage guidance.

**Request**:
```json
{
  "session_id": "uuid",
  "message": "I have a fever",
  "conversation_history": []
}
```

**Response**:
```json
{
  "session_id": "uuid",
  "message": "Response message",
  "triage_result": {
    "triage_level": "SELF_CARE",
    "escalate": false,
    "summary": "Mild fever symptoms",
    "recommended_next_steps": ["Rest", "Stay hydrated"],
    "next_question": "How long have you had this fever?",
    "red_flag_detected": false
  },
  "conversation_complete": false
}
```

### GET `/api/summary/{session_id}`
Get conversation summary for a session.

### POST `/api/providers`
Get nearby healthcare providers.

**Request**:
```json
{
  "latitude": 37.7749,
  "longitude": -122.4194,
  "radius": 10,
  "provider_type": "clinic"
}
```

### POST `/api/session`
Create a new conversation session.

## 🧪 Testing

Run tests from the backend directory:

```bash
pytest tests/ -v
```

## 🚨 Red Flag Symptoms

The system immediately redirects users to emergency care if any of these symptoms are detected:

- Severe difficulty breathing
- Chest pain or pressure
- Confusion or inability to stay awake
- Bluish lips or face
- Seizure
- Severe dehydration (no urine 8+ hours, sunken eyes)
- Severe headache or stiff neck with light sensitivity
- Rash that does not fade when pressed

## 🛡️ Safety & Disclaimer

**IMPORTANT**: HealthGuide is NOT a medical professional and cannot provide diagnoses. This tool is for informational purposes only and is not a substitute for professional medical diagnosis or treatment. Always consult a human doctor for serious symptoms.

## 📝 License

This project is provided as-is for educational and informational purposes.

## 🤝 Contributing

Contributions are welcome! Please ensure that all safety guidelines are followed and that the code maintains the highest standards of user safety.

## 📧 Support

For issues or questions, please open an issue on the GitHub repository.
