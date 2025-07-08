"""
🤖 Zai Scrapybara API - Scout-Level Endpoints
Exposes all Scout capabilities through REST API for Zai
"""

from flask import Blueprint, request, jsonify, Response
import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Import the Scrapybara agent
try:
    from services.zai_scrapybara_integration import (
        ZaiScrapybaraAgent,
        create_zai_scrapybara_agent,
        integrate_with_zai_orchestrator
    )
    SCRAPYBARA_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Scrapybara integration not available: {e}")
    SCRAPYBARA_AVAILABLE = False
    ZaiScrapybaraAgent = None

# Create blueprint
zai_scrapybara_bp = Blueprint('zai_scrapybara', __name__, url_prefix='/api/mama-bear-scrapybara')

# Global agent instance
scrapybara_agent: Optional[ZaiScrapybaraAgent] = None

def create_response(success: bool, data: Any = None, error: str = None, status_code: int = 200) -> Response:
    """Create standardized API response"""
    response_data = {
        "success": success,
        "timestamp": datetime.now().isoformat(),
        "data": data,
        "error": error
    }
    return jsonify(response_data), status_code

async def get_scrapybara_agent() -> Optional[ZaiScrapybaraAgent]:
    """Get or create Scrapybara agent instance"""
    global scrapybara_agent
    
    if scrapybara_agent is None and SCRAPYBARA_AVAILABLE:
        try:
            config = {
                'scrapybara_api_key': request.headers.get('X-Scrapybara-Key') or 'default-key',
                'scrapybara_base_url': 'https://api.scrapybara.com/v1'
            }
            scrapybara_agent = await create_zai_scrapybara_agent(config)
        except Exception as e:
            logger.error(f"Failed to create Scrapybara agent: {e}")
            return None
    
    return scrapybara_agent

# === WEB BROWSING & RESEARCH ===

@zai_scrapybara_bp.route('/web-search', methods=['POST'])
def web_search():
    """Search the web like Scout does"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        user_id = data.get('user_id', 'anonymous')
        count = data.get('count', 5)
        
        if not query:
            return create_response(False, error="Query is required", status_code=400)
        
        async def execute_search():
            agent = await get_scrapybara_agent()
            if not agent:
                return {"success": False, "error": "Scrapybara agent not available"}
            
            async with agent:
                return await agent.web_search(query, user_id, count)
        
        result = asyncio.run(execute_search())
        return create_response(result['success'], result.get('result'), result.get('error'))
        
    except Exception as e:
        logger.error(f"Error in web search: {e}")
        return create_response(False, error=str(e), status_code=500)

@zai_scrapybara_bp.route('/browse-website', methods=['POST'])
def browse_website():
    """Browse websites like Scout does"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        user_id = data.get('user_id', 'anonymous')
        extract_markdown = data.get('extract_markdown', True)
        
        if not url:
            return create_response(False, error="URL is required", status_code=400)
        
        async def execute_browse():
            agent = await get_scrapybara_agent()
            if not agent:
                return {"success": False, "error": "Scrapybara agent not available"}
            
            async with agent:
                return await agent.browse_website(url, user_id, extract_markdown)
        
        result = asyncio.run(execute_browse())
        return create_response(result['success'], result.get('result'), result.get('error'))
        
    except Exception as e:
        logger.error(f"Error browsing website: {e}")
        return create_response(False, error=str(e), status_code=500)

# === CODE EXECUTION ===

@zai_scrapybara_bp.route('/execute-code', methods=['POST'])
def execute_code():
    """Execute code like Scout does"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', 'python')
        user_id = data.get('user_id', 'anonymous')
        session_id = data.get('session_id')
        
        if not code:
            return create_response(False, error="Code is required", status_code=400)
        
        async def execute_code_async():
            agent = await get_scrapybara_agent()
            if not agent:
                return {"success": False, "error": "Scrapybara agent not available"}
            
            async with agent:
                return await agent.execute_code(code, language, user_id, session_id)
        
        result = asyncio.run(execute_code_async())
        return create_response(result['success'], result.get('result'), result.get('error'))
        
    except Exception as e:
        logger.error(f"Error executing code: {e}")
        return create_response(False, error=str(e), status_code=500)

# === COPYCAPY FEATURES ===

@zai_scrapybara_bp.route('/copycapy-analyze', methods=['POST'])
def copycapy_analyze():
    """Analyze website structure with CopyCapy"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        user_id = data.get('user_id', 'anonymous')
        selector = data.get('selector')
        
        if not url:
            return create_response(False, error="URL is required", status_code=400)
        
        async def execute_copycapy():
            agent = await get_scrapybara_agent()
            if not agent:
                return {"success": False, "error": "Scrapybara agent not available"}
            
            async with agent:
                return await agent.copycapy_website(url, user_id, selector)
        
        result = asyncio.run(execute_copycapy())
        return create_response(result['success'], result.get('result'), result.get('error'))
        
    except Exception as e:
        logger.error(f"Error in CopyCapy analysis: {e}")
        return create_response(False, error=str(e), status_code=500)

