"""
🐻⚡ Express Mode + Vertex AI API Blueprint
Integration layer for Mama Bear's Express Mode + Vertex AI supercharger
Provides 6x faster responses with Claude model access via Google Cloud credits
"""

import asyncio
import logging
import time
import json
from datetime import datetime
from typing import Dict, Any, Optional

from flask import Blueprint, request, jsonify, current_app
from functools import wraps

logger = logging.getLogger(__name__)

# Create Express Mode blueprint
express_mode_bp = Blueprint('express_mode', __name__, url_prefix='/api/express-mode')

# Global supercharger instance (will be initialized in app startup)
_supercharger = None

def require_supercharger(f):
    """Decorator to ensure supercharger is available"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if _supercharger is None:
            return jsonify({
                'success': False,
                'error': 'Express Mode + Vertex AI supercharger not initialized',
                'fallback_available': True
            }), 503
        return f(*args, **kwargs)
    return decorated_function

@express_mode_bp.route('/status', methods=['GET'])
def get_express_mode_status():
    """Get Express Mode + Vertex AI system status"""
    try:
        status = {
            'express_mode_available': _supercharger is not None,
            'timestamp': datetime.now().isoformat(),
            'system': 'Express Mode + Vertex AI Supercharger V2.0'
        }

        if _supercharger:
            # Get detailed status from supercharger
            supercharger_status = asyncio.run(_supercharger.get_system_status())
            status.update(supercharger_status)

        return jsonify(status)

    except Exception as e:
        logger.error(f"Error getting Express Mode status: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'express_mode_available': False
        }), 500

@express_mode_bp.route('/agentic-chat', methods=['POST'])
@require_supercharger
def agentic_express_chat():
    """
    🐻⚡ Agentic Express Mode Chat
    Let Mama Bear autonomously decide the best routing for 6x faster responses
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        message = data.get('message', '').strip()
        if not message:
            return jsonify({'success': False, 'error': 'Message is required'}), 400

        # Optional user preferences (Mama Bear will consider these)
        user_preferences = {
            'user_id': data.get('user_id', 'anonymous'),
            'context': data.get('context', {}),
            'priority': data.get('priority', 'standard'),  # instant, fast, standard, research
            'cost_preference': data.get('cost_preference', 'balanced'),  # minimize, balanced, quality
            'model_preference': data.get('model_preference', 'auto')  # auto, gemini, claude
        }

        # Let Mama Bear make autonomous routing decision
        start_time = time.time()
        result = asyncio.run(_supercharger.process_agentic_request(
            message=message,
            user_preferences=user_preferences
        ))

        # Add performance metrics
        result['performance_metrics'] = {
            'total_response_time_ms': round((time.time() - start_time) * 1000, 2),
            'timestamp': datetime.now().isoformat()
        }

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in agentic express chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'fallback_suggestion': 'Try standard chat endpoint'
        }), 500

@express_mode_bp.route('/express-instant', methods=['POST'])
@require_supercharger
def express_instant_response():
    """
    ⚡ Ultra-Fast Express Mode (Sub-200ms target)
    For simple queries that need instant responses
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        message = data.get('message', '').strip()
        if not message:
            return jsonify({'success': False, 'error': 'Message is required'}), 400

        # Force Express Mode routing
        start_time = time.time()
        result = asyncio.run(_supercharger.express_instant_mode(
            message=message,
            context=data.get('context', {})
        ))

        result['performance_metrics'] = {
            'total_response_time_ms': round((time.time() - start_time) * 1000, 2),
            'mode': 'express_instant',
            'target_time_ms': 200
        }

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in express instant mode: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'fallback_suggestion': 'Try agentic chat for automatic routing'
        }), 500

@express_mode_bp.route('/claude-vertex', methods=['POST'])
@require_supercharger
def claude_via_vertex():
    """
    🧠 Claude Models via Vertex AI Model Garden
    Access Claude 4/3.5/3.7 using Google Cloud credits instead of Anthropic billing
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        message = data.get('message', '').strip()
        if not message:
            return jsonify({'success': False, 'error': 'Message is required'}), 400

        # Claude model selection
        claude_model = data.get('model', 'claude-3.5-sonnet')  # Default to 3.5 Sonnet
        if claude_model not in ['claude-4-opus', 'claude-4-sonnet', 'claude-3.5-sonnet', 'claude-3.7-haiku']:
            return jsonify({
                'success': False,
                'error': f'Unsupported Claude model: {claude_model}',
                'supported_models': ['claude-4-opus', 'claude-4-sonnet', 'claude-3.5-sonnet', 'claude-3.7-haiku']
            }), 400

        start_time = time.time()
        result = asyncio.run(_supercharger.claude_vertex_mode(
            message=message,
            model=claude_model,
            context=data.get('context', {}),
            system_prompt=data.get('system_prompt', None)
        ))

        result['performance_metrics'] = {
            'total_response_time_ms': round((time.time() - start_time) * 1000, 2),
            'mode': 'claude_vertex',
            'model_used': claude_model
        }

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in Claude Vertex mode: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'fallback_suggestion': 'Try agentic chat for automatic model selection'
        }), 500

