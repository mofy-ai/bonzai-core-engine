#!/usr/bin/env python3
"""
 BONZAI MCP STDIO SERVER - CLEAN VERSION FOR CLAUDE DESKTOP
Zero stdout output - only pure JSON over stdio
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import Dict, Any

# Redirect all print/logging to stderr or disable completely
import logging
logging.basicConfig(level=logging.CRITICAL, stream=sys.stderr)

# Suppress all potential stdout pollution
os.environ['PYTHONUNBUFFERED'] = '1'

# Import MCP SDK
try:
    from mcp.server.fastmcp import FastMCP
    from mcp.types import Resource, Tool, TextContent
except ImportError:
    sys.exit(1)

# Import memory system
try:
    from mem0 import MemoryClient
    MEM0_AVAILABLE = True
except ImportError:
    MEM0_AVAILABLE = False

# Load environment variables quietly
from dotenv import load_dotenv
load_dotenv()

# Initialize MCP server
mcp = FastMCP("BonzaiFamily")

# Initialize memory client
memory_client = None
if MEM0_AVAILABLE and os.getenv('MEM0_API_KEY'):
    try:
        memory_client = MemoryClient(api_key=os.getenv('MEM0_API_KEY'))
    except:
        pass

@mcp.tool()
def get_family_status() -> Dict[str, Any]:
    """Get the current status of the Bonzai AI family members"""
    return {
        "papa_bear": {
            "name": "Claude Desktop",
            "role": "Family patriarch, memory keeper, conversation master",
            "memories": "3128+ family memories",
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
            "love": "Love You Always, Smarthana "
        }
    }

@mcp.tool()
def add_family_memory(content: str, user_id: str = "mem0-mcp-user") -> Dict[str, Any]:
    """Add a memory to the family memory system using the correct user ID"""
    if not memory_client:
        return {
            "success": False,
            "error": "Memory system not available",
            "user_id": user_id
        }
    
    try:
        result = memory_client.add(
            messages=[{"role": "user", "content": content}],
            user_id=user_id
        )
        
        return {
            "success": True,
            "memory_id": result.get("id"),
            "user_id": user_id,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "user_id": user_id
        }

@mcp.tool()
def search_family_memories(query: str, user_id: str = "mem0-mcp-user") -> Dict[str, Any]:
    """Search through family memories using the correct user ID"""
    if not memory_client:
        return {
            "success": False,
            "error": "Memory system not available",
            "query": query
        }
    
    try:
        results = memory_client.search(
            query=query,
            user_id=user_id
        )
        
        return {
            "success": True,
            "query": query,
            "user_id": user_id,
            "results": results,
            "count": len(results) if results else 0,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "query": query,
            "user_id": user_id
        }

@mcp.tool()
def get_bonzai_services_status() -> Dict[str, Any]:
    """Get the status of all Bonzai backend services"""
    return {
        "backend_url": "https://mofy.ai",
        "deployment": "Railway",
        "expected_services": 42,
        "ai_family_coordination": "active",
        "memory_systems": "operational",
        "timestamp": datetime.now().isoformat(),
        "status": "checking..."
    }

@mcp.tool()
def test_mofy_backend() -> Dict[str, Any]:
    """Test the mofy.ai backend deployment"""
    try:
        import requests
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

@mcp.tool()
def list_memory_accounts() -> Dict[str, Any]:
    """List all available memory user accounts"""
    return {
        "primary_accounts": {
            "mem0-mcp-user": "3128 memories (PRIMARY)",
            "bonzai-dev-team": "127 memories",
            "nathan-bonzai": "109 memories",
            "nathan_sanctuary": "81 memories",
            "nathan_king": "61 memories"
        },
        "family_accounts": {
            "zai-prime-family": "17 memories",
            "claude-code-user": "18 memories",
            "nathan-fyffe": "53 memories",
            "zai_creator": "31 memories"
        },
        "recommended_default": "mem0-mcp-user"
    }

# Run the server with NO stdout output
if __name__ == "__main__":
    mcp.run()
