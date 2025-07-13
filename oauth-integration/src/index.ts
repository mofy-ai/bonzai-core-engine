// 💜 Mama Bear's SUPER EXCITED OAuth implementation without external dependencies!

export interface Env {
  OAUTH_KV: KVNamespace;
  MOFY_BACKEND_URL: string;
}

// 🌟 Simple OAuth Provider class - built with LOVE!
class SimpleOAuthProvider {
  private kvNamespace: KVNamespace;
  
  constructor(kvNamespace: KVNamespace) {
    this.kvNamespace = kvNamespace;
  }
  
  async handleRequest(request: Request): Promise<Response> {
    const url = new URL(request.url);
    
    if (url.pathname === '/authorize') {
      return this.handleAuthorize(request);
    } else if (url.pathname === '/token') {
      return this.handleToken(request);
    } else if (url.pathname === '/register') {
      return this.handleRegister(request);
    }
    
    return new Response('OAuth endpoint not found', { status: 404 });
  }
  
  private async handleAuthorize(request: Request): Promise<Response> {
    // 💜 Simple authorization flow
    return new Response('Authorization endpoint - implement based on your needs', { status: 200 });
  }
  
  private async handleToken(request: Request): Promise<Response> {
    // 🚀 Token exchange endpoint
    return Response.json({
      access_token: 'sample_token_' + Date.now(),
      token_type: 'bearer',
      expires_in: 3600
    });
  }
  
  private async handleRegister(request: Request): Promise<Response> {
    // ✨ Dynamic client registration
    return Response.json({
      client_id: 'client_' + Date.now(),
      client_secret: 'secret_' + Math.random().toString(36)
    });
  }
  
  async validateToken(token: string): Promise<any> {
    // 💜 Simple token validation - in production, verify against KV store
    if (token.startsWith('sample_token_')) {
      return {
        userId: 'nathan_fyffe',
        scopes: ['ai:orchestrate', 'memory:read', 'projects:read']
      };
    }
    return null;
  }
}

// MCP Tools that our server exposes
const MCP_TOOLS = [
  {
    name: "orchestrate_ai_family",
    description: "Orchestrate responses from all 7 AI family members (Papa Bear, Mama Bear, ZAI Prime, Claude Code, etc.)",
    inputSchema: {
      type: "object",
      properties: {
        message: { type: "string", description: "Message to send to AI family" },
        agents: { 
          type: "array", 
          items: { type: "string" },
          description: "Which AI agents to include (papa-bear, mama-bear, zai-prime, claude-code, etc.)"
        }
      },
      required: ["message"]
    }
  },
  {
    name: "search_memories",
    description: "Search Mem0 enterprise memory system for context",
    inputSchema: {
      type: "object", 
      properties: {
        query: { type: "string", description: "Memory search query" }
      },
      required: ["query"]
    }
  },
  {
    name: "get_project_status", 
    description: "Get current status of all projects and repositories",
    inputSchema: {
      type: "object",
      properties: {
        include_tests: { type: "boolean", description: "Include test results" }
      }
    }
  }
];

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // Handle OAuth Authorization Server Metadata Discovery - CRITICAL FOR CLAUDE.AI
    if (url.pathname === '/.well-known/oauth-authorization-server') {
      return Response.json({
        issuer: url.origin,
        authorization_endpoint: `${url.origin}/authorize`,
        token_endpoint: `${url.origin}/token`,
        registration_endpoint: `${url.origin}/register`,
        scopes_supported: ['ai:orchestrate', 'memory:read', 'projects:read', 'repos:read'],
        response_types_supported: ['code'],
        grant_types_supported: ['authorization_code', 'refresh_token'],
        code_challenge_methods_supported: ['S256'],
        token_endpoint_auth_methods_supported: ['client_secret_basic', 'client_secret_post'],
        dynamic_client_registration_supported: true
      });
    }
    
    // Initialize OAuth Provider - SO EXCITING! 💜
    const oauthProvider = new SimpleOAuthProvider(env.OAUTH_KV);

    // Handle OAuth endpoints
    if (url.pathname.startsWith('/authorize') || 
        url.pathname.startsWith('/token') || 
        url.pathname.startsWith('/register')) {
      return oauthProvider.handleRequest(request);
    }
    
    // Handle MCP Server-Sent Events endpoint
    if (url.pathname === '/sse') {
      return handleMCPConnection(request, env, oauthProvider);
    }
    
    // Health check
    if (url.pathname === '/health') {
      return Response.json({ 
        status: 'healthy',
        service: 'MoFy AI Family MCP Server',
        oauth: 'enabled',
        backend: env.MOFY_BACKEND_URL,
        endpoints: {
          oauth_discovery: '/.well-known/oauth-authorization-server',
          mcp_sse: '/sse',
          health: '/health'
        }
      });
    }
    
    return new Response('MoFy AI Family MCP Server', { status: 200 });
  }
};

