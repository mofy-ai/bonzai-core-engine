"""
 Multi-Model API for Podplay Sanctuary
Exposes the multi-model orchestrator through REST endpoints
Supports Claude 3.5, Gemini, and OpenAI with intelligent routing
"""

from flask import Blueprint, request, jsonify
import asyncio
import logging
from typing import Dict, Any, List
from services.multi_model_orchestrator import (
    MultiModelOrchestrator, 
    ModelProvider, 
    CapabilityType,
    create_multi_model_orchestrator
)

logger = logging.getLogger(__name__)

# Create Blueprint
multi_model_bp = Blueprint('multi_model', __name__)

# Global orchestrator instance
orchestrator: MultiModelOrchestrator = None

async def get_orchestrator():
    """Get or create the multi-model orchestrator"""
    global orchestrator
    if orchestrator is None:
        orchestrator = await create_multi_model_orchestrator()
    return orchestrator

@multi_model_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for multi-model system"""
    try:
        return jsonify({
            "success": True,
            "service": "Multi-Model Orchestrator",
            "status": "healthy",
            "sanctuary_ready": True,
            "timestamp": "2025-06-08T00:42:00Z"
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@multi_model_bp.route('/models', methods=['GET'])
def get_available_models():
    """Get information about available AI models"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def _get_models():
            orch = await get_orchestrator()
            return orch.get_available_models()
        
        result = loop.run_until_complete(_get_models())
        loop.close()
        
        return jsonify({
            "success": True,
            "data": result,
            "sanctuary_note": " All models configured for neurodivergent-friendly development"
        })
        
    except Exception as e:
        logger.error(f"Error getting models: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@multi_model_bp.route('/chat', methods=['POST'])
def multi_model_chat():
    """
    Intelligent chat routing across multiple AI models
    Supports Claude 3.5, Gemini, and OpenAI with capability-based routing
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'prompt' not in data:
            return jsonify({
                "success": False,
                "error": "Missing required field: prompt"
            }), 400
        
        prompt = data['prompt']
        user_id = data.get('user_id', 'sanctuary_user')
        
        # Parse capabilities needed
        capabilities_raw = data.get('capabilities', ['function_calling'])
        capabilities_needed = []
        
        for cap in capabilities_raw:
            try:
                capabilities_needed.append(CapabilityType(cap))
            except ValueError:
                logger.warning(f"Unknown capability: {cap}")
        
        # Parse preferred provider
        preferred_provider = None
        if 'preferred_provider' in data:
            try:
                preferred_provider = ModelProvider(data['preferred_provider'])
            except ValueError:
                logger.warning(f"Unknown provider: {data['preferred_provider']}")
        
        # Execute request
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def _execute_chat():
            orch = await get_orchestrator()
            return await orch.route_request(
                prompt=prompt,
                user_id=user_id,
                capabilities_needed=capabilities_needed,
                preferred_provider=preferred_provider
            )
        
        result = loop.run_until_complete(_execute_chat())
        loop.close()
        
        return jsonify({
            "success": True,
            "data": result,
            "sanctuary_note": " Response generated with care for neurodivergent users"
        })
        
    except Exception as e:
        logger.error(f"Error in multi-model chat: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "sanctuary_note": " We're here to help - please try again"
        }), 500

@multi_model_bp.route('/gemini/function-call', methods=['POST'])
def gemini_function_call():
    """
    Specialized endpoint for Gemini function calling
    As requested - Gemini as the preferred function calling model
    """
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({
                "success": False,
                "error": "Missing required field: prompt"
            }), 400
        
        prompt = data['prompt']
        user_id = data.get('user_id', 'sanctuary_user')
        
        # Force Gemini for function calling
        capabilities_needed = [CapabilityType.FUNCTION_CALLING]
        preferred_provider = ModelProvider.GEMINI
        
        # Execute with Gemini
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def _execute_gemini():
            orch = await get_orchestrator()
            return await orch.route_request(
                prompt=prompt,
                user_id=user_id,
                capabilities_needed=capabilities_needed,
                preferred_provider=preferred_provider
            )
        
        result = loop.run_until_complete(_execute_gemini())
        loop.close()
        
        return jsonify({
            "success": True,
            "data": result,
            "provider": "gemini",
            "sanctuary_note": " Gemini function calling optimized for Sanctuary"
        })
        
    except Exception as e:
        logger.error(f"Error in Gemini function call: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@multi_model_bp.route('/claude/computer-use', methods=['POST'])
def claude_computer_use():
    """
    Specialized endpoint for Claude 3.5 Computer Use API
    Routes complex computer use tasks to Claude 3.5
    """
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({
                "success": False,
                "error": "Missing required field: prompt"
            }), 400
        
        prompt = data['prompt']
        user_id = data.get('user_id', 'sanctuary_user')
        
        # Force Claude for Computer Use API
        capabilities_needed = [CapabilityType.COMPUTER_USE, CapabilityType.FUNCTION_CALLING]
        preferred_provider = ModelProvider.CLAUDE
        
        # Execute with Claude
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def _execute_claude():
            orch = await get_orchestrator()
            return await orch.route_request(
                prompt=prompt,
                user_id=user_id,
                capabilities_needed=capabilities_needed,
                preferred_provider=preferred_provider
            )
        
        result = loop.run_until_complete(_execute_claude())
        loop.close()
        
        return jsonify({
            "success": True,
            "data": result,
            "provider": "claude",
            "sanctuary_note": "🖥️ Claude 3.5 Computer Use API for complex tasks"
        })
        
    except Exception as e:
        logger.error(f"Error in Claude Computer Use: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@multi_model_bp.route('/capabilities', methods=['GET'])
def get_capabilities():
    """Get available capabilities across all models"""
    try:
        capabilities = {
            "function_calling": {
                "description": "Execute functions and tools",
                "preferred_model": "gemini",
                "supported_models": ["claude", "gemini", "openai"]
            },
            "computer_use": {
                "description": "Computer Use API for complex interactions",
                "preferred_model": "claude",
                "supported_models": ["claude"]
            },
            "code_execution": {
                "description": "Execute and analyze code",
                "preferred_model": "gemini",
                "supported_models": ["claude", "gemini", "openai"]
            },
            "web_browsing": {
                "description": "Browse and analyze websites",
                "preferred_model": "claude",
                "supported_models": ["claude", "gemini"]
            },
            "image_generation": {
                "description": "Generate and edit images",
                "preferred_model": "openai",
                "supported_models": ["openai"]
            },
            "memory_operations": {
                "description": "Store and retrieve memories",
                "preferred_model": "gemini",
                "supported_models": ["gemini", "openai"]
            }
        }
        
        return jsonify({
            "success": True,
            "capabilities": capabilities,
            "sanctuary_note": "🧠 All capabilities designed for neurodivergent-friendly development"
        })
        
    except Exception as e:
        logger.error(f"Error getting capabilities: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Register the blueprint
def register_multi_model_api(app):
    """Register the multi-model API blueprint"""
    app.register_blueprint(multi_model_bp, url_prefix='/api/multi-model')
    logger.info(" Multi-Model API registered for Podplay Sanctuary")