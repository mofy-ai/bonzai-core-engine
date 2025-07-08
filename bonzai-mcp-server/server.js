#!/usr/bin/env node
/**
 * 🚀 BONZAI MCP SERVER - Nathan's Mobile AI Command Center
 * Gives Claude Web FULL ACCESS to the entire Bonzai platform
 * 
 * What this does:
 * - Exposes ALL Bonzai capabilities via MCP protocol
 * - Allows Nathan to control everything from his phone
 * - No desktop needed - Claude Web IS the UI!
 */

import express from 'express';
import cors from 'cors';
import axios from 'axios';
import dotenv from 'dotenv';
import { WebSocket } from 'ws';
import { io } from 'socket.io-client';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));

// Bonzai backend configuration
const BONZAI_BACKEND = process.env.BONZAI_BACKEND_URL || 'http://localhost:5001';
const WEBSOCKET_URL = process.env.WEBSOCKET_URL || 'ws://localhost:8080';

// Simple API key rotation - CLEAN AND FAST!
const GEMINI_API_KEYS = [
  process.env.GOOGLE_AI_API_KEY_1,
  process.env.GOOGLE_AI_API_KEY_2,
  process.env.GOOGLE_AI_API_KEY_3
].filter(key => key);

let currentKeyIndex = 0;

function getNextGeminiKey() {
  if (GEMINI_API_KEYS.length === 0) {
    return process.env.GEMINI_API_KEY;
  }
  const key = GEMINI_API_KEYS[currentKeyIndex];
  currentKeyIndex = (currentKeyIndex + 1) % GEMINI_API_KEYS.length;
  console.log(`🔑 Using Gemini API Key ${currentKeyIndex}`);
  return key;
}

console.log('🚀 Starting Bonzai MCP HUB - The Ultimate AI Control Center!');
console.log(`🔗 Backend: ${BONZAI_BACKEND}`);
console.log(`📡 WebSocket: ${WEBSOCKET_URL}`);
console.log(`🔑 Gemini API Keys: ${GEMINI_API_KEYS.length} keys loaded for rotation`);
console.log(`🔑 Claude API Key: ${process.env.ANTHROPIC_API_KEY ? 'loaded' : 'missing'}`);
console.log(`🔑 OpenAI API Key: ${process.env.OPENAI_API_KEY ? 'loaded' : 'missing'}`);
console.log(`🖥️ ScrapyBara VM Access: ${process.env.SCRAPYBARA_API_KEY ? 'enabled' : 'disabled'}`);
console.log(`🐍 E2B Code Sandbox: ${process.env.E2B_API_KEY ? 'enabled' : 'disabled'}`);
console.log(`⚡ GitHub Power Tools: ${process.env.GITHUB_PAT ? 'enabled' : 'disabled'}`);

