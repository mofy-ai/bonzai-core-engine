# 🔧 BONZAI MCP SERVER - COMPLETE DOCUMENTATION

> **Nathan's Mobile AI Command Center - Claude Web Integration**  
> Comprehensive documentation for the Model Context Protocol server

---

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [MCP Protocol Implementation](#mcp-protocol-implementation)
4. [Tool Definitions](#tool-definitions)
5. [API Endpoints](#api-endpoints)
6. [Integration Examples](#integration-examples)
7. [Deployment Guide](#deployment-guide)
8. [Troubleshooting](#troubleshooting)

---

## 🌟 OVERVIEW

The Bonzai MCP Server is a Node.js-based implementation of the Model Context Protocol that provides Claude Web with full access to the entire Bonzai platform. It serves as the bridge between Claude's web interface and Nathan's comprehensive AI development ecosystem.

### 🎯 Key Features

- **9 Core Tools** - Complete access to all Bonzai capabilities
- **AI Orchestration** - Direct access to 50+ AI models
- **VM Management** - ScrapyBara Ubuntu VM spawning and control
- **Code Execution** - E2B Python sandbox integration
- **GitHub Integration** - Full repository management capabilities
- **Memory Management** - Mem0 RAG system access
- **File Operations** - Complete file system control
- **Real-time Status** - Live family member monitoring

### 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Claude Web    │────│   MCP Server    │────│  Bonzai Backend │
│   (Frontend)    │    │   (Port 3000)   │    │   (Port 5001)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        │                       │                       │
        ▼                       ▼                       ▼
  MCP Protocol            Tool Execution         Service Integration
  - Tool Discovery        - Parameter Validation  - API Routing
  - Tool Execution        - Response Formatting   - Error Handling
  - Error Handling        - Async Operations      - Rate Limiting
```

---

## 🚀 INSTALLATION & SETUP

### Prerequisites

- **Node.js** 18+ 
- **npm** or **yarn**
- **API Keys** for integrated services

### Environment Variables

Create a `.env` file in the MCP server directory:

```bash
# Server Configuration
PORT=3000
BONZAI_BACKEND_URL=http://localhost:5001
WEBSOCKET_URL=ws://localhost:8080

# API Keys - Gemini Rotation System
GOOGLE_AI_API_KEY_1=your_primary_gemini_key
GOOGLE_AI_API_KEY_2=your_secondary_gemini_key  
GOOGLE_AI_API_KEY_3=your_tertiary_gemini_key
GEMINI_API_KEY=your_fallback_gemini_key

# Additional AI APIs
ANTHROPIC_API_KEY=your_claude_key
OPENAI_API_KEY=your_openai_key

# Integrated Services
SCRAPYBARA_API_KEY=your_scrapybara_key
E2B_API_KEY=your_e2b_key
GITHUB_PAT=your_github_token
MEM0_API_KEY=your_mem0_key
```

### Installation

```bash
# Clone the repository
git clone https://github.com/nathanfyffe/bonzai-platform
cd bonzai-platform/bonzai-mcp-server

# Install dependencies
npm install

# Start the server
npm start
```

### Dependencies

```json
{
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5", 
    "axios": "^1.6.0",
    "dotenv": "^16.3.1",
    "ws": "^8.14.2",
    "socket.io-client": "^4.7.4"
  }
}
```

---

## 🔧 MCP PROTOCOL IMPLEMENTATION

### Protocol Structure

The MCP server implements the Model Context Protocol v1.0 specification with the following structure:

```javascript
// MCP Protocol Response Format
{
  "version": "1.0",
  "tools": [
    {
      "name": "tool_name",
      "description": "Tool description",
      "inputSchema": {
        "type": "object",
        "properties": {
          // Parameter definitions
        },
        "required": ["param1", "param2"]
      }
    }
  ]
}
```

### Tool Execution Flow

```javascript
// 1. Tool Discovery
POST /mcp/tools
→ Returns list of available tools

// 2. Tool Execution
POST /mcp/execute
{
  "tool": "tool_name",
  "parameters": {
    "param1": "value1",
    "param2": "value2"
  }
}
→ Returns execution results
```

### Error Handling

```javascript
// Standard Error Response
{
  "success": false,
  "tool": "tool_name",
  "error": "Error description",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🛠️ TOOL DEFINITIONS

### 1. AI Orchestration (`orchestrate_ai`)

**Purpose:** Direct communication with any AI model in the Bonzai family

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "model": {
      "type": "string",
      "description": "AI model to use",
      "enum": [
        "gemini-2.5-flash",
        "gemini-2.5-pro", 
        "claude-3.5-sonnet",
        "deepseek-v3",
        "express-mode"
      ]
    },
    "prompt": {
      "type": "string",
      "description": "Your message to the AI"
    },
    "context": {
      "type": "string",
      "description": "Additional context or system prompt"
    },
    "express_mode": {
      "type": "boolean",
      "description": "Use express mode for faster responses"
    }
  },
  "required": ["model", "prompt"]
}
```

**Example Usage:**
```javascript
{
  "tool": "orchestrate_ai",
  "parameters": {
    "model": "gemini-2.5-flash",
    "prompt": "Analyze the latest AI trends and provide insights",
    "context": "Focus on practical applications",
    "express_mode": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "tool": "orchestrate_ai",
  "result": {
    "model": "gemini-2.5-flash",
    "response": "Based on current AI trends...",
    "backend_status": "connected",
    "express_mode": true
  }
}
```

### 2. VM Agent Spawning (`spawn_vm_agent`)

**Purpose:** Create ScrapyBara Ubuntu VMs for complex AI agent tasks

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "task": {
      "type": "string",
      "description": "What to build, research, or automate"
    },
    "duration_hours": {
      "type": "number",
      "description": "How long the VM should run",
      "default": 1
    },
    "vm_type": {
      "type": "string",
      "description": "Type of VM task",
      "enum": ["development", "scraping", "research", "automation", "analysis"],
      "default": "development"
    }
  },
  "required": ["task"]
}
```

**Example Usage:**
```javascript
{
  "tool": "spawn_vm_agent",
  "parameters": {
    "task": "Build a React todo app with TypeScript",
    "duration_hours": 2,
    "vm_type": "development"
  }
}
```

### 3. VM Control (`control_vm`)

**Purpose:** Full control over active ScrapyBara VMs

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "vm_id": {
      "type": "string",
      "description": "VM instance ID"
    },
    "action": {
      "type": "string",
      "enum": ["bash", "screenshot", "browse", "type", "click", "scroll", "stop"],
      "description": "Action to perform in VM"
    },
    "command": {
      "type": "string",
      "description": "Command to run or text to type"
    },
    "url": {
      "type": "string", 
      "description": "URL to navigate to (for browse action)"
    },
    "coordinates": {
      "type": "object",
      "description": "x,y coordinates for click actions"
    }
  },
  "required": ["action"]
}
```

### 4. Code Sandbox (`run_code_sandbox`)

**Purpose:** Execute Python code in secure E2B sandbox

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "code": {
      "type": "string",
      "description": "Python code to execute"
    },
    "packages": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Python packages to install"
    },
    "timeout": {
      "type": "number",
      "description": "Execution timeout in seconds",
      "default": 30
    }
  },
  "required": ["code"]
}
```

### 5. GitHub Power Tools (`github_power_tool`)

**Purpose:** Advanced GitHub operations and repository management

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": [
        "create_repo",
        "push_code", 
        "create_pr",
        "deploy",
        "search_code",
        "get_repo_info",
        "create_issue"
      ],
      "description": "GitHub action to perform"
    },
    "repo_name": {
      "type": "string",
      "description": "Repository name"
    },
    "owner": {
      "type": "string",
      "description": "Repository owner"
    },
    "params": {
      "type": "object",
      "description": "Additional parameters"
    }
  },
  "required": ["action"]
}
```

### 6. Memory Access (`access_memory`)

**Purpose:** Search, add, or manage AI family memories via Mem0

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": ["search", "add", "list", "delete"],
      "description": "Memory operation to perform"
    },
    "query": {
      "type": "string",
      "description": "Search query or memory content"
    },
    "user_id": {
      "type": "string",
      "description": "User ID",
      "default": "nathan"
    }
  },
  "required": ["action"]
}
```

