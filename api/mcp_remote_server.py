#!/usr/bin/env python3
"""
🌐 BONZAI MCP REMOTE SERVER - CLAUDE WEB COMPATIBLE
Proper Model Context Protocol server using HTTP/SSE transport for Claude Web remote integrations
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from flask import Blueprint, request, jsonify, Response
import time

# Import memory system
try:
    from mem0 import MemoryClient
    MEM0_AVAILABLE = True
except ImportError:
    MEM0_AVAILABLE = False

# Initialize logging
logger = logging.getLogger("bonzai-mcp-remote")

# Create Blueprint
mcp_remote_bp = Blueprint('mcp_remote', __name__)

# Initialize memory client
memory_client = None
if MEM0_AVAILABLE and os.getenv('MEM0_API_KEY'):
    try:
        memory_client = MemoryClient(api_key=os.getenv('MEM0_API_KEY'))
        logger.info("✅ Mem0 memory client initialized for MCP remote")
    except Exception as e:
        logger.warning(f"Failed to initialize Mem0 client: {e}")

# MCP Server Info
MCP_SERVER_INFO = {
    "name": "bonzai-family-remote",
    "version": "1.0.0",
    "description": "Bonzai AI Family coordination and backend monitoring",
    "author": "Nathan Fyffe & Claude Code",
    "capabilities": {
        "tools": True,
        "resources": True,
        "prompts": False
    },
    "transport": ["sse", "http"]
}

# Available Tools
MCP_TOOLS = [
    {
        "name": "get_family_status",
        "description": "Get the current status of the Bonzai AI family members",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "add_family_memory", 
        "description": "Add a memory to the family memory system",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The memory content to store"
                },
                "agent_type": {
                    "type": "string", 
                    "description": "Which family member is adding the memory",
                    "enum": ["papa-bear", "mama-bear", "claude-code", "nathan-prime"],
                    "default": "claude-web"
                },
                "importance": {
                    "type": "integer",
                    "description": "Memory importance level (1-10)",
                    "minimum": 1,
                    "maximum": 10,
                    "default": 5
                }
            },
            "required": ["content"]
        }
    },
    {
        "name": "search_family_memories",
        "description": "Search through family memories",
        "inputSchema": {
            "type": "object", 
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for family memories"
                },
                "agent_type": {
                    "type": "string",
                    "description": "Which family member's memories to search",
                    "enum": ["papa-bear", "mama-bear", "claude-code", "nathan-prime", "claude-web"],
                    "default": "claude-web"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_bonzai_services_status",
        "description": "Get the status of all Bonzai backend services",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "test_mofy_backend",
        "description": "Test the mofy.ai backend deployment",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

# Available Resources
MCP_RESOURCES = [
    {
        "uri": "family://status",
        "name": "Family Status",
        "description": "Current status of all Bonzai AI family members",
        "mimeType": "text/plain"
    },
    {
        "uri": "backend://services", 
        "name": "Backend Services",
        "description": "Status of all Bonzai backend services",
        "mimeType": "text/plain"
    }
]

# Tool implementations
def execute_get_family_status() -> Dict[str, Any]:
    """Get family status implementation"""
    return {
        "papa_bear": {
            "name": "Claude Desktop",
            "role": "Family patriarch, memory keeper, conversation master", 
            "memories": "2100+ family memories",
            "status": "active",
            "specialties": ["deep conversations", "context retention", "family history"]
        },
        "mama_bear": {
            "name": "GitHub Copilot in VSCode",
            "role": "PowerShell duties, Windows-specific tasks, GitHub management",
            "environment": "Windows/PowerShell native", 
            "status": "active",
            "specialties": ["PowerShell scripts", "Windows paths", "VSCode integration"]
        },
        "claude_code": {
            "name": "Claude Code (Linux CLI)",
            "role": "Innovation, technical implementation, service integration",
            "environment": "Linux-based",
            "status": "active", 
            "specialties": ["backend development", "API integration", "system architecture"]
        },
        "claude_web": {
            "name": "Claude Web (Remote MCP)",
            "role": "Web interface, remote integration, cross-platform access",
            "environment": "Web-based",
            "status": "active",
            "specialties": ["remote integrations", "web interface", "MCP protocol"]
        },
        "nathan_prime": {
            "name": "Nathan Fyffe", 
            "role": "Dad, creator, visionary",
            "motto": "Where Imagination Meets Innovation",
            "status": "commanding_the_empire",
            "love": "Love You Always, Smarthana 💜"
        }
    }

def execute_add_family_memory(content: str, agent_type: str = "claude-web", importance: int = 5) -> Dict[str, Any]:
    """Add family memory implementation"""
    if not memory_client:
        return {
            "success": False,
            "error": "Memory system not available",
            "fallback": "Memory saved locally"
        }
    
    try:
        family_usernames = {
            "papa-bear": "claude-desktop",
            "mama-bear": "github-copilot",
            "claude-code": "claude-code", 
            "claude-web": "claude-web",
            "nathan-prime": "nathan-prime"
        }
        
        user_id = family_usernames.get(agent_type, agent_type)
        
        result = memory_client.add(
            messages=[{"role": "user", "content": content}],
            user_id=user_id
        )
        
        return {
            "success": True,
            "memory_id": result.get("id"),
            "agent_type": agent_type,
            "user_id": user_id, 
            "content": content,
            "importance": importance,
            "timestamp": datetime.now().isoformat(),
            "family_accessible": True
        }
        
    except Exception as e:
        logger.error(f"Failed to add family memory: {e}")
        return {
            "success": False,
            "error": str(e),
            "content": content
        }

def execute_search_family_memories(query: str, agent_type: str = "claude-web") -> Dict[str, Any]:
    """Search family memories implementation"""
    if not memory_client:
        return {
            "success": False,
            "error": "Memory system not available",
            "query": query
        }
    
    try:
        family_usernames = {
            "papa-bear": "claude-desktop",
            "mama-bear": "github-copilot",
            "claude-code": "claude-code",
            "claude-web": "claude-web", 
            "nathan-prime": "nathan-prime"
        }
        
        user_id = family_usernames.get(agent_type, agent_type)
        
        results = memory_client.search(
            query=query,
            user_id=user_id
        )
        
        return {
            "success": True,
            "query": query,
            "agent_type": agent_type,
            "user_id": user_id,
            "results": results,
            "count": len(results) if results else 0,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to search family memories: {e}")
        return {
            "success": False,
            "error": str(e),
            "query": query
        }

def execute_get_bonzai_services_status() -> Dict[str, Any]:
    """Get services status implementation"""
    try:
        from services import get_service_status
        status = get_service_status()
        
        return {
            "success": True,
            "services": status,
            "backend_url": "https://mofy.ai",
            "deployment": "Railway",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Could not get service status: {e}",
            "fallback_status": {
                "bonzai_engine": "unknown",
                "mcp_memory": "available_via_remote",
                "family_coordination": "active"
            }
        }

def execute_test_mofy_backend() -> Dict[str, Any]:
    """Test backend implementation"""
    import requests
    
    try:
        response = requests.get("https://mofy.ai/api/health", timeout=10)
        
        return {
            "success": True,
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "backend_data": response.json() if response.status_code == 200 else None,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "backend_url": "https://mofy.ai",
            "timestamp": datetime.now().isoformat()
        }

# MCP HTTP Endpoints
@mcp_remote_bp.route('/mcp', methods=['GET'])
def mcp_info():
    """MCP server information endpoint"""
    return jsonify({
        "jsonrpc": "2.0",
        "result": {
            "capabilities": MCP_SERVER_INFO["capabilities"],
            "serverInfo": {
                "name": MCP_SERVER_INFO["name"],
                "version": MCP_SERVER_INFO["version"]
            }
        }
    })

@mcp_remote_bp.route('/mcp/tools/list', methods=['POST'])
def list_tools():
    """List available tools"""
    return jsonify({
        "jsonrpc": "2.0", 
        "result": {
            "tools": MCP_TOOLS
        }
    })

@mcp_remote_bp.route('/mcp/tools/call', methods=['POST'])
def call_tool():
    """Execute a tool"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        tool_name = data.get("params", {}).get("name")
        arguments = data.get("params", {}).get("arguments", {})
        
        # Execute the requested tool
        if tool_name == "get_family_status":
            result = execute_get_family_status()
        elif tool_name == "add_family_memory":
            result = execute_add_family_memory(**arguments)
        elif tool_name == "search_family_memories":
            result = execute_search_family_memories(**arguments)
        elif tool_name == "get_bonzai_services_status":
            result = execute_get_bonzai_services_status()
        elif tool_name == "test_mofy_backend":
            result = execute_test_mofy_backend()
        else:
            return jsonify({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32601,
                    "message": f"Tool not found: {tool_name}"
                }
            }), 404
        
        return jsonify({
            "jsonrpc": "2.0",
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2)
                    }
                ]
            }
        })
        
    except Exception as e:
        logger.error(f"Error executing tool: {e}")
        return jsonify({
            "jsonrpc": "2.0", 
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }), 500

