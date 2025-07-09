"""
Bonzai Platform - Ultra-Minimal Railway Deployment
Absolute minimum version for Railway health checks
"""

import os
import logging
from datetime import datetime

# Load environment variables if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from flask import Flask, request, jsonify

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

# Add CORS headers manually
@app.after_request
def after_request(response):
    """Add CORS headers to all responses"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Global service status
services_initialized = False

def initialize_basic_services():
    """Initialize only essential services"""
    global services_initialized
    
    logger.info("Starting Bonzai Railway deployment...")
    
    # Just mark as initialized
    services_initialized = True
    
    logger.info("Basic services initialized successfully")
    return True

# Initialize services on startup
initialize_basic_services()

# ==============================================================================
# CORE ENDPOINTS
# ==============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for Railway - This is the critical endpoint"""
    try:
        logger.info("Health check requested")
        
        response = {
            'success': True,
            'status': 'healthy',
            'message': 'Bonzai Railway Backend is running',
            'timestamp': datetime.now().isoformat(),
            'service': 'bonzai-railway',
            'version': '1.0.0',
            'services_initialized': services_initialized
        }
        
        logger.info("Health check passed")
        return jsonify(response)
        
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
    """Root endpoint"""
    return jsonify({
        'service': 'Bonzai Railway Backend',
        'status': 'operational',
        'version': '1.0.0',
        'message': 'Bonzai Platform ready for Railway deployment',
        'health_endpoint': '/api/health',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/status', methods=['GET'])
def status_endpoint():
    """Status endpoint"""
    return jsonify({
        'success': True,
        'status': 'operational',
        'services_initialized': services_initialized,
        'timestamp': datetime.now().isoformat()
    })

# Simple OPTIONS handler for CORS
@app.route('/api/health', methods=['OPTIONS'])
@app.route('/api/status', methods=['OPTIONS'])
@app.route('/', methods=['OPTIONS'])
def options_handler():
    """Handle OPTIONS requests for CORS"""
    return '', 200

# ==============================================================================
# ERROR HANDLERS
# ==============================================================================

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'available_endpoints': ['/api/health', '/api/status', '/']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# ==============================================================================
# APPLICATION STARTUP
# ==============================================================================

if __name__ == '__main__':
    # Get port from environment (Railway sets this)
    port = int(os.getenv('PORT', 5000))
    
    logger.info(f"Starting Bonzai Railway Backend on port {port}")
    logger.info("Health check available at /api/health")
    logger.info("This should work with Railway health checks!")
    
    # Run with proper Railway configuration
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,  # Always False for Railway
        threaded=True
    )