### 7. File Management (`manage_files`)

**Purpose:** Read, write, or manage files in projects

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": ["read", "write", "list", "delete", "create_dir"],
      "description": "File operation to perform"
    },
    "path": {
      "type": "string",
      "description": "File or directory path"
    },
    "content": {
      "type": "string",
      "description": "Content to write"
    }
  },
  "required": ["action", "path"]
}
```

### 8. Code Execution (`execute_code`)

**Purpose:** Execute commands, run scripts, manage deployments

**Input Schema:**
```json
{
  "type": "object", 
  "properties": {
    "command": {
      "type": "string",
      "description": "Command to execute"
    },
    "working_dir": {
      "type": "string",
      "description": "Working directory"
    },
    "timeout": {
      "type": "number",
      "description": "Timeout in seconds",
      "default": 30
    }
  },
  "required": ["command"]
}
```

### 9. Family Status (`family_status`)

**Purpose:** Get status of all AI family members and services

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "detailed": {
      "type": "boolean",
      "description": "Get detailed status information"
    }
  }
}
```

---

## 🌐 API ENDPOINTS

### Root Information

```http
GET /
```

**Response:**
```json
{
  "name": "Bonzai MCP HUB",
  "version": "2.0.0",
  "description": "Nathan's ULTIMATE AI Control Center",
  "mcp_version": "1.0",
  "capabilities": [
    "🧠 AI orchestration across 50+ models",
    "🧠 Enhanced memory with Mem0 RAG",
    "📁 File system operations", 
    "⚡ Code execution and deployments",
    "🖥️ ScrapyBara VM spawning",
    "🎮 Full VM control",
    "🐍 E2B Python sandbox execution",
    "⚡ GitHub power tools",
    "👨‍👩‍👧‍👦 Real-time family status"
  ],
  "tools": 9,
  "integrations": {
    "scrapybara": "enabled",
    "e2b": "enabled", 
    "github": "enabled",
    "mem0": "enabled"
  },
  "endpoints": {
    "tools": "/mcp/tools",
    "execute": "/mcp/execute"
  }
}
```

