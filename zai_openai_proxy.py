#!/usr/bin/env python3
"""
🔗 ZAI OpenAI-Compatible Proxy Server
Translates OpenAI API calls to ZAI's native format
Run this to make ZAI work with any OpenAI-compatible tool!
"""

import os
import asyncio
import aiohttp
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ZAI backend configuration
ZAI_BASE_URL = "http://localhost:5001"
ZAI_CHAT_ENDPOINT = f"{ZAI_BASE_URL}/api/chat/message"

class ZaiOpenAIProxy:
    """Proxy server that makes ZAI compatible with OpenAI API format"""
    
    def __init__(self):
        self.supported_models = [
            "zai",  # Main ZAI system
            "zai-collective",
            "zai-research", 
            "zai-developer",
            "zai-creative",
            "gpt-4",  # Alias for ZAI
            "gpt-3.5-turbo"  # Alias for ZAI
        ]
    
    async def forward_to_zai(self, openai_request):
        """Convert OpenAI request to ZAI format and forward"""
        try:
            # Extract message from OpenAI format
            messages = openai_request.get('messages', [])
            if not messages:
                return {"error": "No messages provided"}
            
            # Get the latest user message
            user_message = ""
            for msg in reversed(messages):
                if msg.get('role') == 'user':
                    user_message = msg.get('content', '')
                    break
            
            if not user_message:
                return {"error": "No user message found"}
            
            # Prepare ZAI request
            zai_request = {
                "message": user_message,
                "user_id": "openai_proxy_user",
                "context": {
                    "via_proxy": True,
                    "original_format": "openai",
                    "model_requested": openai_request.get('model', 'zai-collective'),
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            # Forward to ZAI
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    ZAI_CHAT_ENDPOINT,
                    json=zai_request,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                ) as response:
                    if response.status == 200:
                        zai_response = await response.json()
                        return zai_response
                    else:
                        error_text = await response.text()
                        return {"error": f"ZAI backend error: {error_text}"}
                        
        except Exception as e:
            return {"error": f"Proxy error: {str(e)}"}
    
    def convert_to_openai_format(self, zai_response):
        """Convert ZAI response to OpenAI format"""
        if "error" in zai_response:
            return {
                "error": {
                    "message": zai_response["error"],
                    "type": "zai_error",
                    "code": "zai_backend_error"
                }
            }
        
        # Extract content from ZAI response
        content = zai_response.get('content', 'ZAI response unavailable')
        agent_used = zai_response.get('agent_id', 'zai_collective')
        
        # OpenAI compatible response
        return {
            "id": f"chatcmpl-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "object": "chat.completion",
            "created": int(datetime.now().timestamp()),
            "model": f"zai-{agent_used}",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(content.split()) // 2,  # Rough estimate
                "completion_tokens": len(content.split()),
                "total_tokens": len(content.split()) * 1.5
            },
            "system_fingerprint": "zai_proxy_v1"
        }

# Initialize proxy
proxy = ZaiOpenAIProxy()