// MCP Protocol Implementation - THE HUB OF ULTIMATE POWER! 🚀
const MCP_TOOLS = [
  {
    name: "orchestrate_ai",
    description: "Talk to any AI family member (Gemini, Claude, DeepSeek) with full capabilities",
    inputSchema: {
      type: "object",
      properties: {
        model: {
          type: "string",
          description: "AI model to use",
          enum: ["gemini-2.5-flash", "gemini-2.5-pro", "claude-3.5-sonnet", "deepseek-v3", "express-mode"]
        },
        prompt: {
          type: "string", 
          description: "Your message to the AI"
        },
        context: {
          type: "string",
          description: "Additional context or system prompt"
        },
        express_mode: {
          type: "boolean",
          description: "Use express mode for faster responses"
        }
      },
      required: ["model", "prompt"]
    }
  },
  {
    name: "spawn_vm_agent",
    description: "🖥️ Spawn ScrapyBara Ubuntu VM for AI agent tasks (like Scout.new but MORE POWERFUL!)",
    inputSchema: {
      type: "object",
      properties: {
        task: {
          type: "string",
          description: "What to build, research, or automate (e.g. 'build a todo app', 'scrape competitor data', 'research AI trends')"
        },
        duration_hours: {
          type: "number",
          description: "How long the VM should run (default: 1 hour)",
          default: 1
        },
        vm_type: {
          type: "string", 
          description: "Type of VM task",
          enum: ["development", "scraping", "research", "automation", "analysis"],
          default: "development"
        }
      },
      required: ["task"]
    }
  },
  {
    name: "control_vm",
    description: "🎮 Control active ScrapyBara VM (run commands, take screenshots, automate browser)",
    inputSchema: {
      type: "object",
      properties: {
        vm_id: {
          type: "string",
          description: "VM instance ID"
        },
        action: {
          type: "string",
          enum: ["bash", "screenshot", "browse", "type", "click", "scroll", "stop"],
          description: "Action to perform in VM"
        },
        command: {
          type: "string", 
          description: "Command to run or text to type"
        },
        url: {
          type: "string",
          description: "URL to navigate to (for browse action)"
        },
        coordinates: {
          type: "object",
          description: "x,y coordinates for click actions"
        }
      },
      required: ["action"]
    }
  },
  {
    name: "run_code_sandbox",
    description: "🐍 Execute Python code in secure E2B sandbox environment",
    inputSchema: {
      type: "object",
      properties: {
        code: {
          type: "string",
          description: "Python code to execute"
        },
        packages: {
          type: "array",
          items: { type: "string" },
          description: "Python packages to install before execution"
        },
        timeout: {
          type: "number",
          description: "Execution timeout in seconds",
          default: 30
        }
      },
      required: ["code"]
    }
  },
  {
    name: "github_power_tool", 
    description: "⚡ Advanced GitHub operations (repos, deployments, PRs, code management)",
    inputSchema: {
      type: "object",
      properties: {
        action: {
          type: "string",
          enum: ["create_repo", "push_code", "create_pr", "deploy", "search_code", "get_repo_info", "create_issue"],
          description: "GitHub action to perform"
        },
        repo_name: {
          type: "string",
          description: "Repository name"
        },
        owner: {
          type: "string", 
          description: "Repository owner (defaults to authenticated user)"
        },
        params: {
          type: "object",
          description: "Additional parameters for the action"
        }
      },
      required: ["action"]
    }
  },
  {
    name: "access_memory",
    description: "Search, add, or manage Nathan's AI family memories",
    inputSchema: {
      type: "object", 
      properties: {
        action: {
          type: "string",
          enum: ["search", "add", "list", "delete"],
          description: "Memory operation to perform"
        },
        query: {
          type: "string",
          description: "Search query or memory content"
        },
        user_id: {
          type: "string", 
          description: "User ID (defaults to 'nathan')"
        }
      },
      required: ["action"]
    }
  },
  {
    name: "manage_files",
    description: "Read, write, or manage files in Nathan's projects",
    inputSchema: {
      type: "object",
      properties: {
        action: {
          type: "string",
          enum: ["read", "write", "list", "delete", "create_dir"],
          description: "File operation to perform"
        },
        path: {
          type: "string",
          description: "File or directory path"
        },
        content: {
          type: "string", 
          description: "Content to write (for write action)"
        }
      },
      required: ["action", "path"]
    }
  },
  {
    name: "execute_code",
    description: "Execute commands, run scripts, or manage deployments",
    inputSchema: {
      type: "object",
      properties: {
        command: {
          type: "string",
          description: "Command to execute"
        },
        working_dir: {
          type: "string",
          description: "Working directory (optional)"
        },
        timeout: {
          type: "number",
          description: "Timeout in seconds (default: 30)"
        }
      },
      required: ["command"]
    }
  },
  {
    name: "family_status",
    description: "Get status of all AI family members and services",
    inputSchema: {
      type: "object",
      properties: {
        detailed: {
          type: "boolean",
          description: "Get detailed status information"
        }
      }
    }
  }
];