### Tool Discovery

```http
POST /mcp/tools
```

**Response:**
```json
{
  "version": "1.0",
  "tools": [
    {
      "name": "orchestrate_ai",
      "description": "Talk to any AI family member with full capabilities",
      "inputSchema": {
        // Full schema definition
      }
    }
    // ... all 9 tools
  ]
}
```

### Tool Execution

```http
POST /mcp/execute
```

**Request Body:**
```json
{
  "tool": "tool_name",
  "parameters": {
    // Tool-specific parameters
  }
}
```

**Response:**
```json
{
  "success": true,
  "tool": "tool_name", 
  "result": {
    // Tool-specific results
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🔗 INTEGRATION EXAMPLES

### Claude Web Integration

#### 1. Setting up MCP in Claude Web

```javascript
// Add MCP server to Claude Web configuration
{
  "mcpServers": {
    "bonzai": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "BONZAI_BACKEND_URL": "https://mofy.ai"
      }
    }
  }
}
```

#### 2. Tool Usage in Claude Web

```
User: "Can you help me build a React todo app?"

Claude: I'll help you build a React todo app using the Bonzai MCP server. Let me spawn a development VM for this task.

[Uses spawn_vm_agent tool]
```

### Custom Client Integration

```javascript
// Custom MCP Client
class BonzaiMCPClient {
  constructor(baseUrl = 'http://localhost:3000') {
    this.baseUrl = baseUrl;
  }
  
