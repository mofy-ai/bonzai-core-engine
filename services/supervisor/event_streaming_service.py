"""
Event Streaming Service - Real-time Event Pipeline

Handles bidirectional event streaming between frontend and ZAI Prime,
enabling real-time synchronization and global event distribution.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Callable, Optional
from flask_socketio import SocketIO, emit

logger = logging.getLogger("EventStreamingService")

class EventStreamingService:
    """Handles real-time bidirectional event streaming"""
    
    def __init__(self, socketio: SocketIO, zai_prime):
        self.socketio = socketio
        self.zai_prime = zai_prime
        self.connected_clients = {}
        self.event_subscriptions = {}
        self.broadcast_filters = {}
        
        # Event statistics
        self.stats = {
            'events_received': 0,
            'events_broadcasted': 0,
            'clients_connected': 0,
            'start_time': datetime.now()
        }
        
        self.setup_handlers()
        logger.info("[STREAMING] Event Streaming Service initialized")
        
    def setup_handlers(self):
        """Setup WebSocket event handlers"""
        
        @self.socketio.on('event:global')
        def handle_global_event(data):
            """Receive events from frontend event bus"""
            try:
                # Validate event data
                if not self._validate_event(data):
                    logger.warning(f"[STREAMING] Invalid event received: {data}")
                    return
                    
                # Add metadata
                enriched_event = self._enrich_event(data)
                
                # Send to ZAI Prime for processing
                asyncio.create_task(self.zai_prime.global_event_stream.put(enriched_event))
                
                # Echo to all connected clients for synchronization
                emit('event:broadcast', enriched_event, broadcast=True)
                
                self.stats['events_received'] += 1
                self.stats['events_broadcasted'] += 1
                
                logger.debug(f"[STREAMING] Global event processed: {enriched_event.get('type')}")
                
            except Exception as e:
                logger.error(f"[STREAMING] Error handling global event: {e}")
                emit('event:error', {'error': str(e), 'event': data})
                
        @self.socketio.on('zai:prime:query')
        def handle_prime_query(data):
            """Direct queries to ZAI Prime"""
            try:
                query = data.get('query', '')
                current_page = data.get('current_page', 'unknown')
                session_id = data.get('session_id')
                
                if not query:
                    emit('zai:prime:response', {'error': 'Query is required'})
                    return
                    
                # Process query asynchronously
                asyncio.create_task(self._process_prime_query(query, current_page, session_id))
                
                logger.info(f"[STREAMING] Prime query received: {query[:50]}...")
                
            except Exception as e:
                logger.error(f"[STREAMING] Error handling Prime query: {e}")
                emit('zai:prime:response', {'error': str(e)})
                
        @self.socketio.on('event:subscribe')
        def handle_event_subscription(data):
            """Subscribe to specific event types"""
            try:
                client_id = self._get_client_id()
                event_types = data.get('event_types', [])
                
                if client_id not in self.event_subscriptions:
                    self.event_subscriptions[client_id] = set()
                    
                for event_type in event_types:
                    self.event_subscriptions[client_id].add(event_type)
                    
                emit('event:subscription:confirmed', {
                    'subscribed_to': list(self.event_subscriptions[client_id])
                })
                
                logger.info(f"[STREAMING] Client {client_id} subscribed to: {event_types}")
                
            except Exception as e:
                logger.error(f"[STREAMING] Error handling subscription: {e}")
                emit('event:subscription:error', {'error': str(e)})
                
        @self.socketio.on('agent:spawn:request')
        def handle_agent_spawn_request(data):
            """Handle agent spawning requests"""
            try:
                agent_type = data.get('agent_type', 'general')
                purpose = data.get('purpose', 'unknown')
                page_context = data.get('page_context', 'unknown')
                
                # Forward to agent spawning service if available
                if hasattr(self.zai_prime, 'agent_spawner'):
                    asyncio.create_task(self._spawn_agent(agent_type, purpose, page_context))
                else:
                    emit('agent:spawn:response', {
                        'success': False,
                        'error': 'Agent spawning service not available'
                    })
                    
            except Exception as e:
                logger.error(f"[STREAMING] Error handling agent spawn request: {e}")
                emit('agent:spawn:response', {'success': False, 'error': str(e)})
                
        @self.socketio.on('system:health:request')
        def handle_health_request():
            """Handle system health requests"""
            try:
                health_data = self.zai_prime.get_system_health()
                streaming_stats = self.get_streaming_stats()
                
                emit('system:health:response', {
                    'system_health': health_data,
                    'streaming_stats': streaming_stats,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"[STREAMING] Error handling health request: {e}")
                emit('system:health:response', {'error': str(e)})
                
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection"""
            try:
                client_id = self._get_client_id()
                self.connected_clients[client_id] = {
                    'connected_at': datetime.now(),
                    'last_activity': datetime.now(),
                    'events_sent': 0,
                    'subscriptions': set()
                }
                
                self.stats['clients_connected'] += 1
                
                emit('connection_established', {
                    'status': 'connected',
                    'client_id': client_id,
                    'zai_prime_ready': True,
                    'streaming_enabled': True,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Notify ZAI Prime of new connection
                asyncio.create_task(self.zai_prime.global_event_stream.put({
                    'type': 'client:connected',
                    'source': 'event_streaming',
                    'data': {'client_id': client_id}
                }))
                
                logger.info(f"[STREAMING] Client {client_id} connected")
                
            except Exception as e:
                logger.error(f"[STREAMING] Error handling connection: {e}")
                
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection"""
            try:
                client_id = self._get_client_id()
                
                if client_id in self.connected_clients:
                    del self.connected_clients[client_id]
                    
                if client_id in self.event_subscriptions:
                    del self.event_subscriptions[client_id]
                    
                # Notify ZAI Prime of disconnection
                asyncio.create_task(self.zai_prime.global_event_stream.put({
                    'type': 'client:disconnected',
                    'source': 'event_streaming',
                    'data': {'client_id': client_id}
                }))
                
                logger.info(f"[STREAMING] Client {client_id} disconnected")
                
            except Exception as e:
                logger.error(f"[STREAMING] Error handling disconnection: {e}")
                
    def _validate_event(self, event_data: Dict[str, Any]) -> bool:
        """Validate incoming event data"""
        required_fields = ['type', 'source']
        
        if not isinstance(event_data, dict):
            return False
            
        for field in required_fields:
            if field not in event_data:
                return False
                
        # Validate event type format
        event_type = event_data.get('type', '')
        if not isinstance(event_type, str) or ':' not in event_type:
            return False
            
        return True
        
    def _enrich_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich event with metadata"""
        enriched = event_data.copy()
        enriched.update({
            'id': f"evt_{datetime.now().timestamp()}",
            'timestamp': datetime.now().isoformat(),
            'client_id': self._get_client_id(),
            'processed_by': 'event_streaming_service'
        })
        
        # Add session information if available
        if 'session_id' not in enriched:
            enriched['session_id'] = self._get_session_id()
            
        return enriched
        
    def _get_client_id(self) -> str:
        """Get current client ID"""
        try:
            from flask import request
            return f"client_{request.sid}"
        except:
            return f"client_{datetime.now().timestamp()}"
            
    def _get_session_id(self) -> str:
        """Get current session ID"""
        try:
            from flask import session
            return session.get('session_id', f"session_{datetime.now().timestamp()}")
        except:
            return f"session_{datetime.now().timestamp()}"
            
    async def _process_prime_query(self, query: str, current_page: str, session_id: str):
        """Process query to ZAI Prime asynchronously"""
        try:
            response = await self.zai_prime.get_contextual_response(
                query, current_page, session_id
            )
            
            # Emit response back to client
            self.socketio.emit('zai:prime:response', response)
            
        except Exception as e:
            logger.error(f"[STREAMING] Error processing Prime query: {e}")
            self.socketio.emit('zai:prime:response', {'error': str(e)})
            
    async def _spawn_agent(self, agent_type: str, purpose: str, page_context: str):
        """Spawn a new agent"""
        try:
            if hasattr(self.zai_prime, 'agent_spawner'):
                agent_id = await self.zai_prime.agent_spawner.spawn_agent(
                    agent_type, purpose, page_context
                )
                
                self.socketio.emit('agent:spawn:response', {
                    'success': True,
                    'agent_id': agent_id,
                    'agent_type': agent_type,
                    'purpose': purpose
                })
            else:
                self.socketio.emit('agent:spawn:response', {
                    'success': False,
                    'error': 'Agent spawning service not available'
                })
                
        except Exception as e:
            logger.error(f"[STREAMING] Error spawning agent: {e}")
            self.socketio.emit('agent:spawn:response', {
                'success': False,
                'error': str(e)
            })
            
    def broadcast_event(self, event_type: str, data: Dict[str, Any], 
                       target_clients: Optional[List[str]] = None):
        """Broadcast event to specific clients or all clients"""
        try:
            event_data = {
                'type': event_type,
                'data': data,
                'timestamp': datetime.now().isoformat(),
                'source': 'zai_prime'
            }
            
            if target_clients:
                # Send to specific clients
                for client_id in target_clients:
                    if client_id in self.connected_clients:
                        self.socketio.emit('event:broadcast', event_data, 
                                         room=client_id)
            else:
                # Broadcast to all clients, respecting subscriptions
                for client_id, client_info in self.connected_clients.items():
                    if self._should_send_to_client(client_id, event_type):
                        self.socketio.emit('event:broadcast', event_data, 
                                         room=client_id)
                        
            self.stats['events_broadcasted'] += 1
            
        except Exception as e:
            logger.error(f"[STREAMING] Error broadcasting event: {e}")
            
    def _should_send_to_client(self, client_id: str, event_type: str) -> bool:
        """Check if event should be sent to specific client"""
        # If no subscriptions, send all events
        if client_id not in self.event_subscriptions:
            return True
            
        # Check if client is subscribed to this event type
        subscriptions = self.event_subscriptions[client_id]
        
        # Exact match
        if event_type in subscriptions:
            return True
            
        # Wildcard match (e.g., 'agent:*' matches 'agent:spawn')
        for subscription in subscriptions:
            if subscription.endswith('*'):
                prefix = subscription[:-1]
                if event_type.startswith(prefix):
                    return True
                    
        return False
        
    def notify_prime_event(self, event_type: str, data: Dict[str, Any]):
        """Notify all clients of a ZAI Prime event"""
        self.broadcast_event(f'zai:prime:{event_type}', data)
        
    def get_streaming_stats(self) -> Dict[str, Any]:
        """Get streaming service statistics"""
        uptime = datetime.now() - self.stats['start_time']
        
        return {
            'events_received': self.stats['events_received'],
            'events_broadcasted': self.stats['events_broadcasted'],
            'clients_connected': len(self.connected_clients),
            'total_connections': self.stats['clients_connected'],
            'active_subscriptions': len(self.event_subscriptions),
            'uptime': str(uptime),
            'events_per_minute': self.stats['events_received'] / max(uptime.total_seconds() / 60, 1)
        }
        
    def get_connected_clients(self) -> Dict[str, Any]:
        """Get information about connected clients"""
        return {
            client_id: {
                'connected_at': info['connected_at'].isoformat(),
                'last_activity': info['last_activity'].isoformat(),
                'events_sent': info['events_sent'],
                'subscriptions': list(info['subscriptions'])
            }
            for client_id, info in self.connected_clients.items()
        }
        
    # Integration methods for ZAI Prime
    def setup_prime_notifications(self):
        """Setup notifications from ZAI Prime to clients"""
        # This would be called by ZAI Prime to register for notifications
        pass
        
    async def send_prime_awareness_update(self, context: Dict[str, Any]):
        """Send awareness update from ZAI Prime"""
        self.notify_prime_event('awareness_update', context)
        
    async def send_intervention_notification(self, intervention_data: Dict[str, Any]):
        """Send intervention notification"""
        self.notify_prime_event('intervention', intervention_data)
        
    async def send_agent_status_update(self, agent_data: Dict[str, Any]):
        """Send agent status update"""
        self.broadcast_event('agent:status:update', agent_data)
        
    async def send_system_alert(self, alert_data: Dict[str, Any]):
        """Send system alert to all clients"""
        self.broadcast_event('system:alert', alert_data)