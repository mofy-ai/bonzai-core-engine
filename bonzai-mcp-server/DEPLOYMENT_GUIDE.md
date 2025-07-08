# 🚀 Railway Deployment Guide

## Quick Deploy to Railway

**GitHub Repository**: https://github.com/mofy-ai/bonzai-mcp-server

### Deploy Now:
1. Visit: https://railway.com/new/github
2. Search for: `mofy-ai/bonzai-mcp-server`
3. Click "Deploy Now"
4. Add environment variables (see below)
5. Deploy!

### Environment Variables Needed:
```
BONZAI_BACKEND_URL=https://bonzai-backend.railway.app
WEBSOCKET_URL=wss://bonzai-websocket.railway.app

# Google AI API Keys (3 keys for rotation)
GOOGLE_AI_API_KEY_1=AIzaSyCrLGbHF6LBTmJggdJW-6TBmLLEKC4nr5g
GOOGLE_AI_API_KEY_2=AIzaSyB0YfTUMuMB13DZM22nvbQcest57Bal8ik
GOOGLE_AI_API_KEY_3=AIzaSyBU9JndWn2Uf1WLgbnMDmw5NHGQNRBO-_U

# Anthropic Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# OpenAI Configuration  
OPENAI_API_KEY=your_openai_api_key_here

# Legacy compatibility
GEMINI_API_KEY=AIzaSyB0YfTUMuMB13DZM22nvbQcest57Bal8ik

PORT=3000
NODE_ENV=production
```

### Expected Deployment URL:
`https://bonzai-mcp-server.railway.app`

### Test Endpoints:
- Health Check: `https://bonzai-mcp-server.railway.app/health`
- MCP Root: `https://bonzai-mcp-server.railway.app/`
- MCP Tools: `https://bonzai-mcp-server.railway.app/mcp/tools`

### Claude Web Integration:
Once deployed, add this to Claude Web integrations:
- **Name**: Bonzai Command Center  
- **URL**: `https://bonzai-mcp-server.railway.app/mcp`

## Success Criteria
✅ GitHub repository created and populated
✅ Railway.json configuration ready
✅ Package.json configured for production
✅ All 5 MCP tools implemented
✅ Health monitoring enabled

**Nathan now has FULL mobile access to the Bonzai platform! 🎉**