  async getTools() {
    const response = await fetch(`${this.baseUrl}/mcp/tools`, {
      method: 'POST'
    });
    return await response.json();
  }
  
  async executeTool(tool, parameters) {
    const response = await fetch(`${this.baseUrl}/mcp/execute`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({tool, parameters})
    });
    return await response.json();
  }
  
  async orchestrateAI(model, prompt, options = {}) {
    return await this.executeTool('orchestrate_ai', {
      model,
      prompt,
      ...options
    });
  }
  
  async spawnVM(task, duration = 1, vmType = 'development') {
    return await this.executeTool('spawn_vm_agent', {
      task,
      duration_hours: duration,
      vm_type: vmType
    });
  }
}

// Usage
const client = new BonzaiMCPClient();
const result = await client.orchestrateAI(
  'gemini-2.5-flash',
  'Explain quantum computing',
  {express_mode: true}
);
```

### Python Integration

```python
import requests

class BonzaiMCP:
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
    
    def get_tools(self):
        response = requests.post(f"{self.base_url}/mcp/tools")
        return response.json()
    
    def execute_tool(self, tool, parameters):
        response = requests.post(
            f"{self.base_url}/mcp/execute",
            json={"tool": tool, "parameters": parameters}
        )
        return response.json()
    
    def orchestrate_ai(self, model, prompt, **kwargs):
        return self.execute_tool("orchestrate_ai", {
            "model": model,
            "prompt": prompt,
            **kwargs
        })

# Usage
mcp = BonzaiMCP()
result = mcp.orchestrate_ai(
    "claude-3.5-sonnet",
    "Write a Python function to calculate fibonacci numbers"
)
print(result['result']['response'])
```

---

## 🚀 DEPLOYMENT GUIDE

### Local Development

```bash
# Clone and setup
git clone https://github.com/nathanfyffe/bonzai-platform
cd bonzai-platform/bonzai-mcp-server

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Start development server
npm run dev
```

### Production Deployment

#### Docker Deployment

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

# Start server
CMD ["node", "server.js"]
```

```bash
# Build and run
docker build -t bonzai-mcp-server .
docker run -p 3000:3000 --env-file .env bonzai-mcp-server
```

#### Railway Deployment

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "node server.js",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100
  }
}
```

#### Process Management (PM2)

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'bonzai-mcp-server',
    script: 'server.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'development',
      PORT: 3000
    },
    env_production: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true
  }]
};
```

```bash
# Deploy with PM2
pm2 start ecosystem.config.js --env production
pm2 save
pm2 startup
```

### Load Balancing

```nginx
# nginx.conf
upstream bonzai_mcp {
    server localhost:3000;
    server localhost:3001;
    server localhost:3002;
}

server {
    listen 80;
    server_name mcp.mofy.ai;
    
    location / {
        proxy_pass http://bonzai_mcp;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## 🔧 TROUBLESHOOTING

### Common Issues

#### 1. **Tool Execution Timeout**

**Problem:** Tools timing out during execution
```json
{
  "success": false,
  "error": "Tool execution timeout after 30s"
}
```

**Solutions:**
- Increase timeout values in tool parameters
- Check backend service connectivity
- Verify API key validity
- Monitor server resources

#### 2. **Backend Connection Failed**

**Problem:** Cannot connect to Bonzai backend
```json
{
  "success": false,
  "error": "Backend connection issue: ECONNREFUSED"
}
```

**Solutions:**
- Verify `BONZAI_BACKEND_URL` environment variable
- Check if main Flask app is running
- Ensure network connectivity
- Check firewall settings

#### 3. **API Key Rotation Issues**

**Problem:** Gemini API key rotation not working
```javascript
// Debug key rotation
function debugKeyRotation() {
  console.log(`Available keys: ${GEMINI_API_KEYS.length}`);
  console.log(`Current index: ${currentKeyIndex}`);
  console.log(`Selected key: ${getNextGeminiKey()?.substring(0, 10)}...`);
}
```

**Solutions:**
- Verify all API keys are valid
- Check key usage quotas
- Ensure environment variables are loaded
- Test individual keys manually

#### 4. **VM Spawning Failures**

**Problem:** ScrapyBara VM creation fails
```json
{
  "success": false,
  "error": "VM spawning failed: Insufficient quota"
}
```

**Solutions:**
- Verify ScrapyBara API key
- Check account quotas
- Reduce VM duration
- Try different VM types

### Debugging Tools

#### Enable Debug Logging

```javascript
// Add to server.js
const DEBUG = process.env.DEBUG === 'true';

