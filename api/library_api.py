"""
 Library API Routes - Deep Research Center
Flask API endpoints for the collaborative Claude-Gemini research system
"""

from flask import Blueprint, request, jsonify, Response
import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any
import uuid

logger = logging.getLogger(__name__)

try:
    from services.deep_research_center import (
        LibrarySection, 
        ResearchMode, 
        ResearchDepth,
        DeepResearchCenter
    )
    LIBRARY_AVAILABLE = True
except ImportError as e:
    LIBRARY_AVAILABLE = False
    LibrarySection = None
    ResearchMode = None
    ResearchDepth = None
    DeepResearchCenter = None
    logger.error(f"Library services not available: {e}")

# Create Blueprint
library_bp = Blueprint('library', __name__, url_prefix='/api/library')

# Global library instance
library_section = None

def init_library_section(app):
    """Initialize the Library section with API keys"""
    global library_section
    
    if not LIBRARY_AVAILABLE or LibrarySection is None:
        logger.error("Library services not available - missing dependencies")
        return False
    
    try:
        anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        gemini_api_key = os.getenv('GEMINI_API_KEY_PRIMARY') or os.getenv('GOOGLE_API_KEY')
        
        if not anthropic_api_key or not gemini_api_key:
            logger.error("Missing required API keys for Library section")
            logger.error(f"Anthropic API Key: {'' if anthropic_api_key else ''}")
            logger.error(f"Gemini API Key: {'' if gemini_api_key else ''}")
            return False
        
        library_section = LibrarySection(
            anthropic_api_key=anthropic_api_key,
            gemini_api_key=gemini_api_key
        )
        
        logger.info(" Library section initialized successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize Library section: {e}")
        return False

@library_bp.route('/status', methods=['GET'])
def get_library_status():
    """Get Library service status"""
    if not library_section:
        return jsonify({
            "status": "error",
            "message": "Library section not initialized",
            "available": False
        }), 503
    
    return jsonify({
        "status": "active",
        "message": "Library section operational",
        "available": True,
        "initialized_at": library_section.initialized_at.isoformat(),
        "research_modes": library_section.get_available_modes(),
        "research_depths": library_section.get_available_depths()
    })

@library_bp.route('/research/modes', methods=['GET'])
def get_research_modes():
    """Get available research modes"""
    if not library_section:
        return jsonify({"error": "Library section not initialized"}), 503
    
    return jsonify({
        "modes": library_section.get_available_modes(),
        "depths": library_section.get_available_depths()
    })

@library_bp.route('/research/start', methods=['POST'])
def start_research():
    """Start a new research session"""
    if not library_section:
        return jsonify({"error": "Library section not initialized"}), 503
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        query = data.get('query')
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        mode = data.get('mode', 'collaborative')
        depth = data.get('depth', 'standard')
        session_id = data.get('session_id', f"research_{uuid.uuid4().hex[:8]}")
        
        # Validate mode and depth
        if ResearchMode is None or ResearchDepth is None:
            return jsonify({"error": "Research enums not available"}), 503
            
        valid_modes = [mode.value for mode in ResearchMode]
        valid_depths = [depth.value for depth in ResearchDepth]
        
        if mode not in valid_modes:
            return jsonify({
                "error": f"Invalid mode. Valid modes: {valid_modes}"
            }), 400
        
        if depth not in valid_depths:
            return jsonify({
                "error": f"Invalid depth. Valid depths: {valid_depths}"
            }), 400
        
        logger.info(f" Starting research session: {session_id}")
        logger.info(f"Query: {query}")
        logger.info(f"Mode: {mode}, Depth: {depth}")
        
        # Start research in background
        def run_research():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    library_section.conduct_research(query, mode, depth, session_id)
                )
                return result
            finally:
                loop.close()
        
        # For now, run synchronously (can be made async later)
        try:
            import threading
            
            # Start research in a separate thread
            research_thread = threading.Thread(target=run_research)
            research_thread.daemon = True
            research_thread.start()
            
            # Return immediate response with session info
            return jsonify({
                "status": "started",
                "session_id": session_id,
                "query": query,
                "mode": mode,
                "depth": depth,
                "estimated_duration": library_section.research_center._get_estimated_duration(ResearchDepth(depth)),
                "message": "Research session started. Use /status/{session_id} to check progress."
            })
            
        except Exception as e:
            logger.error(f"Failed to start research thread: {e}")
            # Fallback to synchronous execution
            result = run_research()
            return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error starting research: {e}")
        return jsonify({"error": str(e)}), 500

@library_bp.route('/research/status/<session_id>', methods=['GET'])
def get_research_status(session_id):
    """Get status of a research session"""
    if not library_section:
        return jsonify({"error": "Library section not initialized"}), 503
    
    try:
        session = library_section.get_session_status(session_id)
        if not session:
            return jsonify({"error": "Session not found"}), 404
        
        return jsonify(session)
        
    except Exception as e:
        logger.error(f"Error getting research status: {e}")
        return jsonify({"error": str(e)}), 500

@library_bp.route('/research/sessions', methods=['GET'])
def list_research_sessions():
    """List all research sessions"""
    if not library_section:
        return jsonify({"error": "Library section not initialized"}), 503
    
    try:
        sessions = library_section.list_sessions()
        return jsonify({
            "sessions": sessions,
            "count": len(sessions)
        })
        
    except Exception as e:
        logger.error(f"Error listing research sessions: {e}")
        return jsonify({"error": str(e)}), 500

@library_bp.route('/research/cancel/<session_id>', methods=['POST'])
def cancel_research(session_id):
    """Cancel a research session"""
    if not library_section:
        return jsonify({"error": "Library section not initialized"}), 503
    
    try:
        success = library_section.research_center.cancel_session(session_id)
        if success:
            return jsonify({
                "status": "cancelled",
                "session_id": session_id,
                "message": "Research session cancelled successfully"
            })
        else:
            return jsonify({"error": "Session not found or already completed"}), 404
            
    except Exception as e:
        logger.error(f"Error cancelling research: {e}")
        return jsonify({"error": str(e)}), 500

@library_bp.route('/research/quick', methods=['POST'])
def quick_research():
    """Quick research endpoint for immediate results"""
    if not library_section:
        return jsonify({"error": "Library section not initialized"}), 503
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        query = data.get('query')
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        mode = data.get('mode', 'claude_only')  # Default to fastest mode
        
        logger.info(f" Quick research: {query}")
        
        # Run quick research synchronously
        def run_quick_research():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    library_section.conduct_research(query, mode, 'quick')
                )
                return result
            finally:
                loop.close()
        
        result = run_quick_research()
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in quick research: {e}")
        return jsonify({"error": str(e)}), 500

@library_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    if not library_section:
        return jsonify({
            "status": "unhealthy",
            "message": "Library section not initialized"
        }), 503
    
    return jsonify({
        "status": "healthy",
        "service": "Deep Research Center",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

# Error handlers
@library_bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@library_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

@library_bp.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

# Integration function for the main app
def integrate_library_api(app):
    """Integrate Library API with the main Flask app"""
    try:
        # Initialize the library section
        if init_library_section(app):
            app.register_blueprint(library_bp)
            logger.info(" Library API integrated successfully!")
            return True
        else:
            logger.warning(" Library API initialization failed - blueprint not registered")
            return False
    except Exception as e:
        logger.error(f"Failed to integrate Library API: {e}")
        return False
