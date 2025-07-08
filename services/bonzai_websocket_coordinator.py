"""
Bonzai WebSocket Coordinator Service
Enables real-time agent-to-agent communication, shared context, and coordination
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict
import weakref

from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from mem0 import MemoryClient

# Import agent registry for service discovery
from .bonzai_agent_registry import get_registry

logger = logging.getLogger(__name__)

class MessageType(Enum):
    # Core messaging types
    DIRECT = "direct"              # Direct agent-to-agent message
    BROADCAST = "broadcast"        # Broadcast to all agents
    MULTICAST = "multicast"        # Send to specific group of agents
    REQUEST = "request"            # Request-response pattern
    RESPONSE = "response"          # Response to a request
    
    # Coordination types
    SYNC = "sync"                  # Synchronization message
    HEARTBEAT = "heartbeat"        # Agent health check
    STATUS_UPDATE = "status"       # Agent status change
    CAPABILITY_ANNOUNCE = "capability"  # Announce agent capabilities
    
    # Context sharing types
    CONTEXT_UPDATE = "context_update"    # Share context update
    CONTEXT_REQUEST = "context_request"  # Request context data
    CONTEXT_SYNC = "context_sync"        # Full context synchronization
    
    # Collaboration types
    TASK_COORDINATION = "task_coord"     # Coordinate on task execution
    RESOURCE_REQUEST = "resource_req"    # Request shared resource
    RESOURCE_RELEASE = "resource_rel"    # Release shared resource
    WORKFLOW_UPDATE = "workflow"         # Workflow status update

class CoordinationProtocol(Enum):
    # Agent discovery and registration
    REGISTER = "register"
    UNREGISTER = "unregister"
    DISCOVER = "discover"
    
    # Subscription management
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    
    # Coordination patterns
    LEADER_ELECTION = "leader_election"
    CONSENSUS = "consensus"
    VOTING = "voting"
    
    # Resource management
    LOCK_ACQUIRE = "lock_acquire"
    LOCK_RELEASE = "lock_release"
    LOCK_STATUS = "lock_status"

@dataclass
class AgentConnection:
    """Represents a connected agent"""
    agent_id: str
    session_id: str
    connected_at: datetime
    capabilities: List[str] = field(default_factory=list)
    status: str = "active"
    metadata: Dict[str, Any] = field(default_factory=dict)
    subscriptions: Set[str] = field(default_factory=set)
    last_heartbeat: Optional[datetime] = None

@dataclass
class Message:
    """WebSocket message structure"""
    id: str
    type: MessageType
    sender_id: str
    recipient_id: Optional[str]  # None for broadcast
    payload: Dict[str, Any]
    timestamp: datetime
    correlation_id: Optional[str] = None  # For request-response
    ttl: Optional[int] = None  # Time to live in seconds
    priority: int = 5  # 1-10, lower is higher priority

@dataclass
class SharedContext:
    """Shared context data structure"""
    context_id: str
    owner_id: str
    data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    access_list: List[str] = field(default_factory=list)  # Agent IDs with access
    version: int = 1
    locked_by: Optional[str] = None

class BonzaiWebSocketCoordinator:
    """Main WebSocket coordination service"""
    
    def __init__(self, socketio: SocketIO, mem0_api_key: Optional[str] = None):
        self.socketio = socketio
        self.registry = get_registry()
        
        # Connection tracking
        self.connections: Dict[str, AgentConnection] = {}
        self.session_to_agent: Dict[str, str] = {}  # session_id -> agent_id
        
        # Message handling
        self.message_handlers: Dict[MessageType, List[Callable]] = defaultdict(list)
        self.pending_requests: Dict[str, Dict[str, Any]] = {}  # correlation_id -> request info
        
        # Shared context management
        self.shared_contexts: Dict[str, SharedContext] = {}
        self.context_subscriptions: Dict[str, Set[str]] = defaultdict(set)  # context_id -> agent_ids
        
        # Resource coordination
        self.resource_locks: Dict[str, str] = {}  # resource_id -> agent_id
        self.lock_queues: Dict[str, List[str]] = defaultdict(list)  # resource_id -> waiting agents
        
        # Channel subscriptions
        self.channel_subscriptions: Dict[str, Set[str]] = defaultdict(set)  # channel -> agent_ids
        
        # Memory integration
        self.mem0_client = None
        if mem0_api_key:
            try:
                self.mem0_client = MemoryClient(api_key=mem0_api_key)
                logger.info("[OK] Mem0 integration initialized for context sharing")
            except Exception as e:
                logger.warning(f"[WARNING] Mem0 integration failed: {str(e)}")
        
        # Initialize WebSocket handlers
        self._setup_handlers()
        
        # Start background tasks
        asyncio.create_task(self._heartbeat_monitor())
        asyncio.create_task(self._message_expiry_handler())
        
        logger.info("[OK] Bonzai WebSocket Coordinator initialized")
    
    def _setup_handlers(self):
        """Setup WebSocket event handlers"""
        
        @self.socketio.on('agent_connect')
        def handle_agent_connect(data):
            """Handle agent connection"""
            try:
                agent_id = data.get('agent_id')
                session_id = data.get('session_id', request.sid)
                capabilities = data.get('capabilities', [])
                
                # Create agent connection
                connection = AgentConnection(
                    agent_id=agent_id,
                    session_id=session_id,
                    connected_at=datetime.now(),
                    capabilities=capabilities,
                    metadata=data.get('metadata', {})
                )
                
                self.connections[agent_id] = connection
                self.session_to_agent[session_id] = agent_id
                
                # Join agent's private room
                join_room(f"agent:{agent_id}")
                
                # Join capability rooms
                for capability in capabilities:
                    join_room(f"capability:{capability}")
                
                # Announce connection
                self._broadcast_agent_status(agent_id, "connected")
                
                emit('connection_confirmed', {
                    'agent_id': agent_id,
                    'timestamp': datetime.now().isoformat()
                })
                
                logger.info(f"[OK] Agent {agent_id} connected")
                
            except Exception as e:
                logger.error(f"[ERROR] Agent connection failed: {str(e)}")
                emit('error', {'message': str(e)})
        
        @self.socketio.on('agent_message')
        def handle_agent_message(data):
            """Handle agent-to-agent message"""
            try:
                session_id = request.sid
                sender_id = self.session_to_agent.get(session_id)
                
                if not sender_id:
                    emit('error', {'message': 'Agent not registered'})
                    return
                
                # Create message
                message = Message(
                    id=str(uuid.uuid4()),
                    type=MessageType(data.get('type', 'direct')),
                    sender_id=sender_id,
                    recipient_id=data.get('recipient_id'),
                    payload=data.get('payload', {}),
                    timestamp=datetime.now(),
                    correlation_id=data.get('correlation_id'),
                    ttl=data.get('ttl'),
                    priority=data.get('priority', 5)
                )
                
                # Route message
                self._route_message(message)
                
                # Acknowledge
                emit('message_sent', {
                    'message_id': message.id,
                    'timestamp': message.timestamp.isoformat()
                })
                
            except Exception as e:
                logger.error(f"[ERROR] Message handling failed: {str(e)}")
                emit('error', {'message': str(e)})
        
        @self.socketio.on('context_update')
        def handle_context_update(data):
            """Handle shared context update"""
            try:
                session_id = request.sid
                agent_id = self.session_to_agent.get(session_id)
                
                if not agent_id:
                    emit('error', {'message': 'Agent not registered'})
                    return
                
                context_id = data.get('context_id')
                context_data = data.get('data', {})
                
                # Update or create context
                self._update_shared_context(agent_id, context_id, context_data)
                
                # Store in Mem0 if available
                if self.mem0_client:
                    self._store_context_in_memory(context_id, context_data, agent_id)
                
                # Notify subscribers
                self._notify_context_subscribers(context_id, agent_id)
                
                emit('context_updated', {
                    'context_id': context_id,
                    'version': self.shared_contexts[context_id].version
                })
                
            except Exception as e:
                logger.error(f"[ERROR] Context update failed: {str(e)}")
                emit('error', {'message': str(e)})
        
        @self.socketio.on('subscribe')
        def handle_subscribe(data):
            """Handle subscription requests"""
            try:
                session_id = request.sid
                agent_id = self.session_to_agent.get(session_id)
                
                if not agent_id:
                    emit('error', {'message': 'Agent not registered'})
                    return
                
                subscription_type = data.get('type')  # 'channel', 'context', 'capability'
                target = data.get('target')
                
                if subscription_type == 'channel':
                    self.channel_subscriptions[target].add(agent_id)
                    join_room(f"channel:{target}")
                elif subscription_type == 'context':
                    self.context_subscriptions[target].add(agent_id)
                elif subscription_type == 'capability':
                    join_room(f"capability:{target}")
                
                # Update agent subscriptions
                if agent_id in self.connections:
                    self.connections[agent_id].subscriptions.add(f"{subscription_type}:{target}")
                
                emit('subscribed', {
                    'type': subscription_type,
                    'target': target
                })
                
            except Exception as e:
                logger.error(f"[ERROR] Subscription failed: {str(e)}")
                emit('error', {'message': str(e)})
        
        @self.socketio.on('coordination_request')
        def handle_coordination_request(data):
            """Handle coordination protocol requests"""
            try:
                session_id = request.sid
                agent_id = self.session_to_agent.get(session_id)
                
                if not agent_id:
                    emit('error', {'message': 'Agent not registered'})
                    return
                
                protocol = CoordinationProtocol(data.get('protocol'))
                
                if protocol == CoordinationProtocol.LOCK_ACQUIRE:
                    resource_id = data.get('resource_id')
                    timeout = data.get('timeout', 30)
                    self._handle_lock_request(agent_id, resource_id, timeout)
                    
                elif protocol == CoordinationProtocol.LOCK_RELEASE:
                    resource_id = data.get('resource_id')
                    self._handle_lock_release(agent_id, resource_id)
                    
                elif protocol == CoordinationProtocol.LEADER_ELECTION:
                    group = data.get('group')
                    self._handle_leader_election(agent_id, group)
                    
                elif protocol == CoordinationProtocol.CONSENSUS:
                    proposal = data.get('proposal')
                    participants = data.get('participants', [])
                    self._handle_consensus_request(agent_id, proposal, participants)
                
            except Exception as e:
                logger.error(f"[ERROR] Coordination request failed: {str(e)}")
                emit('error', {'message': str(e)})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle agent disconnection"""
            try:
                session_id = request.sid
                agent_id = self.session_to_agent.get(session_id)
                
                if agent_id:
                    # Clean up connections
                    self.connections.pop(agent_id, None)
                    self.session_to_agent.pop(session_id, None)
                    
                    # Release any held locks
                    self._release_all_locks(agent_id)
                    
                    # Remove from subscriptions
                    self._remove_from_subscriptions(agent_id)
                    
                    # Leave all rooms
                    for room in rooms():
                        leave_room(room)
                    
                    # Announce disconnection
                    self._broadcast_agent_status(agent_id, "disconnected")
                    
                    logger.info(f"[OK] Agent {agent_id} disconnected")
                    
            except Exception as e:
                logger.error(f"[ERROR] Disconnect handling failed: {str(e)}")
    
    def _route_message(self, message: Message):
        """Route message to appropriate recipient(s)"""
        try:
            # Store message if it expects a response
            if message.type == MessageType.REQUEST:
                self.pending_requests[message.correlation_id or message.id] = {
                    'message': message,
                    'timestamp': datetime.now()
                }
            
            # Route based on message type
            if message.type == MessageType.DIRECT and message.recipient_id:
                # Direct message to specific agent
                self.socketio.emit('agent_message', asdict(message), 
                                 room=f"agent:{message.recipient_id}")
                
            elif message.type == MessageType.BROADCAST:
                # Broadcast to all connected agents
                for agent_id in self.connections:
                    if agent_id != message.sender_id:
                        self.socketio.emit('agent_message', asdict(message),
                                         room=f"agent:{agent_id}")
                        
            elif message.type == MessageType.MULTICAST:
                # Send to specific group
                recipients = message.payload.get('recipients', [])
                for recipient_id in recipients:
                    if recipient_id in self.connections:
                        self.socketio.emit('agent_message', asdict(message),
                                         room=f"agent:{recipient_id}")
            
            # Handle special message types
            if message.type in self.message_handlers:
                for handler in self.message_handlers[message.type]:
                    handler(message)
                    
        except Exception as e:
            logger.error(f"[ERROR] Message routing failed: {str(e)}")
    
    def _update_shared_context(self, agent_id: str, context_id: str, data: Dict[str, Any]):
        """Update or create shared context"""
        if context_id in self.shared_contexts:
            context = self.shared_contexts[context_id]
            
            # Check if agent has access
            if agent_id != context.owner_id and agent_id not in context.access_list:
                raise PermissionError(f"Agent {agent_id} does not have access to context {context_id}")
            
            # Check if context is locked
            if context.locked_by and context.locked_by != agent_id:
                raise RuntimeError(f"Context {context_id} is locked by {context.locked_by}")
            
            # Update context
            context.data.update(data)
            context.updated_at = datetime.now()
            context.version += 1
        else:
            # Create new context
            self.shared_contexts[context_id] = SharedContext(
                context_id=context_id,
                owner_id=agent_id,
                data=data,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                access_list=[agent_id]
            )
    
    def _store_context_in_memory(self, context_id: str, data: Dict[str, Any], agent_id: str):
        """Store context in Mem0 for persistence"""
        if not self.mem0_client:
            return
        
        try:
            # Store as memory with metadata
            self.mem0_client.add(
                messages=[{
                    "role": "system",
                    "content": f"Shared context {context_id}: {json.dumps(data)}"
                }],
                user_id=f"agent_{agent_id}",
                metadata={
                    "type": "shared_context",
                    "context_id": context_id,
                    "timestamp": datetime.now().isoformat()
                }
            )
        except Exception as e:
            logger.warning(f"[WARNING] Failed to store context in Mem0: {str(e)}")
    
    def _notify_context_subscribers(self, context_id: str, updater_id: str):
        """Notify all subscribers of context update"""
        subscribers = self.context_subscriptions.get(context_id, set())
        
        context = self.shared_contexts.get(context_id)
        if not context:
            return
        
        update_message = {
            'type': 'context_update',
            'context_id': context_id,
            'updater_id': updater_id,
            'version': context.version,
            'timestamp': context.updated_at.isoformat()
        }
        
        for subscriber_id in subscribers:
            if subscriber_id != updater_id and subscriber_id in self.connections:
                self.socketio.emit('context_changed', update_message,
                                 room=f"agent:{subscriber_id}")
    
    def _handle_lock_request(self, agent_id: str, resource_id: str, timeout: int):
        """Handle resource lock request"""
        current_holder = self.resource_locks.get(resource_id)
        
        if not current_holder:
            # Grant lock immediately
            self.resource_locks[resource_id] = agent_id
            self.socketio.emit('lock_granted', {
                'resource_id': resource_id,
                'holder': agent_id,
                'timestamp': datetime.now().isoformat()
            }, room=f"agent:{agent_id}")
            
            logger.info(f"[OK] Lock granted to {agent_id} for resource {resource_id}")
            
        elif current_holder == agent_id:
            # Agent already holds the lock
            self.socketio.emit('lock_already_held', {
                'resource_id': resource_id
            }, room=f"agent:{agent_id}")
            
        else:
            # Add to queue
            if agent_id not in self.lock_queues[resource_id]:
                self.lock_queues[resource_id].append(agent_id)
                
            position = self.lock_queues[resource_id].index(agent_id) + 1
            
            self.socketio.emit('lock_queued', {
                'resource_id': resource_id,
                'position': position,
                'current_holder': current_holder
            }, room=f"agent:{agent_id}")
            
            # Schedule timeout
            asyncio.create_task(self._lock_timeout_handler(agent_id, resource_id, timeout))
    
    def _handle_lock_release(self, agent_id: str, resource_id: str):
        """Handle resource lock release"""
        current_holder = self.resource_locks.get(resource_id)
        
        if current_holder != agent_id:
            self.socketio.emit('error', {
                'message': f"Agent {agent_id} does not hold lock for {resource_id}"
            }, room=f"agent:{agent_id}")
            return
        
        # Release lock
        del self.resource_locks[resource_id]
        
        self.socketio.emit('lock_released', {
            'resource_id': resource_id
        }, room=f"agent:{agent_id}")
        
        # Grant to next in queue
        if resource_id in self.lock_queues and self.lock_queues[resource_id]:
            next_agent = self.lock_queues[resource_id].pop(0)
            if next_agent in self.connections:
                self._handle_lock_request(next_agent, resource_id, 30)
    
    def _handle_leader_election(self, initiator_id: str, group: str):
        """Handle leader election for a group of agents"""
        # Get all agents in the group
        group_agents = []
        for agent_id, connection in self.connections.items():
            if group in connection.metadata.get('groups', []):
                group_agents.append(agent_id)
        
        if not group_agents:
            return
        
        # Simple election: agent with lowest ID wins
        leader = min(group_agents)
        
        # Announce election result
        election_result = {
            'group': group,
            'leader': leader,
            'participants': group_agents,
            'timestamp': datetime.now().isoformat()
        }
        
        for agent_id in group_agents:
            self.socketio.emit('leader_elected', election_result,
                             room=f"agent:{agent_id}")
        
        logger.info(f"[OK] Leader election completed for group {group}: {leader}")
    
    def _handle_consensus_request(self, initiator_id: str, proposal: Dict[str, Any], 
                                participants: List[str]):
        """Handle consensus protocol"""
        consensus_id = str(uuid.uuid4())
        
        # Send proposal to all participants
        consensus_request = {
            'consensus_id': consensus_id,
            'initiator': initiator_id,
            'proposal': proposal,
            'participants': participants,
            'timestamp': datetime.now().isoformat()
        }
        
        for participant_id in participants:
            if participant_id in self.connections:
                self.socketio.emit('consensus_request', consensus_request,
                                 room=f"agent:{participant_id}")
        
        # Track consensus state
        asyncio.create_task(self._track_consensus(consensus_id, initiator_id, 
                                                 participants, proposal))
    
    async def _track_consensus(self, consensus_id: str, initiator_id: str,
                              participants: List[str], proposal: Dict[str, Any]):
        """Track consensus voting"""
        votes = {}
        timeout = 30  # seconds
        
        # Wait for votes
        start_time = datetime.now()
        while len(votes) < len(participants):
            if (datetime.now() - start_time).total_seconds() > timeout:
                break
            await asyncio.sleep(0.1)
        
        # Calculate result
        agree_count = sum(1 for v in votes.values() if v)
        consensus_reached = agree_count > len(participants) / 2
        
        # Announce result
        result = {
            'consensus_id': consensus_id,
            'reached': consensus_reached,
            'votes': votes,
            'agree_count': agree_count,
            'total_participants': len(participants)
        }
        
        for participant_id in participants + [initiator_id]:
            if participant_id in self.connections:
                self.socketio.emit('consensus_result', result,
                                 room=f"agent:{participant_id}")
    
    def _broadcast_agent_status(self, agent_id: str, status: str):
        """Broadcast agent status change"""
        status_update = {
            'agent_id': agent_id,
            'status': status,
            'timestamp': datetime.now().isoformat()
        }
        
        # Broadcast to all agents
        self.socketio.emit('agent_status_change', status_update)
    
    def _release_all_locks(self, agent_id: str):
        """Release all locks held by an agent"""
        released_resources = []
        
        for resource_id, holder in list(self.resource_locks.items()):
            if holder == agent_id:
                self._handle_lock_release(agent_id, resource_id)
                released_resources.append(resource_id)
        
        if released_resources:
            logger.info(f"[OK] Released {len(released_resources)} locks for {agent_id}")
    
    def _remove_from_subscriptions(self, agent_id: str):
        """Remove agent from all subscriptions"""
        # Remove from channel subscriptions
        for channel, subscribers in self.channel_subscriptions.items():
            subscribers.discard(agent_id)
        
        # Remove from context subscriptions
        for context_id, subscribers in self.context_subscriptions.items():
            subscribers.discard(agent_id)
        
        # Remove from lock queues
        for queue in self.lock_queues.values():
            if agent_id in queue:
                queue.remove(agent_id)
    
    async def _heartbeat_monitor(self):
        """Monitor agent heartbeats"""
        while True:
            try:
                current_time = datetime.now()
                timeout_threshold = 60  # seconds
                
                for agent_id, connection in list(self.connections.items()):
                    last_heartbeat = connection.last_heartbeat or connection.connected_at
                    
                    if (current_time - last_heartbeat).total_seconds() > timeout_threshold:
                        # Agent timeout - disconnect
                        logger.warning(f"[WARNING] Agent {agent_id} timed out")
                        self._handle_agent_timeout(agent_id)
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"[ERROR] Heartbeat monitor error: {str(e)}")
                await asyncio.sleep(30)
    
    async def _message_expiry_handler(self):
        """Handle message TTL expiry"""
        while True:
            try:
                current_time = datetime.now()
                
                # Check pending requests for timeout
                for correlation_id, request_info in list(self.pending_requests.items()):
                    message = request_info['message']
                    timestamp = request_info['timestamp']
                    
                    if message.ttl:
                        if (current_time - timestamp).total_seconds() > message.ttl:
                            # Request timeout
                            self._handle_request_timeout(correlation_id, message)
                            del self.pending_requests[correlation_id]
                
                await asyncio.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logger.error(f"[ERROR] Message expiry handler error: {str(e)}")
                await asyncio.sleep(5)
    
    def _handle_agent_timeout(self, agent_id: str):
        """Handle agent timeout"""
        if agent_id in self.connections:
            session_id = self.connections[agent_id].session_id
            self.connections.pop(agent_id, None)
            self.session_to_agent.pop(session_id, None)
            
            # Clean up resources
            self._release_all_locks(agent_id)
            self._remove_from_subscriptions(agent_id)
            
            # Notify others
            self._broadcast_agent_status(agent_id, "timeout")
    
    def _handle_request_timeout(self, correlation_id: str, message: Message):
        """Handle request timeout"""
        # Notify sender
        if message.sender_id in self.connections:
            self.socketio.emit('request_timeout', {
                'correlation_id': correlation_id,
                'original_message': asdict(message)
            }, room=f"agent:{message.sender_id}")
    
    async def _lock_timeout_handler(self, agent_id: str, resource_id: str, timeout: int):
        """Handle lock request timeout"""
        await asyncio.sleep(timeout)
        
        # Check if still waiting
        if resource_id in self.lock_queues and agent_id in self.lock_queues[resource_id]:
            self.lock_queues[resource_id].remove(agent_id)
            
            if agent_id in self.connections:
                self.socketio.emit('lock_timeout', {
                    'resource_id': resource_id
                }, room=f"agent:{agent_id}")
    
    # Public API methods
    
    def register_message_handler(self, message_type: MessageType, handler: Callable):
        """Register a handler for specific message type"""
        self.message_handlers[message_type].append(handler)
    
    def send_message_to_agent(self, sender_id: str, recipient_id: str, 
                            message_type: MessageType, payload: Dict[str, Any]) -> str:
        """Send a message from one agent to another"""
        message = Message(
            id=str(uuid.uuid4()),
            type=message_type,
            sender_id=sender_id,
            recipient_id=recipient_id,
            payload=payload,
            timestamp=datetime.now()
        )
        
        self._route_message(message)
        return message.id
    
    def broadcast_to_channel(self, channel: str, message: Dict[str, Any]):
        """Broadcast message to all subscribers of a channel"""
        self.socketio.emit('channel_message', {
            'channel': channel,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }, room=f"channel:{channel}")
    
    def get_shared_context(self, context_id: str, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get shared context data"""
        context = self.shared_contexts.get(context_id)
        
        if not context:
            # Try to load from Mem0
            if self.mem0_client:
                try:
                    memories = self.mem0_client.search(
                        query=f"context_id:{context_id}",
                        user_id=f"agent_{agent_id}",
                        limit=1
                    )
                    if memories:
                        return memories[0].get('data')
                except Exception as e:
                    logger.warning(f"[WARNING] Failed to load context from Mem0: {str(e)}")
            return None
        
        # Check access
        if agent_id != context.owner_id and agent_id not in context.access_list:
            raise PermissionError(f"Agent {agent_id} does not have access to context {context_id}")
        
        return context.data
    
    def grant_context_access(self, context_id: str, owner_id: str, grantee_id: str):
        """Grant access to shared context"""
        context = self.shared_contexts.get(context_id)
        
        if not context:
            raise ValueError(f"Context {context_id} not found")
        
        if context.owner_id != owner_id:
            raise PermissionError(f"Only owner can grant access")
        
        if grantee_id not in context.access_list:
            context.access_list.append(grantee_id)
    
    def get_connected_agents(self) -> List[Dict[str, Any]]:
        """Get list of all connected agents"""
        return [
            {
                'agent_id': conn.agent_id,
                'status': conn.status,
                'capabilities': conn.capabilities,
                'connected_at': conn.connected_at.isoformat(),
                'subscriptions': list(conn.subscriptions)
            }
            for conn in self.connections.values()
        ]
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific agent"""
        connection = self.connections.get(agent_id)
        
        if not connection:
            return None
        
        return {
            'agent_id': agent_id,
            'status': connection.status,
            'connected_at': connection.connected_at.isoformat(),
            'last_heartbeat': connection.last_heartbeat.isoformat() if connection.last_heartbeat else None,
            'capabilities': connection.capabilities,
            'subscriptions': list(connection.subscriptions),
            'metadata': connection.metadata
        }
    
    def get_coordination_status(self) -> Dict[str, Any]:
        """Get overall coordination status"""
        return {
            'connected_agents': len(self.connections),
            'active_locks': len(self.resource_locks),
            'pending_requests': len(self.pending_requests),
            'shared_contexts': len(self.shared_contexts),
            'channels': {
                channel: len(subscribers) 
                for channel, subscribers in self.channel_subscriptions.items()
            },
            'lock_queues': {
                resource: len(queue)
                for resource, queue in self.lock_queues.items()
                if queue
            }
        }

# Global coordinator instance (initialized by app)
websocket_coordinator = None

def initialize_websocket_coordinator(socketio: SocketIO, mem0_api_key: Optional[str] = None):
    """Initialize the global WebSocket coordinator"""
    global websocket_coordinator
    websocket_coordinator = BonzaiWebSocketCoordinator(socketio, mem0_api_key)
    return websocket_coordinator

def get_coordinator():
    """Get the global WebSocket coordinator instance"""
    if not websocket_coordinator:
        raise RuntimeError("WebSocket coordinator not initialized")
    return websocket_coordinator