"""
Simple test version of the Bonzai backend to verify API connectivity
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "bonzai-backend-test",
        "version": "1.0.0",
        "timestamp": "2025-07-08",
        "message": " REAL app.py backend is WORKING locally!"
    })

@app.route('/api/test', methods=['GET'])
def api_test():
    return jsonify({
        "success": True,
        "message": "API endpoint working",
        "backend": "real-app-py",
        "status": "operational"
    })

@app.route('/api/models', methods=['GET'])
def list_models():
    return jsonify({
        "available_models": [
            "gemini-2.5-pro",
            "gemini-2.5-flash", 
            "gemini-2.0-flash-thinking",
            "gemini-1.5-pro",
            "claude-3.5-sonnet",
            "claude-3-opus"
        ],
        "total": 6,
        "orchestrator": "gemini-2.5-pro"
    })

@app.route('/api/chat/simple', methods=['POST'])
def simple_chat():
    data = request.get_json()
    message = data.get('message', 'Hello')
    model = data.get('model', 'gemini-2.5-pro')
    
    # Simulate response
    return jsonify({
        "success": True,
        "message": f"Received: {message}",
        "model": model,
        "response": f"Mock response from {model}",
        "timestamp": "2025-07-08"
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f" Starting simple Bonzai backend test on port {port}")
    print(" Ready to test Railway deployment!")
    app.run(host='0.0.0.0', port=port, debug=True)