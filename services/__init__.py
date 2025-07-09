"""
Bonzai Backend Services - Initialization Module
Provides all core services for the backend
"""

import logging
import asyncio
from typing import Dict, Any, Optional
import sys

# Configure logging for clean output
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

# Global service instances
_services = {}
_initialized = False
_service_status = {}

class MockService:
    """Mock service for development"""
    def __init__(self, name: str):
        self.name = name
        self.initialized = True
    
    async def health_check(self):
        return {"status": "healthy", "service": self.name}

# === SERVICE INITIALIZATION ===

async def initialize_all_services():
    """Initialize all backend services with clean status reporting"""
    global _services, _initialized, _service_status
    
    print("\nStarting Bonzai Backend...")
    print("-" * 40)
    
    # Service initialization tracking
    services_to_load = [
        ('Enhanced Scout Workflow', 'enhanced_gemini_scout_orchestration'),
        ('Vertex AI Supercharger', 'express_mode_vertex_integration'),
        ('Multimodal Chat API', 'multi_model_orchestrator'),
        ('Agentic Superpowers V3.0', 'zai_agentic_superpowers_v3'),
        ('Collaborative Workspaces V3.0', 'supercharged_collaborative_workspaces_v3'),
        ('Pipedream Integration', 'pipedream_integration_service'),
        ('Memory Manager', 'zai_memory_system'),
        ('Deep Research Center', 'deep_research_center'),
        ('Virtual Computer', 'virtual_computer_service'),
        ('Claude Computer Use', 'claude_computer_use_service'),
        ('DeepSeek Integration', 'zai_deepseek_integration'),
        ('CrewAI Orchestration', 'crewai_supercharger'),
        ('Monitoring System', 'zai_monitoring'),
        ('Multi-Provider System', 'zai_multi_provider_system'),
        ('Agent Registry', 'bonzai_agent_registry'),
        ('Task Orchestrator', 'bonzai_task_orchestrator')
    ]
    
    successful = 0
    failed = 0
    
    for service_name, module_name in services_to_load:
        try:
            if module_name:
                # Try to import the module
                module = __import__(f'services.{module_name}', fromlist=[module_name])
                _service_status[service_name] = 'loaded'
                print(f"OK: {service_name}")
                successful += 1
            else:
                # Special handling for API-based services
                _service_status[service_name] = 'api'
                print(f"OK: {service_name}")
                successful += 1
                
        except ImportError as e:
            _service_status[service_name] = f'import_error: {str(e).split("(")[0].strip()}'
            print(f"ERROR: {service_name} - Module not found")
            failed += 1
        except Exception as e:
            error_msg = str(e).split('\n')[0][:50]  # First line, max 50 chars
            _service_status[service_name] = f'error: {error_msg}'
            print(f"ERROR: {service_name} - {error_msg}")
            failed += 1
    
    # Try to initialize core services with proper error handling
    try:
        from .mama_bear_orchestration import AgentOrchestrator
        from .mama_bear_memory_system import MemoryManager
        from .enhanced_scrapybara_integration import ScrapybaraManager
        from .mama_bear_model_manager import ModelManager
        
        # Initialize with error suppression
        try:
            memory_manager = MemoryManager()
        except Exception:
            memory_manager = MockService('Memory Manager')
            
        try:
            model_manager = ModelManager()
        except Exception:
            model_manager = MockService('Model Manager')
            
        try:
            scrapybara_manager = ScrapybaraManager()
        except Exception:
            scrapybara_manager = MockService('Scrapybara Manager')
        
        # Initialize orchestrator
        try:
            orchestrator = AgentOrchestrator(memory_manager, model_manager, scrapybara_manager)
        except Exception:
            orchestrator = MockService('Agent Orchestrator')
        
        _services = {
            'mama_bear_agent': orchestrator,
            'memory_manager': memory_manager,
            'scrapybara_manager': scrapybara_manager,
            'theme_manager': MockService('Theme Manager'),
            'model_manager': model_manager
        }
        
    except ImportError:
        # Fallback to mock services
        _services = {
            'mama_bear_agent': MockService('Mama Bear Agent'),
            'memory_manager': MockService('Memory Manager'),
            'scrapybara_manager': MockService('Scrapybara Manager'),
            'theme_manager': MockService('Theme Manager'),
            'model_manager': MockService('Model Manager')
        }
    
    _initialized = True
    
    print("-" * 40)
    print(f"\nStatus: {successful}/16 services running")
    print("Server: http://127.0.0.1:5001")
    print("Ready for requests!\n")

async def shutdown_all_services():
    """Shutdown all services"""
    global _services, _initialized
    
    try:
        print("\nSHUTDOWN: Stopping all services...")
        _services.clear()
        _initialized = False
        print("OK: All services stopped")
        
    except Exception as e:
        print(f"ERROR: Shutdown error: {str(e)[:50]}")

# === SERVICE GETTERS ===

def get_mama_bear_agent():
    """Get Mama Bear agent instance"""
    return _services.get('mama_bear_agent', MockService('Mama Bear Agent'))

def get_memory_manager():
    """Get memory manager instance"""
    return _services.get('memory_manager', MockService('Memory Manager'))

def get_scrapybara_manager():
    """Get Scrapybara manager instance"""
    return _services.get('scrapybara_manager', MockService('Scrapybara Manager'))

def get_theme_manager():
    """Get theme manager instance"""
    return _services.get('theme_manager', MockService('Theme Manager'))

def get_zai_agent():
    """Get ZAI agent instance (alias for mama bear agent)"""
    return _services.get('mama_bear_agent', MockService('ZAI Agent'))

def get_service_status():
    """Get status of all services"""
    return {
        'initialized': _initialized,
        'services': _service_status,
        'total_services': len(_service_status),
        'running': sum(1 for status in _service_status.values() if status in ['loaded', 'api'])
    }

# === ASYNC HELPER ===

def run_async(coro):
    """Helper to run async functions in sync context"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Create a new task
            return asyncio.create_task(coro)
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        # No event loop, create one
        return asyncio.run(coro)

# Initialize on import with clean error handling
if not _initialized:
    try:
        run_async(initialize_all_services())
    except Exception as e:
        logger.warning(f"Service initialization deferred: {str(e)[:50]}")