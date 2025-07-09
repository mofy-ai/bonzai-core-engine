"""
 Gemini Orchestra API
Flask API endpoints for the revolutionary multi-model orchestration system
"""

from flask import Blueprint, request, jsonify, current_app
import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, Any

from ..services.enhanced_mama_bear_orchestration import EnhancedMamaBearAgent
from ..services.orchestration.orchestra_manager import GeminiOrchestra
from ..services.orchestration.task_analyzer import TaskAnalyzer

logger = logging.getLogger(__name__)

# Create Blueprint
gemini_orchestra_bp = Blueprint('gemini_orchestra', __name__, url_prefix='/api/orchestra')

# Global instances (will be initialized in app factory)
mama_bear_agent = None
orchestra_manager = None
task_analyzer = None

def init_gemini_orchestra(app):
    """Initialize the Gemini Orchestra with the Flask app"""
    global mama_bear_agent, orchestra_manager, task_analyzer
    
    try:
        # Use sophisticated routing system: try primary first, then fallback
        gemini_api_key = (
            os.getenv('GEMINI_API_KEY_PRIMARY') or 
            os.getenv('GEMINI_API_KEY') or 
            os.getenv('GOOGLE_AI_API_KEY')
        )
        anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        
        if not gemini_api_key:
            logger.error("No Gemini API key found. Please set GEMINI_API_KEY_PRIMARY, GEMINI_API_KEY, or GOOGLE_AI_API_KEY")
            return False
        
        # Initialize components
        mama_bear_agent = EnhancedMamaBearAgent(
            gemini_api_key=gemini_api_key,
            anthropic_api_key=anthropic_api_key
        )
        
        orchestra_manager = GeminiOrchestra(
            gemini_api_key=gemini_api_key,
            anthropic_api_key=anthropic_api_key
        )
        
        task_analyzer = TaskAnalyzer()
        
        logger.info(" Gemini Orchestra API initialized successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize Gemini Orchestra: {e}")
        return False

