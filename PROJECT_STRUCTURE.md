# Project Structure - HealthGuide Fever Helpline

## 📁 Complete Folder Structure

```
fever-helpline-healthguide/
│
├── backend/                          # FastAPI Backend
│   ├── app/                         # Main application package
│   │   ├── __init__.py             # Package initialization
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Configuration settings
│   │   ├── models.py               # Pydantic data models
│   │   ├── database.py             # Database setup and session management
│   │   ├── llm_service.py          # LLM integration (OpenAI/Gemini)
│   │   ├── red_flags.py            # Red flag symptom detection
│   │   └── providers.py            # Healthcare provider service
│   │
│   ├── prompts/                     # LLM prompt templates
│   │   ├── system_prompt_healthguide.txt    # System prompt for HealthGuide
│   │   └── triage_prompt.txt                # Triage assessment prompt
│   │
│   ├── data/                        # Data files
│   │   ├── mock_providers.json     # Mock healthcare provider data
│   │   └── samples/                 # Sample data
│   │       └── sample_conversation.json
│   │
│   ├── tests/                       # Test files
│   │   ├── test_red_flags.py       # Red flag detection tests
│   │   └── test_triage.py          # Triage logic tests
│   │
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                # Environment variables template
│   └── run.py                      # Run script
│
├── frontend/                        # React Frontend
│   ├── src/                        # Source files
│   │   ├── components/             # React components
│   │   │   ├── ChatBot.jsx        # Main chatbot component
│   │   │   ├── Message.jsx        # Message component
│   │   │   ├── MessageList.jsx    # Message list component
│   │   │   ├── MessageInput.jsx   # Message input component
│   │   │   ├── Disclaimer.jsx     # Disclaimer modal
│   │   │   ├── LanguageSelector.jsx # Language selector
│   │   │   ├── TriageSummary.jsx  # Triage summary display
│   │   │   ├── ProvidersButton.jsx # Healthcare providers button
│   │   │   └── *.css              # Component styles
│   │   │
│   │   ├── App.jsx                # Main app component
│   │   ├── App.css                # App styles
│   │   ├── main.jsx               # Entry point
│   │   └── index.css              # Global styles
│   │
│   ├── package.json               # Node.js dependencies
│   ├── vite.config.js             # Vite configuration
│   └── index.html                 # HTML template
│
├── README.md                       # Main documentation
├── DEPLOYMENT.md                   # Deployment guide
├── PROJECT_STRUCTURE.md            # This file
└── .gitignore                     # Git ignore file
```

## 📋 File Descriptions

### Backend Files

#### `app/main.py`
- FastAPI application entry point
- API endpoints: `/api/triage`, `/api/summary`, `/api/providers`, `/api/session`
- CORS configuration
- Database initialization

#### `app/config.py`
- Configuration settings using Pydantic
- Environment variable management
- CORS origins configuration

#### `app/models.py`
- Pydantic models for API requests/responses
- `Message`, `TriageResult`, `ConversationRequest`, `ConversationResponse`
- `Provider`, `ProviderRequest`, `SummaryResponse`
- Triage level enumeration

#### `app/database.py`
- SQLAlchemy database setup
- Conversation session model
- Database session management
- Save/retrieve conversation functions

#### `app/llm_service.py`
- LLM service integration (OpenAI/Gemini)
- Triage assessment logic
- Mock LLM service for testing
- Response generation

#### `app/red_flags.py`
- Red flag symptom detection
- Emergency response generation
- Keyword matching for red flags

#### `app/providers.py`
- Healthcare provider service
- Mock provider data
- Distance calculation
- Provider filtering and sorting

### Frontend Files

#### `src/App.jsx`
- Main application component
- Language selector
- Disclaimer handling
- ChatBot integration

#### `src/components/ChatBot.jsx`
- Main chatbot logic
- API communication
- Session management
- Message handling

#### `src/components/Message.jsx`
- Individual message display
- User/assistant message styling
- Emergency message highlighting

#### `src/components/MessageInput.jsx`
- Message input form
- Send button
- Keyboard shortcuts

#### `src/components/Disclaimer.jsx`
- Disclaimer modal
- Multi-language support
- User acceptance handling

#### `src/components/TriageSummary.jsx`
- Triage level display
- Summary and recommendations
- Visual indicators

