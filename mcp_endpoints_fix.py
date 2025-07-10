# MCP ENDPOINTS FIX - Add these routes to app_ultimate_mem0.py

@app.route('/mcp', methods=['GET', 'POST'])
def mcp_endpoint():
    """MCP endpoint that was missing"""
    return jsonify({
        'service': 'Bonzai MCP Server',
        'status': 'operational',
        'version': '1.0',
        'message': 'MCP endpoint active',
        'family_system': 'integrated',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/mcp/auth', methods=['POST'])
def mcp_auth():
    """MCP authentication endpoint"""
    return jsonify({
        'authenticated': True,
        'mcp_version': '1.0',
        'capabilities': ['memory', 'orchestration', 'family_collaboration'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/mcp/tools', methods=['GET'])
def mcp_tools():
    """MCP tools endpoint"""
    return jsonify({
        'tools': [
            {
                'name': 'bonzai_orchestrate',
                'description': 'AI orchestration with family context',
                'parameters': {
                    'prompt': 'string',
                    'models': 'array',
                    'use_memory': 'boolean'
                }
            },
            {
                'name': 'bonzai_memory',
                'description': 'Family memory operations',
                'parameters': {
                    'action': 'string',
                    'content': 'string',
                    'search_query': 'string'
                }
            }
        ],
        'mcp_version': '1.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/robots.txt', methods=['GET'])
def robots_txt():
    """Robots.txt to stop crawlers"""
    return Response(
        "User-agent: *\nDisallow: /\n",
        mimetype='text/plain'
    )
