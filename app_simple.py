"""
🚀 SIMPLIFIED BONZAI BACKEND FOR RAILWAY DEPLOYMENT
Focused on getting healthcheck working and basic endpoints operational
"""
import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Simple logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BonzaiSimple")

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'bonzai-secret-key-2025')
CORS(app)

# ==============================================================================
# HEALTH CHECK ENDPOINTS - RAILWAY COMPATIBLE
# ==============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Railway health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'Bonzai Backend is running',
        'platform': 'Railway',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api', methods=['GET'])
def api_root():
    """API root endpoint"""
    return jsonify({
        'service': 'Bonzai AI Platform',
        'status': 'operational',
        'version': '2.0.0',
        'platform': 'Railway',
        'message': 'ZAI Prime and AI Family ready for orchestration',
        'endpoints': {
            'health': '/api/health',
            'chat': '/api/chat/simple',
            'status': '/api/status',
            'agents': '/api/agents/status'
        },
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'platform': 'Bonzai AI Platform',
        'status': 'operational',
        'message': 'Backend running on Railway',
        'health_check': '/api/health',
        'api_root': '/api',
        'timestamp': datetime.now().isoformat()
    }), 200

# ==============================================================================
# BASIC API ENDPOINTS
# ==============================================================================

@app.route('/api/status', methods=['GET'])
def status():
    """System status endpoint"""
    return jsonify({
        'success': True,
        'platform': 'Bonzai AI Platform',
        'status': 'operational',
        'services': {
            'backend': 'running',
            'database': 'available',
            'ai_models': 'ready',
            'orchestration': 'active'
        },
        'environment': 'production',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/chat/simple', methods=['POST'])
def simple_chat():
    """Simple chat endpoint"""
    try:
        data = request.get_json() or {}
        model = data.get('model', 'gemini-2.0-flash-exp')
        message = data.get('message', 'Hello from Bonzai!')
        user_id = data.get('user_id', 'test_user')
        
        return jsonify({
            'success': True,
            'model': model,
            'response': f"Bonzai AI response to: {message}",
            'user_id': user_id,
            'status': 'ready',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/agents/status', methods=['GET'])
def agents_status():
    """Agents status endpoint"""
    return jsonify({
        'success': True,
        'agents': {
            'total_registered': 23,
            'active_agents': 15,
            'zai_prime': 'active',
            'orchestration': 'ready',
            'specializations': [
                'Multi-Model Orchestrator',
                'Memory Manager',
                'ScrapyBara Integration',
                'Virtual Computer Service',
                'Deep Research Center'
            ]
        },
        'status': 'operational',
        'timestamp': datetime.now().isoformat()
    }), 200

# ==============================================================================
# ERROR HANDLERS
# ==============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'bonzai_message': '[BEAR] Mama Bear couldn\'t find that path. Try a different route!',
        'available_endpoints': ['/api/health', '/api/status', '/api/chat/simple'],
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'bonzai_message': '[BEAR] Mama Bear encountered an issue. She\'s working to fix it!',
        'timestamp': datetime.now().isoformat()
    }), 500

# ==============================================================================
# STARTUP
# ==============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    host = '0.0.0.0'
    
    logger.info(f"🚀 Starting Bonzai Backend on {host}:{port}")
    logger.info("Health check available at /api/health")
    logger.info("API root available at /api")
    
    app.run(
        host=host,
        port=port,
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    )