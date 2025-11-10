# Project Tree Structure

```
fever-helpline-healthguide/
│
├── 📁 backend/                          # FastAPI Backend
│   ├── 📁 app/                         # Main application package
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI application entry point
│   │   ├── config.py                   # Configuration settings
│   │   ├── models.py                   # Pydantic data models
│   │   ├── database.py                 # Database setup and session management
│   │   ├── llm_service.py              # LLM integration (OpenAI/Gemini)
│   │   ├── red_flags.py                # Red flag symptom detection
│   │   └── providers.py                # Healthcare provider service
│   │
│   ├── 📁 prompts/                     # LLM prompt templates
│   │   ├── system_prompt_healthguide.txt
│   │   └── triage_prompt.txt
│   │
│   ├── 📁 data/                        # Data files
│   │   ├── mock_providers.json
│   │   └── 📁 samples/                 # Sample data
│   │       ├── example_conversation.md
│   │       └── sample_conversation.json
│   │
│   ├── 📁 tests/                       # Test files
│   │   ├── test_red_flags.py
│   │   └── test_triage.py
│   │
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example                    # Environment variables template
│   └── run.py                          # Run script
│
├── 📁 frontend/                        # React Frontend
│   ├── 📁 src/                        # Source files
│   │   ├── 📁 components/             # React components
│   │   │   ├── ChatBot.jsx
│   │   │   ├── ChatBot.css
│   │   │   ├── Message.jsx
│   │   │   ├── Message.css
│   │   │   ├── MessageList.jsx
│   │   │   ├── MessageList.css
│   │   │   ├── MessageInput.jsx
│   │   │   ├── MessageInput.css
│   │   │   ├── Disclaimer.jsx
│   │   │   ├── Disclaimer.css
│   │   │   ├── LanguageSelector.jsx
│   │   │   ├── LanguageSelector.css
│   │   │   ├── TriageSummary.jsx
│   │   │   ├── TriageSummary.css
│   │   │   ├── ProvidersButton.jsx
│   │   │   └── ProvidersButton.css
│   │   │
│   │   ├── App.jsx                    # Main app component
│   │   ├── App.css                    # App styles
│   │   ├── main.jsx                   # Entry point
│   │   └── index.css                  # Global styles
│   │
│   ├── package.json                   # Node.js dependencies
│   ├── vite.config.js                 # Vite configuration
│   └── index.html                     # HTML template
│
├── 📄 README.md                       # Main documentation
├── 📄 QUICKSTART.md                   # Quick start guide
├── 📄 DEPLOYMENT.md                   # Deployment guide
├── 📄 PROJECT_STRUCTURE.md            # Project structure details
├── 📄 PROJECT_SUMMARY.md              # Project summary
├── 📄 TREE.md                         # This file
├── 📄 .gitignore                      # Git ignore file
├── 📄 healthguide.py                  # Original standalone version (legacy)
└── 📄 README.md (original)            # Original README
```

## File Count Summary

### Backend
- **Python Files**: 8
- **Prompt Templates**: 2
- **Test Files**: 2
- **Data Files**: 3
- **Configuration Files**: 3

### Frontend
- **React Components**: 8
- **CSS Files**: 8
- **Configuration Files**: 3

### Documentation
- **Markdown Files**: 6

### Total
- **Source Files**: ~40+
- **Documentation Files**: 6
- **Configuration Files**: 6

## Key Files

### Backend Core
- `backend/app/main.py` - FastAPI application
- `backend/app/llm_service.py` - LLM integration
- `backend/app/red_flags.py` - Red flag detection
- `backend/app/models.py` - Data models
- `backend/app/database.py` - Database setup

### Frontend Core
- `frontend/src/App.jsx` - Main app component
- `frontend/src/components/ChatBot.jsx` - Chatbot logic
- `frontend/src/components/Message.jsx` - Message display
- `frontend/src/components/TriageSummary.jsx` - Triage display

### Configuration
- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - Node.js dependencies
- `backend/.env.example` - Environment variables template

### Documentation
- `README.md` - Main documentation
- `QUICKSTART.md` - Quick start guide
- `DEPLOYMENT.md` - Deployment guide
- `PROJECT_STRUCTURE.md` - Structure details
- `PROJECT_SUMMARY.md` - Project summary

## Directory Sizes (Estimated)

### Backend
- `app/` - ~50 KB (Python source code)
- `prompts/` - ~5 KB (Text files)
- `data/` - ~10 KB (JSON and sample data)
- `tests/` - ~5 KB (Test files)

### Frontend
- `src/` - ~30 KB (React source code)
- `components/` - ~20 KB (Component files)
- CSS files - ~15 KB (Styles)

### Documentation
- Markdown files - ~50 KB (Documentation)

## Dependencies

### Backend Dependencies
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- OpenAI
- Google Generative AI
- pytest

### Frontend Dependencies
- React
- Vite
- Axios
- React Icons

## Build Outputs

### Backend
- `__pycache__/` - Python cache (ignored)
- `*.db` - SQLite database (ignored)
- `venv/` - Virtual environment (ignored)

### Frontend
- `dist/` - Build output (ignored)
- `node_modules/` - Dependencies (ignored)

## Environment Files

### Backend
- `.env` - Environment variables (not in repo)
- `.env.example` - Template file

### Frontend
- `.env` - Environment variables (not in repo)
- `.env.example` - Template file (if created)

## Git Ignored Files

- `__pycache__/`
- `*.pyc`
- `*.db`
- `*.sqlite`
- `venv/`
- `env/`
- `.env`
- `node_modules/`
- `dist/`
- `build/`
- `*.log`

## Notes

- All source files are properly organized
- Documentation is comprehensive
- Tests are included
- Configuration templates are provided
- Git ignore is configured
- Project is ready for deployment

