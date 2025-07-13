"""
🚀 GitHub AI Models API Endpoint
RESTful API for accessing GitHub AI models through the Bonzai Core Engine
"""

import logging
from flask import Blueprint, request, jsonify
from services.github_ai_client import GitHubAIClient, create_github_ai_client

logger = logging.getLogger(__name__)

# Create blueprint
github_ai_bp = Blueprint('github_ai', __name__, url_prefix='/api/github-ai')

@github_ai_bp.route('/chat', methods=['POST'])
def chat_completion():
    """Chat completion endpoint using GitHub AI models"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        messages = data.get('messages', [])
        model = data.get('model', 'gpt-4.1')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens')
        
        if not messages:
            return jsonify({"error": "Messages are required"}), 400
        
        # Create client and get response
        client = create_github_ai_client()
        response = client.chat(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return jsonify({
            "success": True,
            "response": response,
            "model": model,
            "timestamp": str(datetime.now())
        })
        
    except Exception as e:
        logger.error(f"GitHub AI chat completion failed: {str(e)}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@github_ai_bp.route('/simple', methods=['POST'])
def simple_completion():
    """Simple completion endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        prompt = data.get('prompt')
        model = data.get('model', 'gpt-4.1')
        system_prompt = data.get('system_prompt')
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        # Create client and get response
        client = create_github_ai_client()
        response = client.simple_completion(
            prompt=prompt,
            model=model,
            system_prompt=system_prompt
        )
        
        return jsonify({
            "success": True,
            "response": response,
            "model": model,
            "timestamp": str(datetime.now())
        })
        
    except Exception as e:
        logger.error(f"GitHub AI simple completion failed: {str(e)}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@github_ai_bp.route('/code-assist', methods=['POST'])
def code_assistance():
    """Code assistance endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        code_context = data.get('code_context', '')
        request_text = data.get('request')
        model = data.get('model', 'gpt-4.1')
        
        if not request_text:
            return jsonify({"error": "Request is required"}), 400
        
        # Create client and get response
        client = create_github_ai_client()
        response = client.code_completion(
            code_context=code_context,
            request=request_text,
            model=model
        )
        
        return jsonify({
            "success": True,
            "response": response,
            "model": model,
            "timestamp": str(datetime.now())
        })
        
    except Exception as e:
        logger.error(f"GitHub AI code assistance failed: {str(e)}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@github_ai_bp.route('/models', methods=['GET'])
def get_models():
    """Get available GitHub AI models"""
    try:
        client = create_github_ai_client()
        models = client.get_available_models()
        
        return jsonify({
            "success": True,
            "models": models,
            "count": len(models)
        })
        
    except Exception as e:
        logger.error(f"Failed to get GitHub AI models: {str(e)}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@github_ai_bp.route('/test', methods=['GET'])
def test_connection():
    """Test GitHub AI connection"""
    try:
        client = create_github_ai_client()
        is_connected = client.test_connection()
        
        return jsonify({
            "success": True,
            "connected": is_connected,
            "endpoint": client.endpoint,
            "models_count": len(client.models)
        })
        
    except Exception as e:
        logger.error(f"GitHub AI connection test failed: {str(e)}")
        return jsonify({
            "error": str(e),
            "success": False,
            "connected": False
        }), 500

@github_ai_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "service": "GitHub AI API",
        "status": "healthy",
        "timestamp": str(datetime.now())
    })

# Add missing import
from datetime import datetime