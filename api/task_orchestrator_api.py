"""
Bonzai Task Orchestrator API
Provides REST endpoints for task submission, monitoring, and management
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any
import logging
import asyncio
from functools import wraps

# Import task orchestrator
from services.bonzai_task_orchestrator import (
    get_orchestrator,
    submit_task,
    get_task_result,
    get_queue_info,
    get_metrics,
    TaskStatus,
    TaskPriority,
    ExecutionStrategy
)

logger = logging.getLogger(__name__)

# Create Blueprint
task_orchestrator_bp = Blueprint('task_orchestrator', __name__, url_prefix='/api/tasks')

def async_route(f):
    """Decorator to handle async routes in Flask"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(f(*args, **kwargs))
        finally:
            loop.close()
    return wrapper

@task_orchestrator_bp.route('/submit', methods=['POST'])
@async_route
async def submit_new_task():
    """
    Submit a new task for orchestration
    
    Request body:
    {
        "type": "task_type",
        "description": "What needs to be done",
        "requirements": ["capability1", "capability2"],
        "priority": "NORMAL",  // CRITICAL, HIGH, NORMAL, LOW, BACKGROUND
        "strategy": "SINGLE",  // SINGLE, PARALLEL, SEQUENTIAL, CONSENSUS, FALLBACK
        "payload": {...},      // Task-specific data
        "timeout": 300,        // Timeout in seconds
        "user_id": "user123",  // Optional
        "callback_url": "http://...",  // Optional webhook
        "metadata": {...}      // Optional metadata
    }
    """
    try:
        task_data = request.get_json()
        if not task_data:
            return jsonify({
                'success': False,
                'error': 'Request body required'
            }), 400
        
        # Validate required fields
        if not task_data.get('description'):
            return jsonify({
                'success': False,
                'error': 'Task description is required'
            }), 400
        
        # Submit task
        result = await submit_task(task_data)
        
        return jsonify(result), 201 if result['success'] else 400
        
    except Exception as e:
        logger.error(f"Failed to submit task: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_orchestrator_bp.route('/<task_id>', methods=['GET'])
def get_task_status(task_id: str):
    """Get status and result of a specific task"""
    try:
        result = get_task_result(task_id)
        
        if not result:
            return jsonify({
                'success': False,
                'error': f'Task {task_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'task': result
        })
        
    except Exception as e:
        logger.error(f"Failed to get task status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_orchestrator_bp.route('/<task_id>/cancel', methods=['POST'])
@async_route
async def cancel_task(task_id: str):
    """Cancel a pending or active task"""
    try:
        orchestrator = get_orchestrator()
        cancelled = await orchestrator.cancel_task(task_id)
        
        if cancelled:
            return jsonify({
                'success': True,
                'message': f'Task {task_id} cancelled'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Task {task_id} not found or already completed'
            }), 404
            
    except Exception as e:
        logger.error(f"Failed to cancel task: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_orchestrator_bp.route('/queue', methods=['GET'])
def get_queue_status():
    """Get current queue status and statistics"""
    try:
        queue_info = get_queue_info()
        
        return jsonify({
            'success': True,
            'queue': queue_info
        })
        
    except Exception as e:
        logger.error(f"Failed to get queue status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_orchestrator_bp.route('/queue/tasks', methods=['GET'])
def list_queued_tasks():
    """List all tasks currently in queue"""
    try:
        orchestrator = get_orchestrator()
        tasks = orchestrator.task_queue.get_tasks()
        
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task.id,
                'type': task.type,
                'description': task.description,
                'priority': task.priority.name,
                'created_at': task.created_at.isoformat(),
                'user_id': task.user_id
            })
        
        return jsonify({
            'success': True,
            'count': len(task_list),
            'tasks': task_list
        })
        
    except Exception as e:
        logger.error(f"Failed to list queued tasks: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_orchestrator_bp.route('/active', methods=['GET'])
def list_active_tasks():
    """List all currently processing tasks"""
    try:
        orchestrator = get_orchestrator()
        active_tasks = []
        
        for task_id, task in orchestrator.active_tasks.items():
            active_tasks.append({
                'id': task.id,
                'type': task.type,
                'description': task.description,
                'priority': task.priority.name,
                'strategy': task.strategy.name,
                'started_at': task.created_at.isoformat(),
                'user_id': task.user_id
            })
        
        return jsonify({
            'success': True,
            'count': len(active_tasks),
            'tasks': active_tasks
        })
        
    except Exception as e:
        logger.error(f"Failed to list active tasks: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_orchestrator_bp.route('/metrics', methods=['GET'])
def get_orchestrator_metrics():
    """Get orchestrator performance metrics"""
    try:
        metrics = get_metrics()
        
        return jsonify({
            'success': True,
            'metrics': metrics
        })
        
    except Exception as e:
        logger.error(f"Failed to get metrics: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_orchestrator_bp.route('/agent-performance', methods=['GET'])
def get_agent_performance():
    """Get performance metrics for all agents"""
    try:
        orchestrator = get_orchestrator()
        agent_performance = dict(orchestrator.agent_performance)
        
        # Add agent names
        from services.bonzai_agent_registry import get_registry
        registry = get_registry()
        
        enhanced_performance = {}
        for agent_id, perf in agent_performance.items():
            agent = registry.get_agent(agent_id)
            enhanced_performance[agent_id] = {
                **perf,
                'agent_name': agent.name if agent else 'Unknown',
                'category': agent.category.value if agent else 'unknown'
            }
        
        return jsonify({
            'success': True,
            'agent_performance': enhanced_performance
        })
        
    except Exception as e:
        logger.error(f"Failed to get agent performance: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_orchestrator_bp.route('/priorities', methods=['GET'])
def list_priorities():
    """List available task priorities"""
    try:
        priorities = [
            {
                'name': p.name,
                'value': p.value,
                'description': {
                    'CRITICAL': 'Immediate execution required',
                    'HIGH': 'High priority, minimal wait',
                    'NORMAL': 'Standard priority',
                    'LOW': 'Can wait for capacity',
                    'BACKGROUND': 'Execute when idle'
                }.get(p.name, '')
            }
            for p in TaskPriority
        ]
        
        return jsonify({
            'success': True,
            'priorities': priorities
        })
        
    except Exception as e:
        logger.error(f"Failed to list priorities: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_orchestrator_bp.route('/strategies', methods=['GET'])
def list_strategies():
    """List available execution strategies"""
    try:
        strategies = [
            {
                'name': s.name,
                'value': s.value,
                'description': {
                    'SINGLE': 'Route to single best agent',
                    'PARALLEL': 'Execute on multiple agents in parallel',
                    'SEQUENTIAL': 'Execute on agents in sequence',
                    'CONSENSUS': 'Get consensus from multiple agents',
                    'FALLBACK': 'Try agents until one succeeds'
                }.get(s.name, '')
            }
            for s in ExecutionStrategy
        ]
        
        return jsonify({
            'success': True,
            'strategies': strategies
        })
        
    except Exception as e:
        logger.error(f"Failed to list strategies: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_orchestrator_bp.route('/estimate', methods=['POST'])
def estimate_task():
    """
    Estimate task execution time and suitable agents
    
    Request body:
    {
        "requirements": ["capability1", "capability2"],
        "priority": "NORMAL"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body required'
            }), 400
        
        requirements = data.get('requirements', [])
        priority = TaskPriority[data.get('priority', 'NORMAL').upper()]
        
        orchestrator = get_orchestrator()
        
        # Find suitable agents
        from services.bonzai_agent_registry import get_registry
        registry = get_registry()
        suitable_agents = []
        
        for agent in registry.agents.values():
            if agent.status.value == "active":
                agent_capabilities = {cap.name for cap in agent.capabilities}
                if all(req in agent_capabilities for req in requirements):
                    suitable_agents.append({
                        'id': agent.id,
                        'name': agent.name,
                        'category': agent.category.value
                    })
        
        # Estimate wait time
        estimated_wait = orchestrator._estimate_wait_time(priority)
        
        return jsonify({
            'success': True,
            'estimation': {
                'suitable_agents': suitable_agents,
                'agent_count': len(suitable_agents),
                'estimated_wait_seconds': estimated_wait,
                'estimated_wait_readable': f"{estimated_wait/60:.1f} minutes",
                'current_queue_size': orchestrator.task_queue.size(),
                'active_tasks': len(orchestrator.active_tasks)
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to estimate task: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_orchestrator_bp.route('/batch', methods=['POST'])
@async_route
async def submit_batch_tasks():
    """
    Submit multiple tasks as a batch
    
    Request body:
    {
        "tasks": [
            { ... task1 data ... },
            { ... task2 data ... }
        ],
        "batch_metadata": { ... }
    }
    """
    try:
        data = request.get_json()
        if not data or 'tasks' not in data:
            return jsonify({
                'success': False,
                'error': 'Request body with tasks array required'
            }), 400
        
        tasks = data['tasks']
        batch_metadata = data.get('batch_metadata', {})
        
        # Submit all tasks
        results = []
        for task_data in tasks:
            task_data['metadata'] = {
                **task_data.get('metadata', {}),
                'batch': True,
                'batch_metadata': batch_metadata
            }
            result = await submit_task(task_data)
            results.append(result)
        
        successful = sum(1 for r in results if r['success'])
        
        return jsonify({
            'success': True,
            'batch_size': len(tasks),
            'successful_submissions': successful,
            'failed_submissions': len(tasks) - successful,
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Failed to submit batch tasks: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_orchestrator_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        orchestrator = get_orchestrator()
        metrics = orchestrator.metrics
        
        # Determine health status
        if metrics['active_tasks'] > orchestrator.max_workers * 0.9:
            status = 'overloaded'
        elif metrics['success_rate'] < 0.5:
            status = 'degraded'
        else:
            status = 'healthy'
        
        return jsonify({
            'status': status,
            'active_tasks': metrics['active_tasks'],
            'queue_size': metrics['queue_size'],
            'capacity': orchestrator.max_workers,
            'success_rate': metrics.get('success_rate', 1.0)
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

# Helper function to integrate with Flask app
def integrate_task_orchestrator_api(app):
    """Integrate the task orchestrator API with the Flask app"""
    try:
        app.register_blueprint(task_orchestrator_bp)
        logger.info("[OK] Task Orchestrator API endpoints registered")
        return True
    except Exception as e:
        logger.error(f"Failed to register Task Orchestrator API: {str(e)}")
        return False