#### `src/components/ProvidersButton.jsx`
- Healthcare provider search
- Provider list display
- Location-based search

### Configuration Files

#### `backend/requirements.txt`
- Python dependencies
- FastAPI, Uvicorn, Pydantic
- OpenAI, Google Generative AI
- SQLAlchemy, pytest

#### `frontend/package.json`
- Node.js dependencies
- React, Vite
- Axios for API calls
- React Icons

#### `backend/.env.example`
- Environment variable template
- API keys configuration
- Database URL
- Server configuration

## 🔄 Data Flow

1. **User sends message** → Frontend `ChatBot.jsx`
2. **API request** → Backend `/api/triage`
3. **Red flag check** → `red_flags.py`
4. **LLM processing** → `llm_service.py`
5. **Triage assessment** → `models.py` (TriageResult)
6. **Response** → Frontend `ChatBot.jsx`
7. **Display** → `Message.jsx`, `TriageSummary.jsx`

## 🗄️ Database Schema

### ConversationSession
- `session_id` (String, Primary Key)
- `messages` (JSON)
- `triage_level` (String)
- `summary` (Text)
- `created_at` (DateTime)
- `updated_at` (DateTime)
- `red_flag_detected` (String)

## 🧪 Testing Structure

### `tests/test_red_flags.py`
- Red flag detection tests
- Emergency response tests
- Keyword matching tests

### `tests/test_triage.py`
- Triage logic tests
- Mock LLM service tests
- Conversation flow tests

## 📦 Dependencies

### Backend
- FastAPI: Web framework
- Uvicorn: ASGI server
- Pydantic: Data validation
- SQLAlchemy: Database ORM
- OpenAI: LLM API
- Google Generative AI: Alternative LLM

### Frontend
- React: UI framework
- Vite: Build tool
- Axios: HTTP client
- React Icons: Icon library

## 🔐 Security Considerations

- API keys stored in environment variables
- CORS configuration
- Input validation (Pydantic)
- SQL injection protection (SQLAlchemy)
- XSS protection (React)

## 🚀 Deployment Files

### `DEPLOYMENT.md`
- Render deployment guide
- Vercel deployment guide
- Docker deployment
- CI/CD pipeline setup

### `.gitignore`
- Python cache files
- Node modules
- Environment variables
- Database files
- Build artifacts

## 📊 API Endpoints

### POST `/api/triage`
- Process user message
- Return triage result
- Update conversation session

### GET `/api/summary/{session_id}`
- Get conversation summary
- Return triage level and recommendations

### POST `/api/providers`
- Find nearby healthcare providers
- Return provider list with distances

### POST `/api/session`
- Create new conversation session
- Return session ID

## 🌍 Multi-language Support

- English (en)
- Hindi (hi)
- Spanish (es)
- Language selector in frontend
- Translated disclaimer

## 📝 Prompt Templates

### `prompts/system_prompt_healthguide.txt`
- HealthGuide system prompt
- Core principles
- Safety rules
- Conversation flow

### `prompts/triage_prompt.txt`
- Triage assessment prompt
- JSON response format
- Triage level guidelines

## 🎨 UI Components

### Chat Interface
- Message bubbles
- Typing indicator
- Scroll to bottom
- Mobile responsive

### Triage Summary
- Color-coded triage levels
- Summary display
- Recommended steps
- Emergency warnings

### Providers
- Provider cards
- Distance display
- Contact information
- Filter by type

## 📱 Responsive Design

- Mobile-friendly layout
- Touch-friendly buttons
- Responsive typography
- Adaptive grid layout

## 🔄 State Management

- React hooks (useState, useEffect)
- Local storage for disclaimer
- Session management
- Conversation history

## 🧹 Code Organization

- Modular component structure
- Separation of concerns
- Reusable components
- Clean code principles

## 📈 Scalability Considerations

- Database connection pooling
- API rate limiting (to be implemented)
- Caching (to be implemented)
- Load balancing (for production)

## 🐛 Error Handling

- Try-catch blocks
- Error messages
- Fallback responses
- Logging (to be implemented)

## 📊 Monitoring (To Be Implemented)

- Health checks
- Error tracking
- Performance monitoring
- Usage analytics

## 🔒 Privacy & Data Safety

- No personal data storage (except session)
- Session data cleanup
- Secure API communication
- Privacy policy compliance

