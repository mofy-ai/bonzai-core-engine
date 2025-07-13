#!/usr/bin/env python3
"""Debug all import failures in bonzai-core-engine"""

import sys
import os
import traceback
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test all problematic imports
imports_to_test = [
    # Backend API imports
    ("backend.api.gemini_orchestra_api", ["gemini_orchestra_bp", "init_gemini_orchestra"]),
    
    # API imports
    ("api.scout_workflow_api", ["integrate_scout_workflow_api"]),
    ("api.express_mode_vertex_api", ["integrate_express_mode_with_app"]),
    ("api.multimodal_chat_api", ["integrate_multimodal_chat_with_app"]),
    ("api.agentic_superpowers_api", ["agentic_superpowers_bp", "init_agentic_service"]),
    ("api.collaborative_workspaces_api", ["collaborative_workspaces_bp", "init_workspace_service"]),
    ("api.pipedream_api", ["pipedream_bp", "integrate_pipedream_api_with_app"]),
    ("api.library_api", ["integrate_library_api", "library_bp"]),
    ("api.openai_vertex_api_simple", ["openai_vertex_api"]),
    ("api.revolutionary_mcp_api", ["revolutionary_mcp_bp"]),
    ("api.agent_registry_api", ["integrate_agent_registry_api"]),
    ("api.task_orchestrator_api", ["integrate_task_orchestrator_api"]),
    ("api.websocket_coordinator_api", ["integrate_websocket_api"]),
    ("api.mcp_remote_server", ["integrate_mcp_remote_with_app"]),
    ("api.zai_scrapybara_api", ["integrate_zai_scrapybara_api"]),
    ("api.multi_model_api", ["register_multi_model_api"]),
    
    # Services imports
    ("services.supervisor", ["ZaiPrimeSupervisor", "EventStreamingService", "AgentSpawningService"]),
    ("services.pipedream_integration_service", ["integrate_pipedream_with_app"]),
    
    # Routes imports
    ("routes.memory", ["memory_bp"]),
    ("routes.chat", ["chat_bp"]),
    ("routes.scrape", ["scrape_bp"]),
    ("routes.agent_workbench", ["agent_workbench_bp"]),
    ("routes.execution_router", ["execution_router_bp"]),
    ("routes.scout", ["scout_bp"]),
    ("routes.themes", ["themes_bp"]),
    
    # External dependencies
    ("mem0", ["MemoryClient"]),
]

print("🔍 BONZAI CORE ENGINE - IMPORT DIAGNOSTIC")
print("=" * 60)
print(f"Timestamp: {datetime.now()}")
print(f"Python: {sys.version}")
print(f"Working Directory: {os.getcwd()}")
print("=" * 60)

failed_imports = []
success_imports = []
missing_files = []

# Check directory structure first
print("\n📁 CHECKING DIRECTORY STRUCTURE:")
directories_to_check = [
    "api", "backend/api", "services", "routes", "config"
]

for dir_path in directories_to_check:
    if os.path.exists(dir_path):
        print(f"✅ {dir_path}/ exists")
    else:
        print(f"❌ {dir_path}/ MISSING")
        missing_files.append(dir_path)

# Test imports
print("\n🧪 TESTING IMPORTS:")
print("-" * 60)

for module_info in imports_to_test:
    if isinstance(module_info, tuple):
        module_name, expected_attrs = module_info
    else:
        module_name = module_info
        expected_attrs = []
    
    try:
        module = __import__(module_name, fromlist=expected_attrs)
        # Check if expected attributes exist
        missing_attrs = []
        for attr in expected_attrs:
            if not hasattr(module, attr):
                missing_attrs.append(attr)
        
        if missing_attrs:
            print(f"⚠️  {module_name} - module loads but missing: {', '.join(missing_attrs)}")
            failed_imports.append((module_name, f"Missing attributes: {', '.join(missing_attrs)}"))
        else:
            print(f"✅ {module_name}")
            success_imports.append(module_name)
            
    except ImportError as e:
        error_msg = str(e)
        print(f"❌ {module_name}: {error_msg}")
        failed_imports.append((module_name, error_msg))
        
        # Check if it's a missing file
        module_path = module_name.replace('.', '/') + '.py'
        if not os.path.exists(module_path):
            missing_files.append(module_path)
            
    except Exception as e:
        print(f"💥 {module_name}: {type(e).__name__}: {str(e)}")
        failed_imports.append((module_name, f"{type(e).__name__}: {str(e)}"))

# Summary
print(f"\n📊 RESULTS SUMMARY:")
print("=" * 60)
print(f"✅ Successful imports: {len(success_imports)}")
print(f"❌ Failed imports: {len(failed_imports)}")
print(f"📁 Missing files/directories: {len(missing_files)}")

if failed_imports:
    print(f"\n🚨 FAILED IMPORTS DETAILS:")
    for module, error in failed_imports:
        print(f"  • {module}")
        print(f"    └─ Error: {error}")

if missing_files:
    print(f"\n📂 MISSING FILES/DIRECTORIES:")
    for file_path in missing_files:
        print(f"  • {file_path}")

# Check installed packages
print(f"\n📦 CHECKING KEY PACKAGES:")
packages_to_check = [
    "flask", "flask-cors", "flask-socketio", "mem0ai", "anthropic", 
    "openai", "google-cloud-aiplatform", "requests", "python-dotenv"
]

import importlib
for package in packages_to_check:
    try:
        importlib.import_module(package.replace('-', '_'))
        print(f"✅ {package}")
    except ImportError:
        print(f"❌ {package} - NOT INSTALLED")

print("\n" + "=" * 60)
print("🏁 DIAGNOSTIC COMPLETE")