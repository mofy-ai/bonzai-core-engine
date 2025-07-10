# CLAUDE.AI INTEGRATION 404 FIX

## What Claude.ai is Looking For:
Based on Railway logs, Claude.ai expects standard MCP protocol endpoints:

```python
# ADD THESE TO app_ultimate_mem0.py:

@app.route('/.well-known/mcp', methods=['GET'])
def mcp_discovery():
    """MCP service discovery"""
    return jsonify({
        "mcp_version": "2024-11-05",
        "server_info": {
            "name": "Bonzai Ultimate Mem0",
            "version": "3.0"
        },
        "capabilities": {
            "tools": ["ultimate_orchestrate", "ultimate_family_memory"],
            "prompts": ["family_collaboration"],
            "resources": ["memory_analytics"]
        }
    })

@app.route('/v1/capabilities', methods=['GET'])
def mcp_capabilities():
    """MCP capabilities endpoint"""
    return jsonify({
        "capabilities": {
            "tools": {"listChanged": True},
            "resources": {"subscribe": True, "listChanged": True},
            "prompts": {"listChanged": True}
        },
        "serverInfo": {
            "name": "Bonzai Ultimate Mem0",
            "version": "3.0"
        }
    })

@app.route('/v1/session', methods=['POST'])
def mcp_session():
    """MCP session initialization"""
    return jsonify({
        "success": True,
        "session_id": str(uuid.uuid4()),
        "server_info": {
            "name": "Bonzai Ultimate Mem0",
            "version": "3.0"
        }
    })
```

## Quick Deploy:
1. Add these endpoints to GitHub
2. Railway auto-deploys 
3. Claude.ai Connect button should work!