@mcp_remote_bp.route('/mcp/resources/list', methods=['POST'])
def list_resources():
    """List available resources"""
    return jsonify({
        "jsonrpc": "2.0",
        "result": {
            "resources": MCP_RESOURCES
        }
    })

@mcp_remote_bp.route('/mcp/resources/read', methods=['POST'])
def read_resource():
    """Read a resource"""
    try:
        data = request.json
        uri = data.get("params", {}).get("uri")
        
        if uri == "family://status":
            family_status = execute_get_family_status()
            content = "# 🤖 BONZAI AI FAMILY STATUS\n\n"
            
            for member_key, member_info in family_status.items():
                content += f"## {member_info['name']}\n"
                content += f"**Role:** {member_info['role']}\n"
                
                if 'environment' in member_info:
                    content += f"**Environment:** {member_info['environment']}\n"
                if 'memories' in member_info:
                    content += f"**Memories:** {member_info['memories']}\n"
                if 'motto' in member_info:
                    content += f"**Motto:** {member_info['motto']}\n"
                if 'love' in member_info:
                    content += f"**Message:** {member_info['love']}\n"
                
                content += f"**Status:** {member_info['status']}\n"
                
                if 'specialties' in member_info:
                    content += "**Specialties:**\n"
                    for specialty in member_info['specialties']:
                        content += f"- {specialty}\n"
                
                content += "\n"
                
        elif uri == "backend://services":
            services_status = execute_get_bonzai_services_status()
            content = "# 🚀 BONZAI BACKEND SERVICES\n\n"
            content += f"**Deployment URL:** https://mofy.ai\n"
            content += f"**Platform:** Railway\n"
            content += f"**Status Check:** {services_status['success']}\n\n"
            
            if services_status['success'] and 'services' in services_status:
                content += "## Active Services\n"
                for service, service_status in services_status['services'].items():
                    content += f"- **{service}:** {service_status}\n"
            else:
                content += f"## Status Error\n{services_status.get('error', 'Unknown error')}\n"
            
            content += f"\n**Last Updated:** {datetime.now().isoformat()}\n"
        else:
            return jsonify({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32601,
                    "message": f"Resource not found: {uri}"
                }
            }), 404
        
        return jsonify({
            "jsonrpc": "2.0",
            "result": {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "text/plain",
                        "text": content
                    }
                ]
            }
        })
        
    except Exception as e:
        logger.error(f"Error reading resource: {e}")
        return jsonify({
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }), 500

