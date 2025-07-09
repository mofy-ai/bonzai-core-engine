#  Agent Creation Workbench API - Mama Bear's autonomous agent management

from flask import Blueprint, request, jsonify
from typing import Dict, Any
import asyncio
import logging
from datetime import datetime

from services.agent_creation_workbench import agent_workbench

# Create blueprint for agent workbench API
agent_workbench_bp = Blueprint('agent_workbench', __name__, url_prefix='/api/agents')

logger = logging.getLogger(__name__)

@agent_workbench_bp.route('/templates', methods=['GET'])
def get_agent_templates():
    """
    📋 Get available agent templates
    """
    try:
        template_type = request.args.get('type')
        
        templates = agent_workbench.get_agent_templates(template_type)
        
        return jsonify({
            'success': True,
            'templates': templates,
            'count': len(templates),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get templates: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/templates/<template_id>', methods=['GET'])
def get_agent_template(template_id):
    """
    📋 Get specific agent template details
    """
    try:
        template = agent_workbench._load_template(template_id)
        
        if not template:
            return jsonify({
                'success': False,
                'error': f'Template {template_id} not found'
            }), 404
        
        from dataclasses import asdict
        return jsonify({
            'success': True,
            'template': asdict(template),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get template: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/create', methods=['POST'])
async def create_custom_agent():
    """
     Create a custom agent using Mama Bear intelligence
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'description', 'user_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create agent specification
        agent_spec = {
            'name': data['name'],
            'description': data['description'],
            'capabilities': data.get('capabilities', []),
            'config': data.get('config', {}),
            'requirements': data.get('requirements', [])
        }
        
        # Create custom agent
        result = await agent_workbench.create_custom_agent(
            user_id=data['user_id'],
            agent_spec=agent_spec
        )
        
        return jsonify({
            'success': result['success'],
            'agent_template': result.get('template'),
            'implementation': result.get('implementation'),
            'recommendations': result.get('recommendations'),
            'error': result.get('error'),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Custom agent creation failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/deploy', methods=['POST'])
async def deploy_agent():
    """
     Deploy an agent from template
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['template_id', 'user_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Deploy agent
        result = await agent_workbench.deploy_agent(
            template_id=data['template_id'],
            user_id=data['user_id'],
            deployment_config=data.get('deployment_config', {})
        )
        
        return jsonify({
            'success': result['success'],
            'agent': result.get('agent'),
            'deployment_info': result.get('deployment_info'),
            'error': result.get('error'),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Agent deployment failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/my-agents', methods=['GET'])
def get_user_agents():
    """
    👤 Get all agents owned by user
    """
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'user_id parameter required'
            }), 400
        
        agents = agent_workbench.get_user_agents(user_id)
        
        return jsonify({
            'success': True,
            'agents': agents,
            'count': len(agents),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get user agents: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/<agent_id>/manage', methods=['POST'])
async def manage_agent(agent_id):
    """
     Manage agent lifecycle (start, stop, pause, restart)
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['action', 'user_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Manage agent
        result = await agent_workbench.manage_agent(
            agent_id=agent_id,
            action=data['action'],
            user_id=data['user_id']
        )
        
        return jsonify({
            'success': result['success'],
            'agent': result.get('agent'),
            'action_performed': result.get('action_performed'),
            'error': result.get('error'),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Agent management failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/<agent_id>/performance', methods=['GET'])
async def get_agent_performance(agent_id):
    """
     Get detailed performance metrics for agent
    """
    try:
        performance = await agent_workbench.get_agent_performance(agent_id)
        
        if 'error' in performance:
            return jsonify({
                'success': False,
                'error': performance['error']
            }), 404
        
        return jsonify({
            'success': True,
            'performance': performance,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get agent performance: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/<agent_id>/status', methods=['GET'])
def get_agent_status(agent_id):
    """
    ℹ️ Get current agent status and basic info
    """
    try:
        if agent_id not in agent_workbench.active_agents:
            return jsonify({
                'success': False,
                'error': f'Agent {agent_id} not found'
            }), 404
        
        agent = agent_workbench.active_agents[agent_id]
        
        from dataclasses import asdict
        return jsonify({
            'success': True,
            'agent': asdict(agent),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get agent status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/stats', methods=['GET'])
def get_workbench_stats():
    """
    📈 Get overall workbench statistics
    """
    try:
        user_id = request.args.get('user_id')
        
        # Calculate stats
        total_templates = len(agent_workbench.get_agent_templates())
        total_agents = len(agent_workbench.active_agents)
        
        user_agents = []
        if user_id:
            user_agents = agent_workbench.get_user_agents(user_id)
        
        active_count = sum(1 for agent in agent_workbench.active_agents.values() 
                          if agent.status == 'active')
        
        stats = {
            'total_templates': total_templates,
            'total_agents': total_agents,
            'active_agents': active_count,
            'user_agents': len(user_agents) if user_id else 0,
            'template_types': {
                'research': len([t for t in agent_workbench.get_agent_templates() if t['type'] == 'research']),
                'ui_design': len([t for t in agent_workbench.get_agent_templates() if t['type'] == 'ui_design']),
                'api': len([t for t in agent_workbench.get_agent_templates() if t['type'] == 'api']),
                'security': len([t for t in agent_workbench.get_agent_templates() if t['type'] == 'security']),
                'custom': len([t for t in agent_workbench.get_agent_templates() if t['type'] == 'custom'])
            }
        }
        
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get workbench stats: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/search', methods=['GET'])
def search_agents():
    """
     Search agents and templates
    """
    try:
        query = request.args.get('q', '')
        agent_type = request.args.get('type')
        user_id = request.args.get('user_id')
        
        # Search templates
        templates = agent_workbench.get_agent_templates(agent_type)
        filtered_templates = []
        
        for template in templates:
            if not query or query.lower() in template['name'].lower() or query.lower() in template['description'].lower():
                filtered_templates.append(template)
        
        # Search user agents if user_id provided
        user_agents = []
        if user_id:
            user_agents = agent_workbench.get_user_agents(user_id)
            filtered_agents = []
            
            for agent in user_agents:
                if not query or query.lower() in agent['name'].lower():
                    filtered_agents.append(agent)
            
            user_agents = filtered_agents
        
        return jsonify({
            'success': True,
            'templates': filtered_templates,
            'agents': user_agents,
            'query': query,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
