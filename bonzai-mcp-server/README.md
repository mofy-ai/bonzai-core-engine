# 🚀 Bonzai MCP Server

Nathan's Mobile AI Command Center - Provides Claude Web with full access to the Bonzai platform via MCP protocol.

## 📱 What This Does

This MCP server gives Claude Web complete access to:
- **All AI Models**: Gemini, Claude, DeepSeek with express mode
- **Memory System**: Full Mem0 integration for context and memories
- **File Operations**: Read/write project files and manage deployments
- **Code Execution**: Run commands and scripts remotely
- **Family Status**: Monitor all AI services in real-time

## 🌐 Deployment

Deployed on Railway with automatic HTTPS and scaling.

**Production URL**: `https://bonzai-mcp-server.railway.app`

## 🔧 Claude Web Integration

Add to Claude Web integrations:
1. Open Claude Web settings
2. Go to "Integrations" 
3. Add new integration:
   - **Name**: Bonzai Command Center
   - **URL**: `https://bonzai-mcp-server.railway.app/mcp`
4. Save and enjoy full mobile AI control!

## 🛠️ Available Tools

1. **orchestrate_ai** - Route messages to any AI family member
2. **access_memory** - Search, add, or manage memories  
3. **manage_files** - File system operations
4. **execute_code** - Run commands and deployments
5. **family_status** - Get real-time status of all services

## 🔒 Security

- CORS restricted to Claude.ai domains
- Request size limits and timeouts
- Secure token authentication
- Health monitoring and auto-restart

Nathan can now control the entire Bonzai platform from his phone! 🎉# Trigger Railway redeploy with SSE endpoints
