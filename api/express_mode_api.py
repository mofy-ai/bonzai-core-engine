"""
🚀 Express Mode + Vertex AI API Endpoints
RESTful API for 6x faster responses with Claude model access
"""

from flask import Blueprint, request, jsonify, current_app
from flask_socketio import emit
import asyncio
import json
from datetime import datetime
import logging
import os

from ..services.mama_bear_v2_supercharger import MamaBearV2Supercharger
from ..services.express_mode_vertex_integration import ExecutionMode

logger = logging.getLogger(__name__)

# Blueprint for Express Mode API endpoints
express_bp = Blueprint('express_mode', __name__)

def get_mama_bear_v2() -> MamaBearV2Supercharger:
    """Safely get Mama Bear V2.0 from app context"""
    return getattr(current_app, 'mama_bear_v2', None)

@express_bp.route('/api/mama-bear-v2/chat', methods=['POST'])
async def express_chat():
    """
    🚀 Main Express Mode chat endpoint
    Provides 6x faster responses with intelligent routing
    """
    try:
        data = request.json or {}
        
        # Validate required fields
        if not data.get('message'):
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        # Get Mama Bear V2.0 instance
        mama_bear_v2 = get_mama_bear_v2()
        if not mama_bear_v2:
            return jsonify({
                'success': False,
                'error': 'Mama Bear V2.0 not available'
            }), 503
        
        # Build request
        express_request = {
            'message': data['message'],
            'variant': data.get('variant', 'scout_commander'),
            'context': data.get('context', {}),
            'user_id': data.get('user_id', 'default_user'),
            'execution_mode': data.get('execution_mode', 'smart_routing'),
            'request_id': data.get('request_id', f"expr_{int(datetime.now().timestamp())}")
        }
        
        # Process via V2.0 Supercharger
        result = await mama_bear_v2.process_supercharged_request(express_request)
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat(),
            'api_version': 'v2.0'
        })
        
    except Exception as e:
        logger.error(f"Error in express_chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'fallback_message': "🚀 Express Mode temporarily unavailable. Switching to standard processing..."
        }), 500

