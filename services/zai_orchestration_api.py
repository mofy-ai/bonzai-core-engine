# backend/api/zai_orchestration_api.py
"""
[BEAR] Zai Orchestration API
RESTful endpoints and WebSocket handlers for agent coordination
"""

from flask import Blueprint, request, jsonify, current_app
from flask_socketio import emit, join_room, leave_room
import asyncio
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Blueprint for REST endpoints
orchestration_bp = Blueprint('orchestration', __name__)

def get_orchestrator():
    """Safely get orchestrator from app context"""
    return getattr(current_app, 'zai_orchestrator', None)

@orchestration_bp.route('/api/zai/chat', methods=['POST'])
async def intelligent_chat():
    """
    [BEAR] Main chat endpoint with intelligent agent routing
    Automatically determines which agents to involve based on the request
    """
    try:
        data = request.json or {}
        message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')
        page_context = data.get('page_context', 'main_chat')
        
        # Get orchestrator from app
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
        
        # Process the request with intelligent routing
        result = await orchestrator.process_user_request(
            message=message,
            user_id=user_id,
            page_context=page_context
        )
        
        return jsonify({
            'success': True,
            'response': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in intelligent_chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'fallback_message': "[BEAR] I'm having a moment! Let me gather myself and try again."
        }), 500

