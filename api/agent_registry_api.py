"""
Bonzai Agent Registry API
Provides REST endpoints for agent discovery, status, and management
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any
import logging
from datetime import datetime

# Import the agent registry
from services.bonzai_agent_registry import (
    get_registry, 
    discover_agents, 
    get_agent_details, 
    get_registry_health,
    AgentCategory,
    AgentStatus
)

logger = logging.getLogger(__name__)

# Create Blueprint
agent_registry_bp = Blueprint('agent_registry', __name__, url_prefix='/api/agent-registry')

@agent_registry_bp.route('/agents', methods=['GET'])
def list_agents():
    """
    List all registered agents with optional filtering
    
    Query Parameters:
    - category: Filter by agent category
    - capability: Filter by capability name
    - status: Filter by agent status
    - search: Search in agent names and descriptions
    """
    try:
        category = request.args.get('category')
        capability = request.args.get('capability')
        status = request.args.get('status')
        search = request.args.get('search')
        
        # Get agents based on filters
        if capability or category:
            agents = discover_agents(capability=capability, category=category)
        else:
            registry = get_registry()
            agents = [agent.dict() for agent in registry.agents.values()]
        
        # Apply additional filters
        if status:
            agents = [a for a in agents if a.get('status') == status]
        
        if search:
            registry = get_registry()
            search_results = registry.search_agents(search)
            agent_ids = {a.id for a in search_results}
            agents = [a for a in agents if a.get('id') in agent_ids]
        
        return jsonify({
            'success': True,
            'count': len(agents),
            'agents': agents
        })
        
    except Exception as e:
        logger.error(f"Failed to list agents: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_registry_bp.route('/agents/<agent_id>', methods=['GET'])
def get_agent(agent_id: str):
    """Get detailed information about a specific agent"""
    try:
        agent_info = get_agent_details(agent_id)
        
        if 'error' in agent_info:
            return jsonify({
                'success': False,
                'error': agent_info['error']
            }), 404
        
        return jsonify({
            'success': True,
            'agent': agent_info
        })
        
    except Exception as e:
        logger.error(f"Failed to get agent {agent_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_registry_bp.route('/agents/<agent_id>/status', methods=['GET'])
def get_agent_status(agent_id: str):
    """Get current status and health of a specific agent"""
    try:
        registry = get_registry()
        status = registry.get_agent_status(agent_id)
        
        if 'error' in status:
            return jsonify({
                'success': False,
                'error': status['error']
            }), 404
        
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        logger.error(f"Failed to get agent status {agent_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_registry_bp.route('/agents/<agent_id>/metrics', methods=['POST'])
def update_agent_metrics(agent_id: str):
    """Update metrics for a specific agent"""
    try:
        metrics = request.get_json()
        if not metrics:
            return jsonify({
                'success': False,
                'error': 'No metrics provided'
            }), 400
        
        registry = get_registry()
        registry.update_agent_metrics(agent_id, metrics)
        
        return jsonify({
            'success': True,
            'message': f'Metrics updated for agent {agent_id}'
        })
        
    except Exception as e:
        logger.error(f"Failed to update agent metrics {agent_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_registry_bp.route('/categories', methods=['GET'])
def list_categories():
    """List all available agent categories with agent counts"""
    try:
        registry = get_registry()
        categories = []
        
        for category in AgentCategory:
            agents = registry.get_agents_by_category(category)
            categories.append({
                'name': category.value,
                'display_name': category.value.replace('_', ' ').title(),
                'agent_count': len(agents),
                'agents': [{'id': a.id, 'name': a.name} for a in agents]
            })
        
        return jsonify({
            'success': True,
            'categories': categories
        })
        
    except Exception as e:
        logger.error(f"Failed to list categories: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_registry_bp.route('/capabilities', methods=['GET'])
def list_capabilities():
    """List all available capabilities across all agents"""
    try:
        registry = get_registry()
        capabilities = []
        
        # Get unique capabilities
        capability_map = {}
        for agent in registry.agents.values():
            for cap in agent.capabilities:
                if cap.name not in capability_map:
                    capability_map[cap.name] = {
                        'name': cap.name,
                        'description': cap.description,
                        'agents': []
                    }
                capability_map[cap.name]['agents'].append({
                    'id': agent.id,
                    'name': agent.name
                })
        
        capabilities = list(capability_map.values())
        
        return jsonify({
            'success': True,
            'count': len(capabilities),
            'capabilities': capabilities
        })
        
    except Exception as e:
        logger.error(f"Failed to list capabilities: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_registry_bp.route('/status', methods=['GET'])
def get_registry_status():
    """Get overall registry status and health metrics"""
    try:
        status = get_registry_health()
        
        return jsonify({
            'success': True,
            'registry_status': status
        })
        
    except Exception as e:
        logger.error(f"Failed to get registry status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_registry_bp.route('/search', methods=['GET'])
def search_agents():
    """Search agents by query string"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query parameter "q" is required'
            }), 400
        
        registry = get_registry()
        results = registry.search_agents(query)
        
        return jsonify({
            'success': True,
            'query': query,
            'count': len(results),
            'results': [{'id': a.id, 'name': a.name, 'description': a.description} for a in results]
        })
        
    except Exception as e:
        logger.error(f"Failed to search agents: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_registry_bp.route('/export', methods=['GET'])
def export_registry():
    """Export the complete agent registry"""
    try:
        registry = get_registry()
        export_data = registry.export_registry()
        
        return jsonify({
            'success': True,
            'export': export_data
        })
        
    except Exception as e:
        logger.error(f"Failed to export registry: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_registry_bp.route('/discover', methods=['POST'])
def discover_agents_by_requirement():
    """
    Discover agents that match specific requirements
    
    Body:
    {
        "task": "string describing what you want to do",
        "requirements": ["list", "of", "required", "capabilities"],
        "preferences": {
            "category": "preferred category",
            "max_agents": 5
        }
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body required'
            }), 400
        
        task = data.get('task', '')
        requirements = data.get('requirements', [])
        preferences = data.get('preferences', {})
        
        registry = get_registry()
        matching_agents = []
        
        # Find agents that have all required capabilities
        for agent in registry.agents.values():
            agent_capabilities = {cap.name for cap in agent.capabilities}
            if all(req in agent_capabilities for req in requirements):
                matching_agents.append({
                    'id': agent.id,
                    'name': agent.name,
                    'description': agent.description,
                    'category': agent.category.value,
                    'match_score': len(set(requirements) & agent_capabilities) / len(requirements) if requirements else 1.0,
                    'capabilities': [cap.name for cap in agent.capabilities]
                })
        
        # Filter by category preference if specified
        if preferences.get('category'):
            matching_agents = [a for a in matching_agents if a['category'] == preferences['category']]
        
        # Sort by match score
        matching_agents.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Limit results if specified
        max_agents = preferences.get('max_agents', 10)
        matching_agents = matching_agents[:max_agents]
        
        return jsonify({
            'success': True,
            'task': task,
            'requirements': requirements,
            'count': len(matching_agents),
            'agents': matching_agents
        })
        
    except Exception as e:
        logger.error(f"Failed to discover agents: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_registry_bp.route('/health-check', methods=['GET'])
def registry_health_check():
    """Quick health check endpoint for monitoring"""
    try:
        registry = get_registry()
        total_agents = len(registry.agents)
        active_agents = sum(1 for a in registry.agents.values() if a.status == AgentStatus.ACTIVE)
        
        health_status = 'healthy' if active_agents > total_agents * 0.5 else 'degraded'
        
        return jsonify({
            'status': health_status,
            'total_agents': total_agents,
            'active_agents': active_agents,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

# Helper function to integrate with Flask app
def integrate_agent_registry_api(app):
    """Integrate the agent registry API with the Flask app"""
    try:
        app.register_blueprint(agent_registry_bp)
        logger.info("[OK] Agent Registry API endpoints registered")
        return True
    except Exception as e:
        logger.error(f"Failed to register Agent Registry API: {str(e)}")
        return False