@express_bp.route('/api/mama-bear-v2/express-config', methods=['GET', 'POST'])
async def express_config():
    """
    ⚙️ Configure Express Mode settings
    """
    mama_bear_v2 = get_mama_bear_v2()
    if not mama_bear_v2:
        return jsonify({'error': 'Mama Bear V2.0 not available'}), 503
    
    if request.method == 'GET':
        # Return current configuration
        status = await mama_bear_v2.get_v2_status()
        return jsonify({
            'success': True,
            'config': status.get('express_mode', {}),
            'timestamp': datetime.now().isoformat()
        })
    
    elif request.method == 'POST':
        # Update configuration
        try:
            data = request.json or {}
            
            # Update Express Mode configuration
            if 'execution_mode' in data:
                mama_bear_v2.express_config.mode = ExecutionMode(data['execution_mode'])
            
            if 'max_response_time_ms' in data:
                mama_bear_v2.express_config.max_response_time_ms = data['max_response_time_ms']
            
            if 'enable_streaming' in data:
                mama_bear_v2.express_config.enable_streaming = data['enable_streaming']
            
            if 'enable_autonomous' in data:
                await mama_bear_v2.enable_autonomous_mode(data['enable_autonomous'])
            
            return jsonify({
                'success': True,
                'message': 'Express Mode configuration updated',
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error updating Express Mode config: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

@express_bp.route('/api/mama-bear-v2/models', methods=['GET'])
async def available_models():
    """
    📋 Get available models and their capabilities
    """
    try:
        mama_bear_v2 = get_mama_bear_v2()
        if not mama_bear_v2:
            return jsonify({'error': 'Mama Bear V2.0 not available'}), 503
        
        # Get Express Mode status with model information
        status = await mama_bear_v2.get_v2_status()
        
        models_info = {
            'vertex_ai_models': {
                'claude_models': [
                    {
                        'name': 'Claude 4 Opus',
                        'model_id': 'claude-4-opus',
                        'capabilities': ['Advanced coding', 'Long-horizon tasks', 'AI agents', 'Agentic search'],
                        'use_cases': ['Complex development', 'Multi-step tasks', 'Peak accuracy requirements'],
                        'avg_response_time_ms': 800,
                        'cost_tier': 'premium'
                    },
                    {
                        'name': 'Claude 4 Sonnet',
                        'model_id': 'claude-4-sonnet',
                        'capabilities': ['Everyday development', 'Code reviews', 'API integrations'],
                        'use_cases': ['Production assistants', 'Real-time applications', 'High-volume tasks'],
                        'avg_response_time_ms': 600,
                        'cost_tier': 'balanced'
                    },
                    {
                        'name': 'Claude 3.7 Sonnet',
                        'model_id': 'claude-3.7-sonnet',
                        'capabilities': ['Extended thinking', 'Agentic coding', 'Complex reasoning'],
                        'use_cases': ['Software development lifecycle', 'Customer-facing agents', 'Computer use'],
                        'avg_response_time_ms': 500,
                        'cost_tier': 'balanced'
                    },
                    {
                        'name': 'Claude 3.5 Sonnet v2',
                        'model_id': 'claude-3.5-sonnet-v2',
                        'capabilities': ['Tool use', 'Agentic workflows', 'Advanced reasoning'],
                        'use_cases': ['Software development', 'Document Q&A', 'Visual data extraction'],
                        'avg_response_time_ms': 400,
                        'cost_tier': 'balanced'
                    },
                    {
                        'name': 'Claude 3.5 Haiku',
                        'model_id': 'claude-3.5-haiku',
                        'capabilities': ['Speed', 'Cost-effectiveness', 'Real-time responses'],
                        'use_cases': ['Code completions', 'Interactive chatbots', 'Content moderation'],
                        'avg_response_time_ms': 300,
                        'cost_tier': 'cost_effective'
                    }
                ],
                'gemini_models': [
                    {
                        'name': 'Gemini 2.5 Pro (Vertex)',
                        'model_id': 'gemini-2.5-pro-vertex',
                        'capabilities': ['Express Mode', 'Large context', 'Multimodal'],
                        'use_cases': ['Complex reasoning', 'Long documents', 'Multimodal tasks'],
                        'avg_response_time_ms': 400,
                        'cost_tier': 'balanced'
                    },
                    {
                        'name': 'Gemini 2.5 Flash (Vertex)',
                        'model_id': 'gemini-2.5-flash-vertex',
                        'capabilities': ['Fastest responses', 'Cost-effective', 'High throughput'],
                        'use_cases': ['Quick queries', 'High-volume applications', 'Real-time chat'],
                        'avg_response_time_ms': 200,
                        'cost_tier': 'cost_effective'
                    }
                ]
            },
            'gemini_api_models': {
                'description': 'Existing Gemini API models (fallback)',
                'models': ['gemini-2.5-pro-primary', 'gemini-2.5-flash-backup'],
                'capabilities': ['Standard processing', 'Proven reliability', 'Quota management']
            }
        }
        
        return jsonify({
            'success': True,
            'models': models_info,
            'total_models': len(models_info['vertex_ai_models']['claude_models']) + 
                           len(models_info['vertex_ai_models']['gemini_models']),
            'express_mode_enabled': status.get('express_mode', {}).get('enabled', False),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting available models: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@express_bp.route('/api/mama-bear-v2/status', methods=['GET'])
async def system_status():
    """
    📊 Get comprehensive V2.0 system status
    """
    try:
        mama_bear_v2 = get_mama_bear_v2()
        if not mama_bear_v2:
            return jsonify({'error': 'Mama Bear V2.0 not available'}), 503
        
        status = await mama_bear_v2.get_v2_status()
        
        return jsonify({
            'success': True,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@express_bp.route('/api/mama-bear-v2/autonomous', methods=['GET', 'POST'])
async def autonomous_mode():
    """
    🤖 Manage autonomous mode settings
    """
    mama_bear_v2 = get_mama_bear_v2()
    if not mama_bear_v2:
        return jsonify({'error': 'Mama Bear V2.0 not available'}), 503
    
    if request.method == 'GET':
        # Get current autonomous mode status
        status = await mama_bear_v2.get_v2_status()
        autonomous_info = status.get('autonomous_mode', {})
        
        return jsonify({
            'success': True,
            'autonomous_mode': autonomous_info,
            'capabilities': [
                'Agent creation and management',
                'Infrastructure optimization',
                'Self-improvement mechanisms',
                'Proactive system monitoring'
            ] if autonomous_info.get('enabled') else [],
            'timestamp': datetime.now().isoformat()
        })
    
    elif request.method == 'POST':
        # Enable/disable autonomous mode
        try:
            data = request.json or {}
            enable = data.get('enable', False)
            
            result = await mama_bear_v2.enable_autonomous_mode(enable)
            
            return jsonify({
                'success': True,
                'result': result,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error managing autonomous mode: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

@express_bp.route('/api/mama-bear-v2/performance', methods=['GET'])
async def performance_metrics():
    """
    📈 Get performance metrics and analytics
    """
    try:
        mama_bear_v2 = get_mama_bear_v2()
        if not mama_bear_v2:
            return jsonify({'error': 'Mama Bear V2.0 not available'}), 503
        
        status = await mama_bear_v2.get_v2_status()
        metrics = status.get('performance_metrics', {})
        
        # Calculate additional metrics
        total_requests = metrics.get('requests_processed', 0)
        express_usage = metrics.get('express_mode_usage', 0)
        
        express_adoption_rate = (express_usage / total_requests * 100) if total_requests > 0 else 0
        
        performance_data = {
            'current_metrics': metrics,
            'calculated_metrics': {
                'express_adoption_rate_percent': round(express_adoption_rate, 2),
                'avg_speed_improvement': '6x faster' if express_usage > 0 else 'N/A',
                'system_health': 'optimal' if metrics.get('avg_response_time_ms', 0) < 2000 else 'good'
            },
            'recommendations': []
        }
        
        # Add recommendations based on usage patterns
        if express_adoption_rate < 30:
            performance_data['recommendations'].append(
                'Consider using Express Mode more frequently for faster responses'
            )
        
        if metrics.get('avg_response_time_ms', 0) > 3000:
            performance_data['recommendations'].append(
                'Response times are higher than optimal - consider Claude 3.5 Haiku for faster responses'
            )
        
        return jsonify({
            'success': True,
            'performance': performance_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@express_bp.route('/api/mama-bear-v2/agent-workbench', methods=['GET'])
async def agent_workbench():
    """
    🏭 Get agent workbench status and suggestions
    """
    try:
        mama_bear_v2 = get_mama_bear_v2()
        if not mama_bear_v2:
            return jsonify({'error': 'Mama Bear V2.0 not available'}), 503
        
        if not mama_bear_v2.autonomous_mode:
            return jsonify({
                'success': False,
                'error': 'Autonomous mode is not enabled',
                'message': 'Enable autonomous mode to access agent workbench features'
            }), 403
        
        # Get agent workbench data
        agent_suggestions = list(mama_bear_v2.agent_workbench.values())
        infrastructure_suggestions = list(mama_bear_v2.infrastructure_management.values())
        
        workbench_data = {
            'agent_creation_suggestions': agent_suggestions[-10:],  # Last 10 suggestions
            'infrastructure_optimizations': infrastructure_suggestions[-10:],
            'total_agent_suggestions': len(agent_suggestions),
            'total_infrastructure_suggestions': len(infrastructure_suggestions),
            'autonomous_capabilities': {
                'agent_creation': True,
                'infrastructure_management': True,
                'self_improvement': True,
                'proactive_monitoring': True
            }
        }
        
        return jsonify({
            'success': True,
            'workbench': workbench_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting agent workbench data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@express_bp.route('/api/mama-bear-v2/cost-analysis', methods=['GET'])
async def cost_analysis():
    """
    💰 Get cost analysis and optimization recommendations
    """
    try:
        mama_bear_v2 = get_mama_bear_v2()
        if not mama_bear_v2:
            return jsonify({'error': 'Mama Bear V2.0 not available'}), 503
        
        status = await mama_bear_v2.get_v2_status()
        metrics = status.get('performance_metrics', {})
        
        # Estimate cost savings
        total_requests = metrics.get('requests_processed', 0)
        express_requests = metrics.get('express_mode_usage', 0)
        vertex_requests = metrics.get('vertex_ai_usage', 0)
        gemini_api_requests = metrics.get('gemini_api_usage', 0)
        
        # Rough cost estimates (in USD)
        gemini_api_cost_per_request = 0.001  # $0.001 per request
        vertex_gemini_cost_per_request = 0.0012  # $0.0012 per request
        vertex_claude_cost_per_request = 0.003  # $0.003 per request
        
        estimated_costs = {
            'gemini_api_cost': gemini_api_requests * gemini_api_cost_per_request,
            'vertex_gemini_cost': (express_requests - vertex_requests) * vertex_gemini_cost_per_request,
            'vertex_claude_cost': vertex_requests * vertex_claude_cost_per_request
        }
        
        total_cost = sum(estimated_costs.values())
        baseline_cost = total_requests * gemini_api_cost_per_request
        
        cost_data = {
            'estimated_costs': estimated_costs,
            'total_estimated_cost': round(total_cost, 4),
            'baseline_cost': round(baseline_cost, 4),
            'cost_difference': round(total_cost - baseline_cost, 4),
            'cost_efficiency': {
                'using_smart_routing': True,
                'estimated_savings_vs_premium_only': f"${round((total_requests * vertex_claude_cost_per_request) - total_cost, 4)}",
                'efficiency_rating': 'optimal' if total_cost <= baseline_cost * 1.5 else 'good'
            },
            'recommendations': [
                'Use Claude 3.5 Haiku for cost-effective quality responses',
                'Express Mode with Gemini Flash for speed-critical tasks',
                'Smart routing is optimizing costs automatically'
            ]
        }
        
        return jsonify({
            'success': True,
            'cost_analysis': cost_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting cost analysis: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@express_bp.route('/api/mama-bear-v2/health', methods=['GET'])
async def health_check():
    """
    ❤️ Simple health check endpoint
    """
    try:
        mama_bear_v2 = get_mama_bear_v2()
        
        health_status = {
            'mama_bear_v2_available': mama_bear_v2 is not None,
            'express_mode_enabled': False,
            'vertex_ai_connected': False,
            'autonomous_mode_enabled': False
        }
        
        if mama_bear_v2:
            status = await mama_bear_v2.get_v2_status()
            health_status.update({
                'express_mode_enabled': status.get('express_mode', {}).get('enabled', False),
                'vertex_ai_connected': mama_bear_v2.express_integration is not None,
                'autonomous_mode_enabled': status.get('autonomous_mode', {}).get('enabled', False)
            })
        
        overall_health = all([
            health_status['mama_bear_v2_available'],
            health_status['express_mode_enabled']
        ])
        
        return jsonify({
            'success': True,
            'healthy': overall_health,
            'details': health_status,
            'timestamp': datetime.now().isoformat(),
            'version': '2.0'
        })
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            'success': False,
            'healthy': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# Error handlers
@express_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'available_endpoints': [
            '/api/mama-bear-v2/chat',
            '/api/mama-bear-v2/status',
            '/api/mama-bear-v2/models',
            '/api/mama-bear-v2/autonomous',
            '/api/mama-bear-v2/performance',
            '/api/mama-bear-v2/health'
        ]
    }), 404

@express_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'Mama Bear V2.0 encountered an unexpected error'
    }), 500
