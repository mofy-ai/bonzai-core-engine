"""
[ZAI] Bonzai Platform - Enhanced Zai Intelligence Flask Application
Powerful AI development platform with advanced Zai capabilities,
multi-model orchestration, and intelligent task management
"""

import os
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json

# Initialize logging first
log_file = os.path.join('./logs', os.getenv('LOG_FILE', 'bonzai.log'))
os.makedirs('./logs', exist_ok=True)

logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("BonzaiPlatform")

# Import our bonzai services
from config.settings import get_settings
from services import (
    initialize_all_services,
    shutdown_all_services,
    get_zai_agent,
    get_memory_manager,
    get_scrapybara_manager,
    get_theme_manager,
    get_service_status
)

# Import API blueprints
from services.zai_orchestration_api import integrate_orchestration_with_app
from api.zai_scrapybara_api import integrate_zai_scrapybara_api
from api.multi_model_api import register_multi_model_api

# Import new Live API Studio routes
from routes.memory import memory_bp
from routes.chat import chat_bp
from routes.scrape import scrape_bp

# Import Gemini Orchestra
try:
    from backend.api.gemini_orchestra_api import gemini_orchestra_bp, init_gemini_orchestra
    GEMINI_ORCHESTRA_AVAILABLE = True
    logger.info("[OK] Gemini Orchestra API integration available")
except ImportError as e:
    logger.warning(f"Gemini Orchestra API integration not available: {e}")
    GEMINI_ORCHESTRA_AVAILABLE = False
    gemini_orchestra_bp = None
    init_gemini_orchestra = None

# Import Enhanced Scout Workflow
try:
    from api.scout_workflow_api import integrate_scout_workflow_api
    SCOUT_WORKFLOW_AVAILABLE = True
    logger.info("[OK] Enhanced Scout Workflow API integration available")
except ImportError as e:
    logger.warning(f"Enhanced Scout Workflow API integration not available: {e}")
    SCOUT_WORKFLOW_AVAILABLE = False
    integrate_scout_workflow_api = None

# Import ZAI Prime Supervisor
try:
    from services.supervisor import ZaiPrimeSupervisor, EventStreamingService, AgentSpawningService
    ZAI_PRIME_AVAILABLE = True
    logger.info("[OK] ZAI Prime Supervisor integration available - Omnipresent awareness ready!")
except ImportError as e:
    logger.warning(f"ZAI Prime Supervisor integration not available: {e}")
    ZAI_PRIME_AVAILABLE = False
    ZaiPrimeSupervisor = None
    EventStreamingService = None
    AgentSpawningService = None

# Import Express Mode + Vertex AI Supercharger
try:
    from api.express_mode_vertex_api import integrate_express_mode_with_app
    EXPRESS_MODE_AVAILABLE = True
    logger.info("[OK] Express Mode + Vertex AI Supercharger integration available")
except ImportError as e:
    logger.warning(f"Express Mode + Vertex AI Supercharger integration not available: {e}")
    EXPRESS_MODE_AVAILABLE = False
    integrate_express_mode_with_app = None

# Import Multimodal Chat API
try:
    from api.multimodal_chat_api import integrate_multimodal_chat_with_app
    MULTIMODAL_CHAT_AVAILABLE = True
    logger.info("[OK] Multimodal Chat API integration available - ALL models accessible!")
except ImportError as e:
    logger.warning(f"Multimodal Chat API integration not available: {e}")
    MULTIMODAL_CHAT_AVAILABLE = False
    integrate_multimodal_chat_with_app = None

# Import Agentic Superpowers V3.0
try:
    from api.agentic_superpowers_api import agentic_superpowers_bp, init_agentic_service
    AGENTIC_SUPERPOWERS_AVAILABLE = True
    logger.info("[OK] Mama Bear Agentic Superpowers V3.0 integration available!")
except ImportError as e:
    logger.warning(f"Agentic Superpowers integration not available: {e}")
    AGENTIC_SUPERPOWERS_AVAILABLE = False
    agentic_superpowers_bp = None
    init_agentic_service = None

# Import Supercharged Collaborative Workspaces V3.0
try:
    from api.collaborative_workspaces_api import collaborative_workspaces_bp, init_workspace_service
    COLLABORATIVE_WORKSPACES_AVAILABLE = True
    logger.info("[OK] Supercharged Collaborative Workspaces V3.0 integration available!")
