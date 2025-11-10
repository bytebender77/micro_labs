# Quick Start Guide - HealthGuide Fever Helpline

Get up and running with HealthGuide in 5 minutes!

## 🚀 Quick Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd fever-helpline-healthguide
```

### 2. Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API key (OpenAI or Gemini)
# OPENAI_API_KEY=your_key_here
# or
# GEMINI_API_KEY=your_key_here

# Run backend
python run.py
```

Backend will run on `http://localhost:8000`

### 3. Frontend Setup (2 minutes)

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:3000`

### 4. Test the Application

1. Open `http://localhost:3000` in your browser
2. Accept the disclaimer
3. Start chatting with HealthGuide!

## 📋 Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] OpenAI API key OR Gemini API key
- [ ] Internet connection

## 🔑 Getting API Keys

### OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Go to API Keys section
4. Create new API key
5. Copy the key to your `.env` file

### Google Gemini API Key

1. Go to [makersuite.google.com](https://makersuite.google.com)
2. Sign up or log in
3. Go to API Keys section
4. Create new API key
5. Copy the key to your `.env` file

## 🧪 Test the API

### Test Triage Endpoint

```bash
curl -X POST http://localhost:8000/api/triage \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-123",
    "message": "I have a fever",
    "conversation_history": []
  }'
```

### Test Health Check

```bash
curl http://localhost:8000/health
```

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'app'`
**Solution**: Make sure you're in the `backend` directory when running the server

**Problem**: `API key not found`
**Solution**: Check your `.env` file and make sure the API key is set correctly

**Problem**: `Port already in use`
**Solution**: Change the port in `config.py` or kill the process using port 8000

### Frontend Issues

**Problem**: `Cannot connect to backend`
**Solution**: Make sure the backend is running on port 8000

**Problem**: `CORS error`
**Solution**: Check `ALLOWED_ORIGINS` in backend `.env` file

**Problem**: `npm install fails`
**Solution**: Try deleting `node_modules` and `package-lock.json`, then run `npm install` again

## 📚 Next Steps

1. **Read the README**: Check `README.md` for detailed documentation
2. **Review Deployment Guide**: See `DEPLOYMENT.md` for production deployment
3. **Explore the Code**: Check `PROJECT_STRUCTURE.md` for code organization
4. **Run Tests**: Execute `pytest tests/ -v` to run tests

## 🎯 Example Usage

### Start a Conversation

1. Open the application in your browser
2. Accept the disclaimer
3. Type: "I have a fever"
4. Follow the conversation flow
5. Receive triage assessment

### Test Red Flag Detection

1. Type: "I have chest pain"
2. HealthGuide should immediately redirect to emergency care
3. No further questions should be asked

### Test Provider Search

1. Complete a conversation
2. Click "Find Nearby Healthcare Providers"
3. View the list of providers

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure
- Use environment variables for all sensitive data
- Don't share your API keys publicly

## 📞 Support

If you encounter any issues:

1. Check the troubleshooting section
2. Review the documentation
3. Check the GitHub issues
4. Contact support

## 🎉 You're Ready!

You now have HealthGuide running locally. Start exploring the features and customize it for your needs!

---

**Note**: This is a development setup. For production deployment, see `DEPLOYMENT.md`.

