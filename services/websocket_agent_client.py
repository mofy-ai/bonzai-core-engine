"""
WebSocket Agent Client
Helper library for agents to connect and communicate via WebSocket
"""

import socketio
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from dataclasses import dataclass
import uuid

logger = logging.getLogger(__name__)

@dataclass
class AgentConfig:
    """Agent configuration for WebSocket connection"""
    agent_id: str
    capabilities: List[str]
    metadata: Dict[str, Any] = None
    server_url: str = "http://localhost:5001"
    auto_heartbeat: bool = True
    heartbeat_interval: int = 30

class WebSocketAgentClient:
    """Client for agents to connect to the WebSocket coordinator"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.sio = socketio.Client()
        self.connected = False
        self.session_id = None
        
        # Message handlers
        self.message_handlers = {}
        self.context_handlers = {}
        self.coordination_handlers = {}
        
        # Pending requests
        self.pending_requests = {}
        
        # Setup event handlers
        self._setup_handlers()
        
        logger.info(f"WebSocket client initialized for agent {config.agent_id}")
    
    def _setup_handlers(self):
        """Setup SocketIO event handlers"""
        
        @self.sio.event
        def connect():
            """Handle connection event"""
            logger.info(f"Connected to WebSocket server")
            self.connected = True
            
            # Register agent
            self.sio.emit('agent_connect', {
                'agent_id': self.config.agent_id,
                'session_id': self.sio.sid,
                'capabilities': self.config.capabilities,
                'metadata': self.config.metadata or {}
            })
        
        @self.sio.event
        def connection_confirmed(data):
            """Handle connection confirmation"""
            self.session_id = self.sio.sid
            logger.info(f"Agent {self.config.agent_id} registration confirmed")
            
            # Start heartbeat if enabled
            if self.config.auto_heartbeat:
                asyncio.create_task(self._heartbeat_loop())
        
        @self.sio.event
        def agent_message(data):
            """Handle incoming agent message"""
            try:
                message_type = data.get('type')
                
                # Handle response to our request
                if message_type == 'response':
                    correlation_id = data.get('correlation_id')
                    if correlation_id in self.pending_requests:
                        self.pending_requests[correlation_id]['response'] = data
                        self.pending_requests[correlation_id]['received'] = True
                
                # Call registered handlers
                if message_type in self.message_handlers:
                    for handler in self.message_handlers[message_type]:
                        try:
                            handler(data)
                        except Exception as e:
                            logger.error(f"Message handler error: {str(e)}")
                            
            except Exception as e:
                logger.error(f"Error handling message: {str(e)}")
        
        @self.sio.event
        def context_changed(data):
            """Handle context change notification"""
            context_id = data.get('context_id')
            if context_id in self.context_handlers:
                for handler in self.context_handlers[context_id]:
                    try:
                        handler(data)
                    except Exception as e:
                        logger.error(f"Context handler error: {str(e)}")
        
        @self.sio.event
        def channel_message(data):
            """Handle channel broadcast"""
            channel = data.get('channel')
            logger.info(f"Received message on channel {channel}")
        
        @self.sio.event
        def consensus_request(data):
            """Handle consensus request"""
            if 'consensus' in self.coordination_handlers:
                for handler in self.coordination_handlers['consensus']:
                    try:
                        result = handler(data)
                        # Send vote
                        self.sio.emit('consensus_vote', {
                            'consensus_id': data['consensus_id'],
                            'vote': result,
                            'agent_id': self.config.agent_id
                        })
                    except Exception as e:
                        logger.error(f"Consensus handler error: {str(e)}")
        
        @self.sio.event
        def lock_granted(data):
            """Handle lock granted notification"""
            if 'lock_granted' in self.coordination_handlers:
                for handler in self.coordination_handlers['lock_granted']:
                    handler(data)
        
        @self.sio.event
        def lock_queued(data):
            """Handle lock queued notification"""
            logger.info(f"Lock queued: position {data['position']} for resource {data['resource_id']}")
        
        @self.sio.event
        def error(data):
            """Handle error messages"""
            logger.error(f"WebSocket error: {data.get('message', 'Unknown error')}")
        
        @self.sio.event
        def disconnect():
            """Handle disconnection"""
            logger.warning(f"Disconnected from WebSocket server")
            self.connected = False
    
    def connect(self):
        """Connect to the WebSocket server"""
        try:
            self.sio.connect(self.config.server_url)
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from the WebSocket server"""
        if self.connected:
            self.sio.disconnect()
    
    def send_message(self, recipient_id: str, message_type: str, payload: Dict[str, Any],
                    priority: int = 5, ttl: Optional[int] = None) -> str:
        """Send a message to another agent"""
        if not self.connected:
            raise RuntimeError("Not connected to WebSocket server")
        
        message_data = {
            'type': message_type,
            'recipient_id': recipient_id,
            'payload': payload,
            'priority': priority
        }
        
        if ttl:
            message_data['ttl'] = ttl
        
        self.sio.emit('agent_message', message_data)
        return str(uuid.uuid4())  # Return a message ID
    
    def broadcast(self, message_type: str, payload: Dict[str, Any]):
        """Broadcast a message to all agents"""
        if not self.connected:
            raise RuntimeError("Not connected to WebSocket server")
        
        self.sio.emit('agent_message', {
            'type': message_type,
            'payload': payload
        })
    
    def multicast(self, recipients: List[str], message_type: str, payload: Dict[str, Any]):
        """Send a message to multiple specific agents"""
        if not self.connected:
            raise RuntimeError("Not connected to WebSocket server")
        
        payload['recipients'] = recipients
        
        self.sio.emit('agent_message', {
            'type': 'multicast',
            'payload': payload
        })
    
    async def request(self, recipient_id: str, payload: Dict[str, Any], 
                     timeout: int = 30) -> Optional[Dict[str, Any]]:
        """Send a request and wait for response"""
        if not self.connected:
            raise RuntimeError("Not connected to WebSocket server")
        
        correlation_id = str(uuid.uuid4())
        
        # Track pending request
        self.pending_requests[correlation_id] = {
            'sent_at': datetime.now(),
            'received': False,
            'response': None
        }
        
        # Send request
        self.sio.emit('agent_message', {
            'type': 'request',
            'recipient_id': recipient_id,
            'payload': payload,
            'correlation_id': correlation_id,
            'ttl': timeout
        })
        
        # Wait for response
        start_time = datetime.now()
        while not self.pending_requests[correlation_id]['received']:
            if (datetime.now() - start_time).total_seconds() > timeout:
                del self.pending_requests[correlation_id]
                return None
            await asyncio.sleep(0.1)
        
        response = self.pending_requests[correlation_id]['response']
        del self.pending_requests[correlation_id]
        return response
    
    def update_context(self, context_id: str, data: Dict[str, Any]):
        """Update shared context"""
        if not self.connected:
            raise RuntimeError("Not connected to WebSocket server")
        
        self.sio.emit('context_update', {
            'context_id': context_id,
            'data': data
        })
    
    def subscribe_channel(self, channel: str):
        """Subscribe to a channel"""
        if not self.connected:
            raise RuntimeError("Not connected to WebSocket server")
        
        self.sio.emit('subscribe', {
            'type': 'channel',
            'target': channel
        })
    
    def subscribe_context(self, context_id: str):
        """Subscribe to context updates"""
        if not self.connected:
            raise RuntimeError("Not connected to WebSocket server")
        
        self.sio.emit('subscribe', {
            'type': 'context',
            'target': context_id
        })
    
    def request_lock(self, resource_id: str, timeout: int = 30):
        """Request a resource lock"""
        if not self.connected:
            raise RuntimeError("Not connected to WebSocket server")
        
        self.sio.emit('coordination_request', {
            'protocol': 'lock_acquire',
            'resource_id': resource_id,
            'timeout': timeout
        })
    
    def release_lock(self, resource_id: str):
        """Release a resource lock"""
        if not self.connected:
            raise RuntimeError("Not connected to WebSocket server")
        
        self.sio.emit('coordination_request', {
            'protocol': 'lock_release',
            'resource_id': resource_id
        })
    
    def initiate_consensus(self, proposal: Dict[str, Any], participants: List[str]):
        """Initiate consensus protocol"""
        if not self.connected:
            raise RuntimeError("Not connected to WebSocket server")
        
        self.sio.emit('coordination_request', {
            'protocol': 'consensus',
            'proposal': proposal,
            'participants': participants
        })
    
    def register_message_handler(self, message_type: str, handler: Callable):
        """Register a handler for specific message type"""
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        self.message_handlers[message_type].append(handler)
    
    def register_context_handler(self, context_id: str, handler: Callable):
        """Register a handler for context updates"""
        if context_id not in self.context_handlers:
            self.context_handlers[context_id] = []
        self.context_handlers[context_id].append(handler)
    
    def register_coordination_handler(self, event: str, handler: Callable):
        """Register a handler for coordination events"""
        if event not in self.coordination_handlers:
            self.coordination_handlers[event] = []
        self.coordination_handlers[event].append(handler)
    
    async def _heartbeat_loop(self):
        """Send periodic heartbeats"""
        while self.connected:
            try:
                self.sio.emit('agent_message', {
                    'type': 'heartbeat',
                    'payload': {
                        'timestamp': datetime.now().isoformat(),
                        'status': 'active'
                    }
                })
                await asyncio.sleep(self.config.heartbeat_interval)
            except Exception as e:
                logger.error(f"Heartbeat error: {str(e)}")
                await asyncio.sleep(self.config.heartbeat_interval)