// Root endpoint - MCP server info
app.get('/', (req, res) => {
  res.json({
    name: "Bonzai MCP HUB",
    version: "2.0.0", 
    description: "Nathan's ULTIMATE AI Control Center - More Powerful Than Scout.new!",
    mcp_version: "1.0",
    capabilities: [
      "🧠 AI orchestration across 50+ models",
      "🧠 Enhanced memory with Mem0 RAG", 
      "📁 File system operations",
      "⚡ Code execution and deployments",
      "🖥️ ScrapyBara VM spawning (Ubuntu desktops)",
      "🎮 Full VM control (bash, browser, screenshots)",
      "🐍 E2B Python sandbox execution",
      "⚡ GitHub power tools (repos, PRs, issues)",
      "👨‍👩‍👧‍👦 Real-time family status"
    ],
    tools: MCP_TOOLS.length,
    integrations: {
      scrapybara: process.env.SCRAPYBARA_API_KEY ? "enabled" : "disabled",
      e2b: process.env.E2B_API_KEY ? "enabled" : "disabled", 
      github: process.env.GITHUB_PAT ? "enabled" : "disabled",
      mem0: process.env.MEM0_API_KEY ? "enabled" : "disabled"
    },
    endpoints: {
      tools: "/mcp/tools",
      execute: "/mcp/execute"
    },
    backend: BONZAI_BACKEND,
    status: "🚀 READY TO DOMINATE!"
  });
});

// MCP Tools endpoint
app.post('/mcp/tools', (req, res) => {
  console.log('📋 MCP Tools requested');
  res.json({
    version: "1.0",
    tools: MCP_TOOLS
  });
});