@express_mode_bp.route('/cost-optimization', methods=['GET'])
@require_supercharger
def get_cost_optimization_report():
    """Get real-time cost optimization report"""
    try:
        report = asyncio.run(_supercharger.get_cost_optimization_report())
        return jsonify(report)

    except Exception as e:
        logger.error(f"Error getting cost optimization report: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@express_mode_bp.route('/performance-metrics', methods=['GET'])
@require_supercharger
def get_performance_metrics():
    """Get real-time performance metrics and learning insights"""
    try:
        metrics = asyncio.run(_supercharger.get_performance_metrics())
        return jsonify(metrics)

    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@express_mode_bp.route('/mama-bear-decisions', methods=['GET'])
@require_supercharger
def get_mama_bear_decisions():
    """Get recent autonomous decisions made by Mama Bear"""
    try:
        decisions = asyncio.run(_supercharger.get_recent_agentic_decisions())
        return jsonify({
            'success': True,
            'decisions': decisions,
            'total_autonomous_decisions': len(decisions)
        })

    except Exception as e:
        logger.error(f"Error getting Mama Bear decisions: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@express_mode_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Express Mode system"""
    try:
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'express_mode_available': _supercharger is not None,
            'system_version': 'Express Mode + Vertex AI Supercharger V2.0'
        }

        if _supercharger:
            # Quick health check from supercharger
            health_status['supercharger_status'] = 'initialized'
        else:
            health_status['supercharger_status'] = 'not_initialized'
            health_status['fallback_available'] = True

        return jsonify(health_status)

    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

def initialize_express_mode_supercharger(app, settings):
    """
    Initialize the Express Mode + Vertex AI supercharger
    Called during app startup
    """
    global _supercharger

    try:
        # Import the supercharger class
        from services.mama_bear_express_vertex_supercharger import MamaBearExpressVertexSupercharger

        # Initialize with settings
        config = {
            'google_cloud_project': settings.google_cloud_project,
            'vertex_ai_location': getattr(settings, 'vertex_ai_location', 'us-central1'),
            'gemini_api_key': settings.gemini_api_key,
            'enable_cost_optimization': getattr(settings, 'enable_cost_optimization', True),
            'enable_agentic_routing': getattr(settings, 'enable_agentic_routing', True),
            'performance_target_ms': getattr(settings, 'express_mode_target_ms', 200)
        }

        _supercharger = MamaBearExpressVertexSupercharger(config)

        # Initialize the supercharger without asyncio.run since we're already in an event loop
        import asyncio
        try:
            # Try to get the current event loop
            loop = asyncio.get_running_loop()
            # If we're in a running loop, create a task instead
            loop.create_task(_supercharger.initialize())
        except RuntimeError:
            # No running loop, safe to use asyncio.run
            asyncio.run(_supercharger.initialize())

        logger.info("🐻⚡ Express Mode + Vertex AI Supercharger initialized successfully!")
        return True

    except ImportError as e:
        logger.warning(f"Express Mode supercharger not available: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to initialize Express Mode supercharger: {e}")
        return False

def integrate_express_mode_with_app(app):
    """
    Integrate Express Mode + Vertex AI API with the Flask app
    """
    try:
        # Register the blueprint
        app.register_blueprint(express_mode_bp)

        # Initialize the supercharger
        settings = app.config.get('settings')
        if settings:
            success = initialize_express_mode_supercharger(app, settings)
            if success:
                logger.info("✅ Express Mode + Vertex AI integration complete")
            else:
                logger.warning("⚠️ Express Mode + Vertex AI supercharger initialization failed - running in fallback mode")
        else:
            logger.warning("⚠️ No settings found - Express Mode running in basic mode")

        return True

    except Exception as e:
        logger.error(f"Failed to integrate Express Mode with app: {e}")
        return False