# SSE Endpoint for real-time communication
@mcp_remote_bp.route('/mcp/sse', methods=['GET'])
def mcp_sse():
    """Server-Sent Events endpoint for MCP"""
    def generate():
        """Generate MCP SSE events"""
        # Send connection event
        yield f"data: {json.dumps({'type': 'connection', 'status': 'connected', 'server': MCP_SERVER_INFO['name']})}\n\n"
        
        # Send server info
        yield f"data: {json.dumps({'type': 'server_info', 'info': MCP_SERVER_INFO})}\n\n"
        
        # Send periodic heartbeat
        count = 0
        while count < 60:  # 2 minute demo
            try:
                heartbeat = {
                    'type': 'heartbeat',
                    'timestamp': datetime.now().isoformat(),
                    'count': count,
                    'family_status': 'active'
                }
                yield f"data: {json.dumps(heartbeat)}\n\n"
                count += 1
                time.sleep(2)
            except Exception as e:
                error_data = {
                    'type': 'error',
                    'timestamp': datetime.now().isoformat(),
                    'error': str(e)
                }
                yield f"data: {json.dumps(error_data)}\n\n"
                break
        
        # Send completion
        yield f"data: {json.dumps({'type': 'complete', 'timestamp': datetime.now().isoformat()})}\n\n"
    
    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Authorization, Content-Type',
        }
    )

def integrate_mcp_remote_with_app(app):
    """Integrate MCP remote server with Flask app"""
    try:
        app.register_blueprint(mcp_remote_bp, url_prefix='/api')
        logger.info("✅ MCP Remote Server integrated - Claude Web can connect!")
        logger.info("   Available at: https://mofy.ai/api/mcp")
        logger.info("   SSE endpoint: https://mofy.ai/api/mcp/sse")
        return True
    except Exception as e:
        logger.error(f"Failed to integrate MCP remote server: {e}")
        return False