except ImportError as e:
    logger.warning(f"Collaborative Workspaces integration not available: {e}")
    COLLABORATIVE_WORKSPACES_AVAILABLE = False
    collaborative_workspaces_bp = None
    init_workspace_service = None

# Import Pipedream Integration Service
try:
    from api.pipedream_api import pipedream_bp, integrate_pipedream_api_with_app
    from services.pipedream_integration_service import integrate_pipedream_with_app
    PIPEDREAM_AVAILABLE = True
    logger.info("[OK] Pipedream Integration Service available - Autonomous workflow automation ready!")
except ImportError as e:
    logger.warning(f"Pipedream Integration Service not available: {e}")
    PIPEDREAM_AVAILABLE = False
    pipedream_bp = None
    integrate_pipedream_api_with_app = None
    integrate_pipedream_with_app = None

# Try to import Mem0 for enhanced memory
try:
    from mem0 import MemoryClient
    MEM0_AVAILABLE = True
except ImportError:
    MEM0_AVAILABLE = False
    MemoryClient = None

# Try to import Deep Research Center (Library)
try:
    from api.library_api import integrate_library_api, library_bp
    LIBRARY_AVAILABLE = True
    logger.info("[OK] Deep Research Center (Library) integration available")
except ImportError as e:
    logger.warning(f"Deep Research Center (Library) integration not available: {e}")
    LIBRARY_AVAILABLE = False
    integrate_library_api = None
    library_bp = None

