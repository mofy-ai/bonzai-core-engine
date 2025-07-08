/**
 * 🔄 PIPEDREAM MCP AUTH PROXY
 * 
 * Solves Claude Web authentication by acting as OAuth middleman:
 * Claude Web → Pipedream (OAuth) → Railway MCP Server → Response
 * 
 * Deploy this to Pipedream to get a URL like: https://abc123.m.pipedream.net
 * Then use that URL in Claude Web integrations!
 */

export default defineComponent({
  async run({ steps, $ }) {
    const { event } = steps.trigger;
    const { method, path, headers, body, query } = event;
    
    console.log(`🔄 MCP Proxy: ${method} ${path}`);
    
    // 🔐 OAUTH ENDPOINTS FOR CLAUDE WEB
    if (path.includes('/oauth') || path.includes('/.well-known')) {
      return this.handleOAuth(path, query);
    }
    
    // 🚀 FORWARD MCP REQUESTS TO RAILWAY
    try {
      const railwayUrl = 'https://bonzai-mcp-server.up.railway.app';
      const targetUrl = `${railwayUrl}${path}`;
      
      // Clean headers (remove Pipedream-specific ones)
      const cleanHeaders = {
        'Content-Type': headers['content-type'] || 'application/json',
        'User-Agent': 'Pipedream-MCP-Proxy/1.0'
      };
      
      // Add auth header if Claude Web sent one (Railway will ignore it)
      if (headers.authorization) {
        cleanHeaders.Authorization = headers.authorization;
      }
      
      console.log(`🎯 Forwarding to: ${targetUrl}`);
      
      const response = await fetch(targetUrl, {
        method: method,
        headers: cleanHeaders,
        body: method !== 'GET' ? JSON.stringify(body) : undefined
      });
      
      const responseData = await response.json();
      
      // 📡 SSE ENDPOINT - Return proper SSE format
      if (path.includes('/sse')) {
        $.respond({
          status: 200,
          headers: {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
          },
          body: this.formatSSEResponse(responseData)
        });
        return;
      }
      
      // 📤 REGULAR JSON RESPONSE
      return {
        statusCode: response.status,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        body: responseData
      };
      
    } catch (error) {
      console.error('❌ Proxy Error:', error);
      return {
        statusCode: 500,
        body: { 
          error: 'MCP Proxy Error',
          message: error.message,
          timestamp: new Date().toISOString()
        }
      };
    }
  },
  
  // 🔐 OAUTH HANDLER - Make Claude Web Happy
  handleOAuth(path, query) {
    console.log(`🔐 OAuth Request: ${path}`);
    
    // OAuth metadata
    if (path.includes('/metadata') || path.includes('/.well-known')) {
      return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          issuer: "https://enobhehxkxz7e.m.pipedream.net",
          authorization_endpoint: "https://enobhehxkxz7e.m.pipedream.net/oauth/authorize",
          token_endpoint: "https://enobhehxkxz7e.m.pipedream.net/oauth/token",
          registration_endpoint: "https://enobhehxkxz7e.m.pipedream.net/oauth/register",
          response_types_supported: ["code"],
          grant_types_supported: ["authorization_code"],
          code_challenge_methods_supported: ["S256"],
          scopes_supported: ["mcp:read", "mcp:write"]
        }
      };
    }
    
    // Authorization endpoint
    if (path.includes('/authorize')) {
      const { redirect_uri, state } = query;
      const redirectUrl = new URL(redirect_uri);
      redirectUrl.searchParams.set('code', 'pipedream-bonzai-auth-code');
      if (state) redirectUrl.searchParams.set('state', state);
      
      return {
        statusCode: 302,
        headers: { 'Location': redirectUrl.toString() }
      };
    }
    
    // Token endpoint
    if (path.includes('/token')) {
      return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          access_token: "zai-mcp-token-" + Date.now(),
          token_type: "Bearer",
          expires_in: 86400,
          scope: "mcp:read mcp:write",
          client_id: "QY4eq13T9ktZJp_X-jAsGa3jOszpm0DcY9NOSoc1fec"
        }
      };
    }
    
    // Registration endpoint
    if (path.includes('/register')) {
      return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          client_id: "QY4eq13T9ktZJp_X-jAsGa3jOszpm0DcY9NOSoc1fec",
          client_secret: "eirGMdui23aRPU45tSHi7DfqpfItXiwFNwJm0Ao5teY",
          registration_access_token: "zai-oauth-registration-token"
        }
      };
    }
    
    return { statusCode: 404, body: { error: 'OAuth endpoint not found' } };
  },
  
  // 📡 FORMAT SSE RESPONSE FOR CLAUDE WEB
  formatSSEResponse(data) {
    if (typeof data === 'string') return data;
    
    return [
      'data: ' + JSON.stringify(data),
      '',
      ''
    ].join('\\n');
  }
});