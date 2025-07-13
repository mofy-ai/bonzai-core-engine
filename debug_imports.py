#!/usr/bin/env python3
"""Debug all import failures in bonzai-core-engine"""

import sys
import traceback

# Test all problematic imports
imports_to_test = [
    "backend.api.gemini_orchestra_api",
    "api.scout_workflow_api", 
    "services.supervisor",
    "api.express_mode_vertex_api",
    "api.multimodal_chat_api",
    "api.agentic_superpowers_api",
    "api.collaborative_workspaces_api",
    "api.pipedream_api",
    "services.pipedream_integration_service",
    "api.library_api",
    "routes.agent_workbench",
    "routes.execution_router", 
    "routes.scout",
    "routes.themes",
    "api.openai_vertex_api_simple",
    "api.revolutionary_mcp_api",
    "api.agent_registry_api",
    "api.task_orchestrator_api",
    "api.websocket_coordinator_api",
    "api.mcp_remote_server"
]

print("🔍 TESTING ALL IMPORTS...")
print("=" * 50)

failed_imports = []
success_imports = []

for module_name in imports_to_test:
    try:
        __import__(module_name)
        print(f"✅ {module_name}")
        success_imports.append(module_name)
    except Exception as e:
        print(f"❌ {module_name}: {str(e)}")
        failed_imports.append((module_name, str(e)))

print(f"\n📊 RESULTS:")
print(f"✅ Success: {len(success_imports)}")
print(f"❌ Failed: {len(failed_imports)}")

if failed_imports:
    print(f"\n🚨 FAILED IMPORTS TO FIX:")
    for module, error in failed_imports:
        print(f"  - {module}: {error}")

# Also test the correct supervisor import path
print(f"\n🔍 TESTING CORRECT SUPERVISOR IMPORT PATH...")
try:
    from services.supervisor import ZaiPrimeSupervisor, EventStreamingService, AgentSpawningService
    print("✅ services.supervisor (with classes) - THIS SHOULD BE USED IN app.py!")
except Exception as e:
    print(f"❌ services.supervisor (with classes): {e}")

# Test the correct supervisor submodule imports
try:
    from services.supervisor.zai_prime_supervisor import ZaiPrimeSupervisor
    from services.supervisor.event_streaming_service import EventStreamingService
    from services.supervisor.agent_spawning_service import AgentSpawningService
    print("✅ services.supervisor submodules - Working correctly!")
except Exception as e:
    print(f"❌ services.supervisor submodules: {e}")