# === IMAGE GENERATION ===

@zai_scrapybara_bp.route('/generate-image', methods=['POST'])
def generate_image():
    """Generate images like Scout does"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        user_id = data.get('user_id', 'anonymous')
        aspect_ratio = data.get('aspect_ratio', 'square')
        style = data.get('style', 'digital_art')
        
        if not prompt:
            return create_response(False, error="Prompt is required", status_code=400)
        
        async def execute_generation():
            agent = await get_scrapybara_agent()
            if not agent:
                return {"success": False, "error": "Scrapybara agent not available"}
            
            async with agent:
                return await agent.generate_image(prompt, user_id, aspect_ratio, style)
        
        result = asyncio.run(execute_generation())
        return create_response(result['success'], result.get('result'), result.get('error'))
        
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return create_response(False, error=str(e), status_code=500)

# === FILE OPERATIONS ===

@zai_scrapybara_bp.route('/file-operations', methods=['POST'])
def file_operations():
    """Handle file operations like Scout does"""
    try:
        data = request.get_json()
        operation = data.get('operation', '')  # read, write, list, delete
        file_path = data.get('file_path', '')
        user_id = data.get('user_id', 'anonymous')
        content = data.get('content')
        
        if not operation:
            return create_response(False, error="Operation is required", status_code=400)
        
        async def execute_file_op():
            agent = await get_scrapybara_agent()
            if not agent:
                return {"success": False, "error": "Scrapybara agent not available"}
            
            async with agent:
                return await agent.manage_files(operation, file_path, user_id, content)
        
        result = asyncio.run(execute_file_op())
        return create_response(result['success'], result.get('result'), result.get('error'))
        
    except Exception as e:
        logger.error(f"Error in file operations: {e}")
        return create_response(False, error=str(e), status_code=500)

@zai_scrapybara_bp.route('/download-file', methods=['POST'])
def download_file():
    """Download files like Scout does"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        save_path = data.get('save_path', '')
        user_id = data.get('user_id', 'anonymous')
        
        if not url or not save_path:
            return create_response(False, error="URL and save_path are required", status_code=400)
        
        async def execute_download():
            agent = await get_scrapybara_agent()
            if not agent:
                return {"success": False, "error": "Scrapybara agent not available"}
            
            async with agent:
                return await agent.download_file(url, save_path, user_id)
        
        result = asyncio.run(execute_download())
        return create_response(result['success'], result.get('result'), result.get('error'))
        
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return create_response(False, error=str(e), status_code=500)

# === COLLABORATIVE FEATURES ===

@zai_scrapybara_bp.route('/start-collaboration', methods=['POST'])
def start_collaboration():
    """Start collaborative session between user and Zai"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'anonymous')
        
        async def start_session():
            agent = await get_scrapybara_agent()
            if not agent:
                return {"success": False, "error": "Scrapybara agent not available"}
            
            async with agent:
                return await agent.start_collaborative_session(user_id)
        
        result = asyncio.run(start_session())
        return create_response(result['success'], result.get('result'), result.get('error'))
        
    except Exception as e:
        logger.error(f"Error starting collaboration: {e}")
        return create_response(False, error=str(e), status_code=500)

# === SCOUT WORKFLOW ===

@zai_scrapybara_bp.route('/scout-workflow', methods=['POST'])
def scout_workflow():
    """Execute Scout-style workflow: prompt → plan → production"""
    try:
        data = request.get_json()
        user_prompt = data.get('prompt', '')
        user_id = data.get('user_id', 'anonymous')
        workflow_type = data.get('workflow_type', 'full_stack')
        
        if not user_prompt:
            return create_response(False, error="Prompt is required", status_code=400)
        
        async def execute_workflow():
            agent = await get_scrapybara_agent()
            if not agent:
                return {"success": False, "error": "Scrapybara agent not available"}
            
            async with agent:
                return await agent.execute_scout_workflow(user_prompt, user_id, workflow_type)
        
        result = asyncio.run(execute_workflow())
        return create_response(result['success'], result.get('result'), result.get('error'))
        
    except Exception as e:
        logger.error(f"Error executing Scout workflow: {e}")
        return create_response(False, error=str(e), status_code=500)

# === STATUS & MANAGEMENT ===

@zai_scrapybara_bp.route('/capabilities', methods=['GET'])
def get_capabilities():
    """Get available Scrapybara capabilities"""
    try:
        async def get_caps():
            agent = await get_scrapybara_agent()
            if not agent:
                return {"success": False, "error": "Scrapybara agent not available"}
            
            async with agent:
                return await agent.get_capabilities()
        
        result = asyncio.run(get_caps())
        return create_response(True, result)
        
    except Exception as e:
        logger.error(f"Error getting capabilities: {e}")
        return create_response(False, error=str(e), status_code=500)

@zai_scrapybara_bp.route('/task-history', methods=['GET'])
def get_task_history():
    """Get recent task history for user"""
    try:
        user_id = request.args.get('user_id', 'anonymous')
        limit = int(request.args.get('limit', 10))
        
        async def get_history():
            agent = await get_scrapybara_agent()
            if not agent:
                return {"success": False, "error": "Scrapybara agent not available"}
            
            async with agent:
                history = await agent.get_task_history(user_id, limit)
                return {"success": True, "tasks": history}
        
        result = asyncio.run(get_history())
        return create_response(result['success'], result.get('tasks'), result.get('error'))
        
    except Exception as e:
        logger.error(f"Error getting task history: {e}")
        return create_response(False, error=str(e), status_code=500)

@zai_scrapybara_bp.route('/active-sessions', methods=['GET'])
def get_active_sessions():
    """Get active collaborative sessions for user"""
    try:
        user_id = request.args.get('user_id', 'anonymous')
        
        async def get_sessions():
            agent = await get_scrapybara_agent()
            if not agent:
                return {"success": False, "error": "Scrapybara agent not available"}
            
            async with agent:
                sessions = await agent.get_active_sessions(user_id)
                return {"success": True, "sessions": sessions}
        
        result = asyncio.run(get_sessions())
        return create_response(result['success'], result.get('sessions'), result.get('error'))
        
    except Exception as e:
        logger.error(f"Error getting active sessions: {e}")
        return create_response(False, error=str(e), status_code=500)

# === MEM0 MEMORY & RAG ENDPOINTS ===

@zai_scrapybara_bp.route('/memory/store', methods=['POST'])
def store_memory():
    """Store information in persistent memory using Mem0"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        user_id = data.get('user_id', 'anonymous')
        metadata = data.get('metadata', {})
        
        if not content:
            return create_response(False, error="Content is required", status_code=400)
        
        async def store_memory_async():
            agent = await get_scrapybara_agent()
            if not agent:
                return {"success": False, "error": "Scrapybara agent not available"}
            
            async with agent:
                return await agent.store_memory(content, metadata)
        
        result = asyncio.run(store_memory_async())
        return create_response(result['success'], result.get('memory_id'), result.get('error'))
        
    except Exception as e:
        logger.error(f"Error storing memory: {e}")
        return create_response(False, error=str(e), status_code=500)