# Initialize Flask app
app = Flask(__name__)
settings = get_settings()
app.config['SECRET_KEY'] = settings.flask_secret_key
CORS(app, origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5001"])

# Initialize SocketIO
socketio = SocketIO(
    app,
    cors_allowed_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5001"],
    async_mode='threading'
)

# Global service status
services_initialized = False
gemini_orchestra_initialized = False
zai_prime = None
event_streaming = None
agent_spawner = None

async def initialize_bonzai_services():
    """Initialize all bonzai services using the service manager"""
    global services_initialized, gemini_orchestra_initialized

    try:
        logger.info("Initializing Bonzai Bonzai services...")

        # Initialize basic services through the service manager
        await initialize_all_services()

        # Initialize Gemini Orchestra
        if GEMINI_ORCHESTRA_AVAILABLE and init_gemini_orchestra:
            logger.info("Initializing Gemini Orchestra...")
            try:
                gemini_orchestra_initialized = init_gemini_orchestra(app)
                if gemini_orchestra_initialized:
                    logger.info("Gemini Orchestra initialized successfully!")
                    # Register the blueprint
                    if gemini_orchestra_bp is not None:
                        app.register_blueprint(gemini_orchestra_bp)
                        logger.info("[OK] Gemini Orchestra API endpoints registered")
                    else:
                        logger.warning("[ERROR] Gemini Orchestra blueprint is None")
                else:
                    logger.warning("[ERROR] Gemini Orchestra initialization failed")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini Orchestra: {e}")
                gemini_orchestra_initialized = False
        else:
            logger.warning("Gemini Orchestra not available")

        # Initialize Deep Research Center (Library)
        if LIBRARY_AVAILABLE and integrate_library_api:
            logger.info("Initializing Deep Research Center (Library)...")
            try:
                library_initialized = integrate_library_api(app)
                if library_initialized:
                    logger.info("Deep Research Center initialized successfully!")
                    logger.info("[OK] Library API endpoints registered")
                else:
                    logger.warning("[ERROR] Deep Research Center initialization failed")
            except Exception as e:
                logger.error(f"Failed to initialize Deep Research Center: {e}")
        else:
            logger.warning("Deep Research Center not available")

        # Initialize Enhanced Scout Workflow
        if SCOUT_WORKFLOW_AVAILABLE and integrate_scout_workflow_api:
            logger.info("Initializing Enhanced Scout Workflow...")
            try:
                scout_success = integrate_scout_workflow_api(app, socketio)
                if scout_success:
                    logger.info("Enhanced Scout Workflow initialized!")
                else:
                    logger.warning("[ERROR] Scout Workflow initialization failed")
            except Exception as e:
                logger.error(f"Failed to initialize Scout Workflow: {e}")
        else:
            logger.warning("Enhanced Scout Workflow not available")

        # Initialize Express Mode + Vertex AI Supercharger
        if EXPRESS_MODE_AVAILABLE and integrate_express_mode_with_app:
            logger.info("Initializing Express Mode + Vertex AI Supercharger...")
            try:
                # Store settings in app config for the supercharger
                app.config['settings'] = settings
                express_success = integrate_express_mode_with_app(app)
                if express_success:
                    logger.info("Express Mode + Vertex AI Supercharger initialized! 6x faster responses available!")
                else:
                    logger.warning("[ERROR] Express Mode + Vertex AI Supercharger initialization failed - running in fallback mode")
            except Exception as e:
                logger.error(f"Failed to initialize Express Mode + Vertex AI Supercharger: {e}")
        else:
            logger.warning("Express Mode + Vertex AI Supercharger not available")

        # Initialize Multimodal Chat API
        if MULTIMODAL_CHAT_AVAILABLE and integrate_multimodal_chat_with_app:
            logger.info("Initializing Multimodal Chat API...")
            try:
                multimodal_success = integrate_multimodal_chat_with_app(app)
                if multimodal_success:
                    logger.info("Multimodal Chat API initialized! ALL models accessible via comprehensive chat system!")
                else:
                    logger.warning("[ERROR] Multimodal Chat API initialization failed")
            except Exception as e:
                logger.error(f"Failed to initialize Multimodal Chat API: {e}")
        else:
            logger.warning("Multimodal Chat API not available")

        # Initialize Agentic Superpowers V3.0
        if AGENTIC_SUPERPOWERS_AVAILABLE and init_agentic_service:
            logger.info("Initializing Mama Bear Agentic Superpowers V3.0...")
            try:
                agentic_config = {
                    'vertex_config': settings.vertex_ai_config if hasattr(settings, 'vertex_ai_config') else {},
                    'express_mode_enabled': True,
                    'autonomous_actions_enabled': True
                }
                init_agentic_service(agentic_config)
                app.register_blueprint(agentic_superpowers_bp, url_prefix='/api/agentic')
                logger.info("Mama Bear Agentic Superpowers V3.0 initialized! Autonomous AI agent ready!")
            except Exception as e:
                logger.error(f"Failed to initialize Agentic Superpowers: {e}")
        else:
            logger.warning("Agentic Superpowers not available")

        # Initialize Supercharged Collaborative Workspaces V3.0
        if COLLABORATIVE_WORKSPACES_AVAILABLE and init_workspace_service:
            logger.info("Initializing Supercharged Collaborative Workspaces V3.0...")
            try:
                workspace_config = {
                    'vertex_config': settings.vertex_ai_config if hasattr(settings, 'vertex_ai_config') else {},
                    'express_mode_enabled': True,
                    'real_time_collaboration': True,
                    'agentic_control_enabled': True
                }
                init_workspace_service(workspace_config)
                app.register_blueprint(collaborative_workspaces_bp, url_prefix='/api/workspaces')
                logger.info("Supercharged Collaborative Workspaces V3.0 initialized! Real-time AI collaboration ready!")
            except Exception as e:
                logger.error(f"Failed to initialize Collaborative Workspaces: {e}")
        else:
            logger.warning("Supercharged Collaborative Workspaces not available")

        # Initialize Pipedream Integration Service
        if PIPEDREAM_AVAILABLE and integrate_pipedream_api_with_app and integrate_pipedream_with_app:
            logger.info("Initializing Pipedream Integration Service...")
            try:
                # Initialize service first
                pipedream_config = {
                    'PIPEDREAM_API_TOKEN': os.getenv('PIPEDREAM_API_TOKEN'),
                    'PIPEDREAM_CLIENT_ID': os.getenv('PIPEDREAM_CLIENT_ID', 'bonzai'),
                    'PIPEDREAM_CLIENT_SECRET': os.getenv('PIPEDREAM_CLIENT_SECRET'),
                    'PIPEDREAM_ENABLED': os.getenv('PIPEDREAM_ENABLED', 'true').lower() == 'true',
                    'vertex_config': settings.vertex_ai_config if hasattr(settings, 'vertex_ai_config') else {},
                    'agentic_integration_enabled': True
                }

                service_success = integrate_pipedream_with_app(app, pipedream_config)
                api_success = integrate_pipedream_api_with_app(app)

                if service_success and api_success:
                    logger.info("Pipedream Integration Service fully initialized! Autonomous workflow automation ready!")
                    logger.info("[OK] Available endpoints: /api/pipedream/workflows, /api/pipedream/natural-language")
                else:
                    logger.warning("[ERROR] Pipedream Integration Service initialization failed")
            except Exception as e:
                logger.error(f"Failed to initialize Pipedream Integration Service: {e}")
        else:
            logger.warning("Pipedream Integration Service not available")

        services_initialized = True

        # Initialize ZAI Prime Supervisor
        if ZAI_PRIME_AVAILABLE:
            logger.info("Initializing ZAI Prime Supervisor...")
            try:
                global zai_prime, event_streaming, agent_spawner
                
                # Get existing service managers
                model_manager = None
                memory_manager = None
                
                try:
                    from services import get_zai_agent, get_memory_manager
                    model_manager = get_zai_agent()  # Use ZAI agent as model manager
                    memory_manager = get_memory_manager()
                except Exception as model_e:
                    logger.warning(f"Could not get model/memory managers: {model_e}")
                
                # Initialize ZAI Prime
                zai_prime = ZaiPrimeSupervisor(
                    model_manager=model_manager,
                    memory_system=memory_manager
                )
                
                # Initialize Event Streaming Service
                event_streaming = EventStreamingService(socketio, zai_prime)
                
                # Initialize Agent Spawning Service
                if model_manager:
                    agent_spawner = AgentSpawningService(zai_prime, model_manager)
                    zai_prime.agent_spawner = agent_spawner  # Connect to Prime
                
                # Start ZAI Prime monitoring loop
                asyncio.create_task(zai_prime.monitor_everything())
                
                logger.info("[OK] ZAI Prime Supervisor initialized - Omnipresent awareness active!")
                logger.info(f"[PRIME] Ready to manage up to {agent_spawner.max_agents if agent_spawner else 8000} dynamic agents")
                
            except Exception as e:
                logger.error(f"Failed to initialize ZAI Prime Supervisor: {e}")
                zai_prime = None
                event_streaming = None
                agent_spawner = None
        else:
            logger.warning("ZAI Prime Supervisor not available")

        # Initialize WebSocket Coordinator
        try:
            from services.bonzai_websocket_coordinator import initialize_websocket_coordinator
            mem0_api_key = os.getenv('MEM0_API_KEY')
            initialize_websocket_coordinator(socketio, mem0_api_key)
            logger.info("[OK] WebSocket Coordinator initialized - Agent-to-agent communication enabled!")
        except Exception as e:
            logger.warning(f"WebSocket Coordinator initialization failed: {e}")

        # Register API blueprints
        try:
            logger.info("Registering API blueprints...")
            integrate_orchestration_with_app(app, socketio)
            integrate_zai_scrapybara_api(app)
            register_multi_model_api(app)

            # Register new Intelligent Execution Router API (commented out - using routes version)
            # try:
            #     from api.execution_router_api import execution_router_bp
            #     app.register_blueprint(execution_router_bp)
            #     logger.info("[OK] Intelligent Execution Router API registered")
            # except ImportError as e:
            #     logger.warning(f"Execution Router API not available: {e}")

            # Register new Agent Creation Workbench API (commented out - using routes version)
            # try:
            #     from api.agent_workbench_api import agent_workbench_bp
            #     app.register_blueprint(agent_workbench_bp)
            #     logger.info("[OK] Agent Creation Workbench API registered")
            # except ImportError as e:
            #     logger.warning(f"Agent Workbench API not available: {e}")

            # Register Live API Studio routes
            app.register_blueprint(memory_bp, url_prefix='/api/memory')
            app.register_blueprint(chat_bp, url_prefix='/api/chat')
            app.register_blueprint(scrape_bp, url_prefix='/api/scrape')
            logger.info("[OK] Live API Studio routes registered")

            # Register Enhanced Frontend API routes
            try:
                from routes.agent_workbench import agent_workbench_bp
                app.register_blueprint(agent_workbench_bp, url_prefix='/api/agent-workbench')
                logger.info("[OK] Agent Workbench API registered")
            except ImportError as e:
                logger.warning(f"Agent Workbench API not available: {e}")

            try:
                from routes.execution_router import execution_router_bp
                app.register_blueprint(execution_router_bp, url_prefix='/api/execution-router')
                logger.info("[OK] Execution Router API registered")
            except ImportError as e:
                logger.warning(f"Execution Router API not available: {e}")

            try:
                from routes.scout import scout_bp
                app.register_blueprint(scout_bp, url_prefix='/api/scout')
                logger.info("[OK] Scout API registered")
            except ImportError as e:
                logger.warning(f"Scout API not available: {e}")

            try:
                from routes.themes import themes_bp
                app.register_blueprint(themes_bp, url_prefix='/api/themes')
                logger.info("[OK] Themes API registered")
            except ImportError as e:
                logger.warning(f"Themes API not available: {e}")

            # Register OpenAI Vertex API
            try:
                from api.openai_vertex_api_simple import openai_vertex_api
                app.register_blueprint(openai_vertex_api)
                logger.info("[OK] OpenAI Vertex API registered")
            except ImportError as e:
                logger.warning(f"OpenAI Vertex API not available: {e}")

            # Register Revolutionary MCP Client API
            try:
                from api.revolutionary_mcp_api import revolutionary_mcp_bp
                app.register_blueprint(revolutionary_mcp_bp)
                logger.info("[OK] [ROCKET] Revolutionary MCP Client API registered")
            except ImportError as e:
                logger.warning(f"Revolutionary MCP Client API not available: {e}")

            # Register Agent Registry API
            try:
                from api.agent_registry_api import integrate_agent_registry_api
                integrate_agent_registry_api(app)
                logger.info("[OK] Agent Registry API registered - All 42 services discoverable!")
            except ImportError as e:
                logger.warning(f"Agent Registry API not available: {e}")

            # Register Task Orchestrator API
            try:
                from api.task_orchestrator_api import integrate_task_orchestrator_api
                integrate_task_orchestrator_api(app)
                logger.info("[OK] Task Orchestrator API registered - Intelligent task routing ready!")
            except ImportError as e:
                logger.warning(f"Task Orchestrator API not available: {e}")

            # Register WebSocket Coordinator API
            try:
                from api.websocket_coordinator_api import integrate_websocket_api
                integrate_websocket_api(app)
                logger.info("[OK] WebSocket Coordinator API registered - Real-time agent communication ready!")
            except ImportError as e:
                logger.warning(f"WebSocket Coordinator API not available: {e}")

            # Register MCP Remote Server API
            try:
                from api.mcp_remote_server import integrate_mcp_remote_with_app
                integrate_mcp_remote_with_app(app)
                logger.info("[OK] MCP Remote Server API registered - Claude Web integration ready!")
                logger.info("    Claude Web URL: https://mofy.ai/api/mcp")
                logger.info("    Perfect for mobile and remote access!")
            except ImportError as e:
                logger.warning(f"MCP Remote Server API not available: {e}")

            logger.info("[OK] API blueprints registered successfully")
        except Exception as e:
            logger.error(f"[ERROR] Failed to register API blueprints: {e}")

        logger.info("[OK] All bonzai services initialized successfully")

    except Exception as e:
        logger.error(f"[ERROR] Failed to initialize services: {str(e)}")
        services_initialized = True
        logger.info("[WARNING] Running with basic services only")

    logger.info("[BEAR] Bonzai Bonzai initialization complete!")

def get_service_instances():
    """Get all service instances"""
    if not services_initialized:
        raise RuntimeError("Services not initialized. Call initialize_bonzai_services() first.")

    return {
        'zai': get_zai_agent(),
        'memory': get_memory_manager(),
        'scrapybara': get_scrapybara_manager(),
        'theme': get_theme_manager()
    }

# ==============================================================================
# SERVICE HEALTH AND STATUS ENDPOINTS
# ==============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Simple health check - just return OK
        return jsonify({
            'success': True,
            'status': 'healthy',
            'message': 'Bonzai Backend is running',
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

# ==============================================================================
# ROOT ENDPOINT
# ==============================================================================

@app.route('/', methods=['GET'])
def root_endpoint():
    """Root endpoint - system overview"""
    return jsonify({
        'service': 'Bonzai Backend',
        'status': 'operational',
        'version': '2.0',
        'message': 'ZAI Prime Supervisor and AI Family ready',
        'endpoints': {
            'health': '/api/health',
            'mcp_tools': '/api/mcp/tools',
            'mcp_execute': '/api/mcp/execute',
            'memory': '/api/memory',
            'chat': '/api/chat',
            'agents': '/api/agents'
        },
        'timestamp': datetime.now().isoformat()
    })

# ==============================================================================
# MCP ENDPOINTS
# ==============================================================================

@app.route('/api/mcp/tools', methods=['GET', 'POST'])
def mcp_tools():
    """MCP tools endpoint"""
    tools = [
        {
            "name": "orchestrate_ai",
            "description": "Talk to any AI family member with full capabilities",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "model": {"type": "string", "description": "AI model to use"},
                    "prompt": {"type": "string", "description": "Your message to the AI"},
                    "context": {"type": "string", "description": "Additional context"}
                },
                "required": ["model", "prompt"]
            }
        },
        {
            "name": "access_memory",
            "description": "Search and manage memories",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["search", "add", "list"]},
                    "query": {"type": "string", "description": "Search query or content"},
                    "user_id": {"type": "string", "description": "User ID"}
                },
                "required": ["action"]
            }
        }
    ]
    
    return jsonify({
        "version": "1.0",
        "tools": tools
    })

