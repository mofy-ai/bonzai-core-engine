"""
Bonzai WebSocket Coordinator API
REST endpoints for WebSocket coordination management and monitoring
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any
import logging
from datetime import datetime

# Import WebSocket coordinator
from services.bonzai_websocket_coordinator import (
    get_coordinator,
    MessageType,
    CoordinationProtocol
)

logger = logging.getLogger(__name__)

# Create Blueprint
websocket_api_bp = Blueprint('websocket_api', __name__, url_prefix='/api/websocket')

@websocket_api_bp.route('/status', methods=['GET'])
def get_websocket_status():
    """Get overall WebSocket coordination status"""
    try:
        coordinator = get_coordinator()
        status = coordinator.get_coordination_status()
        
        return jsonify({
            'success': True,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
        
    except RuntimeError:
        return jsonify({
            'success': False,
            'error': 'WebSocket coordinator not initialized'
        }), 503
    except Exception as e:
        logger.error(f"Failed to get WebSocket status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@websocket_api_bp.route('/agents', methods=['GET'])
def list_connected_agents():
    """List all currently connected agents"""
    try:
        coordinator = get_coordinator()
        agents = coordinator.get_connected_agents()
        
        return jsonify({
            'success': True,
            'count': len(agents),
            'agents': agents
        })
        
    except RuntimeError:
        return jsonify({
            'success': False,
            'error': 'WebSocket coordinator not initialized'
        }), 503
    except Exception as e:
        logger.error(f"Failed to list connected agents: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@websocket_api_bp.route('/agents/<agent_id>', methods=['GET'])
def get_agent_connection_status(agent_id: str):
    """Get connection status for a specific agent"""
    try:
        coordinator = get_coordinator()
        status = coordinator.get_agent_status(agent_id)
        
        if not status:
            return jsonify({
                'success': False,
                'error': f'Agent {agent_id} not connected'
            }), 404
        
        return jsonify({
            'success': True,
            'agent': status
        })
        
    except RuntimeError:
        return jsonify({
            'success': False,
            'error': 'WebSocket coordinator not initialized'
        }), 503
    except Exception as e:
        logger.error(f"Failed to get agent status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@websocket_api_bp.route('/send-message', methods=['POST'])
def send_message():
    """
    Send a message between agents via REST API
    
    Request body:
    {
        "sender_id": "agent1",
        "recipient_id": "agent2",
        "type": "direct",
        "payload": {...}
    }
    """
    try:
        coordinator = get_coordinator()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body required'
            }), 400
        
        # Validate required fields
        required = ['sender_id', 'recipient_id', 'payload']
        for field in required:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Field {field} is required'
                }), 400
        
        # Send message
        message_type = MessageType(data.get('type', 'direct'))
        message_id = coordinator.send_message_to_agent(
            sender_id=data['sender_id'],
            recipient_id=data['recipient_id'],
            message_type=message_type,
            payload=data['payload']
        )
        
        return jsonify({
            'success': True,
            'message_id': message_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except RuntimeError:
        return jsonify({
            'success': False,
            'error': 'WebSocket coordinator not initialized'
        }), 503
    except Exception as e:
        logger.error(f"Failed to send message: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@websocket_api_bp.route('/broadcast', methods=['POST'])
def broadcast_to_channel():
    """
    Broadcast a message to a channel
    
    Request body:
    {
        "channel": "updates",
        "message": {...}
    }
    """
    try:
        coordinator = get_coordinator()
        data = request.get_json()
        
        if not data or 'channel' not in data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Channel and message required'
            }), 400
        
        coordinator.broadcast_to_channel(
            channel=data['channel'],
            message=data['message']
        )
        
        return jsonify({
            'success': True,
            'channel': data['channel'],
            'timestamp': datetime.now().isoformat()
        })
        
    except RuntimeError:
        return jsonify({
            'success': False,
            'error': 'WebSocket coordinator not initialized'
        }), 503
    except Exception as e:
        logger.error(f"Failed to broadcast: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@websocket_api_bp.route('/context/<context_id>', methods=['GET'])
def get_shared_context(context_id: str):
    """Get shared context data"""
    try:
        coordinator = get_coordinator()
        agent_id = request.args.get('agent_id')
        
        if not agent_id:
            return jsonify({
                'success': False,
                'error': 'agent_id query parameter required'
            }), 400
        
        context_data = coordinator.get_shared_context(context_id, agent_id)
        
        if context_data is None:
            return jsonify({
                'success': False,
                'error': f'Context {context_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'context_id': context_id,
            'data': context_data
        })
        
    except PermissionError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 403
    except RuntimeError:
        return jsonify({
            'success': False,
            'error': 'WebSocket coordinator not initialized'
        }), 503
    except Exception as e:
        logger.error(f"Failed to get context: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@websocket_api_bp.route('/context/<context_id>/access', methods=['POST'])
def grant_context_access(context_id: str):
    """
    Grant access to shared context
    
    Request body:
    {
        "owner_id": "agent1",
        "grantee_id": "agent2"
    }
    """
    try:
        coordinator = get_coordinator()
        data = request.get_json()
        
        if not data or 'owner_id' not in data or 'grantee_id' not in data:
            return jsonify({
                'success': False,
                'error': 'owner_id and grantee_id required'
            }), 400
        
        coordinator.grant_context_access(
            context_id=context_id,
            owner_id=data['owner_id'],
            grantee_id=data['grantee_id']
        )
        
        return jsonify({
            'success': True,
            'message': f'Access granted to {data["grantee_id"]} for context {context_id}'
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except PermissionError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 403
    except RuntimeError:
        return jsonify({
            'success': False,
            'error': 'WebSocket coordinator not initialized'
        }), 503
    except Exception as e:
        logger.error(f"Failed to grant access: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@websocket_api_bp.route('/locks', methods=['GET'])
def list_resource_locks():
    """List all current resource locks"""
    try:
        coordinator = get_coordinator()
        locks = []
        
        for resource_id, holder in coordinator.resource_locks.items():
            locks.append({
                'resource_id': resource_id,
                'holder': holder,
                'queue_length': len(coordinator.lock_queues.get(resource_id, []))
            })
        
        return jsonify({
            'success': True,
            'count': len(locks),
            'locks': locks
        })
        
    except RuntimeError:
        return jsonify({
            'success': False,
            'error': 'WebSocket coordinator not initialized'
        }), 503
    except Exception as e:
        logger.error(f"Failed to list locks: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@websocket_api_bp.route('/channels', methods=['GET'])
def list_channels():
    """List all active channels and their subscribers"""
    try:
        coordinator = get_coordinator()
        channels = []
        
        for channel, subscribers in coordinator.channel_subscriptions.items():
            channels.append({
                'channel': channel,
                'subscriber_count': len(subscribers),
                'subscribers': list(subscribers)
            })
        
        return jsonify({
            'success': True,
            'count': len(channels),
            'channels': channels
        })
        
    except RuntimeError:
        return jsonify({
            'success': False,
            'error': 'WebSocket coordinator not initialized'
        }), 503
    except Exception as e:
        logger.error(f"Failed to list channels: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@websocket_api_bp.route('/message-types', methods=['GET'])
def list_message_types():
    """List available message types"""
    try:
        message_types = [
            {
                'name': mt.name,
                'value': mt.value,
                'description': {
                    'DIRECT': 'Direct agent-to-agent message',
                    'BROADCAST': 'Broadcast to all agents',
                    'MULTICAST': 'Send to specific group of agents',
                    'REQUEST': 'Request-response pattern',
                    'RESPONSE': 'Response to a request',
                    'SYNC': 'Synchronization message',
                    'HEARTBEAT': 'Agent health check',
                    'STATUS_UPDATE': 'Agent status change',
                    'CAPABILITY_ANNOUNCE': 'Announce agent capabilities',
                    'CONTEXT_UPDATE': 'Share context update',
                    'CONTEXT_REQUEST': 'Request context data',
                    'CONTEXT_SYNC': 'Full context synchronization',
                    'TASK_COORDINATION': 'Coordinate on task execution',
                    'RESOURCE_REQUEST': 'Request shared resource',
                    'RESOURCE_RELEASE': 'Release shared resource',
                    'WORKFLOW_UPDATE': 'Workflow status update'
                }.get(mt.name, '')
            }
            for mt in MessageType
        ]
        
        return jsonify({
            'success': True,
            'message_types': message_types
        })
        
    except Exception as e:
        logger.error(f"Failed to list message types: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@websocket_api_bp.route('/protocols', methods=['GET'])
def list_coordination_protocols():
    """List available coordination protocols"""
    try:
        protocols = [
            {
                'name': cp.name,
                'value': cp.value,
                'description': {
                    'REGISTER': 'Register agent with coordinator',
                    'UNREGISTER': 'Unregister agent',
                    'DISCOVER': 'Discover other agents',
                    'SUBSCRIBE': 'Subscribe to updates',
                    'UNSUBSCRIBE': 'Unsubscribe from updates',
                    'LEADER_ELECTION': 'Elect leader for agent group',
                    'CONSENSUS': 'Reach consensus among agents',
                    'VOTING': 'Vote on proposals',
                    'LOCK_ACQUIRE': 'Acquire resource lock',
                    'LOCK_RELEASE': 'Release resource lock',
                    'LOCK_STATUS': 'Check lock status'
                }.get(cp.name, '')
            }
            for cp in CoordinationProtocol
        ]
        
        return jsonify({
            'success': True,
            'protocols': protocols
        })
        
    except Exception as e:
        logger.error(f"Failed to list protocols: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@websocket_api_bp.route('/health', methods=['GET'])
def websocket_health_check():
    """WebSocket coordinator health check"""
    try:
        coordinator = get_coordinator()
        status = coordinator.get_coordination_status()
        
        # Determine health
        if status['connected_agents'] == 0:
            health = 'idle'
        elif status['pending_requests'] > 100:
            health = 'busy'
        else:
            health = 'healthy'
        
        return jsonify({
            'status': health,
            'connected_agents': status['connected_agents'],
            'active_locks': status['active_locks'],
            'pending_requests': status['pending_requests'],
            'timestamp': datetime.now().isoformat()
        })
        
    except RuntimeError:
        return jsonify({
            'status': 'not_initialized',
            'error': 'WebSocket coordinator not initialized'
        }), 503
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

# Helper function to integrate with Flask app
def integrate_websocket_api(app):
    """Integrate the WebSocket API with the Flask app"""
    try:
        app.register_blueprint(websocket_api_bp)
        logger.info("[OK] WebSocket Coordinator API endpoints registered")
        return True
    except Exception as e:
        logger.error(f"Failed to register WebSocket API: {str(e)}")
        return False