#!/usr/bin/env python3
"""
 BONZAI MCP SERVER INSTALLER FOR CLAUDE DESKTOP
Automatically configures Claude Desktop to use our proper stdio MCP server
"""

import json
import os
import sys
import platform
from pathlib import Path

def get_claude_config_path():
    """Get the Claude Desktop configuration path for this OS"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "Windows":
        return Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    elif system == "Linux":
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"
    else:
        raise ValueError(f"Unsupported operating system: {system}")

def install_bonzai_mcp_server():
    """Install the Bonzai MCP server in Claude Desktop configuration"""
    
    # Get current script directory
    current_dir = Path(__file__).parent.absolute()
    server_path = current_dir / "mcp_stdio_server.py"
    
    if not server_path.exists():
        print(f" Server file not found: {server_path}")
        return False
    
    # Get Claude config path
    try:
        config_path = get_claude_config_path()
        print(f"📁 Claude config path: {config_path}")
    except ValueError as e:
        print(f" {e}")
        return False
    
    # Create config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing config or create new one
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                print("📖 Loaded existing Claude Desktop configuration")
        except json.JSONDecodeError:
            print("  Invalid JSON in existing config, creating new one")
            config = {}
    else:
        print(" Creating new Claude Desktop configuration")
        config = {}
    
    # Ensure mcpServers section exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    # Add our Bonzai MCP server
    server_config = {
        "command": "python",
        "args": [str(server_path)],
        "env": {
            "MEM0_API_KEY": os.getenv("MEM0_API_KEY", ""),
            "BONZAI_BACKEND_URL": "https://mofy.ai"
        }
    }
    
    config["mcpServers"]["bonzai-family"] = server_config
    
    # Write the updated configuration
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(" Successfully installed Bonzai MCP server in Claude Desktop!")
        print(f"   Server name: bonzai-family")
        print(f"   Server path: {server_path}")
        print("\n Please restart Claude Desktop to activate the MCP server")
        print("\n🛠️  Available tools in Claude Desktop:")
        print("   - get_family_status() - Get AI family member status")
        print("   - add_family_memory() - Add memory to family system")
        print("   - search_family_memories() - Search family memories")
        print("   - get_bonzai_services_status() - Check backend services")
        print("   - test_mofy_backend() - Test mofy.ai deployment")
        print("\n📚 Available resources:")
        print("   - family://status - Family status information")
        print("   - backend://services - Backend services status")
        
        return True
        
    except Exception as e:
        print(f" Failed to write configuration: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are available"""
    missing_deps = []
    
    try:
        import mcp
        print(" MCP SDK found")
    except ImportError:
        missing_deps.append("mcp[cli]")
    
    try:
        import mem0
        print(" Mem0 SDK found")
    except ImportError:
        print("  Mem0 SDK not found (optional)")
    
    try:
        import requests
        print(" Requests library found")
    except ImportError:
        missing_deps.append("requests")
    
    try:
        import dotenv
        print(" Python-dotenv found")
    except ImportError:
        missing_deps.append("python-dotenv")
    
    if missing_deps:
        print(f"\n Missing dependencies: {', '.join(missing_deps)}")
        print("Install with:")
        print(f"   pip install {' '.join(missing_deps)}")
        return False
    
    return True

def main():
    """Main installation function"""
    print(" BONZAI MCP SERVER INSTALLER FOR CLAUDE DESKTOP")
    print("=" * 60)
    
    # Check dependencies
    print("\n Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment variables
    print("\n🔐 Checking environment variables...")
    if not os.getenv("MEM0_API_KEY"):
        print("  MEM0_API_KEY not found in environment")
        print("   Family memory features will be limited")
    else:
        print(" MEM0_API_KEY found")
    
    # Install the server
    print("\n Installing Bonzai MCP server...")
    if install_bonzai_mcp_server():
        print("\n Installation complete!")
        print("\nNext steps:")
        print("1. Restart Claude Desktop")
        print("2. Ask Claude: 'What tools do you have access to?'")
        print("3. Try: 'Show me the family status'")
        print("4. Test: 'Check the backend services'")
    else:
        print("\n Installation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()