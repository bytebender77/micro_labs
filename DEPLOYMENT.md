# Deployment Guide - HealthGuide Fever Helpline

This guide covers deploying the HealthGuide application to various platforms.

## 📋 Prerequisites

- GitHub account (for code repository)
- API keys (OpenAI/Gemini, Google Maps)
- Account on deployment platform (Render, Vercel, etc.)

## 🚀 Deployment Options

### Option 1: Render (Backend) + Vercel (Frontend)

#### Backend on Render

1. **Create Render Account**:
   - Go to [render.com](https://render.com)
   - Sign up or log in

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Service**:
   - **Name**: `healthguide-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free or Starter

4. **Environment Variables**:
   Add these in Render dashboard:
   ```
   OPENAI_API_KEY=your_key_here
   GEMINI_API_KEY=your_key_here (optional)
   MAPS_API_KEY=your_key_here (optional)
   DATABASE_URL=postgresql://user:pass@host/db (or use Render PostgreSQL)
   LLM_PROVIDER=openai
   DEBUG=False
   ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
   ```

5. **Deploy**:
   - Click "Create Web Service"
   - Render will build and deploy automatically

#### Frontend on Vercel

1. **Create Vercel Account**:
   - Go to [vercel.com](https://vercel.com)
   - Sign up or log in

2. **Import Project**:
   - Click "New Project"
   - Import your GitHub repository
   - Select the repository

3. **Configure Project**:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Environment Variables**:
   Add in Vercel dashboard:
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```

5. **Deploy**:
   - Click "Deploy"
   - Vercel will build and deploy automatically

### Option 2: Hugging Face Spaces

#### Backend

1. **Create Space**:
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Create new space
   - Select "Docker" SDK

2. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY backend/requirements.txt .
   RUN pip install -r requirements.txt
   COPY backend/ .
   CMD uvicorn app.main:app --host 0.0.0.0 --port 7860
   ```

3. **Add Secrets**:
   - Go to Settings → Secrets
   - Add API keys as secrets

#### Frontend

1. **Create Space**:
   - Create new space
   - Select "Gradio" or "Streamlit"

2. **Deploy**:
   - Upload frontend code
   - Configure environment variables

### Option 3: Docker Deployment

#### Build Docker Images

1. **Backend Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY backend/requirements.txt .
   RUN pip install -r requirements.txt
   COPY backend/ .
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Frontend Dockerfile**:
   ```dockerfile
   FROM node:16-alpine
   WORKDIR /app
   COPY frontend/package*.json ./
   RUN npm install
   COPY frontend/ .
   RUN npm run build
   FROM nginx:alpine
   COPY --from=0 /app/dist /usr/share/nginx/html
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

3. **Docker Compose**:
   ```yaml
   version: '3.8'
   services:
     backend:
       build: ./backend
       ports:
         - "8000:8000"
       environment:
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - DATABASE_URL=sqlite:///./healthguide.db
       volumes:
         - ./backend/data:/app/data
   
     frontend:
       build: ./frontend
       ports:
         - "3000:80"
       depends_on:
         - backend
   ```

4. **Deploy**:
   ```bash
   docker-compose up -d
   ```

## 🔒 Security Considerations

### Environment Variables

- **Never commit API keys** to version control
- Use environment variables for all sensitive data
- Rotate API keys regularly
- Use different keys for development and production

### CORS Configuration

- Configure `ALLOWED_ORIGINS` to only allow your frontend domain
- Never use `*` in production

### Database Security

- Use PostgreSQL or MySQL for production (not SQLite)
- Enable SSL connections
- Use strong passwords
- Regularly backup database

### API Rate Limiting

Consider adding rate limiting to prevent abuse:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/triage")
@limiter.limit("10/minute")
async def triage(request: Request, ...):
    ...
```

## 📊 Monitoring & Logging

### Backend Logging

Add logging configuration:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Health Checks

The API includes a health check endpoint:

```bash
curl https://your-backend-url/health
```

### Error Tracking

Consider integrating error tracking services:
- Sentry
- Rollbar
- LogRocket

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        uses: johnbeynon/render-deploy@v1
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

## 📱 Mobile App Considerations

### Progressive Web App (PWA)

Convert the frontend to a PWA:

1. Add `manifest.json`
2. Add service worker
3. Enable offline functionality

### Native Apps

Consider React Native for native mobile apps:
- iOS App Store
- Google Play Store

## 🌍 Multi-region Deployment

For global availability:

1. **Use CDN** (Cloudflare, AWS CloudFront)
2. **Multiple regions** (AWS, Google Cloud)
3. **Database replication** (PostgreSQL streaming replication)
4. **Load balancing** (Nginx, HAProxy)

## 📈 Scaling

### Backend Scaling

- Use multiple instances (horizontal scaling)
- Implement load balancing
- Use connection pooling for database
- Cache frequently accessed data (Redis)

### Frontend Scaling

- Use CDN for static assets
- Enable browser caching
- Implement code splitting
- Use lazy loading

## 🧪 Testing in Production

1. **Staging Environment**:
   - Create separate staging environment
   - Test all features before production

2. **Health Checks**:
   - Monitor API endpoints
   - Check database connectivity
   - Verify LLM API connections

3. **Performance Testing**:
   - Load testing (Locust, k6)
   - Stress testing
   - Capacity planning

## 📞 Support & Maintenance

### Monitoring

- Set up uptime monitoring (UptimeRobot, Pingdom)
- Monitor API response times
- Track error rates
- Monitor LLM API usage and costs

### Updates

- Regular dependency updates
- Security patches
- Feature updates
- Bug fixes

### Backup

- Regular database backups
- Code repository backups
- Configuration backups

## 🎯 Production Checklist

- [ ] Environment variables configured
- [ ] API keys secured
- [ ] CORS properly configured
- [ ] Database backups enabled
- [ ] Logging configured
- [ ] Error tracking set up
- [ ] Health checks working
- [ ] Rate limiting implemented
- [ ] SSL/TLS enabled
- [ ] Monitoring set up
- [ ] Documentation updated
- [ ] Security audit completed

## 🚨 Emergency Procedures

### If API Key is Compromised

1. Revoke compromised key immediately
2. Generate new API key
3. Update environment variables
4. Redeploy application
5. Monitor for unauthorized usage

### If Service is Down

1. Check health endpoints
2. Review logs
3. Check API quotas
4. Verify database connectivity
5. Check deployment status

### If Data Breach Occurs

1. Immediately secure systems
2. Notify affected users
3. Investigate breach
4. Implement fixes
5. Report to authorities if required

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [React Deployment](https://react.dev/learn/start-a-new-react-project)

