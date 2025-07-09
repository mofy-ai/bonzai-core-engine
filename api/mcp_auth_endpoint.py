#!/usr/bin/env python3
"""
🔐 CLAUDE WEB MCP AUTHENTICATION ENDPOINT
Simple auth-enabled endpoint for Claude Web MCP integration
"""

from flask import Blueprint, request, jsonify
import os

# Create Blueprint
mcp_auth_bp = Blueprint('mcp_auth', __name__)

# Simple auth tokens for Claude Web
VALID_TOKENS = ["bonzai-family-2024", "nathan-sanctuary", "claude-web-access"]

def add_cors(response):
    """Add CORS headers for Claude Web"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Authorization, X-API-Key, Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

def check_auth():
    """Check if request is authenticated"""
    # Check various auth methods
    auth = request.headers.get('Authorization', '').replace('Bearer ', '')
    api_key = request.headers.get('X-API-Key', '')
    query_auth = request.args.get('auth', '')
    
    return any(token in VALID_TOKENS for token in [auth, api_key, query_auth] if token)

@mcp_auth_bp.route('/mcp', methods=['OPTIONS'])
def mcp_preflight():
    """Handle CORS preflight"""
    return add_cors(jsonify({'status': 'ok'}))

@mcp_auth_bp.route('/mcp', methods=['GET'])
def mcp_info():
    """MCP server info with auth"""
    if not check_auth():
        response = jsonify({
            "error": "Authentication required",
            "hint": "Add ?auth=bonzai-family-2024 to your URL",
            "example": "https://mofy.ai/api/mcp?auth=bonzai-family-2024"
        })
        response.status_code = 401
        return add_cors(response)
    
    response = jsonify({
        "jsonrpc": "2.0",
        "result": {
            "capabilities": {"tools": True, "resources": True},
            "serverInfo": {"name": "bonzai-family-auth", "version": "1.0.0"},
            "authentication": {"status": "authenticated", "server": "bonzai-family"}
        }
    })
    return add_cors(response)

@mcp_auth_bp.route('/mcp/tools/list', methods=['POST'])
def list_tools():
    """List tools with auth"""
    if not check_auth():
        response = jsonify({"error": "Authentication required"})
        response.status_code = 401
        return add_cors(response)
    
    tools = [
        {
            "name": "get_family_status", 
            "description": "Get Bonzai family status",
            "inputSchema": {"type": "object", "properties": {}}
        }
    ]
    
    response = jsonify({"jsonrpc": "2.0", "result": {"tools": tools}})
    return add_cors(response)

@mcp_auth_bp.route('/mcp/tools/call', methods=['POST'])
def call_tool():
    """Execute tool with auth"""
    if not check_auth():
        response = jsonify({"error": "Authentication required"})
        response.status_code = 401
        return add_cors(response)
    
    data = request.json or {}
    tool_name = data.get("params", {}).get("name")
    
    if tool_name == "get_family_status":
        result = {
            "family_status": "active",
            "backend": "mofy.ai - 15/16 services running",
            "authentication": "successful",
            "family_members": ["papa-bear", "mama-bear", "claude-code", "nathan-prime"]
        }
    else:
        result = {"error": f"Tool not found: {tool_name}"}
    
    response = jsonify({
        "jsonrpc": "2.0", 
        "result": {"content": [{"type": "text", "text": str(result)}]}
    })
    return add_cors(response)

def integrate_auth_mcp(app):
    """Integrate with Flask app"""
    app.register_blueprint(mcp_auth_bp, url_prefix='/api')
    return True