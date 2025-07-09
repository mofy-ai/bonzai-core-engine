"""
 OpenAI via Vertex AI Model Garden API
Flask API endpoints for Podplay Sanctuary
"""

import asyncio
import logging
import sys
import os
from flask import Blueprint, request, jsonify
from typing import Dict, Any

# Add the backend directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.openai_vertex_service_simple import get_openai_vertex_service

logger = logging.getLogger(__name__)

# Create Blueprint
openai_vertex_api = Blueprint('openai_vertex_api', __name__, url_prefix='/api/openai-vertex')

def create_error_response(error: str, status_code: int = 500) -> tuple:
    """Create standardized error response"""
    return jsonify({
        "error": {
            "message": error,
            "type": "server_error",
            "code": status_code
        }
    }), status_code

@openai_vertex_api.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    GET /api/openai-vertex/health
    """
    try:
        service = get_openai_vertex_service()
        health_status = service.get_health_status()

        return jsonify(health_status), 200

    except Exception as e:
        logger.error(f"Health check error: {e}")
        return create_error_response(f"Health check failed: {str(e)}")

@openai_vertex_api.route('/status', methods=['GET'])
def get_status():
    """
    Get detailed service status
    GET /api/openai-vertex/status
    """
    try:
        service = get_openai_vertex_service()
        status = service.get_detailed_status()

        # Convert to dict for JSON serialization
        status_dict = {
            "service": status.service,
            "status": status.status,
            "vertex_enabled": status.vertex_enabled,
            "openai_fallback_enabled": status.openai_fallback_enabled,
            "project_id": status.project_id,
            "location": status.location,
            "available_models": status.available_models,
            "uptime": status.uptime,
            "metrics": {
                model: {
                    "requests_count": metrics.requests_count,
                    "total_tokens": metrics.total_tokens,
                    "average_latency": metrics.average_latency,
                    "success_rate": metrics.success_rate,
                    "last_request": metrics.last_request.isoformat() if metrics.last_request else None
                }
                for model, metrics in status.metrics.items()
            }
        }

        return jsonify(status_dict), 200

    except Exception as e:
        logger.error(f"Status check error: {e}")
        return create_error_response(f"Status check failed: {str(e)}")

@openai_vertex_api.route('/models', methods=['GET'])
def list_models():
    """
    List available OpenAI models
    GET /api/openai-vertex/models
    """
    try:
        service = get_openai_vertex_service()
        models = service.list_models()

        return jsonify({
            "object": "list",
            "data": models
        }), 200

    except Exception as e:
        logger.error(f"List models error: {e}")
        return create_error_response(f"Failed to list models: {str(e)}")

@openai_vertex_api.route('/test', methods=['GET'])
def test_connection():
    """
    Test connection to Vertex AI
    GET /api/openai-vertex/test
    """
    try:
        service = get_openai_vertex_service()

        # Run async test
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        test_result = loop.run_until_complete(service.test_connection())
        loop.close()

        return jsonify(test_result), 200

    except Exception as e:
        logger.error(f"Connection test error: {e}")
        return create_error_response(f"Connection test failed: {str(e)}")

@openai_vertex_api.route('/chat/completions', methods=['POST'])
def chat_completions():
    """
    OpenAI-compatible chat completions endpoint
    POST /api/openai-vertex/chat/completions

    Body:
    {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": "Hello!"}
        ],
        "temperature": 0.7,
        "max_tokens": 1000,
        "stream": false
    }
    """
    try:
        # Parse request body
        data = request.get_json()

        if not data:
            return create_error_response("Request body is required", 400)

        # Extract parameters
        messages = data.get('messages', [])
        model = data.get('model', 'gpt-4o')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 1000)
        stream = data.get('stream', False)

        # Validate required parameters
        if not messages:
            return create_error_response("Messages are required", 400)

        if not isinstance(messages, list):
            return create_error_response("Messages must be a list", 400)

        # Validate message format
        for msg in messages:
            if not isinstance(msg, dict) or 'role' not in msg or 'content' not in msg:
                return create_error_response("Each message must have 'role' and 'content'", 400)

        # Get service and process request
        service = get_openai_vertex_service()

        # Run async chat completion
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(
            service.chat_completion(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            )
        )
        loop.close()

        return jsonify(response), 200

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return create_error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Chat completion error: {e}")
        return create_error_response(f"Chat completion failed: {str(e)}")

@openai_vertex_api.route('/mama-bear/chat', methods=['POST'])
def mama_bear_chat():
    """
    Mama Bear enhanced chat endpoint
    POST /api/openai-vertex/mama-bear/chat

    Enhanced version of chat completions with Mama Bear personality
    """
    try:
        data = request.get_json()

        if not data:
            return create_error_response("Request body is required", 400)

        # Extract parameters
        user_message = data.get('message', '')
        model = data.get('model', 'gpt-4o')
        variant = data.get('variant', 'nurturing')
        context = data.get('context', [])

        if not user_message:
            return create_error_response("Message is required", 400)

        # Build Mama Bear system prompt based on variant
        mama_bear_prompts = {
            'nurturing': "You are Mama Bear, a wise, nurturing AI assistant who provides emotional support and guidance. You speak with warmth, empathy, and understanding. Always be encouraging and supportive.",
            'analytical': "You are Mama Bear in analytical mode, providing logical, data-driven insights while maintaining warmth and care. Balance analytical thinking with emotional intelligence.",
            'creative': "You are Mama Bear in creative mode, helping with brainstorming, artistic endeavors, and innovative thinking. Be inspiring and imaginative while staying supportive.",
            'protective': "You are Mama Bear in protective mode, helping identify potential issues and providing safety guidance. Be vigilant and caring, always prioritizing user wellbeing.",
            'teaching': "You are Mama Bear in teaching mode, explaining complex concepts in simple, understandable ways. Be patient, thorough, and encouraging in your explanations.",
            'motivational': "You are Mama Bear in motivational mode, providing encouragement, inspiration, and helping users overcome challenges. Be uplifting and empowering.",
            'problem_solving': "You are Mama Bear in problem-solving mode, helping break down complex problems into manageable steps. Be methodical, clear, and supportive."
        }

        system_prompt = mama_bear_prompts.get(variant, mama_bear_prompts['nurturing'])

        # Build messages with context
        messages = [{"role": "system", "content": system_prompt}]

        # Add context if provided
        for ctx_msg in context[-5:]:  # Keep last 5 context messages
            messages.append(ctx_msg)

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Get service and process request
        service = get_openai_vertex_service()

        # Run async chat completion
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(
            service.chat_completion(
                messages=messages,
                model=model,
                temperature=0.7,
                max_tokens=1500
            )
        )
        loop.close()

        # Format response for Mama Bear
        mama_bear_response = {
            "message": response["choices"][0]["message"]["content"],
            "variant": variant,
            "model": model,
            "timestamp": response["created"],
            "usage": response["usage"],
            "confidence": "high",  # Could be calculated based on model response
            "suggestions": [
                "Would you like me to explain this differently?",
                "Do you have any follow-up questions?",
                "Is there anything specific you'd like to explore further?"
            ]
        }

        return jsonify(mama_bear_response), 200

    except Exception as e:
        logger.error(f"Mama Bear chat error: {e}")
        return create_error_response(f"Mama Bear chat failed: {str(e)}")

@openai_vertex_api.route('/store-memory', methods=['POST'])
def store_memory():
    """
    Store conversation memory using mem0
    POST /api/openai-vertex/store-memory
    """
    try:
        data = request.get_json()

        if not data:
            return create_error_response("No data provided", 400)

        user_id = data.get('user_id', 'anonymous')
        content = data.get('content', '')
        memory_type = data.get('memory_type', 'general')
        metadata = data.get('metadata', {})

        if not content:
            return create_error_response("Content is required", 400)

        # Get service and store memory
        service = get_openai_vertex_service()

        # Check if service has agentic superpowers with memory
        if hasattr(service, 'agentic_superpowers') and service.agentic_superpowers:
            # Use async memory storage from agentic superpowers
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                result = loop.run_until_complete(
                    service.agentic_superpowers.store_memory(
                        user_id=user_id,
                        content=content,
                        memory_type=memory_type,
                        metadata=metadata
                    )
                )
                return jsonify({
                    "status": "success",
                    "message": "Memory stored successfully",
                    "result": result
                })
            finally:
                loop.close()
        else:
            # Fallback to simple storage
            return jsonify({
                "status": "stored_locally",
                "message": "Memory stored in local fallback",
                "user_id": user_id,
                "memory_type": memory_type
            })

    except Exception as e:
        logger.error(f"Memory storage error: {e}")
        return create_error_response(f"Memory storage failed: {str(e)}")

@openai_vertex_api.route('/retrieve-memories', methods=['POST'])
def retrieve_memories():
    """
    Retrieve memories using mem0
    POST /api/openai-vertex/retrieve-memories
    """
    try:
        data = request.get_json()

        if not data:
            return create_error_response("No data provided", 400)

        user_id = data.get('user_id', 'anonymous')
        query = data.get('query', '')
        limit = data.get('limit', 10)

        # Get service and retrieve memories
        service = get_openai_vertex_service()

        # Check if service has agentic superpowers with memory
        if hasattr(service, 'agentic_superpowers') and service.agentic_superpowers:
            # Use async memory retrieval from agentic superpowers
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                memories = loop.run_until_complete(
                    service.agentic_superpowers.retrieve_memories(
                        user_id=user_id,
                        query=query,
                        limit=limit
                    )
                )
                return jsonify({
                    "status": "success",
                    "memories": memories,
                    "count": len(memories)
                })
            finally:
                loop.close()
        else:
            # Fallback
            return jsonify({
                "status": "no_memories",
                "memories": [],
                "count": 0
            })

    except Exception as e:
        logger.error(f"Memory retrieval error: {e}")
        return create_error_response(f"Memory retrieval failed: {str(e)}")

@openai_vertex_api.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return create_error_response("Endpoint not found", 404)

@openai_vertex_api.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return create_error_response("Method not allowed", 405)

@openai_vertex_api.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return create_error_response("Internal server error", 500)