@zai_scrapybara_bp.route('/memory/search', methods=['POST'])
def search_memory():
    """Search persistent memory using Mem0"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        user_id = data.get('user_id', 'anonymous')
        limit = data.get('limit', 5)
        
        if not query:
            return create_response(False, error="Query is required", status_code=400)
        
        async def search_memory_async():
            agent = await get_scrapybara_agent()
            if not agent:
                return {"success": False, "error": "Scrapybara agent not available"}
            
            async with agent:
                return await agent.search_memory(query, limit)
        
        result = asyncio.run(search_memory_async())
        return create_response(result['success'], result.get('memories'), result.get('error'))
        
    except Exception as e:
        logger.error(f"Error searching memory: {e}")
        return create_response(False, error=str(e), status_code=500)

@zai_scrapybara_bp.route('/memory/stats', methods=['GET'])
def get_memory_stats():
    """Get memory usage statistics"""
    try:
        user_id = request.args.get('user_id', 'anonymous')
        
        async def get_stats():
            agent = await get_scrapybara_agent()
            if not agent:
                return {"success": False, "error": "Scrapybara agent not available"}
            
            async with agent:
                return await agent.get_memory_stats()
        
        result = asyncio.run(get_stats())
        return create_response(result['success'], result.get('stats'), result.get('error'))
        
    except Exception as e:
        logger.error(f"Error getting memory stats: {e}")
        return create_response(False, error=str(e), status_code=500)

@zai_scrapybara_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for Scrapybara integration"""
    try:
        status = {
            "scrapybara_available": SCRAPYBARA_AVAILABLE,
            "agent_initialized": scrapybara_agent is not None,
            "timestamp": datetime.now().isoformat(),
            "capabilities": [
                "web_search",
                "browse_website", 
                "execute_code",
                "copycapy_analyze",
                "generate_image",
                "file_operations",
                "download_file",
                "start_collaboration",
                "scout_workflow",
                "memory_store",
                "memory_search",
                "memory_stats"
            ],
            "mem0_enabled": True,
            "mem0_rag_enabled": True,
            "mem0_user_id": "nathan_sanctuary"
        }
        
        return create_response(True, status)
        
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return create_response(False, error=str(e), status_code=500)

# === INTEGRATION FUNCTION ===

def integrate_zai_scrapybara_api(app):
    """Integrate Zai Scrapybara API with Flask app"""
    try:
        app.register_blueprint(zai_scrapybara_bp)
        logger.info("🐻 Zai Scrapybara API integrated successfully")
        
        # Initialize agent on startup
        with app.app_context():
            if SCRAPYBARA_AVAILABLE:
                logger.info("🚀 Initializing Zai Scrapybara agent...")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to integrate Zai Scrapybara API: {e}")
        return False