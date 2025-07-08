# backend/api/scout_workflow_api.py
"""
🎯 Scout Workflow API - Integration with Enhanced Gemini Orchestration
RESTful endpoints for autonomous full-stack development workflows
"""

from flask import Blueprint, request, jsonify, Response
from flask_socketio import emit, join_room, leave_room
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import uuid

from services.enhanced_gemini_scout_orchestration import (
    EnhancedGeminiScoutOrchestrator, 
    WorkflowStage,
    ModelTier
)
from config.settings import get_settings

logger = logging.getLogger(__name__)

# Blueprint for Scout workflow endpoints
scout_bp = Blueprint('scout_workflow', __name__)

# Global orchestrator instance
scout_orchestrator: Optional[EnhancedGeminiScoutOrchestrator] = None

def initialize_scout_orchestrator():
    """Initialize the Scout orchestrator with API keys"""
    global scout_orchestrator
    
    settings = get_settings()
    gemini_api_key = settings.google_api_key
    
    if not gemini_api_key:
        logger.error("Google API key not configured for Scout orchestrator")
        return False
    
    try:
        scout_orchestrator = EnhancedGeminiScoutOrchestrator(gemini_api_key)
        logger.info("🎯 Scout orchestrator initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Scout orchestrator: {e}")
        return False

def get_scout_orchestrator() -> Optional[EnhancedGeminiScoutOrchestrator]:
    """Get the Scout orchestrator instance"""
    global scout_orchestrator
    if not scout_orchestrator:
        initialize_scout_orchestrator()
    return scout_orchestrator

