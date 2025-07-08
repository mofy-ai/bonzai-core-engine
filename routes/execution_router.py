"""
Execution Router API routes  
Provides intelligent task routing, metrics, and execution management
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import uuid
import json
import random
from typing import Dict, List, Optional

execution_router_bp = Blueprint('execution_router_routes', __name__)

# Mock execution data
execution_store = {}
route_metrics = {}

# Initialize sample execution data
sample_executions = {
    'exec-001': {
        'id': 'exec-001',
        'task_name': 'Frontend Component Analysis',
        'route': 'code_review_bear',
        'status': 'completed',
        'priority': 'high',
        'confidence': 0.94,
        'created_at': '2024-01-20T10:30:00Z',
        'completed_at': '2024-01-20T10:35:22Z',
        'duration': 322,
        'success': True,
        'metadata': {
            'input_tokens': 1250,
            'output_tokens': 890,
            'model_used': 'gpt-4o'
        }
    },
    'exec-002': {
        'id': 'exec-002',
        'task_name': 'Research API Integration Patterns',
        'route': 'research_specialist',
        'status': 'in_progress',
        'priority': 'medium',
        'confidence': 0.88,
        'created_at': '2024-01-20T14:15:00Z',
        'completed_at': None,
        'duration': None,
        'success': None,
        'metadata': {
            'input_tokens': 2100,
            'output_tokens': None,
            'model_used': 'claude-3-opus'
        }
    },
    'exec-003': {
        'id': 'exec-003',
        'task_name': 'Debug Memory Leak Issue',
        'route': 'debugging_detective',
        'status': 'queued',
        'priority': 'urgent',
        'confidence': 0.92,
        'created_at': '2024-01-20T15:45:00Z',
        'completed_at': None,
        'duration': None,
        'success': None,
        'metadata': {
            'input_tokens': None,
            'output_tokens': None,
            'model_used': 'gpt-4o-mini'
        }
    }
}

execution_store.update(sample_executions)

@execution_router_bp.route('/health', methods=['GET'])
def execution_router_health():
    """Health check endpoint for execution router system"""
    try:
        total_executions = len(execution_store)
        active_executions = len([e for e in execution_store.values() if e['status'] in ['in_progress', 'queued']])
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'service': 'execution_router',
            'timestamp': datetime.utcnow().isoformat(),
            'total_executions': total_executions,
            'active_executions': active_executions,
            'router_uptime': '99.8%'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@execution_router_bp.route('/executions', methods=['GET'])
def get_executions():
    """Get all executions with optional filtering"""
    try:
        status_filter = request.args.get('status')
        priority_filter = request.args.get('priority')
        route_filter = request.args.get('route')
        limit = request.args.get('limit', type=int)
        
        executions = list(execution_store.values())
        
        if status_filter:
            executions = [e for e in executions if e['status'] == status_filter]
        
        if priority_filter:
            executions = [e for e in executions if e['priority'] == priority_filter]
            
        if route_filter:
            executions = [e for e in executions if e['route'] == route_filter]
        
        # Sort by created_at descending
        executions.sort(key=lambda x: x['created_at'], reverse=True)
        
        if limit:
            executions = executions[:limit]
        
        return jsonify({
            'success': True,
            'executions': executions,
            'total': len(executions)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@execution_router_bp.route('/executions', methods=['POST'])
def create_execution():
    """Create a new execution task"""
    try:
        data = request.get_json()
        
        execution_id = f"exec-{str(uuid.uuid4())[:8]}"
        
        # Simple routing logic based on task name
        task_name = data.get('task_name', '').lower()
        route = 'scout_commander'  # default
        confidence = 0.75  # default
        
        if any(word in task_name for word in ['debug', 'error', 'bug', 'fix']):
            route = 'debugging_detective'
            confidence = 0.92
        elif any(word in task_name for word in ['research', 'analyze', 'study']):
            route = 'research_specialist'
            confidence = 0.88
        elif any(word in task_name for word in ['review', 'code', 'quality']):
            route = 'code_review_bear'
            confidence = 0.85
        elif any(word in task_name for word in ['creative', 'design', 'innovate']):
            route = 'creative_bear'
            confidence = 0.80
        elif any(word in task_name for word in ['teach', 'learn', 'explain']):
            route = 'learning_bear'
            confidence = 0.83
        elif any(word in task_name for word in ['optimize', 'efficient', 'performance']):
            route = 'efficiency_bear'
            confidence = 0.86
        
        execution = {
            'id': execution_id,
            'task_name': data.get('task_name', 'Untitled Task'),
            'route': route,
            'status': 'queued',
            'priority': data.get('priority', 'medium'),
            'confidence': confidence,
            'created_at': datetime.utcnow().isoformat(),
            'completed_at': None,
            'duration': None,
            'success': None,
            'metadata': {
                'input_tokens': None,
                'output_tokens': None,
                'model_used': data.get('model', 'gpt-4o'),
                'user_id': data.get('user_id', 'default')
            }
        }
        
        execution_store[execution_id] = execution
        
        return jsonify({
            'success': True,
            'execution': execution,
            'message': 'Execution created and queued successfully'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@execution_router_bp.route('/executions/<execution_id>', methods=['GET'])
def get_execution(execution_id):
    """Get a specific execution by ID"""
    try:
        execution = execution_store.get(execution_id)
        if not execution:
            return jsonify({
                'success': False,
                'error': 'Execution not found'
            }), 404
        
        return jsonify({
            'success': True,
            'execution': execution
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@execution_router_bp.route('/executions/<execution_id>/status', methods=['PUT'])
def update_execution_status(execution_id):
    """Update execution status"""
    try:
        execution = execution_store.get(execution_id)
        if not execution:
            return jsonify({
                'success': False,
                'error': 'Execution not found'
            }), 404
        
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['queued', 'in_progress', 'completed', 'failed', 'cancelled']:
            return jsonify({
                'success': False,
                'error': 'Invalid status'
            }), 400
        
        execution['status'] = new_status
        
        if new_status == 'in_progress':
            execution['started_at'] = datetime.utcnow().isoformat()
        elif new_status in ['completed', 'failed']:
            execution['completed_at'] = datetime.utcnow().isoformat()
            if 'started_at' in execution:
                start_time = datetime.fromisoformat(execution['started_at'].replace('Z', '+00:00'))
                end_time = datetime.utcnow()
                execution['duration'] = int((end_time - start_time).total_seconds())
            execution['success'] = new_status == 'completed'
        
        return jsonify({
            'success': True,
            'execution': execution,
            'message': f'Execution status updated to {new_status}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@execution_router_bp.route('/metrics', methods=['GET'])
def get_metrics():
    """Get execution router metrics and statistics"""
    try:
        executions = list(execution_store.values())
        total_executions = len(executions)
        
        if total_executions == 0:
            return jsonify({
                'success': True,
                'metrics': {
                    'total_executions': 0,
                    'success_rate': 0,
                    'avg_duration': 0,
                    'avg_confidence': 0,
                    'route_distribution': {},
                    'priority_distribution': {},
                    'status_distribution': {}
                }
            })
        
        # Calculate metrics
        completed_executions = [e for e in executions if e['status'] == 'completed']
        successful_executions = [e for e in completed_executions if e.get('success', False)]
        
        success_rate = len(successful_executions) / len(completed_executions) if completed_executions else 0
        
        # Average duration for completed executions
        durations = [e['duration'] for e in completed_executions if e['duration'] is not None]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # Average confidence
        avg_confidence = sum(e['confidence'] for e in executions) / total_executions
        
        # Distribution calculations
        route_distribution = {}
        priority_distribution = {}
        status_distribution = {}
        
        for execution in executions:
            # Route distribution
            route = execution['route']
            route_distribution[route] = route_distribution.get(route, 0) + 1
            
            # Priority distribution
            priority = execution['priority']
            priority_distribution[priority] = priority_distribution.get(priority, 0) + 1
            
            # Status distribution
            status = execution['status']
            status_distribution[status] = status_distribution.get(status, 0) + 1
        
        metrics = {
            'total_executions': total_executions,
            'success_rate': round(success_rate, 3),
            'avg_duration': round(avg_duration, 2),
            'avg_confidence': round(avg_confidence, 3),
            'route_distribution': route_distribution,
            'priority_distribution': priority_distribution,
            'status_distribution': status_distribution,
            'active_executions': len([e for e in executions if e['status'] in ['queued', 'in_progress']]),
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

@execution_router_bp.route('/routes', methods=['GET'])
def get_available_routes():
    """Get available execution routes and their capabilities"""
    try:
        routes = {
            'scout_commander': {
                'name': 'Scout Commander',
                'description': 'Strategic project leadership and architecture decisions',
                'capabilities': ['project_planning', 'architecture', 'team_coordination'],
                'confidence_threshold': 0.75,
                'avg_duration': 180
            },
            'research_specialist': {
                'name': 'Research Specialist',
                'description': 'Deep research and comprehensive analysis',
                'capabilities': ['research', 'analysis', 'documentation'],
                'confidence_threshold': 0.85,
                'avg_duration': 300
            },
            'code_review_bear': {
                'name': 'Code Review Bear',
                'description': 'Code quality assurance and best practices',
                'capabilities': ['code_review', 'quality_assurance', 'security'],
                'confidence_threshold': 0.80,
                'avg_duration': 240
            },
            'creative_bear': {
                'name': 'Creative Bear',
                'description': 'Creative problem solving and innovative solutions',
                'capabilities': ['creativity', 'innovation', 'design'],
                'confidence_threshold': 0.70,
                'avg_duration': 200
            },
            'learning_bear': {
                'name': 'Learning Bear',
                'description': 'Educational guidance and skill development',
                'capabilities': ['teaching', 'mentoring', 'skill_development'],
                'confidence_threshold': 0.78,
                'avg_duration': 220
            },
            'efficiency_bear': {
                'name': 'Efficiency Bear',
                'description': 'Process optimization and productivity enhancement',
                'capabilities': ['optimization', 'automation', 'efficiency'],
                'confidence_threshold': 0.82,
                'avg_duration': 150
            },
            'debugging_detective': {
                'name': 'Debugging Detective',
                'description': 'Problem diagnosis and error resolution',
                'capabilities': ['debugging', 'troubleshooting', 'error_analysis'],
                'confidence_threshold': 0.88,
                'avg_duration': 120
            }
        }
        
        return jsonify({
            'success': True,
            'routes': routes
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@execution_router_bp.route('/routes/recommend', methods=['POST'])
def recommend_route():
    """Recommend the best route for a given task"""
    try:
        data = request.get_json()
        task_description = data.get('task_description', '').lower()
        
        # Simple keyword-based routing logic
        route_scores = {
            'debugging_detective': 0,
            'research_specialist': 0,
            'code_review_bear': 0,
            'creative_bear': 0,
            'learning_bear': 0,
            'efficiency_bear': 0,
            'scout_commander': 0
        }
        
        # Keyword scoring
        debug_keywords = ['debug', 'error', 'bug', 'fix', 'issue', 'problem', 'crash']
        research_keywords = ['research', 'analyze', 'study', 'investigate', 'explore']
        review_keywords = ['review', 'code', 'quality', 'best practice', 'security']
        creative_keywords = ['creative', 'design', 'innovate', 'brainstorm', 'idea']
        learning_keywords = ['teach', 'learn', 'explain', 'tutorial', 'guide']
        efficiency_keywords = ['optimize', 'efficient', 'performance', 'speed', 'automate']
        strategic_keywords = ['plan', 'architecture', 'strategy', 'coordinate', 'manage']
        
        for keyword in debug_keywords:
            if keyword in task_description:
                route_scores['debugging_detective'] += 1
        
        for keyword in research_keywords:
            if keyword in task_description:
                route_scores['research_specialist'] += 1
        
        for keyword in review_keywords:
            if keyword in task_description:
                route_scores['code_review_bear'] += 1
        
        for keyword in creative_keywords:
            if keyword in task_description:
                route_scores['creative_bear'] += 1
        
        for keyword in learning_keywords:
            if keyword in task_description:
                route_scores['learning_bear'] += 1
        
        for keyword in efficiency_keywords:
            if keyword in task_description:
                route_scores['efficiency_bear'] += 1
        
        for keyword in strategic_keywords:
            if keyword in task_description:
                route_scores['scout_commander'] += 1
        
        # Find best route
        best_route = max(route_scores, key=route_scores.get)
        confidence = min(0.95, 0.65 + (route_scores[best_route] * 0.1))
        
        # If no clear match, default to scout_commander
        if route_scores[best_route] == 0:
            best_route = 'scout_commander'
            confidence = 0.65
        
        recommendation = {
            'recommended_route': best_route,
            'confidence': round(confidence, 3),
            'scores': route_scores,
            'reasoning': f'Based on task analysis, {best_route} scored highest with {route_scores[best_route]} matching keywords'
        }
        
        return jsonify({
            'success': True,
            'recommendation': recommendation
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
