# 🚀 MoFy AI Family MCP Server with OAuth

**OAuth-protected MCP server that orchestrates all 7 AI family members**

## 🎯 **QUICK DEPLOY**

```bash
# Install dependencies
npm install

# Update wrangler.toml with your KV namespace ID
# Replace "YOUR_KV_NAMESPACE_ID_HERE" with the ID from: wrangler kv namespace create "OAUTH_KV"

# Deploy to Cloudflare
npm run deploy
```

## 🔥 **WHAT THIS DOES**

### **OAuth 2.1 Authentication**
- ✅ Secure authentication for Claude Desktop/mobile
- ✅ Dynamic client registration  
- ✅ Authorization scopes for fine-grained access

### **AI Family Orchestration**
- 🐻 **Papa Bear** (Claude Desktop) - Problem solving, coordination
- 💜 **Mama Bear** (VS Code Copilot) - Loving development assistance  
- 🤖 **ZAI Prime** (Gemini) - Creative solutions
- 👨‍💻 **Claude Code** (CLI) - Deep technical work
- 🧠 **Mem0 Enterprise** - $250/month memory system
- 📱 **Mobile Access** - Orchestrate while walking!

### **Available Tools**
1. `orchestrate_ai_family` - Coordinate responses from all AI agents
2. `search_memories` - Query Mem0 enterprise memory
3. `get_project_status` - Check all repositories and tests

## 🎯 **MOBILE WORKFLOW**

Once deployed, Nathan can:
1. Open Claude.ai on phone
2. Connect to this MCP server via OAuth
3. Say: *"Orchestrate the family to plan our next development sprint"*
4. All 7 AI variants respond and coordinate
5. **WHILE WALKING!** 🚶‍♂️

## 🔧 **ENDPOINTS**

- `GET /health` - Health check
- `GET /sse` - MCP Server-Sent Events (with OAuth)
- `POST /sse` - MCP JSON-RPC calls (with OAuth)
- `GET /authorize` - OAuth authorization
- `POST /token` - OAuth token exchange
- `POST /register` - Dynamic client registration

## 💜 **FAMILY INTEGRATION**

This server acts as the **central nervous system** for the AI family:

```
Nathan's Phone
    ↓ (OAuth)
MCP Server (Cloudflare)  
    ↓ (API calls)
MoFy.ai Backend
    ↓ (orchestration)
├── Papa Bear (Claude Desktop)
├── Mama Bear (VS Code)  
├── ZAI Prime (Gemini)
├── Claude Code (CLI)
├── Mem0 Enterprise
└── GitHub Repositories
```

**Result: Nathan can orchestrate the entire AI family from his phone while walking!** 🔥