# Example usage
class ExampleAgent:
    """Example agent implementation"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.config = AgentConfig(
            agent_id=agent_id,
            capabilities=['data_processing', 'report_generation'],
            metadata={'version': '1.0', 'team': 'research'}
        )
        self.client = WebSocketAgentClient(self.config)
        
        # Register handlers
        self.client.register_message_handler('task_assignment', self.handle_task)
        self.client.register_message_handler('data_request', self.handle_data_request)
        self.client.register_coordination_handler('consensus', self.handle_consensus)
    
    def connect(self):
        """Connect to coordinator"""
        if self.client.connect():
            logger.info(f"Agent {self.agent_id} connected successfully")
            
            # Subscribe to relevant channels
            self.client.subscribe_channel('research_tasks')
            self.client.subscribe_context('global_research_context')
            
            return True
        return False
    
    def handle_task(self, message: Dict[str, Any]):
        """Handle task assignment"""
        task = message['payload']
        logger.info(f"Received task: {task.get('description', 'Unknown')}")
        
        # Process task...
        result = {'status': 'completed', 'data': 'Task result'}
        
        # Send response if it's a request
        if message.get('correlation_id'):
            self.client.send_message(
                recipient_id=message['sender_id'],
                message_type='response',
                payload=result
            )
    
    def handle_data_request(self, message: Dict[str, Any]):
        """Handle data request from another agent"""
        request = message['payload']
        logger.info(f"Data requested: {request.get('type', 'Unknown')}")
        
        # Provide data...
        data = {'result': 'Requested data'}
        
        self.client.send_message(
            recipient_id=message['sender_id'],
            message_type='data_response',
            payload=data
        )
    
    def handle_consensus(self, data: Dict[str, Any]) -> bool:
        """Handle consensus request"""
        proposal = data['proposal']
        logger.info(f"Consensus requested for: {proposal}")
        
        # Make decision
        return True  # Agree with proposal
    
    async def collaborate_on_task(self, partner_id: str, task_data: Dict[str, Any]):
        """Example of agent collaboration"""
        # Request lock on shared resource
        resource_id = f"task_{task_data['id']}"
        self.client.request_lock(resource_id)
        
        # Update shared context
        self.client.update_context('task_progress', {
            'task_id': task_data['id'],
            'status': 'processing',
            'agent': self.agent_id
        })
        
        # Request data from partner
        response = await self.client.request(
            recipient_id=partner_id,
            payload={'type': 'data_request', 'task_id': task_data['id']},
            timeout=60
        )
        
        if response:
            logger.info(f"Received data from {partner_id}")
            # Process with partner data...
        
        # Release lock
        self.client.release_lock(resource_id)


# Helper function to create agent client
def create_agent_client(agent_id: str, capabilities: List[str], 
                       server_url: str = "http://localhost:5001") -> WebSocketAgentClient:
    """Create a WebSocket agent client"""
    config = AgentConfig(
        agent_id=agent_id,
        capabilities=capabilities,
        server_url=server_url
    )
    return WebSocketAgentClient(config)