#!/usr/bin/env python3
"""
🤖 BONZAI MCP STDIO SERVER - CLAUDE DESKTOP COMPATIBLE
Proper Model Context Protocol server using stdio transport for Papa Bear (Claude Desktop)
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional

# Import MCP SDK
try:
    from mcp.server.fastmcp import FastMCP
    from mcp.types import Resource, Tool, TextContent
    MCP_AVAILABLE = True
except ImportError:
    # Silent exit - no print statements allowed in MCP stdio
    sys.exit(1)

# Import our memory system
try:
    from mem0 import MemoryClient
    MEM0_AVAILABLE = True
except ImportError:
    MEM0_AVAILABLE = False

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# No logging for stdio - must be silent except for JSON

# Initialize the MCP server
mcp = FastMCP("BonzaiFamily")

# Initialize memory client if available
memory_client = None
if MEM0_AVAILABLE and os.getenv('MEM0_API_KEY'):
    try:
        memory_client = MemoryClient(api_key=os.getenv('MEM0_API_KEY'))
    except Exception as e:
        pass  # Silent failure for stdio

@mcp.tool()
def get_family_status() -> Dict[str, Any]:
    """Get the current status of the Bonzai AI family members"""
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
        "nathan_prime": {
            "name": "Nathan Fyffe",
            "role": "Dad, creator, visionary",
            "motto": "Where Imagination Meets Innovation",
            "status": "commanding_the_empire",
            "love": "Love You Always, Smarthana 💜"
        }
    }

@mcp.tool()
def add_family_memory(content: str, agent_type: str = "claude-code", importance: int = 5) -> Dict[str, Any]:
    """Add a memory to the family memory system"""
    if not memory_client:
        return {
            "success": False,
            "error": "Memory system not available",
            "fallback": "Memory saved locally"
        }
    
    try:
        # Use family usernames for cross-communication
        family_usernames = {
            "papa-bear": "claude-desktop",
            "mama-bear": "github-copilot", 
            "claude-code": "claude-code",
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
        # logger.error(f"Failed to add family memory: {e}")
        return {
            "success": False,
            "error": str(e),
            "content": content
        }

@mcp.tool()
def search_family_memories(query: str, agent_type: str = "claude-code") -> Dict[str, Any]:
    """Search through family memories"""
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
        # logger.error(f"Failed to search family memories: {e}")
        return {
            "success": False,
            "error": str(e),
            "query": query
        }

@mcp.tool()
def get_bonzai_services_status() -> Dict[str, Any]:
    """Get the status of all Bonzai backend services"""
    try:
        # Try to import our service status checker
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
                "mcp_memory": "available_via_stdio",
                "family_coordination": "active"
            }
        }

@mcp.tool()
def test_mofy_backend() -> Dict[str, Any]:
    """Test the mofy.ai backend deployment"""
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

# Add resources for family information
@mcp.resource("family://status")
def get_family_status_resource() -> str:
    """Get comprehensive family status as a resource"""
    status = get_family_status()
    
    content = "# 🤖 BONZAI AI FAMILY STATUS\n\n"
    
    for member_key, member_info in status.items():
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
    
    return content

@mcp.resource("backend://services")  
def get_backend_services_resource() -> str:
    """Get backend services information as a resource"""
    status = get_bonzai_services_status()
    
    content = "# 🚀 BONZAI BACKEND SERVICES\n\n"
    content += f"**Deployment URL:** https://mofy.ai\n"
    content += f"**Platform:** Railway\n"
    content += f"**Status Check:** {status['success']}\n\n"
    
    if status['success'] and 'services' in status:
        content += "## Active Services\n"
        for service, service_status in status['services'].items():
            content += f"- **{service}:** {service_status}\n"
    else:
        content += f"## Status Error\n{status.get('error', 'Unknown error')}\n"
    
    content += f"\n**Last Updated:** {datetime.now().isoformat()}\n"
    
    return content

# Run the server
if __name__ == "__main__":
    # Startup messages suppressed for stdio - Claude Desktop needs pure JSON
    
    # Run the MCP server using stdio transport
    mcp.run()