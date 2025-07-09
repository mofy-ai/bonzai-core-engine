"""
 MCP + Agentic RAG API Endpoint for Revolutionary Workspace
This creates a FastAPI endpoint that connects our React frontend with the Python MCP system
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
import logging
import uvicorn
from datetime import datetime
import sys
import os

# Add the backend to Python path for services
backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_root)

logger = logging.getLogger(__name__)

app = FastAPI(title="Revolutionary Workspace API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances - We'll use mock implementations for now
mcp_orchestrator: Optional[Any] = None
gemini_orchestra: Optional[Any] = None

# Request/Response Models
class MCPAgenticRequest(BaseModel):
    user_request: str
    user_id: str
    session_context: Dict[str, Any] = {}
    intelligence_level: str = "AUTONOMOUS"

class MCPAgenticResponse(BaseModel):
    response: Dict[str, Any]
    agentic_enhancements: Dict[str, Any]
    processing_time_ms: float
    success: bool
    error_message: Optional[str] = None

class WorkspaceStatus(BaseModel):
    mcp_status: str
    orchestra_status: str
    intelligence_level: str
    active_models: List[str]
    performance_metrics: Dict[str, Any]

@app.on_event("startup")
async def startup_event():
    """Initialize the MCP + Agentic RAG system on startup"""
    global mcp_orchestrator, gemini_orchestra

    try:
        logger.info(" Initializing Revolutionary Workspace Backend...")

        # For now, we'll run in demo mode with mock implementations
        # This allows the frontend to work while we integrate the full MCP system
        logger.info(" Revolutionary Workspace Backend initialized in demo mode!")

    except Exception as e:
        logger.error(f" Failed to initialize backend: {e}")
        # Continue with demo mode

@app.post("/api/mcp-agentic-rag", response_model=MCPAgenticResponse)
async def process_mcp_agentic_request(request: MCPAgenticRequest, background_tasks: BackgroundTasks):
    """
    🧠 Main endpoint for MCP + Agentic RAG processing
    This is what our React frontend calls when users interact with the system
    """

    start_time = datetime.now()

    try:
        if not mcp_orchestrator:
            # Fallback demo response if not fully initialized
            return MCPAgenticResponse(
                response={
                    "message": f"🧠 MCP Agentic RAG processed: '{request.user_request}' (Demo Mode)",
                    "reasoning": "System is in demo mode - showing revolutionary capabilities!",
                    "enhancements": [
                        "Autonomous context retrieval",
                        "Cross-session learning patterns",
                        "Predictive model selection",
                        "Enhanced memory integration"
                    ]
                },
                agentic_enhancements={
                    "rag_decisions_made": 4,
                    "context_sources_used": 7,
                    "models_optimized": ["context_master_primary", "deep_thinker_primary", "creative_writer_primary"],
                    "processing_time_ms": 850,
                    "intelligence_level": request.intelligence_level
                },
                processing_time_ms=850,
                success=True
            )

        # Process with full MCP + Agentic RAG system
        result = await mcp_orchestrator.process_agentic_request(
            user_request=request.user_request,
            user_id=request.user_id,
            session_context=request.session_context
        )

        processing_time = (datetime.now() - start_time).total_seconds() * 1000

        return MCPAgenticResponse(
            response=result["response"],
            agentic_enhancements=result["agentic_enhancements"],
            processing_time_ms=processing_time,
            success=True
        )

    except Exception as e:
        logger.error(f"MCP Agentic processing failed: {e}")
        processing_time = (datetime.now() - start_time).total_seconds() * 1000

        return MCPAgenticResponse(
            response={"message": "Processing failed", "error": str(e)},
            agentic_enhancements={},
            processing_time_ms=processing_time,
            success=False,
            error_message=str(e)
        )

@app.get("/api/workspace/status", response_model=WorkspaceStatus)
async def get_workspace_status():
    """Get current status of the revolutionary workspace"""

    try:
        if not mcp_orchestrator or not gemini_orchestra:
            return WorkspaceStatus(
                mcp_status="demo_mode",
                orchestra_status="demo_mode",
                intelligence_level="AUTONOMOUS",
                active_models=["demo_model_1", "demo_model_2"],
                performance_metrics={
                    "total_requests": 0,
                    "average_response_time": 0,
                    "success_rate": 1.0,
                    "intelligence_improvements": 0.34
                }
            )

        # Get real status from initialized systems
        orchestra_models = await gemini_orchestra.get_active_models()
        metrics = mcp_orchestrator.rag_metrics

        return WorkspaceStatus(
            mcp_status="active",
            orchestra_status="active",
            intelligence_level=mcp_orchestrator.intelligence_level.name,
            active_models=orchestra_models,
            performance_metrics={
                "total_requests": metrics["total_decisions"],
                "average_response_time": metrics.get("average_response_time", 0),
                "success_rate": metrics["successful_predictions"] / max(metrics["total_decisions"], 1),
                "intelligence_improvements": metrics["average_response_improvement"]
            }
        )

    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workspace/intelligence-level")
async def set_intelligence_level(level: str):
    """Set the intelligence level of the MCP system"""

    try:
        if mcp_orchestrator:
            level_map = {
                "REACTIVE": RAGIntelligenceLevel.REACTIVE,
                "PROACTIVE": RAGIntelligenceLevel.PROACTIVE,
                "PREDICTIVE": RAGIntelligenceLevel.PREDICTIVE,
                "AUTONOMOUS": RAGIntelligenceLevel.AUTONOMOUS,
                "ORCHESTRATIVE": RAGIntelligenceLevel.ORCHESTRATIVE
            }

            if level in level_map:
                mcp_orchestrator.intelligence_level = level_map[level]
                return {"success": True, "new_level": level}
            else:
                raise HTTPException(status_code=400, detail="Invalid intelligence level")
        else:
            return {"success": True, "new_level": level, "note": "Demo mode"}

    except Exception as e:
        logger.error(f"Intelligence level change failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/workspace/metrics")
async def get_performance_metrics():
    """Get detailed performance metrics"""

    try:
        if not mcp_orchestrator:
            return {
                "demo_mode": True,
                "metrics": {
                    "decisions_made": 127,
                    "successful_predictions": 98,
                    "context_cache_hits": 45,
                    "average_improvement": 0.34,
                    "user_satisfaction": 0.89
                }
            }

        metrics = mcp_orchestrator.rag_metrics
        return {
            "demo_mode": False,
            "metrics": metrics,
            "learning_patterns": dict(mcp_orchestrator.learning_patterns),
            "decision_history": list(mcp_orchestrator.decision_history)[-10:]  # Last 10 decisions
        }

    except Exception as e:
        logger.error(f"Metrics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "Revolutionary Workspace API is running! ",
        "version": "1.0.0",
        "features": [
            "MCP + Agentic RAG Integration",
            "5-Level Intelligence System",
            "Autonomous Context Retrieval",
            "Cross-Session Learning",
            "Predictive Model Selection"
        ]
    }

# Revolutionary MCP Client Models and Endpoints
from services.revolutionary_mcp_service import revolutionary_mcp_service, McpAgent

class AgentSearchRequest(BaseModel):
    query: str = ""
    filters: Dict[str, Any] = {}

class AgentSuggestionRequest(BaseModel):
    project_context: str
    user_preferences: Optional[Dict[str, Any]] = {}

class AgentInstallRequest(BaseModel):
    agent_id: str
    source: str
    configuration: Optional[Dict[str, Any]] = {}

class AgentCreateRequest(BaseModel):
    name: str
    description: str
    capabilities: List[str]
    template_id: Optional[str] = None
    configuration: Dict[str, Any] = {}

# Revolutionary MCP Client Endpoints

@app.get("/api/revolutionary-mcp/status")
async def get_mcp_status():
    """Get Revolutionary MCP Client connection status"""
    try:
        status = revolutionary_mcp_service.get_connection_status()
        return {
            "success": True,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting MCP status: {e}")
        return {"success": False, "error": str(e)}

@app.post("/api/revolutionary-mcp/agents/search")
async def search_agents(request: AgentSearchRequest):
    """Search agents across all MCP marketplaces"""
    try:
        agents = await revolutionary_mcp_service.search_agents(request.query, request.filters)

        # Convert agents to dictionaries
        agent_dicts = []
        for agent in agents:
            agent_dicts.append({
                "id": agent.id,
                "name": agent.name,
                "description": agent.description,
                "author": agent.author,
                "category": agent.category,
                "rating": agent.rating,
                "downloads": agent.downloads,
                "logo": agent.logo,
                "source": agent.source,
                "capabilities": agent.capabilities,
                "configuration": agent.configuration
            })

        return {
            "success": True,
            "agents": agent_dicts,
            "total": len(agent_dicts),
            "query": request.query,
            "filters": request.filters
        }
    except Exception as e:
        logger.error(f"Error searching agents: {e}")
        return {"success": False, "error": str(e)}

@app.post("/api/revolutionary-mcp/agents/suggestions")
async def get_agent_suggestions(request: AgentSuggestionRequest):
    """Get Mama Bear AI agent suggestions for the project"""
    try:
        suggestions = await revolutionary_mcp_service.get_mama_bear_suggestions(
            request.project_context
        )

        return {
            "success": True,
            "suggestions": suggestions,
            "context": request.project_context,
            "mama_bear_reasoning": "Based on your project needs, I've identified these optimal agents for maximum productivity and code quality."
        }
    except Exception as e:
        logger.error(f"Error getting agent suggestions: {e}")
        return {"success": False, "error": str(e)}

@app.post("/api/revolutionary-mcp/agents/install")
async def install_agent(request: AgentInstallRequest):
    """Install an agent from a marketplace"""
    try:
        result = await revolutionary_mcp_service.install_agent(
            request.agent_id,
            request.source,
            request.configuration or {}
        )

        return {
            "success": True,
            "agent_id": request.agent_id,
            "installation_result": result,
            "message": f"Agent '{request.agent_id}' installed successfully from {request.source}"
        }
    except Exception as e:
        logger.error(f"Error installing agent: {e}")
        return {"success": False, "error": str(e)}

@app.post("/api/revolutionary-mcp/agents/create")
async def create_custom_agent(request: AgentCreateRequest):
    """Create a custom agent using Mama Bear orchestration"""
    try:
        config = {
            "name": request.name,
            "description": request.description,
            "capabilities": request.capabilities,
            "template_id": request.template_id,
            **request.configuration
        }

        agent = await revolutionary_mcp_service.create_custom_agent(config)

        return {
            "success": True,
            "agent": {
                "id": agent.id,
                "name": agent.name,
                "description": agent.description,
                "capabilities": agent.capabilities,
                "source": agent.source
            },
            "message": f"Custom agent '{agent.name}' created successfully with Mama Bear orchestration"
        }
    except Exception as e:
        logger.error(f"Error creating custom agent: {e}")
        return {"success": False, "error": str(e)}

@app.post("/api/revolutionary-mcp/docker/connect")
async def test_docker_connection():
    """Test Docker MCP Toolkit connection"""
    try:
        await revolutionary_mcp_service._connect_docker_mcp()
        return {
            "success": True,
            "message": "Docker MCP Toolkit connection successful",
            "docker_url": revolutionary_mcp_service.config['docker_mcp_url']
        }
    except Exception as e:
        logger.error(f"Error testing Docker connection: {e}")
        return {"success": False, "error": str(e)}

@app.on_event("startup")
async def startup_event():
    """Initialize Revolutionary MCP Service on startup"""
    logger.info(" Initializing Revolutionary MCP Client...")
    try:
        await revolutionary_mcp_service.initialize()
        logger.info(" Revolutionary MCP Client initialized successfully")
    except Exception as e:
        logger.error(f" Failed to initialize Revolutionary MCP Client: {e}")

if __name__ == "__main__":
    # Run the API server
    uvicorn.run(
        "mcp_api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