@scout_bp.route('/api/scout/workflow/start', methods=['POST'])
def start_scout_workflow():
    """
    🚀 Start a new Scout workflow
    
    Expected payload:
    {
        "description": "Build a React todo app with Firebase backend",
        "user_id": "user123",
        "preferences": {
            "frontend": "react",
            "backend": "firebase",
            "styling": "tailwindcss"
        }
    }
    """
    try:
        data = request.json or {}
        description = data.get('description', '')
        user_id = data.get('user_id', 'anonymous')
        preferences = data.get('preferences', {})
        
        if not description:
            return jsonify({
                'success': False,
                'error': 'Project description is required'
            }), 400
        
        orchestrator = get_scout_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Scout orchestrator not available'
            }), 503
        
        # Generate workflow ID
        workflow_id = f"scout_{user_id}_{int(datetime.now().timestamp())}"
        
        # Enhance description with preferences
        enhanced_description = description
        if preferences:
            enhanced_description += f"\n\nPreferences: {json.dumps(preferences, indent=2)}"
        
        # Start the workflow asynchronously
        def run_workflow():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    orchestrator.execute_full_workflow(enhanced_description, preferences)
                )
                logger.info(f"🎯 Workflow {workflow_id} completed: {result['success']}")
            except Exception as e:
                logger.error(f"❌ Workflow {workflow_id} failed: {e}")
            finally:
                loop.close()
        
        # Run workflow in background thread
        import threading
        workflow_thread = threading.Thread(target=run_workflow)
        workflow_thread.daemon = True
        workflow_thread.start()
        
        return jsonify({
            'success': True,
            'workflow_id': workflow_id,
            'message': 'Scout workflow started successfully',
            'estimated_duration': '3-8 minutes'
        })
        
    except Exception as e:
        logger.error(f"Failed to start Scout workflow: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scout_bp.route('/api/scout/workflow/status/<workflow_id>', methods=['GET'])
def get_workflow_status(workflow_id: str):
    """
    📊 Get the status of a specific workflow
    """
    try:
        orchestrator = get_scout_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Scout orchestrator not available'
            }), 503
        
        status = orchestrator.get_workflow_status(workflow_id)
        if not status:
            return jsonify({
                'success': False,
                'error': 'Workflow not found'
            }), 404
        
        return jsonify({
            'success': True,
            'workflow': status
        })
        
    except Exception as e:
        logger.error(f"Failed to get workflow status: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scout_bp.route('/api/scout/orchestration/status', methods=['GET'])
def get_orchestration_status():
    """
    🎭 Get the current orchestration status and model health
    """
    try:
        orchestrator = get_scout_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Scout orchestrator not available'
            }), 503
        
        status = orchestrator.get_orchestration_status()
        
        return jsonify({
            'success': True,
            'orchestration': status
        })
        
    except Exception as e:
        logger.error(f"Failed to get orchestration status: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scout_bp.route('/api/scout/models', methods=['GET'])
def get_available_models():
    """
    🤖 Get list of all available Gemini models with their configurations
    """
    try:
        orchestrator = get_scout_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Scout orchestrator not available'
            }), 503
        
        models = []
        for model_id, config in orchestrator.gemini_models.items():
            quota_status = orchestrator.quota_status.get(model_id)
            
            models.append({
                'id': model_id,
                'name': model_id.replace('-', ' ').title(),
                'tier': config['tier'].value,
                'context_window': config['context_window'],
                'output_limit': config['output_limit'],
                'specialties': config['specialties'],
                'scout_roles': config['scout_roles'],
                'workflow_stages': [stage.value for stage in config['workflow_stages']],
                'cost_tier': config['cost_tier'],
                'latency': config['latency'],
                'health_score': quota_status.overall_health_score if quota_status else 0.0,
                'is_healthy': quota_status.is_healthy if quota_status else False
            })
        
        return jsonify({
            'success': True,
            'models': models,
            'total_models': len(models)
        })
        
    except Exception as e:
        logger.error(f"Failed to get available models: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scout_bp.route('/api/scout/workflow/execute-stage', methods=['POST'])
def execute_single_stage():
    """
    ⚡ Execute a single workflow stage for testing or manual execution
    
    Expected payload:
    {
        "stage": "planning",
        "prompt": "Create a todo app with React and Firebase",
        "context": {"preferences": {"frontend": "react"}}
    }
    """
    try:
        data = request.json or {}
        stage_name = data.get('stage', '')
        prompt = data.get('prompt', '')
        context = data.get('context', {})
        
        if not stage_name or not prompt:
            return jsonify({
                'success': False,
                'error': 'Stage and prompt are required'
            }), 400
        
        # Validate stage
        try:
            stage = WorkflowStage(stage_name.lower())
        except ValueError:
            return jsonify({
                'success': False,
                'error': f'Invalid stage: {stage_name}. Valid stages: {[s.value for s in WorkflowStage]}'
            }), 400
        
        orchestrator = get_scout_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Scout orchestrator not available'
            }), 503
        
        # Execute stage synchronously for API response
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                orchestrator.execute_workflow_stage(stage, prompt, context)
            )
        finally:
            loop.close()
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Failed to execute single stage: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scout_bp.route('/api/scout/models/suggest', methods=['POST'])
def suggest_model_for_task():
    """
    🎯 Suggest the best model for a specific task or stage
    
    Expected payload:
    {
        "stage": "coding",
        "task_description": "Build a React component with complex state management",
        "context": {"complexity": "high", "type": "frontend"}
    }
    """
    try:
        data = request.json or {}
        stage_name = data.get('stage', '')
        task_description = data.get('task_description', '')
        context = data.get('context', {})
        
        if not stage_name:
            return jsonify({
                'success': False,
                'error': 'Stage is required'
            }), 400
        
        # Validate stage
        try:
            stage = WorkflowStage(stage_name.lower())
        except ValueError:
            return jsonify({
                'success': False,
                'error': f'Invalid stage: {stage_name}. Valid stages: {[s.value for s in WorkflowStage]}'
            }), 400
        
        orchestrator = get_scout_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Scout orchestrator not available'
            }), 503
        
        # Get best model for stage
        suggested_model = orchestrator.get_best_model_for_stage(stage)
        
        if not suggested_model:
            return jsonify({
                'success': False,
                'error': f'No healthy models available for {stage_name}'
            }), 503
        
        # Get model configuration and status
        model_config = orchestrator.gemini_models[suggested_model]
        quota_status = orchestrator.quota_status[suggested_model]
        
        suggestion = {
            'model_id': suggested_model,
            'model_name': suggested_model.replace('-', ' ').title(),
            'tier': model_config['tier'].value,
            'specialties': model_config['specialties'],
            'scout_roles': model_config['scout_roles'],
            'health_score': quota_status.overall_health_score,
            'quota_available': {
                'minute': quota_status.minute_quota_available,
                'day': quota_status.day_quota_available
            },
            'reason': f"Best available model for {stage_name} with health score {quota_status.overall_health_score:.2f}",
            'context_window': model_config['context_window'],
            'cost_tier': model_config['cost_tier'],
            'latency': model_config['latency']
        }
        
        return jsonify({
            'success': True,
            'suggestion': suggestion,
            'alternatives': orchestrator.routing_preferences.get(stage.value, [])[:3]  # Top 3 alternatives
        })
        
    except Exception as e:
        logger.error(f"Failed to suggest model: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def integrate_scout_workflow_api(app, socketio):
    """
    🔗 Integrate Scout Workflow API with the Flask app
    """
    try:
        # Initialize the orchestrator
        initialized = initialize_scout_orchestrator()
        if not initialized:
            logger.warning("❌ Scout orchestrator initialization failed")
            return False
        
        # Register the blueprint
        app.register_blueprint(scout_bp)
        
        logger.info("✅ Scout Workflow API integrated successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to integrate Scout Workflow API: {e}")
        return False
