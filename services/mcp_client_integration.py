# backend/services/mcp_client_integration.py
"""
[LINK] MCP Client Integration for Gemini Orchestra
Connects your 7 Gemini models to MCP servers via standardized protocol
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class MCPServer:
    """Represents an MCP server connection"""
    name: str
    url: str
    capabilities: List[str]
    health_endpoint: str = "/health"

class MCPClientManager:
    """
    [MUSIC] MCP Client for Gemini Orchestra
    
    Provides standardized tool access for your 7 Gemini models:
    - Filesystem operations
    - Web search capabilities  
    - Memory management
    - Custom tool integration
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.servers: Dict[str, MCPServer] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Default MCP servers for your setup
        self.default_servers = {
            "filesystem": MCPServer(
                name="filesystem",
                url="http://localhost:3001",
                capabilities=["read_file", "write_file", "list_directory", "search_files"]
            ),
            "search": MCPServer(
                name="search", 
                url="http://localhost:3002",
                capabilities=["web_search", "local_search"]
            ),
            "memory": MCPServer(
                name="memory",
                url="http://localhost:3003", 
                capabilities=["store_memory", "search_memory", "update_memory"]
            )
        }
        
        logger.info("[LINK] MCP Client Manager initialized for Gemini Orchestra")
    
    async def initialize(self):
        """Initialize MCP client connections"""
        self.session = aiohttp.ClientSession()
        
        # Register default servers
        for server_name, server in self.default_servers.items():
            await self.register_server(server)
        
        logger.info("[OK] MCP Client connections established")
    
    async def register_server(self, server: MCPServer):
        """Register a new MCP server"""
        try:
            # Test server health
            health_check = await self.check_server_health(server)
            if health_check:
                self.servers[server.name] = server
                logger.info(f"[OK] MCP Server '{server.name}' registered successfully")
            else:
                logger.warning(f"[EMOJI] MCP Server '{server.name}' health check failed")
        except Exception as e:
            logger.error(f"Failed to register MCP server '{server.name}': {e}")
    
    async def check_server_health(self, server: MCPServer) -> bool:
        """Check if MCP server is healthy"""
        try:
            if not self.session:
                return False
                
            async with self.session.get(f"{server.url}{server.health_endpoint}") as response:
                return response.status == 200
        except Exception as e:
            logger.error(f"Health check failed for {server.name}: {e}")
            return False
    
    async def call_mcp_tool(self, 
                           server_name: str, 
                           tool_name: str, 
                           parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call an MCP tool for your Gemini Orchestra
        
        Args:
            server_name: Name of MCP server (filesystem, search, memory)
            tool_name: Tool to call (read_file, web_search, etc.)
            parameters: Tool parameters
            
        Returns:
            Tool response data
        """
        
        if server_name not in self.servers:
            raise ValueError(f"MCP server '{server_name}' not registered")
        
        server = self.servers[server_name]
        
        if tool_name not in server.capabilities:
            raise ValueError(f"Tool '{tool_name}' not available on server '{server_name}'")
        
        try:
            # Prepare MCP request
            mcp_request = {
                "jsonrpc": "2.0",
                "id": f"gemini_orchestra_{asyncio.current_task().get_name() if asyncio.current_task() else 'unknown'}",
                "method": f"tools/{tool_name}",
                "params": parameters
            }
            
            # Call MCP server
            async with self.session.post(
                f"{server.url}/mcp",
                json=mcp_request,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"[OK] MCP tool '{tool_name}' executed successfully")
                    return result.get("result", {})
                else:
                    error_text = await response.text()
                    logger.error(f"MCP tool call failed: {response.status} - {error_text}")
                    return {"error": f"MCP call failed: {response.status}"}
                    
        except Exception as e:
            logger.error(f"MCP tool call exception: {e}")
            return {"error": str(e)}
    
    # Convenience methods for your Gemini Orchestra
    
    async def read_file_via_mcp(self, file_path: str) -> Dict[str, Any]:
        """Read file using MCP filesystem server"""
        return await self.call_mcp_tool("filesystem", "read_file", {"path": file_path})
    
    async def search_web_via_mcp(self, query: str, count: int = 5) -> Dict[str, Any]:
        """Search web using MCP search server"""
        return await self.call_mcp_tool("search", "web_search", {"query": query, "count": count})
    
    async def store_memory_via_mcp(self, user_id: str, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Store memory using MCP memory server"""
        return await self.call_mcp_tool("memory", "store_memory", {
            "user_id": user_id,
            "content": content,
            "metadata": metadata or {}
        })
    
    async def search_memory_via_mcp(self, user_id: str, query: str) -> Dict[str, Any]:
        """Search memory using MCP memory server"""
        return await self.call_mcp_tool("memory", "search_memory", {
            "user_id": user_id,
            "query": query
        })
    
    async def get_available_tools(self) -> Dict[str, List[str]]:
        """Get all available MCP tools across servers"""
        tools = {}
        for server_name, server in self.servers.items():
            tools[server_name] = server.capabilities
        return tools
    
    async def route_request_to_mcp(self, 
                                  user_request: str, 
                                  context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        [MUSIC] Smart routing for Gemini Orchestra + MCP
        
        Analyzes user request and routes to appropriate MCP tools
        """
        
        request_lower = user_request.lower()
        mcp_results = {}
        
        # File operations
        if any(word in request_lower for word in ["file", "read", "write", "directory"]):
            if "filesystem" in self.servers:
                # Extract file path from request (simple heuristic)
                if "read" in request_lower and "/" in user_request:
                    file_path = user_request.split("/")[-1].split()[0]
                    mcp_results["file_content"] = await self.read_file_via_mcp(file_path)
        
        # Web search
        if any(word in request_lower for word in ["search", "find", "latest", "current", "web"]):
            if "search" in self.servers:
                mcp_results["search_results"] = await self.search_web_via_mcp(user_request)
        
        # Memory operations
        if any(word in request_lower for word in ["remember", "recall", "memory", "previous"]):
            if "memory" in self.servers:
                user_id = context.get("user_id", "anonymous") if context else "anonymous"
                mcp_results["memory_results"] = await self.search_memory_via_mcp(user_id, user_request)
        
        return {
            "mcp_enhanced": True,
            "tools_used": list(mcp_results.keys()),
            "results": mcp_results,
            "available_servers": list(self.servers.keys())
        }
    
    async def close(self):
        """Close MCP client connections"""
        if self.session:
            await self.session.close()
        logger.info("[LINK] MCP Client connections closed")

# Integration with your existing Gemini Orchestra
async def integrate_mcp_with_gemini_orchestra(gemini_orchestra, config: Dict[str, Any] = None):
    """
    [MUSIC] Integrate MCP with your existing Gemini Orchestra
    
    This enhances your 7 Gemini models with standardized tool access
    """
    
    mcp_client = MCPClientManager(config)
    await mcp_client.initialize()
    
    # Add MCP capabilities to your orchestra
    if hasattr(gemini_orchestra, 'mcp_client'):
        gemini_orchestra.mcp_client = mcp_client
        logger.info("[OK] MCP integrated with Gemini Orchestra")
    
    return mcp_client

# Example usage for your setup
async def example_gemini_mcp_usage():
    """Example of how your Gemini Orchestra can use MCP"""
    
    mcp_client = MCPClientManager()
    await mcp_client.initialize()
    
    # Your Gemini model can now use standardized tools
    user_request = "Search for the latest AI developments and save to memory"
    
    # Route through MCP
    mcp_results = await mcp_client.route_request_to_mcp(
        user_request, 
        context={"user_id": "example_user"}
    )
    
    print(f"MCP Enhanced Results: {mcp_results}")
    
    await mcp_client.close()

if __name__ == "__main__":
    # Test the MCP integration
    asyncio.run(example_gemini_mcp_usage())