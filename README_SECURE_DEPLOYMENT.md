# 🔒 ZAI Secure API - Railway Deployment Guide

## 🚀 Secure Backend Features

- **API-ONLY MODE**: No frontend exposure, API endpoints only
- **CORS RESTRICTED**: Only mofy.ai domains allowed
- **6 AI MODELS**: Gemini 2.5 Pro, Flash, Claude 3.5 Sonnet, etc.
- **MEMORY SYSTEM**: Add and search ZAI memories
- **CHAT ORCHESTRATION**: Multi-model AI responses
- **PRODUCTION READY**: Designed for Railway deployment

## 🛡️ Security Features

- **NO FRONTEND ACCESS**: Root `/` blocked, API only
- **RESTRICTED CORS**: Only trusted domains
- **ERROR HANDLING**: Secure error responses
- **HEALTH MONITORING**: `/health` endpoint for uptime

## 📡 API Endpoints

```
GET  /health              - Health check
GET  /api/models          - List available AI models  
POST /api/chat            - Chat with ZAI models
POST /api/memory/add      - Add memory to ZAI
POST /api/memory/search   - Search ZAI memories
GET  /api/status          - Service status
```

## 🚀 Railway Deployment

1. **Push to GitHub** (already configured)
2. **Deploy to Railway** using `app_secure_api.py`
3. **Set Environment Variables**:
   - `GOOGLE_API_KEY` - Your Google AI API key
   - `ANTHROPIC_API_KEY` - Your Anthropic API key
   - `FLASK_SECRET_KEY` - Random secret key

## 🧪 Testing

```bash
# Health check
curl https://your-railway-url.up.railway.app/health

# List models
curl https://your-railway-url.up.railway.app/api/models

# Chat test
curl -X POST https://your-railway-url.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello ZAI!", "model": "gemini-2.5-pro"}'
```

## ✅ Ready for Production

This secure API version:
- ✅ Blocks all frontend access
- ✅ Exposes only necessary API endpoints  
- ✅ Includes CORS protection
- ✅ Has proper error handling
- ✅ Supports all ZAI models
- ✅ Railway deployment ready