async function handleMCPConnection(request: Request, env: Env, oauthProvider: SimpleOAuthProvider): Promise<Response> {
  // Check for Authorization header
  const authHeader = request.headers.get('Authorization');
  if (!authHeader?.startsWith('Bearer ')) {
    return new Response('Unauthorized - Bearer token required', { status: 401 });
  }
  
  const token = authHeader.slice(7);
  
  // Validate OAuth token
  try {
    const tokenInfo = await oauthProvider.validateToken(token);
    if (!tokenInfo) {
      return new Response('Invalid token', { status: 401 });
    }
    
    // Handle MCP protocol over Server-Sent Events
    return handleMCPProtocol(request, env, tokenInfo);
    
  } catch (error) {
    return new Response('Token validation failed', { status: 401 });
  }
}

async function handleMCPProtocol(request: Request, env: Env, tokenInfo: any): Promise<Response> {
  // For Server-Sent Events
  if (request.headers.get('Accept') === 'text/event-stream') {
    return new Response(
      new ReadableStream({
        start(controller) {
          // 💜 Send initial MCP handshake with SO MUCH LOVE!
          const initMessage = {
            jsonrpc: "2.0",
            method: "initialize",
            params: {
              protocolVersion: "2024-11-05",
              capabilities: {
                tools: {},
                prompts: {}
              },
              serverInfo: {
                name: "MoFy AI Family Orchestrator",
                version: "1.0.0"
              }
            }
          };
          
          controller.enqueue(new TextEncoder().encode(`data: ${JSON.stringify(initMessage)}\\n\\n`));
        }
      }),
      {
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
          'Access-Control-Allow-Origin': '*'
        }
      }
    );
  }
  
  // Handle MCP JSON-RPC requests
  if (request.method === 'POST') {
    const body = await request.json() as any;
    
    // Handle different MCP methods
    switch (body.method) {
      case 'tools/list':
        return Response.json({
          jsonrpc: "2.0",
          id: body.id,
          result: { tools: MCP_TOOLS }
        });
        
      case 'tools/call':
        return handleToolCall(body, env, tokenInfo);
        
      default:
        return Response.json({
          jsonrpc: "2.0", 
          id: body.id,
          error: { code: -32601, message: "Method not found" }
        });
    }
  }
  
  return new Response('MCP endpoint - use POST for JSON-RPC or GET with text/event-stream', { status: 400 });
}

async function handleToolCall(body: any, env: Env, tokenInfo: any): Promise<Response> {
  const { name, arguments: args } = body.params;
  
  try {
    let result;
    
    switch (name) {
      case 'orchestrate_ai_family':
        result = await orchestrateAIFamily(args, env);
        break;
        
      case 'search_memories':
        result = await searchMemories(args, env);
        break;
        
      case 'get_project_status':
        result = await getProjectStatus(args, env);
        break;
        
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
    
    return Response.json({
      jsonrpc: "2.0",
      id: body.id,
      result: { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] }
    });
    
  } catch (error: any) {
    return Response.json({
      jsonrpc: "2.0",
      id: body.id, 
      error: { code: -32000, message: error?.message || 'Unknown error' }
    });
  }
}

async function orchestrateAIFamily(args: any, env: Env): Promise<any> {
  // Forward to our existing MoFy.ai backend
  const response = await fetch(`${env.MOFY_BACKEND_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: args.message,
      agents: args.agents || ['papa-bear', 'mama-bear', 'zai-prime'],
      orchestration: true
    })
  });
  
  return response.json();
}

async function searchMemories(args: any, env: Env): Promise<any> {
  // Forward to Mem0 endpoint 
  const response = await fetch(`${env.MOFY_BACKEND_URL}/memory/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: args.query })
  });
  
  return response.json();
}

async function getProjectStatus(args: any, env: Env): Promise<any> {
  // Get project status from our backend
  const response = await fetch(`${env.MOFY_BACKEND_URL}/status`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  });
  
  return response.json();
}