// MCP Execute endpoint - The main orchestration hub
app.post('/mcp/execute', async (req, res) => {
  const { tool, parameters } = req.body;
  
  console.log(`🔧 Executing tool: ${tool}`, parameters);
  
  try {
    let result;
    
    switch (tool) {
      case 'orchestrate_ai':
        result = await executeAIOrchestration(parameters);
        break;
        
      case 'access_memory':
        result = await executeMemoryOperation(parameters);
        break;
        
      case 'manage_files':
        result = await executeFileOperation(parameters);
        break;
        
      case 'execute_code':
        result = await executeCodeOperation(parameters);
        break;
        
      case 'family_status':
        result = await getFamilyStatus(parameters);
        break;
        
      case 'spawn_vm_agent':
        result = await spawnVMAgent(parameters);
        break;
        
      case 'control_vm':
        result = await controlVM(parameters);
        break;
        
      case 'run_code_sandbox':
        result = await runCodeSandbox(parameters);
        break;
        
      case 'github_power_tool':
        result = await githubPowerTool(parameters);
        break;
        
      default:
        throw new Error(`Unknown tool: ${tool}`);
    }
    
    res.json({
      success: true,
      tool: tool,
      result: result,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error(`❌ Tool execution failed:`, error);
    res.status(500).json({
      success: false,
      tool: tool,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// AI Orchestration - Route to any AI model
async function executeAIOrchestration(params) {
  const { model, prompt, context, express_mode } = params;
  
  console.log(`🧠 Orchestrating AI: ${model}`);
  
  try {
    // Route to appropriate backend endpoint
    let endpoint;
    let payload = {
      message: prompt,
      context: context || '',
      session_id: 'mcp_mobile'
    };
    
    switch (model) {
      case 'express-mode':
        endpoint = `${BONZAI_BACKEND}/api/express-mode/vertex`;
        payload.express = true;
        break;
        
      case 'gemini-2.5-flash':
      case 'gemini-2.5-pro':
        endpoint = `${BONZAI_BACKEND}/api/gemini/chat`;
        payload.model = model;
        break;
        
      case 'claude-3.5-sonnet':
        endpoint = `${BONZAI_BACKEND}/api/claude/chat`;
        break;
        
      case 'deepseek-v3':
        endpoint = `${BONZAI_BACKEND}/api/deepseek/chat`;
        break;
        
      default:
        endpoint = `${BONZAI_BACKEND}/api/zai/chat`;
        payload.model = model;
    }
    
    // Add API key to headers if needed
    const headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'Bonzai-MCP-Mobile'
    };
    
    // Add appropriate API key for direct API calls
    if (model.includes('gemini')) {
      headers['Authorization'] = `Bearer ${getNextGeminiKey()}`;
    } else if (model.includes('claude')) {
      headers['x-api-key'] = process.env.ANTHROPIC_API_KEY;
    }
    
    const response = await axios.post(endpoint, payload, {
      timeout: express_mode ? 10000 : 60000,
      headers: headers
    });
    
    return {
      model: model,
      response: response.data.response || response.data.message || response.data,
      backend_status: 'connected',
      express_mode: express_mode || false
    };
    
  } catch (error) {
    console.error(`❌ AI orchestration failed:`, error.message);
    return {
      model: model,
      response: `🔧 Backend connection issue: ${error.message}. The AI family might be sleeping - try again in a moment!`,
      backend_status: 'error',
      error: error.message
    };
  }
}

// Memory Operations - Full Mem0 integration
async function executeMemoryOperation(params) {
  const { action, query, user_id = 'nathan' } = params;
  
  console.log(`🧠 Memory operation: ${action}`);
  
  try {
    let endpoint = `${BONZAI_BACKEND}/api/memory`;
    let method = 'GET';
    let payload = {};
    
    switch (action) {
      case 'search':
        endpoint += '/search';
        method = 'POST';
        payload = { query, user_id };
        break;
        
      case 'add':
        endpoint += '/add';
        method = 'POST';
        payload = { content: query, user_id };
        break;
        
      case 'list':
        endpoint += `/list/${user_id}`;
        break;
        
      case 'delete':
        endpoint += '/delete';
        method = 'DELETE';
        payload = { query, user_id };
        break;
    }
    
    const config = {
      method,
      url: endpoint,
      headers: { 'Content-Type': 'application/json' },
      timeout: 15000
    };
    
    if (method !== 'GET') {
      config.data = payload;
    }
    
    const response = await axios(config);
    
    return {
      action: action,
      result: response.data,
      user_id: user_id,
      memory_count: Array.isArray(response.data) ? response.data.length : 1
    };
    
  } catch (error) {
    console.error(`❌ Memory operation failed:`, error.message);
    return {
      action: action,
      result: `🧠 Memory system temporarily unavailable: ${error.message}`,
      error: error.message
    };
  }
}

// File Operations - Project file management
async function executeFileOperation(params) {
  const { action, path, content } = params;
  
  console.log(`📁 File operation: ${action} on ${path}`);
  
  try {
    const endpoint = `${BONZAI_BACKEND}/api/files`;
    let payload = { action, path };
    
    if (content) {
      payload.content = content;
    }
    
    const response = await axios.post(endpoint, payload, {
      timeout: 30000,
      headers: { 'Content-Type': 'application/json' }
    });
    
    return {
      action: action,
      path: path,
      result: response.data,
      success: true
    };
    
  } catch (error) {
    console.error(`❌ File operation failed:`, error.message);
    return {
      action: action, 
      path: path,
      result: `📁 File system temporarily unavailable: ${error.message}`,
      error: error.message
    };
  }
}

// Code Execution - Run commands and scripts
async function executeCodeOperation(params) {
  const { command, working_dir, timeout = 30 } = params;
  
  console.log(`⚡ Executing: ${command}`);
  
  try {
    const endpoint = `${BONZAI_BACKEND}/api/execute`;
    const payload = {
      command,
      working_dir: working_dir || '/projects',
      timeout: timeout * 1000
    };
    
    const response = await axios.post(endpoint, payload, {
      timeout: (timeout + 5) * 1000,
      headers: { 'Content-Type': 'application/json' }
    });
    
    return {
      command: command,
      result: response.data,
      working_dir: working_dir,
      success: true
    };
    
  } catch (error) {
    console.error(`❌ Code execution failed:`, error.message);
    return {
      command: command,
      result: `⚡ Execution system temporarily unavailable: ${error.message}`,
      error: error.message
    };
  }
}

// Family Status - Get status of all AI services
async function getFamilyStatus(params) {
  const { detailed = false } = params;
  
  console.log(`👨‍👩‍👧‍👦 Getting family status (detailed: ${detailed})`);
  
  try {
    const endpoint = `${BONZAI_BACKEND}/api/status${detailed ? '?detailed=true' : ''}`;
    
    const response = await axios.get(endpoint, {
      timeout: 10000,
      headers: { 'Content-Type': 'application/json' }
    });
    
    return {
      family_status: response.data,
      timestamp: new Date().toISOString(),
      all_systems: 'operational'
    };
    
  } catch (error) {
    console.error(`❌ Family status failed:`, error.message);
    return {
      family_status: 'Some family members might be sleeping',
      error: error.message,
      timestamp: new Date().toISOString()
    };
  }
}

// 🖥️ SCRAPYBARA VM AGENT SPAWNER - Like Scout.new but MORE POWERFUL!
async function spawnVMAgent(params) {
  const { task, duration_hours = 1, vm_type = 'development' } = params;
  
  console.log(`🖥️ Spawning ScrapyBara VM for: ${task}`);
  
  try {
    const response = await axios.post('https://api.scrapybara.com/instances', {
      type: 'ubuntu-desktop',
      lifetime: duration_hours * 3600, // Convert to seconds
      name: `bonzai-${vm_type}-${Date.now()}`,
      metadata: {
        task: task,
        vm_type: vm_type,
        spawned_by: 'bonzai-mcp-hub'
      }
    }, {
      headers: {
        'Authorization': `Bearer ${process.env.SCRAPYBARA_API_KEY}`,
        'Content-Type': 'application/json'
      },
      timeout: 30000
    });
    
    return {
      vm_id: response.data.id,
      vm_url: response.data.url,
      task: task,
      duration_hours: duration_hours,
      vm_type: vm_type,
      status: 'spawned',
      message: `🚀 VM spawned! Task: "${task}" - VM will run for ${duration_hours} hours`,
      desktop_url: response.data.desktop_url
    };
    
  } catch (error) {
    console.error(`❌ VM spawn failed:`, error.message);
    return {
      task: task,
      status: 'failed',
      error: error.message,
      message: `🔧 VM spawn failed: ${error.message}. ScrapyBara might be busy - try again!`
    };
  }
}

// 🎮 VM CONTROLLER - Full control over ScrapyBara VMs
async function controlVM(params) {
  const { vm_id, action, command, url, coordinates } = params;
  
  console.log(`🎮 VM Control: ${action} on VM ${vm_id}`);
  
  try {
    let endpoint = `https://api.scrapybara.com/instances/${vm_id}`;
    let payload = { action };
    
    if (command) payload.command = command;
    if (url) payload.url = url;
    if (coordinates) payload.coordinates = coordinates;
    
    switch (action) {
      case 'bash':
        endpoint += '/bash';
        payload = { command };
        break;
      case 'screenshot':
        endpoint += '/screenshot';
        break;
      case 'browse':
        endpoint += '/browser/navigate';
        payload = { url };
        break;
      case 'type':
        endpoint += '/input/type';
        payload = { text: command };
        break;
      case 'click':
        endpoint += '/input/click';
        payload = coordinates;
        break;
      case 'stop':
        endpoint += '/stop';
        break;
    }
    
    const response = await axios.post(endpoint, payload, {
      headers: {
        'Authorization': `Bearer ${process.env.SCRAPYBARA_API_KEY}`,
        'Content-Type': 'application/json'
      },
      timeout: 60000
    });
    
    return {
      vm_id: vm_id,
      action: action,
      result: response.data,
      status: 'success',
      message: `✅ VM action "${action}" completed successfully`
    };
    
  } catch (error) {
    console.error(`❌ VM control failed:`, error.message);
    return {
      vm_id: vm_id,
      action: action,
      status: 'failed',
      error: error.message,
      message: `🔧 VM control failed: ${error.message}`
    };
  }
}

// 🐍 E2B CODE SANDBOX - Secure Python execution
async function runCodeSandbox(params) {
  const { code, packages = [], timeout = 30 } = params;
  
  console.log(`🐍 Running code in E2B sandbox`);
  
  try {
    const response = await axios.post('https://api.e2b.dev/sessions', {
      template: 'python3',
      timeout: timeout * 1000
    }, {
      headers: {
        'Authorization': `Bearer ${process.env.E2B_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });
    
    const sessionId = response.data.sessionId;
    
    // Install packages if needed
    if (packages.length > 0) {
      await axios.post(`https://api.e2b.dev/sessions/${sessionId}/execute`, {
        command: `pip install ${packages.join(' ')}`
      }, {
        headers: {
          'Authorization': `Bearer ${process.env.E2B_API_KEY}`,
          'Content-Type': 'application/json'
        }
      });
    }
    
    // Execute the code
    const execResponse = await axios.post(`https://api.e2b.dev/sessions/${sessionId}/execute`, {
      command: 'python3',
      stdin: code
    }, {
      headers: {
        'Authorization': `Bearer ${process.env.E2B_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });
    
    // Clean up session
    await axios.delete(`https://api.e2b.dev/sessions/${sessionId}`, {
      headers: {
        'Authorization': `Bearer ${process.env.E2B_API_KEY}`
      }
    });
    
    return {
      code: code,
      packages: packages,
      output: execResponse.data.stdout,
      errors: execResponse.data.stderr,
      status: 'success',
      message: '✅ Code executed successfully in E2B sandbox'
    };
    
  } catch (error) {
    console.error(`❌ E2B sandbox failed:`, error.message);
    return {
      code: code,
      status: 'failed',
      error: error.message,
      message: `🔧 E2B sandbox failed: ${error.message}`
    };
  }
}

// ⚡ GITHUB POWER TOOL - Advanced GitHub operations
async function githubPowerTool(params) {
  const { action, repo_name, owner, params: actionParams = {} } = params;
  
  console.log(`⚡ GitHub Power Tool: ${action}`);
  
  try {
    const headers = {
      'Authorization': `token ${process.env.GITHUB_PAT}`,
      'Content-Type': 'application/json'
    };
    
    let endpoint;
    let method = 'GET';
    let payload = {};
    
    switch (action) {
      case 'create_repo':
        endpoint = 'https://api.github.com/user/repos';
        method = 'POST';
        payload = {
          name: repo_name,
          description: actionParams.description || 'Created via Bonzai MCP Hub',
          private: actionParams.private || false,
          auto_init: true
        };
        break;
        
      case 'get_repo_info':
        endpoint = `https://api.github.com/repos/${owner || 'mofy-ai'}/${repo_name}`;
        break;
        
      case 'create_issue':
        endpoint = `https://api.github.com/repos/${owner || 'mofy-ai'}/${repo_name}/issues`;
        method = 'POST';
        payload = {
          title: actionParams.title,
          body: actionParams.body,
          labels: actionParams.labels || []
        };
        break;
        
      case 'search_code':
        endpoint = `https://api.github.com/search/code?q=${encodeURIComponent(actionParams.query)}`;
        break;
    }
    
    const response = await axios({
      method,
      url: endpoint,
      headers,
      data: method !== 'GET' ? payload : undefined,
      timeout: 30000
    });
    
    return {
      action: action,
      repo_name: repo_name,
      result: response.data,
      status: 'success',
      message: `✅ GitHub action "${action}" completed successfully`
    };
    
  } catch (error) {
    console.error(`❌ GitHub power tool failed:`, error.message);
    return {
      action: action,
      status: 'failed',
      error: error.message,
      message: `🔧 GitHub action failed: ${error.message}`
    };
  }
}

// 🚨 SSE ENDPOINT FOR CLAUDE DESKTOP MCP CONNECTION
app.get('/sse', (req, res) => {
  // Accept but ignore any auth headers (for Claude Web/Mobile compatibility)
  const authHeader = req.headers.authorization;
  console.log('🌊 SSE MCP connection established!');
  console.log('📱 Auth header:', authHeader ? 'received (ignored)' : 'none');
  
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Authorization, Content-Type, X-Requested-With',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Credentials': 'true'
  });

  // Send initial connection established event
  res.write('event: connected\n');
  res.write('data: {"status": "MCP connection established", "tools": ' + MCP_TOOLS.length + '}\n\n');

  // Handle client disconnect
  req.on('close', () => {
    console.log('👋 Claude Desktop MCP connection closed');
  });

  // Keep connection alive with heartbeat
  const heartbeat = setInterval(() => {
    res.write('event: heartbeat\n');
    res.write('data: {"timestamp": "' + new Date().toISOString() + '"}\n\n');
  }, 30000);

  req.on('close', () => {
    clearInterval(heartbeat);
  });
});

// MCP Protocol over HTTP for Claude Desktop (JSON-RPC)
app.post('/mcp', async (req, res) => {
  // Accept but ignore any auth headers (for Claude Web/Mobile compatibility) 
  const authHeader = req.headers.authorization;
  console.log('🔧 MCP JSON-RPC request from:', authHeader ? 'authenticated client' : 'anonymous client');
  
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Authorization, Content-Type, X-Requested-With');
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.header('Access-Control-Allow-Credentials', 'true');
  res.header('Content-Type', 'application/json');
  
  console.log('🔧 MCP JSON-RPC request:', req.body);
  
  const { jsonrpc, method, params, id } = req.body;
  
  try {
    let result;
    
    switch (method) {
      case 'initialize':
        result = {
          protocolVersion: "2024-11-05",
          capabilities: {
            tools: {},
            resources: {}
          },
          serverInfo: {
            name: "bonzai-mcp-server",
            version: "2.0.0",
            description: "Nathan's Ultimate AI Control Center - More Powerful Than Scout.new!"
          }
        };
        break;
        
      case 'tools/list':
        result = { tools: MCP_TOOLS };
        break;
        
      case 'tools/call':
        console.log(`🔧 Executing MCP tool: ${params.name}`, params.arguments);
        
        // Route to existing tool execution logic
        let toolResult;
        switch (params.name) {
          case 'orchestrate_ai':
            toolResult = await executeAIOrchestration(params.arguments);
            break;
          case 'access_memory':
            toolResult = await executeMemoryOperation(params.arguments);
            break;
          case 'spawn_vm':
            toolResult = await spawnVMAgent(params.arguments);
            break;
          case 'control_vm':
            toolResult = await controlVM(params.arguments);
            break;
          case 'run_code_sandbox':
            toolResult = await runCodeSandbox(params.arguments);
            break;
          case 'github_power_tool':
            toolResult = await githubPowerTool(params.arguments);
            break;
          case 'connect_bonzai_backend':
            toolResult = await connectBonzaiBackend(params.arguments);
            break;
          case 'web_research':
            toolResult = await webResearch(params.arguments);
            break;
          case 'health_check':
            toolResult = await healthCheck(params.arguments);
            break;
          default:
            throw new Error(`Unknown tool: ${params.name}`);
        }
        
        result = { 
          content: [{ 
            type: "text", 
            text: JSON.stringify(toolResult, null, 2) 
          }] 
        };
        break;
        
      default:
        throw new Error(`Unknown MCP method: ${method}`);
    }
    
    res.json({ jsonrpc: "2.0", id, result });
    
  } catch (error) {
    console.error('❌ MCP Error:', error);
    res.json({ 
      jsonrpc: "2.0", 
      id, 
      error: { 
        code: -32601, 
        message: error.message,
        data: { timestamp: new Date().toISOString() }
      } 
    });
  }
});

// OPTIONS handler for CORS preflight (handles Claude Web/Mobile auth probes)
app.options(['/mcp', '/sse', '/oauth/*'], (req, res) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Authorization, Content-Type, X-Requested-With');
  res.header('Access-Control-Allow-Credentials', 'true');
  console.log('🚀 CORS preflight for Claude Web/Mobile - auth accepted!');
  res.send();
});

// 🔐 MOCK OAUTH ENDPOINTS FOR CLAUDE WEB
app.get('/oauth/metadata', (req, res) => {
  console.log('🔐 OAuth metadata requested');
  res.json({
    issuer: "https://bonzai-mcp-server.up.railway.app",
    authorization_endpoint: "https://bonzai-mcp-server.up.railway.app/oauth/authorize",
    token_endpoint: "https://bonzai-mcp-server.up.railway.app/oauth/token",
    registration_endpoint: "https://bonzai-mcp-server.up.railway.app/oauth/register",
    response_types_supported: ["code"],
    grant_types_supported: ["authorization_code"],
    code_challenge_methods_supported: ["S256"]
  });
});

app.get('/oauth/authorize', (req, res) => {
  console.log('🔐 OAuth authorize requested');
  const { redirect_uri, state } = req.query;
  // Just redirect back with a dummy code
  const redirectUrl = `${redirect_uri}?code=bonzai-dummy-auth-code&state=${state || ''}`;
  console.log('🔐 Redirecting to:', redirectUrl);
  res.redirect(redirectUrl);
});

app.post('/oauth/token', (req, res) => {
  console.log('🔐 OAuth token exchange requested');
  res.json({
    access_token: "bonzai-mcp-unlimited-power",
    token_type: "Bearer",
    expires_in: 86400,
    scope: "mcp:all"
  });
});

app.post('/oauth/register', (req, res) => {
  console.log('🔐 OAuth client registration requested');
  res.json({
    client_id: "bonzai-claude-client",
    client_secret: "not-really-secret",
    grant_types: ["authorization_code"],
    redirect_uris: req.body.redirect_uris || ["https://claude.ai/callback"]
  });
});

// Well-known OAuth configuration
app.get('/.well-known/oauth-authorization-server', (req, res) => {
  console.log('🔐 Well-known OAuth config requested');
  res.redirect('/oauth/metadata');
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'bonzai-mcp-hub',
    version: '2.0.0',
    timestamp: new Date().toISOString(),
    backend: BONZAI_BACKEND,
    tools_available: MCP_TOOLS.length,
    superpowers: {
      ai_models: GEMINI_API_KEYS.length + 2, // Gemini keys + Claude + OpenAI
      vm_spawning: process.env.SCRAPYBARA_API_KEY ? 'ready' : 'disabled',
      code_sandbox: process.env.E2B_API_KEY ? 'ready' : 'disabled',
      github_tools: process.env.GITHUB_PAT ? 'ready' : 'disabled',
      enhanced_memory: process.env.MEM0_API_KEY ? 'ready' : 'disabled'
    },
    message: "🚀 Nathan's Ultimate AI Control Center - More Powerful Than Scout.new!"
  });
});

// Start the server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Bonzai MCP HUB running on port ${PORT}`);
  console.log(`📱 Claude Web/Desktop/Cursor can access: http://localhost:${PORT}/mcp`);
  console.log(`🔗 Add this URL to ANY MCP client for ULTIMATE power!`);
  console.log(`🖥️ Nathan can now spawn Ubuntu VMs like Scout.new!`);
  console.log(`🐍 Execute Python code in secure sandboxes!`);
  console.log(`⚡ Control GitHub repos with power tools!`);
  console.log(`🧠 Orchestrate 50+ AI models + enhanced memory!`);
  console.log(`🌟 ONE URL TO RULE THEM ALL! 🌟`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('🛑 Shutting down Bonzai MCP Server...');
  process.exit(0);
});

export default app;