def run_async(coro):
    """Helper to run async functions in Flask routes"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)

@gemini_orchestra_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the orchestra"""
    
    if not mama_bear_agent or not orchestra_manager:
        return jsonify({
            "status": "error",
            "message": "Orchestra not initialized",
            "timestamp": datetime.now().isoformat()
        }), 503
    
    try:
        # Get orchestra status
        orchestra_status = run_async(orchestra_manager.get_orchestra_status())
        
        return jsonify({
            "status": "healthy",
            "orchestra_health": orchestra_status["orchestra_health"],
            "available_models": orchestra_status["available_models"],
            "claude_available": orchestra_status["claude_available"],
            "mama_bear_variants": 7,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@gemini_orchestra_bp.route('/mama-bear/chat', methods=['POST'])
def mama_bear_chat():
    """Main Mama Bear chat endpoint with orchestra integration"""
    
    if not mama_bear_agent:
        return jsonify({
            "error": "Mama Bear not initialized",
            "timestamp": datetime.now().isoformat()
        }), 503
    
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Message is required",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        message = data['message']
        variant = data.get('variant', 'scout_commander')
        context = data.get('context', {})
        user_id = data.get('user_id', 'anonymous')
        
        # Process through enhanced Mama Bear
        response = run_async(mama_bear_agent.process_message(
            message=message,
            variant=variant,
            context=context,
            user_id=user_id
        ))
        
        return jsonify({
            "success": True,
            "data": response,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Mama Bear chat failed: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@gemini_orchestra_bp.route('/mama-bear/variants', methods=['GET'])
def get_mama_bear_variants():
    """Get all available Mama Bear variants and their status"""
    
    if not mama_bear_agent:
        return jsonify({
            "error": "Mama Bear not initialized",
            "timestamp": datetime.now().isoformat()
        }), 503
    
    try:
        variant_status = run_async(mama_bear_agent.get_variant_status())
        
        return jsonify({
            "success": True,
            "data": variant_status,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get variant status: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@gemini_orchestra_bp.route('/mama-bear/switch-variant', methods=['POST'])
def switch_mama_bear_variant():
    """Switch to a different Mama Bear variant"""
    
    if not mama_bear_agent:
        return jsonify({
            "error": "Mama Bear not initialized",
            "timestamp": datetime.now().isoformat()
        }), 503
    
    try:
        data = request.get_json()
        
        if not data or 'variant' not in data:
            return jsonify({
                "error": "Variant is required",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        user_id = data.get('user_id', 'anonymous')
        new_variant = data['variant']
        context = data.get('context', '')
        
        response = run_async(mama_bear_agent.switch_variant(
            user_id=user_id,
            new_variant=new_variant,
            context=context
        ))
        
        return jsonify({
            "success": True,
            "data": response,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to switch variant: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@gemini_orchestra_bp.route('/orchestra/direct', methods=['POST'])
def direct_orchestra_request():
    """Direct access to the Gemini Orchestra (advanced users)"""
    
    if not orchestra_manager:
        return jsonify({
            "error": "Orchestra not initialized",
            "timestamp": datetime.now().isoformat()
        }), 503
    
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Message is required",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # Build orchestra request
        orchestra_request = {
            "message": data['message'],
            "task_type": data.get('task_type', 'general'),
            "require_speed": data.get('require_speed', False),
            "require_creativity": data.get('require_creativity', False),
            "require_reasoning": data.get('require_reasoning', False),
            "max_tokens_needed": data.get('max_tokens_needed', 1000),
            "context": data.get('context', {}),
            "urgency": data.get('urgency', 'normal'),
            "prefer_claude": data.get('prefer_claude', False)
        }
        
        # Process through orchestra
        response = run_async(orchestra_manager.process_request(orchestra_request))
        
        return jsonify({
            "success": True,
            "data": response,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Direct orchestra request failed: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@gemini_orchestra_bp.route('/orchestra/status', methods=['GET'])
def get_orchestra_status():
    """Get comprehensive orchestra status and performance metrics"""
    
    if not orchestra_manager:
        return jsonify({
            "error": "Orchestra not initialized",
            "timestamp": datetime.now().isoformat()
        }), 503
    
    try:
        status = run_async(orchestra_manager.get_orchestra_status())
        
        return jsonify({
            "success": True,
            "data": status,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get orchestra status: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@gemini_orchestra_bp.route('/orchestra/optimize', methods=['POST'])
def optimize_orchestra():
    """Run orchestra optimization and performance tuning"""
    
    if not orchestra_manager:
        return jsonify({
            "error": "Orchestra not initialized",
            "timestamp": datetime.now().isoformat()
        }), 503
    
    try:
        optimization_result = run_async(orchestra_manager.optimize_orchestra())
        
        return jsonify({
            "success": True,
            "data": optimization_result,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Orchestra optimization failed: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@gemini_orchestra_bp.route('/task-analyzer/analyze', methods=['POST'])
def analyze_task():
    """Analyze a task to understand its requirements"""
    
    if not task_analyzer:
        return jsonify({
            "error": "Task analyzer not initialized",
            "timestamp": datetime.now().isoformat()
        }), 503
    
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Message is required",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # Analyze the task
        analysis = run_async(task_analyzer.analyze_request(data))
        
        return jsonify({
            "success": True,
            "data": analysis,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Task analysis failed: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@gemini_orchestra_bp.route('/conversation/history/<user_id>', methods=['GET'])
def get_conversation_history(user_id):
    """Get conversation history for a specific user"""
    
    if not mama_bear_agent:
        return jsonify({
            "error": "Mama Bear not initialized",
            "timestamp": datetime.now().isoformat()
        }), 503
    
    try:
        history = run_async(mama_bear_agent.get_conversation_summary(user_id))
        
        return jsonify({
            "success": True,
            "data": history,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get conversation history: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@gemini_orchestra_bp.route('/models/registry', methods=['GET'])
def get_model_registry():
    """Get the complete model registry with capabilities"""
    
    try:
        from ..services.orchestration.model_registry import GEMINI_REGISTRY, export_registry_json
        
        registry_json = export_registry_json()
        
        return jsonify({
            "success": True,
            "data": {
                "registry": registry_json,
                "total_models": len(GEMINI_REGISTRY),
                "model_sections": {
                    "conductors": 1,
                    "deep_thinkers": 2,
                    "speed_demons": 2,
                    "context_masters": 2,
                    "creative_writers": 2,
                    "audio_specialists": 2,
                    "realtime_collaborators": 2,
                    "specialists": 3
                }
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get model registry: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@gemini_orchestra_bp.route('/performance/report', methods=['GET'])
def get_performance_report():
    """Get detailed performance report for all models"""
    
    if not orchestra_manager:
        return jsonify({
            "error": "Orchestra not initialized",
            "timestamp": datetime.now().isoformat()
        }), 503
    
    try:
        performance_report = run_async(orchestra_manager.performance_tracker.get_performance_report())
        
        return jsonify({
            "success": True,
            "data": performance_report,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get performance report: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@gemini_orchestra_bp.route('/performance/export', methods=['GET'])
def export_performance_data():
    """Export performance data for analysis"""
    
    if not orchestra_manager:
        return jsonify({
            "error": "Orchestra not initialized",
            "timestamp": datetime.now().isoformat()
        }), 503
    
    try:
        performance_data = run_async(orchestra_manager.performance_tracker.export_performance_data())
        
        return jsonify({
            "success": True,
            "data": performance_data,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to export performance data: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

# Error handlers
@gemini_orchestra_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested orchestra endpoint does not exist",
        "timestamp": datetime.now().isoformat()
    }), 404

@gemini_orchestra_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred in the orchestra",
        "timestamp": datetime.now().isoformat()
    }), 500

# Utility endpoints for development
@gemini_orchestra_bp.route('/dev/test-models', methods=['POST'])
def test_models():
    """Test specific models with a simple request (development only)"""
    
    if not orchestra_manager:
        return jsonify({
            "error": "Orchestra not initialized",
            "timestamp": datetime.now().isoformat()
        }), 503
    
    try:
        data = request.get_json()
        test_message = data.get('message', 'Hello, this is a test message.')
        models_to_test = data.get('models', ['speed_demon_primary', 'creative_writer_primary'])
        
        results = {}
        
        for model_key in models_to_test:
            try:
                test_request = {
                    "message": test_message,
                    "task_type": "test",
                    "max_tokens_needed": 100,
                    "test_mode": True
                }
                
                # Force specific model by manipulating routing
                test_request["force_model"] = model_key
                
                result = run_async(orchestra_manager.process_request(test_request))
                results[model_key] = {
                    "success": True,
                    "response": result.get("response", "")[:200],  # Truncate for testing
                    "model_used": result.get("model_used"),
                    "processing_time": result.get("orchestra_metadata", {}).get("processing_time_ms")
                }
                
            except Exception as e:
                results[model_key] = {
                    "success": False,
                    "error": str(e)
                }
        
        return jsonify({
            "success": True,
            "data": {
                "test_message": test_message,
                "results": results,
                "models_tested": len(models_to_test),
                "successful_tests": len([r for r in results.values() if r.get("success")])
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Model testing failed: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

# WebSocket support for real-time features (placeholder)
@gemini_orchestra_bp.route('/realtime/connect', methods=['POST'])
def connect_realtime():
    """Connect to real-time orchestra features (WebSocket placeholder)"""
    
    return jsonify({
        "message": "Real-time WebSocket support coming soon!",
        "features": [
            "Live collaboration with Gemini 2.0 Flash Live",
            "Real-time code review",
            "Interactive debugging sessions",
            "Live audio conversations"
        ],
        "timestamp": datetime.now().isoformat()
    })