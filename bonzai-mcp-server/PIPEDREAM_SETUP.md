# 🔄 Pipedream MCP Auth Proxy Setup

## 🎯 What This Solves
Claude Web expects OAuth 2.0 authentication for remote MCP servers. Our Railway server is simple and doesn't handle OAuth. Pipedream acts as the perfect middleman!

## 🔑 OAuth Credentials (CONFIGURED!)
- **Client ID**: `QY4eq13T9ktZJp_X-jAsGa3jOszpm0DcY9NOSoc1fec`
- **Client Secret**: `eirGMdui23aRPU45tSHi7DfqpfItXiwFNwJm0Ao5teY`
- **Client Name**: `zai`
- **Workspace ID**: `o_NeI3yYD`

## 🚀 Quick Setup (5 minutes)

### Step 1: Deploy to Pipedream
1. Go to [Pipedream.com](https://pipedream.com)
2. Create new workflow
3. Choose "HTTP Trigger" 
4. Copy code from `pipedream-mcp-proxy.js` into the workflow
5. Deploy and get your URL (like `https://abc123.m.pipedream.net`)

### Step 2: Update URLs in the Code
Edit `pipedream-mcp-proxy.js` line 65:
```javascript
issuer: "https://YOUR-PIPEDREAM-URL.m.pipedream.net",
authorization_endpoint: "https://YOUR-PIPEDREAM-URL.m.pipedream.net/oauth/authorize",
// ... update all URLs with your actual Pipedream URL
```

### Step 3: Configure Claude Clients

#### 🌐 Claude Web/Mobile:
- **Integration URL**: `https://YOUR-PIPEDREAM-URL.m.pipedream.net/sse`
- **Auth**: Automatic OAuth 2.0 (Pipedream handles it)

#### 🖥️ Claude Desktop:  
- **Direct URL**: `https://bonzai-mcp-server.up.railway.app/sse`
- **Auth**: None needed (direct connection)

## 🔄 How It Works

```
Claude Web → Pipedream OAuth → Railway MCP → Response
           ↘️ (satisfies auth) ↗️ (actual work)

Claude Desktop → Railway MCP (direct)
               ↗️ (no auth needed)
```

## ✅ Test It

1. **Health Check**: `https://YOUR-PIPEDREAM-URL.m.pipedream.net/health`
2. **MCP Tools**: `https://YOUR-PIPEDREAM-URL.m.pipedream.net/mcp/tools`
3. **OAuth Metadata**: `https://YOUR-PIPEDREAM-URL.m.pipedream.net/oauth/metadata`

## 🎉 Benefits

- ✅ Claude Web gets proper OAuth 2.0
- ✅ Railway stays simple (no auth complexity)  
- ✅ Built-in logging (see all requests in Pipedream)
- ✅ Auto-scaling (handles traffic spikes)
- ✅ One URL works everywhere!

**Perfect solution using existing infrastructure!** 🚀