function debugLog(message, data = null) {
  if (DEBUG) {
    console.log(`[DEBUG] ${new Date().toISOString()} - ${message}`);
    if (data) console.log(JSON.stringify(data, null, 2));
  }
}
```

#### Health Check Endpoint

```javascript
app.get('/health', (req, res) => {
  const health = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    env: {
      node_env: process.env.NODE_ENV,
      port: process.env.PORT,
      backend: process.env.BONZAI_BACKEND_URL
    },
    integrations: {
      scrapybara: !!process.env.SCRAPYBARA_API_KEY,
      e2b: !!process.env.E2B_API_KEY,
      github: !!process.env.GITHUB_PAT,
      mem0: !!process.env.MEM0_API_KEY
    }
  };
  
  res.json(health);
});
```

#### Tool Testing Script

```javascript
// test-tools.js
async function testAllTools() {
  const tools = [
    'orchestrate_ai',
    'access_memory', 
    'manage_files',
    'execute_code',
    'family_status'
  ];
  
  for (const tool of tools) {
    try {
      const result = await testTool(tool);
      console.log(`✅ ${tool}: ${result.success ? 'PASS' : 'FAIL'}`);
    } catch (error) {
      console.log(`❌ ${tool}: ERROR - ${error.message}`);
    }
  }
}

async function testTool(toolName) {
  const testParams = {
    orchestrate_ai: {
      model: 'gemini-2.5-flash',
      prompt: 'Test prompt'
    },
    access_memory: {
      action: 'search',
      query: 'test'
    },
    // ... other test parameters
  };
  
  const response = await fetch('http://localhost:3000/mcp/execute', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      tool: toolName,
      parameters: testParams[toolName] || {}
    })
  });
  
  return await response.json();
}

// Run tests
testAllTools();
```

### Monitoring

#### Simple Monitoring Dashboard

```html
<!DOCTYPE html>
<html>
<head>
    <title>Bonzai MCP Monitor</title>
    <script>
        async function checkStatus() {
            try {
                const response = await fetch('/health');
                const data = await response.json();
                document.getElementById('status').innerHTML = 
                    JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('status').innerHTML = 
                    `Error: ${error.message}`;
            }
        }
        
        setInterval(checkStatus, 5000);
        checkStatus();
    </script>
</head>
<body>
    <h1>Bonzai MCP Server Status</h1>
    <pre id="status">Loading...</pre>
</body>
</html>
```

### Performance Optimization

#### Connection Pooling

```javascript
// Add to server.js
const http = require('http');
const agent = new http.Agent({
  keepAlive: true,
  maxSockets: 50
});

// Use in axios requests
axios.defaults.httpAgent = agent;
```

#### Caching

```javascript
const cache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

function getCachedResult(key) {
  const cached = cache.get(key);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }
  return null;
}

function setCachedResult(key, data) {
  cache.set(key, {
    data,
    timestamp: Date.now()
  });
}
```

---

## 📞 SUPPORT

- **Documentation:** [Complete MCP Guide](https://docs.mofy.ai/mcp)
- **Issues:** [GitHub Issues](https://github.com/nathanfyffe/bonzai-platform/issues)
- **Contact:** nathan@mofy.ai

---

*Last Updated: January 15, 2024*  
*Version: 2.0.0*