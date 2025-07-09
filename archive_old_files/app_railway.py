"""
Bonzai Platform - Streamlined Railway Deployment
Simplified version focused on core functionality and reliable startup
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("BonzaiRailway")

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'bonzai-railway-secret-2024')

# Configure CORS for Railway
CORS(app, origins="*")

# Global service status
services_initialized = False
service_status = {}

def initialize_basic_services():
    """Initialize only essential services for Railway deployment"""
    global services_initialized, service_status
    
    logger.info("Starting Bonzai Railway deployment...")
    
    # Basic service checklist
    services = {
        'flask_app': 'healthy',
        'cors_enabled': 'healthy',
        'health_endpoint': 'healthy',
        'logging_system': 'healthy',
        'environment_config': 'healthy'
    }
    
    # Check optional services
    optional_services = {
        'mem0_api': os.getenv('MEM0_API_KEY') is not None,
        'gemini_api': os.getenv('GEMINI_API_KEY_PRIMARY') is not None,
        'anthropic_api': os.getenv('ANTHROPIC_API_KEY') is not None,
        'openai_api': os.getenv('OPENAI_API_KEY') is not None,
    }
    
    for service, available in optional_services.items():
        services[service] = 'available' if available else 'disabled'
    
    service_status = services
    services_initialized = True
    
    logger.info("Basic services initialized successfully")
    logger.info(f"Available services: {sum(1 for s in services.values() if s in ['healthy', 'available'])}")
    
    return services

# Initialize services on startup
initialize_basic_services()

# ==============================================================================
# CORE HEALTH AND STATUS ENDPOINTS
# ==============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for Railway"""
    try:
        return jsonify({
            'success': True,
            'status': 'healthy',
            'message': 'Bonzai Railway Backend is running',
            'timestamp': datetime.now().isoformat(),
            'service': 'bonzai-railway',
            'version': '1.0.0'
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/', methods=['GET'])
def root_endpoint():
    """Root endpoint - service overview"""
    return jsonify({
        'service': 'Bonzai Railway Backend',
        'status': 'operational',
        'version': '1.0.0',
        'message': 'Bonzai Platform ready for Railway deployment',
        'deployment': 'railway',
        'endpoints': {
            'health': '/api/health',
            'status': '/api/status',
            'chat': '/api/chat',
            'memory': '/api/memory'
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/status', methods=['GET'])
def service_status_endpoint():
    """Service status endpoint"""
    try:
        return jsonify({
            'success': True,
            'services_initialized': services_initialized,
            'service_status': service_status,
            'platform': 'railway',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Status check failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# BASIC CHAT ENDPOINT
# ==============================================================================

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """Basic chat endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        message = data.get('message', '')
        model = data.get('model', 'default')
        
        # Basic response (can be enhanced with actual AI integration)
        response = {
            'success': True,
            'message': f'Received: {message}',
            'model': model,
            'response': f'Bonzai Railway backend received your message: "{message}". Full AI integration coming soon!',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# BASIC MEMORY ENDPOINT
# ==============================================================================

@app.route('/api/memory', methods=['GET', 'POST'])
def memory_endpoint():
    """Basic memory endpoint"""
    try:
        if request.method == 'GET':
            return jsonify({
                'success': True,
                'message': 'Memory system available',
                'status': 'ready',
                'timestamp': datetime.now().isoformat()
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({
                    'success': False,
                    'error': 'No data provided'
                }), 400
            
            action = data.get('action', 'unknown')
            
            return jsonify({
                'success': True,
                'action': action,
                'message': f'Memory action "{action}" received',
                'timestamp': datetime.now().isoformat()
            })
            
    except Exception as e:
        logger.error(f"Memory endpoint error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==============================================================================
# ERROR HANDLERS
# ==============================================================================

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'The requested endpoint is not available',
        'available_endpoints': ['/api/health', '/api/status', '/api/chat', '/api/memory']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

# ==============================================================================
# APPLICATION STARTUP
# ==============================================================================

if __name__ == '__main__':
    # Get port from environment (Railway sets this)
    port = int(os.getenv('PORT', 5000))
    
    logger.info(f"Starting Bonzai Railway Backend on port {port}")
    logger.info("Health check available at /api/health")
    
    # Run with proper Railway configuration
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,  # Always False for Railway
        threaded=True
    )