@app.route('/v1', methods=['GET'])
def v1_info():
    """OpenAI v1 API information"""
    return jsonify({
        "message": "🧠 ZAI OpenAI-Compatible API v1",
        "available_endpoints": {
            "chat_completions": "/v1/chat/completions",
            "models": "/v1/models"
        },
        "usage": {
            "base_url": "http://localhost:8080/v1",
            "api_key": "zai-local-key",
            "example": "POST /v1/chat/completions"
        },
        "status": "ready"
    })

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    """OpenAI-compatible chat completions endpoint"""
    try:
        openai_request = request.get_json()
        
        # Validate model
        model = openai_request.get('model', 'zai')
        if model not in proxy.supported_models:
            return jsonify({
                "error": {
                    "message": f"Model {model} not supported. Use: {', '.join(proxy.supported_models)}",
                    "type": "invalid_request_error",
                    "code": "model_not_found"
                }
            }), 400
        
        # Forward to ZAI synchronously
        import requests
        
        # Extract message from OpenAI format
        messages = openai_request.get('messages', [])
        if not messages:
            return jsonify({
                "error": {
                    "message": "No messages provided",
                    "type": "invalid_request_error",
                    "code": "missing_messages"
                }
            }), 400
        
        # Get the latest user message
        user_message = ""
        for msg in reversed(messages):
            if msg.get('role') == 'user':
                user_message = msg.get('content', '')
                break
        
        if not user_message:
            return jsonify({
                "error": {
                    "message": "No user message found",
                    "type": "invalid_request_error",
                    "code": "missing_user_message"
                }
            }), 400
        
        # Prepare ZAI request
        zai_request = {
            "message": user_message,
            "user_id": "openai_proxy_user",
            "context": {
                "via_proxy": True,
                "original_format": "openai",
                "model_requested": model,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Forward to ZAI
        try:
            response = requests.post(
                ZAI_CHAT_ENDPOINT,
                json=zai_request,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                zai_response = response.json()
            else:
                return jsonify({
                    "error": {
                        "message": f"ZAI backend error: {response.text}",
                        "type": "zai_error",
                        "code": "backend_error"
                    }
                }), 500
                
        except Exception as e:
            return jsonify({
                "error": {
                    "message": f"Connection error: {str(e)}",
                    "type": "connection_error",
                    "code": "backend_unreachable"
                }
            }), 500
        
        # Convert to OpenAI format
        if "error" in zai_response:
            return jsonify({
                "error": {
                    "message": zai_response["error"],
                    "type": "zai_error",
                    "code": "zai_backend_error"
                }
            }), 500
        
        # Extract content from ZAI response
        content = zai_response.get('content', 'ZAI response unavailable')
        agent_used = zai_response.get('agent_id', 'zai_collective')
        
        # OpenAI compatible response
        openai_response = {
            "id": f"chatcmpl-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "object": "chat.completion",
            "created": int(datetime.now().timestamp()),
            "model": f"zai-{agent_used}",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(user_message.split()),
                "completion_tokens": len(content.split()),
                "total_tokens": len(user_message.split()) + len(content.split())
            },
            "system_fingerprint": "zai_proxy_v1"
        }
        
        return jsonify(openai_response)
        
    except Exception as e:
        return jsonify({
            "error": {
                "message": str(e),
                "type": "internal_error",
                "code": "proxy_error"
            }
        }), 500

@app.route('/v1/models', methods=['GET'])
def list_models():
    """List available models (OpenAI compatible)"""
    models = []
    for model_id in proxy.supported_models:
        models.append({
            "id": model_id,
            "object": "model",
            "created": int(datetime.now().timestamp()),
            "owned_by": "zai-system",
            "permission": [],
            "root": model_id
        })
    
    return jsonify({
        "object": "list",
        "data": models
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "ZAI OpenAI Proxy",
        "zai_backend": ZAI_BASE_URL,
        "supported_models": proxy.supported_models,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def welcome():
    """Welcome page"""
    return jsonify({
        "service": "🧠 ZAI OpenAI-Compatible Proxy",
        "description": "Makes ZAI work with any OpenAI-compatible tool",
        "endpoints": {
            "chat": "/v1/chat/completions",
            "models": "/v1/models", 
            "health": "/health"
        },
        "usage": {
            "base_url": "http://localhost:8080",
            "api_key": "zai-local-key",
            "models": proxy.supported_models
        },
        "zai_backend": ZAI_BASE_URL,
        "status": "online"
    })

if __name__ == '__main__':
    print("🔗 Starting ZAI OpenAI-Compatible Proxy...")
    print("🎯 This makes ZAI work with Roo, Cline, and other OpenAI tools!")
    print()
    print("📍 Proxy URL: http://localhost:8080")
    print("🔑 API Key: zai-local-key")
    print("🧠 ZAI Backend: http://localhost:5001")
    print()
    print("✅ Ready for OpenAI-compatible requests!")
    
    app.run(host='0.0.0.0', port=8080, debug=True)
