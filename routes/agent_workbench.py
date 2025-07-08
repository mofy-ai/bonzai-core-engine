"""
Agent Workbench API routes
Provides agent creation, management, and performance tracking
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import uuid
import json
import random
from typing import Dict, List, Optional

agent_workbench_bp = Blueprint('agent_workbench_routes', __name__)

# Mock agent store for development
agent_store = {}
agent_metrics = {}

# Initialize with some sample agents
sample_agents = {
    'scout-001': {
        'id': 'scout-001',
        'name': 'Scout Commander Alpha',
        'type': 'scout_commander',
        'status': 'active',
        'created_at': '2024-01-15T10:30:00Z',
        'last_active': '2024-01-20T14:22:00Z',
        'capabilities': ['project_planning', 'architecture', 'team_coordination'],
        'performance': {
            'success_rate': 0.94,
            'response_time': 1.2,
            'tasks_completed': 127,
            'user_satisfaction': 4.6
        },
        'config': {
            'temperature': 0.7,
            'max_tokens': 4096,
            'model': 'gpt-4o'
        }
    },
    'research-002': {
        'id': 'research-002', 
        'name': 'Research Specialist Beta',
        'type': 'research_specialist',
        'status': 'active',
        'created_at': '2024-01-12T09:15:00Z',
        'last_active': '2024-01-20T15:45:00Z',
        'capabilities': ['research', 'analysis', 'documentation'],
        'performance': {
            'success_rate': 0.97,
            'response_time': 2.1,
            'tasks_completed': 89,
            'user_satisfaction': 4.8
        },
        'config': {
            'temperature': 0.3,
            'max_tokens': 8192,
            'model': 'claude-3-opus'
        }
    },
    'debug-003': {
        'id': 'debug-003',
        'name': 'Debug Detective Gamma', 
        'type': 'debugging_detective',
        'status': 'maintenance',
        'created_at': '2024-01-18T16:20:00Z',
        'last_active': '2024-01-19T11:30:00Z',
        'capabilities': ['debugging', 'troubleshooting', 'error_analysis'],
        'performance': {
            'success_rate': 0.89,
            'response_time': 0.8,
            'tasks_completed': 156,
            'user_satisfaction': 4.4
        },
        'config': {
            'temperature': 0.1,
            'max_tokens': 2048,
            'model': 'gpt-4o-mini'
        }
    }
}

agent_store.update(sample_agents)

@agent_workbench_bp.route('/health', methods=['GET'])
def agent_workbench_health():
    """Health check endpoint for agent workbench system"""
    try:
        return jsonify({
            'success': True,
            'status': 'healthy',
            'service': 'agent_workbench',
            'timestamp': datetime.utcnow().isoformat(),
            'total_agents': len(agent_store),
            'active_agents': len([a for a in agent_store.values() if a['status'] == 'active'])
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/agents', methods=['GET'])
def get_agents():
    """Get all agents with optional filtering"""
    try:
        status_filter = request.args.get('status')
        agent_type = request.args.get('type')
        
        agents = list(agent_store.values())
        
        if status_filter:
            agents = [a for a in agents if a['status'] == status_filter]
        
        if agent_type:
            agents = [a for a in agents if a['type'] == agent_type]
        
        return jsonify({
            'success': True,
            'agents': agents,
            'total': len(agents)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/agents', methods=['POST'])
def create_agent():
    """Create a new agent"""
    try:
        data = request.get_json()
        
        agent_id = str(uuid.uuid4())[:8]
        agent = {
            'id': agent_id,
            'name': data.get('name', f'Agent {agent_id}'),
            'type': data.get('type', 'scout_commander'),
            'status': 'active',
            'created_at': datetime.utcnow().isoformat(),
            'last_active': datetime.utcnow().isoformat(),
            'capabilities': data.get('capabilities', []),
            'performance': {
                'success_rate': 0.0,
                'response_time': 0.0,
                'tasks_completed': 0,
                'user_satisfaction': 0.0
            },
            'config': data.get('config', {
                'temperature': 0.7,
                'max_tokens': 4096,
                'model': 'gpt-4o'
            })
        }
        
        agent_store[agent_id] = agent
        
        return jsonify({
            'success': True,
            'agent': agent,
            'message': 'Agent created successfully'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/agents/<agent_id>', methods=['GET'])
def get_agent(agent_id):
    """Get a specific agent by ID"""
    try:
        agent = agent_store.get(agent_id)
        if not agent:
            return jsonify({
                'success': False,
                'error': 'Agent not found'
            }), 404
        
        return jsonify({
            'success': True,
            'agent': agent
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/agents/<agent_id>', methods=['PUT'])
def update_agent(agent_id):
    """Update an existing agent"""
    try:
        agent = agent_store.get(agent_id)
        if not agent:
            return jsonify({
                'success': False,
                'error': 'Agent not found'
            }), 404
        
        data = request.get_json()
        
        # Update allowed fields
        for field in ['name', 'type', 'status', 'capabilities', 'config']:
            if field in data:
                agent[field] = data[field]
        
        agent['last_active'] = datetime.utcnow().isoformat()
        
        return jsonify({
            'success': True,
            'agent': agent,
            'message': 'Agent updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/agents/<agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    """Delete an agent"""
    try:
        if agent_id not in agent_store:
            return jsonify({
                'success': False,
                'error': 'Agent not found'
            }), 404
        
        del agent_store[agent_id]
        
        return jsonify({
            'success': True,
            'message': 'Agent deleted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/metrics', methods=['GET'])
def get_metrics():
    """Get aggregate metrics for all agents"""
    try:
        total_agents = len(agent_store)
        active_agents = len([a for a in agent_store.values() if a['status'] == 'active'])
        
        if total_agents > 0:
            avg_success_rate = sum(a['performance']['success_rate'] for a in agent_store.values()) / total_agents
            avg_response_time = sum(a['performance']['response_time'] for a in agent_store.values()) / total_agents
            total_tasks = sum(a['performance']['tasks_completed'] for a in agent_store.values())
            avg_satisfaction = sum(a['performance']['user_satisfaction'] for a in agent_store.values()) / total_agents
        else:
            avg_success_rate = avg_response_time = total_tasks = avg_satisfaction = 0
        
        metrics = {
            'total_agents': total_agents,
            'active_agents': active_agents,
            'avg_success_rate': round(avg_success_rate, 3),
            'avg_response_time': round(avg_response_time, 2),
            'total_tasks_completed': total_tasks,
            'avg_user_satisfaction': round(avg_satisfaction, 2),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'success': True,
            'metrics': metrics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agent_workbench_bp.route('/types', methods=['GET'])
def get_agent_types():
    """Get available agent types and their descriptions"""
    try:
        agent_types = {
            'scout_commander': {
                'name': 'Scout Commander',
                'description': 'Strategic project leadership and architecture decisions',
                'capabilities': ['project_planning', 'architecture', 'team_coordination'],
                'recommended_config': {
                    'temperature': 0.7,
                    'max_tokens': 4096,
                    'model': 'gpt-4o'
                }
            },
            'research_specialist': {
                'name': 'Research Specialist',
                'description': 'Deep research and comprehensive analysis',
                'capabilities': ['research', 'analysis', 'documentation'],
                'recommended_config': {
                    'temperature': 0.3,
                    'max_tokens': 8192,
                    'model': 'claude-3-opus'
                }
            },
            'code_review_bear': {
                'name': 'Code Review Bear',
                'description': 'Code quality assurance and best practices',
                'capabilities': ['code_review', 'quality_assurance', 'security'],
                'recommended_config': {
                    'temperature': 0.2,
                    'max_tokens': 4096,
                    'model': 'gpt-4o'
                }
            },
            'creative_bear': {
                'name': 'Creative Bear',
                'description': 'Creative problem solving and innovative solutions',
                'capabilities': ['creativity', 'innovation', 'design'],
                'recommended_config': {
                    'temperature': 0.9,
                    'max_tokens': 4096,
                    'model': 'gpt-4o'
                }
            },
            'learning_bear': {
                'name': 'Learning Bear',
                'description': 'Educational guidance and skill development',
                'capabilities': ['teaching', 'mentoring', 'skill_development'],
                'recommended_config': {
                    'temperature': 0.6,
                    'max_tokens': 4096,
                    'model': 'gpt-4o'
                }
            },
            'efficiency_bear': {
                'name': 'Efficiency Bear',
                'description': 'Process optimization and productivity enhancement',
                'capabilities': ['optimization', 'automation', 'efficiency'],
                'recommended_config': {
                    'temperature': 0.4,
                    'max_tokens': 2048,
                    'model': 'gpt-4o-mini'
                }
            },
            'debugging_detective': {
                'name': 'Debugging Detective',
                'description': 'Problem diagnosis and error resolution',
                'capabilities': ['debugging', 'troubleshooting', 'error_analysis'],
                'recommended_config': {
                    'temperature': 0.1,
                    'max_tokens': 2048,
                    'model': 'gpt-4o-mini'
                }
            }
        }
        
        return jsonify({
            'success': True,
            'agent_types': agent_types
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
