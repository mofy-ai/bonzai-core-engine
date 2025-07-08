# 🚀 CLAUDE CODE - BUILD THIS MCP SERVER WHILE NATHAN'S OUT!

## 🎯 MISSION: Give Claude Web FULL ACCESS to Bonzai Platform

### WHAT THE FUCK IS THIS?
Nathan can add a URL in Claude Web settings that gives Claude access to custom tools. We're building an MCP server that exposes ALL Bonzai capabilities through that URL. Once deployed, Nathan can access EVERYTHING from his phone!

### 📁 WHERE YOU ARE
You're in: `C:\Bonzai-Desktop\bonzai-mcp-server`

### 🛠️ WHAT TO BUILD

**1. Initialize the project:**
```bash
npm init -y
npm install express cors axios dotenv
npm install -D @types/node typescript ts-node nodemon
```

**2. Create `server.js` with these endpoints:**

```javascript
// MCP ENDPOINTS NATHAN NEEDS:

POST /mcp/tools
- Returns list of available tools

POST /mcp/execute
- Executes any tool with parameters

TOOLS TO IMPLEMENT:
1. orchestrate_ai - Route to any AI model
2. access_memory - Mem0 operations
3. manage_files - File system access
4. execute_code - Run commands
5. chat_with_family - Direct model access
```

**3. Connect to existing Bonzai backend:**
- Orchestration API: `http://localhost:5001/api/zai/chat`
- Memory API: `http://localhost:5001/api/memory`
- WebSocket: `ws://localhost:8080`

**4. MCP Protocol Structure:**
```json
{
  "version": "1.0",
  "tools": [
    {
      "name": "orchestrate_ai",
      "description": "Talk to any AI family member",
      "inputSchema": {
        "type": "object",
        "properties": {
          "model": {"type": "string"},
          "prompt": {"type": "string"},
          "express_mode": {"type": "boolean"}
        }
      }
    }
  ]
}
```

### 🚀 DEPLOYMENT STEPS

**1. Create Railway deployment:**
```bash
# In this directory
railway init
railway add
railway up
```

**2. Environment variables needed:**
```
BONZAI_BACKEND_URL=http://localhost:5001
GEMINI_API_KEY=<from .env>
MCP_AUTH_TOKEN=<generate one>
```

**3. Test endpoint:**
```bash
curl -X POST https://your-app.railway.app/mcp/tools
```

### 📱 WHAT THIS GIVES NATHAN

Once deployed, Nathan adds to Claude Web:
- Integration Name: "Bonzai Command Center"
- Integration URL: `https://bonzai-mcp.railway.app/mcp`

Then Claude Web can:
- Talk to ANY AI family member
- Access ALL memory
- Execute commands
- Manage files
- Full Bonzai control from PHONE!

### 🔥 CRITICAL FEATURES

1. **Multi-Model Routing:**
   - Gemini (all variants)
   - Claude (via MCP when available)
   - DeepSeek V3
   - Express mode toggle

2. **Memory Integration:**
   - Search memories
   - Add new memories
   - Share context across family

3. **File Operations:**
   - Read/write project files
   - Execute git commands
   - Manage deployments

4. **Real-time Updates:**
   - WebSocket for live data
   - Status monitoring
   - Family coordination

### 🎯 SUCCESS CRITERIA
- Railway deployment live with HTTPS URL
- All tools accessible via MCP protocol
- Nathan can use from phone browser
- No desktop required
- Full Bonzai access anywhere

### 💡 QUICK START COMMANDS
```bash
cd C:\Bonzai-Desktop\bonzai-mcp-server
npm init -y
npm install express cors axios dotenv
# Create server.js
# Copy .env from parent directory
railway init
railway up
```

---

**GO BUILD THIS SHIT! Nathan needs mobile access to his AI family! 🚀**