@orchestration_bp.route('/api/zai/agents/status', methods=['GET'])
async def get_agents_status():
    """Get status of all agents"""
    try:
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
            
        status = await orchestrator.get_system_status()
        
        return jsonify({
            'success': True,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/zai/agents/<agent_id>/direct', methods=['POST'])
async def direct_agent_communication(agent_id):
    """Communicate directly with a specific agent"""
    try:
        data = request.json or {}
        message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')
        
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
        
        # Get the specific agent
        agent = orchestrator.agents.get(agent_id) if orchestrator.agents else None
        if not agent:
            return jsonify({
                'success': False,
                'error': f'Agent {agent_id} not found'
            }), 404
        
        # Direct communication with agent
        result = await agent.handle_request(message, user_id)
        
        return jsonify({
            'success': True,
            'response': result,
            'agent_id': agent_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/zai/workflow/analyze', methods=['POST'])
async def analyze_workflow():
    """Analyze a request and suggest workflow approach"""
    try:
        data = request.json or {}
        request_text = data.get('request', '')
        user_id = data.get('user_id', 'default_user')
        
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
            
        workflow_intelligence = getattr(orchestrator, 'workflow_intelligence', None)
        if not workflow_intelligence:
            return jsonify({
                'success': False,
                'error': 'Workflow intelligence not available'
            }), 500
        
        # Analyze the workflow
        analysis = await workflow_intelligence.analyze_request(request_text, user_id)
        
        return jsonify({
            'success': True,
            'analysis': {
                'workflow_type': analysis.workflow_type.value,
                'confidence': analysis.confidence,
                'recommended_agents': analysis.recommended_agents,
                'estimated_complexity': analysis.estimated_complexity,
                'estimated_duration': analysis.estimated_duration,
                'resource_requirements': analysis.resource_requirements
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/zai/memory/search', methods=['POST'])
async def search_memory():
    """Search user memories"""
    try:
        data = request.json or {}
        query = data.get('query', '')
        user_id = data.get('user_id', 'default_user')
        limit = data.get('limit', 10)
        
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
            
        memory_manager = getattr(orchestrator, 'memory_manager', None)
        if not memory_manager:
            return jsonify({
                'success': False,
                'error': 'Memory manager not available'
            }), 500
        
        # Search memories
        memories = await memory_manager.search_memories(query, user_id, limit)
        
        # Convert memories to serializable format
        memory_data = []
        for memory in memories:
            memory_data.append({
                'id': memory.id,
                'type': memory.type.value,
                'content': memory.content,
                'importance': memory.importance.value,
                'tags': memory.tags or [],
                'created_at': memory.created_at.isoformat() if memory.created_at else None,
                'access_count': memory.access_count
            })
        
        return jsonify({
            'success': True,
            'memories': memory_data,
            'total_found': len(memory_data),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/zai/context', methods=['GET'])
async def get_global_context():
    """Get current global context"""
    try:
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
            
        context_awareness = getattr(orchestrator, 'context_awareness', None)
        global_context = getattr(context_awareness, 'global_context', {}) if context_awareness else {}
        
        return jsonify({
            'success': True,
            'context': global_context,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/zai/context', methods=['POST'])
async def update_global_context():
    """Update global context"""
    try:
        data = request.json or {}
        key = data.get('key')
        value = data.get('value')
        
        if not key:
            return jsonify({
                'success': False,
                'error': 'Key is required'
            }), 400
        
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
            
        context_awareness = getattr(orchestrator, 'context_awareness', None)
        if context_awareness and hasattr(context_awareness, 'update_global_context'):
            await context_awareness.update_global_context(key, value)
        
        return jsonify({
            'success': True,
            'message': f'Context updated: {key}',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/zai/user/profile', methods=['GET'])
async def get_user_profile():
    """Get user profile and preferences"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
            
        memory_manager = getattr(orchestrator, 'memory_manager', None)
        if not memory_manager:
            return jsonify({
                'success': False,
                'error': 'Memory manager not available'
            }), 500
        
        # Get user profile
        profile = await memory_manager.get_user_profile(user_id)
        
        # Get decision patterns
        patterns = await memory_manager.analyze_decision_patterns(user_id)
        
        return jsonify({
            'success': True,
            'profile': {
                'user_id': profile.user_id,
                'expertise_level': profile.expertise_level,
                'preferred_agents': profile.preferred_agents or [],
                'communication_style': profile.communication_style or {},
                'success_patterns': profile.success_patterns or {},
                'learning_preferences': profile.learning_preferences or {},
                'last_updated': profile.last_updated.isoformat() if profile.last_updated else None
            },
            'patterns': patterns,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orchestration_bp.route('/api/zai/system/stats', methods=['GET'])
async def get_system_stats():
    """Get comprehensive system statistics"""
    try:
        orchestrator = get_orchestrator()
        if not orchestrator:
            return jsonify({
                'success': False,
                'error': 'Orchestrator not available'
            }), 500
        
        # Get memory stats
        memory_manager = getattr(orchestrator, 'memory_manager', None)
        memory_stats = await memory_manager.get_memory_stats() if memory_manager else {}
        
        # Get agent stats
        agent_stats = {}
        agents = getattr(orchestrator, 'agents', {})
        for agent_id, agent in agents.items():
            agent_stats[agent_id] = {
                'name': getattr(agent, 'name', agent_id),
                'personality': getattr(agent, 'personality', 'unknown'),
                'active': True,
                'specialties': getattr(agent, 'specialties', [])
            }
        
        # Get workflow stats
        workflow_stats = {
            'total_requests_processed': getattr(orchestrator, 'total_requests', 0),
            'active_collaborations': len(getattr(orchestrator, 'active_tasks', {}))
        }
        
        return jsonify({
            'success': True,
            'stats': {
                'memory': memory_stats,
                'agents': agent_stats,
                'workflow': workflow_stats,
                'system_uptime': datetime.now().isoformat()
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# WebSocket handlers for real-time communication
def setup_orchestration_websockets(socketio):
    """Setup WebSocket handlers for orchestration"""
    
    @socketio.on('join_zai')
    def on_join_zai(data):
        """Join Zai room for real-time updates"""
        data = data or {}
        user_id = data.get('user_id', 'default_user')
        room = f"zai_{user_id}"
        join_room(room)
        emit('joined_zai', {'room': room, 'status': 'connected'})
        logger.info(f"[BEAR] User {user_id} joined Zai room")
    
    @socketio.on('leave_zai')
    def on_leave_zai(data):
        """Leave Zai room"""
        data = data or {}
        user_id = data.get('user_id', 'default_user')
        room = f"zai_{user_id}"
        leave_room(room)
        emit('left_zai', {'room': room, 'status': 'disconnected'})
    
    @socketio.on('zai_chat')
    async def on_zai_chat(data):
        """Handle real-time chat with Zai"""
        try:
            data = data or {}
            message = data.get('message', '')
            user_id = data.get('user_id', 'default_user')
            page_context = data.get('page_context', 'main_chat')
            room = f"zai_{user_id}"
            
            # Get orchestrator
            orchestrator = get_orchestrator()
            if not orchestrator:
                emit('zai_error', {
                    'success': False,
                    'error': 'Orchestrator not available'
                })
                return
            
            # Emit thinking status
            socketio.emit('zai_thinking', {
                'status': 'processing',
                'message': '[BEAR] Let me think about this...'
            }, to=room)
            
            # Process the request
            result = await orchestrator.process_user_request(
                message=message,
                user_id=user_id,
                page_context=page_context
            )
            
            # Emit response
            socketio.emit('zai_response', {
                'success': True,
                'response': result,
                'timestamp': datetime.now().isoformat()
            }, to=room)
            
        except Exception as e:
            logger.error(f"Error in zai_chat: {e}")
            socketio.emit('zai_error', {
                'success': False,
                'error': str(e),
                'fallback_message': "[BEAR] I'm having a moment! Let me gather myself and try again."
            }, to=room)
    
    @socketio.on('zai_agent_direct')
    async def on_direct_agent_chat(data):
        """Direct communication with specific agent"""
        try:
            data = data or {}
            agent_id = data.get('agent_id')
            message = data.get('message', '')
            user_id = data.get('user_id', 'default_user')
            room = f"zai_{user_id}"
            
            orchestrator = get_orchestrator()
            if not orchestrator:
                socketio.emit('agent_error', {
                    'error': 'Orchestrator not available'
                }, to=room)
                return
                
            agents = getattr(orchestrator, 'agents', {})
            agent = agents.get(agent_id) if agents else None
            
            if not agent:
                socketio.emit('agent_error', {
                    'error': f'Agent {agent_id} not found'
                }, to=room)
                return
            
            # Direct communication
            result = await agent.handle_request(message, user_id)
            
            socketio.emit('agent_response', {
                'agent_id': agent_id,
                'response': result,
                'timestamp': datetime.now().isoformat()
            }, to=room)
            
        except Exception as e:
            logger.error(f"Error in direct agent chat: {e}")
            socketio.emit('agent_error', {
                'error': str(e)
            }, to=room)

def integrate_orchestration_with_app(app, socketio):
    """Integrate orchestration API with Flask app"""
    
    # Register blueprint
    app.register_blueprint(orchestration_bp)
    
    # Setup WebSocket handlers
    setup_orchestration_websockets(socketio)
    
    logger.info("[BEAR] Zai Orchestration API integrated successfully")