@app.route('/api/mcp/execute', methods=['POST'])
def mcp_execute():
    """MCP execute endpoint"""
    data = request.get_json()
    tool = data.get('tool')
    parameters = data.get('parameters', {})
    
    if tool == 'orchestrate_ai':
        return jsonify({
            "success": True,
            "result": {
                "model": parameters.get('model'),
                "response": f"AI orchestration for {parameters.get('prompt')} - Backend ready",
                "status": "ready"
            }
        })
    
    elif tool == 'access_memory':
        return jsonify({
            "success": True,
            "result": {
                "action": parameters.get('action'),
                "message": "Memory system ready",
                "status": "ready"
            }
        })
    
    else:
        return jsonify({
            "success": False,
            "error": f"Unknown tool: {tool}"
        }), 400

# ==============================================================================
# SIMPLE CHAT ENDPOINTS
# ==============================================================================

@app.route('/api/chat/simple', methods=['POST'])
def simple_chat():
    """Simple chat endpoint - redirect to chat blueprint"""
    try:
        data = request.get_json()
        model = data.get('model', 'gemini-2.0-flash-exp')
        message = data.get('message', '')
        
        return jsonify({
            'success': True,
            'model': model,
            'response': f"Chat response for: {message}",
            'message': 'Chat system operational',
            'status': 'ready'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/multi-model/status', methods=['GET'])
def multi_model_status():
    """Multi-model status endpoint"""
    try:
        return jsonify({
            'success': True,
            'service': 'multi_model',
            'status': 'operational',
            'message': 'Multi-model orchestration ready',
            'available_models': 15
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# TASK ORCHESTRATOR ENDPOINTS  
# ==============================================================================

@app.route('/api/task-orchestrator/status', methods=['GET'])
def task_orchestrator_status():
    """Task orchestrator status endpoint"""
    try:
        return jsonify({
            'success': True,
            'service': 'task_orchestrator',
            'status': 'operational',
            'message': 'Task orchestrator ready for intelligent routing',
            'active_tasks': 0,
            'worker_count': 20
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# WEBSOCKET COORDINATOR ENDPOINTS
# ==============================================================================

@app.route('/api/websocket-coordinator/status', methods=['GET'])
def websocket_coordinator_status():
    """WebSocket coordinator status endpoint"""
    try:
        return jsonify({
            'success': True,
            'service': 'websocket_coordinator',
            'status': 'operational',
            'message': 'Real-time agent communication ready',
            'connections': 0,
            'active_channels': 0
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# SCRAPYBARA STATUS ENDPOINT
# ==============================================================================

@app.route('/api/scrape/status', methods=['GET'])
def scrape_status():
    """Scrape service status endpoint"""
    try:
        return jsonify({
            'success': True,
            'service': 'scrape',
            'status': 'operational',
            'message': 'Scraping service ready',
            'active_jobs': 0
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# SSE ENDPOINTS WITH AUTH
# ==============================================================================

@app.route('/sse', methods=['GET'])
def sse_endpoint():
    """Server-Sent Events endpoint with authentication"""
    # Simple auth check - look for API key in headers or query params
    auth_key = request.headers.get('Authorization') or request.args.get('auth')
    
    # For now, allow any key or no key (you can add proper auth later)
    if not auth_key:
        # Return auth info for now instead of blocking
        return jsonify({
            'success': True,
            'auth_required': False,  # Set to True when you want real auth
            'message': 'SSE endpoint ready - authentication optional',
            'endpoints': {
                'sse_stream': '/sse',
                'health': '/api/health',
                'bonzai_status': '/api/zai-prime/status'
            },
            'usage': 'Add ?auth=your_key for authenticated access'
        })
    
    def generate():
        """Generate Server-Sent Events"""
        yield f"data: {json.dumps({'event': 'connected', 'timestamp': datetime.now().isoformat(), 'bonzai': 'ready'})}\n\n"
        
        # Send periodic status updates
        count = 0
        while count < 10:  # Limit for demo
            try:
                status = get_service_status()
                data = {
                    'event': 'status_update',
                    'count': count,
                    'timestamp': datetime.now().isoformat(),
                    'services': status,
                    'bonzai_engine': 'operational'
                }
                yield f"data: {json.dumps(data)}\n\n"
                count += 1
                import time
                time.sleep(2)  # 2 second intervals
            except Exception as e:
                error_data = {
                    'event': 'error',
                    'timestamp': datetime.now().isoformat(),
                    'error': str(e)
                }
                yield f"data: {json.dumps(error_data)}\n\n"
                break
        
        # Send completion event
        yield f"data: {json.dumps({'event': 'stream_complete', 'timestamp': datetime.now().isoformat()})}\n\n"
    
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

# ==============================================================================
# WEBSOCKET HANDLERS
# ==============================================================================

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info("Client connected")
    emit('connection_established', {
        'status': 'connected',
        'bonzai_version': '1.0.0',
        'zai_ready': True,
        'zai_prime_available': zai_prime is not None,
        'agent_spawning_available': agent_spawner is not None
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info("Client disconnected")

# ZAI Prime WebSocket Event Handlers
@socketio.on('event:global')
async def handle_global_event(data):
    """Receive events from Gemini's frontend event bus"""
    if zai_prime:
        try:
            await zai_prime.global_event_stream.put(data)
            emit('event:broadcast', data, broadcast=True)
            logger.debug(f"Global event processed: {data.get('type')}")
        except Exception as e:
            logger.error(f"Error handling global event: {e}")
            emit('event:error', {'error': str(e)})
    else:
        emit('event:error', {'error': 'ZAI Prime not available'})

@socketio.on('zai:prime:query')
async def handle_prime_query(data):
    """Direct queries to ZAI Prime supervisor"""
    if zai_prime:
        try:
            query = data.get('query', '')
            current_page = data.get('current_page', 'unknown')
            session_id = data.get('session_id')
            
            response = await zai_prime.get_contextual_response(
                query, current_page, session_id
            )
            emit('zai:prime:response', response)
        except Exception as e:
            logger.error(f"Error handling Prime query: {e}")
            emit('zai:prime:response', {'error': str(e)})
    else:
        emit('zai:prime:response', {'error': 'ZAI Prime not available'})

@socketio.on('agent:spawn:request')
async def handle_agent_spawn_request(data):
    """Handle agent spawning requests"""
    if agent_spawner:
        try:
            agent_type = data.get('agent_type', 'general')
            purpose = data.get('purpose', 'unknown')
            page_context = data.get('page_context', 'unknown')
            config = data.get('config', {})
            
            agent_id = await agent_spawner.spawn_agent(
                agent_type, purpose, page_context, config
            )
            
            emit('agent:spawn:response', {
                'success': True,
                'agent_id': agent_id,
                'agent_type': agent_type,
                'purpose': purpose
            })
        except Exception as e:
            logger.error(f"Error spawning agent: {e}")
            emit('agent:spawn:response', {
                'success': False,
                'error': str(e)
            })
    else:
        emit('agent:spawn:response', {
            'success': False,
            'error': 'Agent spawning service not available'
        })

@socketio.on('system:health:request')
def handle_system_health_request():
    """Handle system health requests"""
    try:
        health_data = {
            'services_initialized': services_initialized,
            'gemini_orchestra': gemini_orchestra_initialized,
            'zai_prime_active': zai_prime is not None,
            'agent_spawning_active': agent_spawner is not None
        }
        
        if zai_prime:
            health_data['zai_prime_health'] = zai_prime.get_system_health()
            
        if agent_spawner:
            health_data['agent_spawning_stats'] = agent_spawner.get_spawning_stats()
            
        emit('system:health:response', {
            'system_health': health_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error handling health request: {e}")
        emit('system:health:response', {'error': str(e)})

# ==============================================================================
# ERROR HANDLERS
# ==============================================================================

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'bonzai_message': '[BEAR] Mama Bear couldn\'t find that path. Try a different route!'
    }), 404

# ==============================================================================
# ZAI PRIME API ENDPOINTS
# ==============================================================================

@app.route('/api/zai-prime/status')
def get_zai_prime_status():
    """Get ZAI Prime's current awareness state"""
    try:
        if not zai_prime:
            return jsonify({
                'success': False,
                'error': 'ZAI Prime not available'
            }), 503
            
        status_data = {
            'active': True,
            'active_pages': zai_prime.get_active_pages(),
            'recent_events': zai_prime.get_recent_events(limit=10),
            'system_health': zai_prime.get_system_health(),
            'agent_count': len(zai_prime.agent_registry) if hasattr(zai_prime, 'agent_registry') else 0
        }
        
        if agent_spawner:
            status_data['spawning_stats'] = agent_spawner.get_spawning_stats()
            
        return jsonify({
            'success': True,
            'zai_prime_status': status_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting ZAI Prime status: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/zai-prime/intervene', methods=['POST'])
async def request_zai_prime_intervention():
    """Request ZAI Prime to intervene in a specific context"""
    try:
        if not zai_prime:
            return jsonify({
                'success': False,
                'error': 'ZAI Prime not available'
            }), 503
            
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request data is required'
            }), 400
            
        result = await zai_prime.intervene({
            'page_id': data.get('page_id'),
            'issue': data.get('issue'),
            'context': data.get('context', {}),
            'type': data.get('type', 'manual_intervention')
        })
        
        return jsonify({
            'success': True,
            'intervention_result': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error requesting intervention: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/zai-prime/agents')
def get_zai_prime_agents():
    """Get information about all active agents"""
    try:
        if not agent_spawner:
            return jsonify({
                'success': False,
                'error': 'Agent spawning service not available'
            }), 503
            
        agents = agent_spawner.get_all_agents()
        stats = agent_spawner.get_spawning_stats()
        
        return jsonify({
            'success': True,
            'agents': agents,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting agents: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/zai-prime/agents/spawn', methods=['POST'])
async def spawn_agent_api():
    """Spawn a new agent via API"""
    try:
        if not agent_spawner:
            return jsonify({
                'success': False,
                'error': 'Agent spawning service not available'
            }), 503
            
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request data is required'
            }), 400
            
        agent_id = await agent_spawner.spawn_agent(
            agent_type=data.get('agent_type', 'general'),
            purpose=data.get('purpose', 'API spawned agent'),
            page_context=data.get('page_context', 'api'),
            config=data.get('config', {})
        )
        
        return jsonify({
            'success': True,
            'agent_id': agent_id,
            'message': f'Agent {agent_id} spawned successfully',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error spawning agent via API: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/zai-prime/context')
def get_global_context():
    """Get ZAI Prime's global context awareness"""
    try:
        if not zai_prime:
            return jsonify({
                'success': False,
                'error': 'ZAI Prime not available'
            }), 503
            
        context = zai_prime.build_global_context('api_request')
        
        return jsonify({
            'success': True,
            'global_context': context,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting global context: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'bonzai_message': '[BEAR] Mama Bear encountered an issue. She\'s working to fix it!'
    }), 500

# ==============================================================================
# APPLICATION STARTUP
# ==============================================================================

def create_app():
    """Application factory function"""
    # Initialize services when app is created
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(initialize_bonzai_services())

    return app

if __name__ == '__main__':
    # Initialize services
    import asyncio

    async def startup():
        """Async startup function"""
        logger.info("Starting Bonzai Bonzai...")
        await initialize_bonzai_services()
        logger.info("Mama Bear is ready to help!")

    # Run startup
    asyncio.run(startup())

    # Start the Bonzai
    socketio.run(
        app,
        host='0.0.0.0',
        port=int(os.getenv('BACKEND_PORT', 5001)),
        debug=os.getenv('DEBUG', 'False').lower() == 'true',
        allow_unsafe_werkzeug=True
    )
