"""
Agent Spawning Service - Dynamic Agent Creation

Manages creation and lifecycle of 8000+ dynamic agent instances
on demand based on system needs and user interactions.
"""

import asyncio
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Type
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger("AgentSpawningService")

class AgentType(Enum):
    """Available agent types"""
    GENERAL = "general"
    SPECIALIST = "specialist"
    RESEARCHER = "researcher"
    CODER = "coder"
    DESIGNER = "designer"
    QA = "qa"
    MONITOR = "monitor"
    OPTIMIZER = "optimizer"
    SECURITY = "security"
    ANALYTICS = "analytics"

class AgentStatus(Enum):
    """Agent lifecycle status"""
    INITIALIZING = "initializing"
    ACTIVE = "active"
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    TERMINATED = "terminated"

@dataclass
class AgentInstance:
    """Represents a spawned agent instance"""
    agent_id: str
    agent_type: AgentType
    purpose: str
    page_context: str
    status: AgentStatus = AgentStatus.INITIALIZING
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    task_count: int = 0
    error_count: int = 0
    config: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)

class AgentSpawningService:
    """Manages creation of 8000+ dynamic agent instances"""
    
    def __init__(self, zai_prime, model_manager):
        self.zai_prime = zai_prime
        self.model_manager = model_manager
        self.agent_pool = {}
        self.agent_templates = {}
        self.spawn_queue = asyncio.Queue()
        
        # Configuration
        self.max_agents = 8000
        self.max_idle_time = timedelta(minutes=30)
        self.cleanup_interval = timedelta(minutes=5)
        
        # Statistics
        self.stats = {
            'total_spawned': 0,
            'active_agents': 0,
            'terminated_agents': 0,
            'spawn_requests': 0,
            'spawn_failures': 0,
            'cleanup_runs': 0
        }
        
        # Setup agent templates
        self._setup_agent_templates()
        
        # Start background tasks
        asyncio.create_task(self._spawn_worker())
        asyncio.create_task(self._cleanup_worker())
        
        logger.info(f"[SPAWNER] Agent Spawning Service initialized - Ready for {self.max_agents} agents")
        
    def _setup_agent_templates(self):
        """Setup agent templates for different types"""
        self.agent_templates = {
            AgentType.GENERAL: {
                'capabilities': ['general_assistance', 'task_routing', 'context_awareness'],
                'model_preference': 'gemini-2.0-flash',
                'max_tasks': 100,
                'idle_timeout': 30
            },
            AgentType.SPECIALIST: {
                'capabilities': ['deep_analysis', 'specialized_knowledge', 'expert_advice'],
                'model_preference': 'gemini-2.5-pro',
                'max_tasks': 50,
                'idle_timeout': 60
            },
            AgentType.RESEARCHER: {
                'capabilities': ['web_search', 'data_analysis', 'report_generation'],
                'model_preference': 'gemini-2.5-pro',
                'max_tasks': 25,
                'idle_timeout': 45
            },
            AgentType.CODER: {
                'capabilities': ['code_generation', 'debugging', 'optimization'],
                'model_preference': 'gemini-2.5-pro',
                'max_tasks': 30,
                'idle_timeout': 45
            },
            AgentType.DESIGNER: {
                'capabilities': ['ui_design', 'visual_analysis', 'creative_assistance'],
                'model_preference': 'gemini-2.0-flash',
                'max_tasks': 20,
                'idle_timeout': 60
            },
            AgentType.QA: {
                'capabilities': ['testing', 'quality_assurance', 'validation'],
                'model_preference': 'gemini-2.0-flash',
                'max_tasks': 40,
                'idle_timeout': 30
            },
            AgentType.MONITOR: {
                'capabilities': ['system_monitoring', 'health_checks', 'alerting'],
                'model_preference': 'gemini-2.0-flash',
                'max_tasks': 1000,
                'idle_timeout': 5
            },
            AgentType.OPTIMIZER: {
                'capabilities': ['performance_optimization', 'resource_management'],
                'model_preference': 'gemini-2.5-pro',
                'max_tasks': 10,
                'idle_timeout': 120
            },
            AgentType.SECURITY: {
                'capabilities': ['security_analysis', 'threat_detection', 'compliance'],
                'model_preference': 'gemini-2.5-pro',
                'max_tasks': 15,
                'idle_timeout': 90
            },
            AgentType.ANALYTICS: {
                'capabilities': ['data_analysis', 'metrics_collection', 'insights'],
                'model_preference': 'gemini-2.5-pro',
                'max_tasks': 20,
                'idle_timeout': 60
            }
        }
        
    async def spawn_agent(self, agent_type: str, purpose: str, page_context: str, 
                         config: Optional[Dict[str, Any]] = None) -> str:
        """Spawn a new agent and return its ID"""
        try:
            # Validate agent type
            try:
                agent_type_enum = AgentType(agent_type)
            except ValueError:
                agent_type_enum = AgentType.GENERAL
                logger.warning(f"[SPAWNER] Unknown agent type '{agent_type}', using GENERAL")
                
            # Check agent limit
            if len(self.agent_pool) >= self.max_agents:
                # Try to cleanup idle agents first
                cleaned = await self._cleanup_idle_agents()
                if len(self.agent_pool) >= self.max_agents:
                    raise RuntimeError(f"Agent limit reached ({self.max_agents}). Cleaned {cleaned} idle agents.")
                    
            # Generate unique agent ID
            agent_id = f"{agent_type_enum.value}_{uuid.uuid4().hex[:8]}"
            
            # Create agent instance
            agent_config = config or {}
            template = self.agent_templates.get(agent_type_enum, {})
            agent_config.update(template)
            
            agent = AgentInstance(
                agent_id=agent_id,
                agent_type=agent_type_enum,
                purpose=purpose,
                page_context=page_context,
                config=agent_config
            )
            
            # Add to spawn queue for processing
            await self.spawn_queue.put(agent)
            self.stats['spawn_requests'] += 1
            
            logger.info(f"[SPAWNER] Agent spawn queued: {agent_id} ({agent_type}) for {purpose}")
            
            return agent_id
            
        except Exception as e:
            self.stats['spawn_failures'] += 1
            logger.error(f"[SPAWNER] Failed to spawn agent: {e}")
            raise
            
    async def _spawn_worker(self):
        """Background worker to process spawn queue"""
        while True:
            try:
                # Get next agent to spawn
                agent = await self.spawn_queue.get()
                
                # Initialize the agent
                success = await self._initialize_agent(agent)
                
                if success:
                    # Add to agent pool
                    self.agent_pool[agent.agent_id] = agent
                    self.stats['total_spawned'] += 1
                    self.stats['active_agents'] += 1
                    
                    # Register with ZAI Prime
                    await self.zai_prime.register_agent(agent.agent_id, {
                        'type': agent.agent_type.value,
                        'purpose': agent.purpose,
                        'page_context': agent.page_context,
                        'config': agent.config
                    })
                    
                    # Notify about successful spawn
                    await self._notify_agent_spawned(agent)
                    
                    logger.info(f"[SPAWNER] Agent spawned successfully: {agent.agent_id}")
                    
                else:
                    self.stats['spawn_failures'] += 1
                    logger.error(f"[SPAWNER] Failed to initialize agent: {agent.agent_id}")
                    
            except Exception as e:
                logger.error(f"[SPAWNER] Error in spawn worker: {e}")
                await asyncio.sleep(1)
                
    async def _initialize_agent(self, agent: AgentInstance) -> bool:
        """Initialize an agent instance"""
        try:
            # Set up agent's AI model
            model_preference = agent.config.get('model_preference', 'gemini-2.0-flash')
            agent.config['model'] = self.model_manager.get_model(model_preference)
            
            # Initialize agent metrics
            agent.metrics = {
                'tasks_completed': 0,
                'average_response_time': 0,
                'success_rate': 100,
                'last_performance_check': datetime.now()
            }
            
            # Set agent status to active
            agent.status = AgentStatus.ACTIVE
            agent.last_activity = datetime.now()
            
            # Send initial heartbeat to ZAI Prime
            await self._send_heartbeat(agent)
            
            return True
            
        except Exception as e:
            logger.error(f"[SPAWNER] Agent initialization failed for {agent.agent_id}: {e}")
            agent.status = AgentStatus.ERROR
            agent.error_count += 1
            return False
            
    async def _notify_agent_spawned(self, agent: AgentInstance):
        """Notify system about agent spawn"""
        await self.zai_prime.global_event_stream.put({
            'type': 'agent:spawned',
            'source': 'agent_spawning_service',
            'data': {
                'agent_id': agent.agent_id,
                'agent_type': agent.agent_type.value,
                'purpose': agent.purpose,
                'page_context': agent.page_context,
                'capabilities': agent.config.get('capabilities', [])
            }
        })
        
    async def _send_heartbeat(self, agent: AgentInstance):
        """Send agent heartbeat to ZAI Prime"""
        await self.zai_prime.global_event_stream.put({
            'type': 'agent:heartbeat',
            'source': 'agent_spawning_service',
            'data': {
                'agent_id': agent.agent_id,
                'status': agent.status.value,
                'task_count': agent.task_count,
                'error_count': agent.error_count,
                'last_activity': agent.last_activity.isoformat(),
                'metrics': agent.metrics
            }
        })
        
    async def terminate_agent(self, agent_id: str, reason: str = "manual_termination") -> bool:
        """Terminate a specific agent"""
        try:
            if agent_id not in self.agent_pool:
                logger.warning(f"[SPAWNER] Agent {agent_id} not found for termination")
                return False
                
            agent = self.agent_pool[agent_id]
            
            # Update agent status
            agent.status = AgentStatus.TERMINATED
            
            # Notify ZAI Prime
            await self.zai_prime.global_event_stream.put({
                'type': 'agent:terminated',
                'source': 'agent_spawning_service',
                'data': {
                    'agent_id': agent_id,
                    'reason': reason,
                    'lifetime': str(datetime.now() - agent.created_at),
                    'final_metrics': agent.metrics
                }
            })
            
            # Remove from pool
            del self.agent_pool[agent_id]
            self.stats['active_agents'] -= 1
            self.stats['terminated_agents'] += 1
            
            logger.info(f"[SPAWNER] Agent terminated: {agent_id} ({reason})")
            
            return True
            
        except Exception as e:
            logger.error(f"[SPAWNER] Failed to terminate agent {agent_id}: {e}")
            return False
            
    async def _cleanup_worker(self):
        """Background worker for agent cleanup"""
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval.total_seconds())
                await self._cleanup_idle_agents()
                self.stats['cleanup_runs'] += 1
                
            except Exception as e:
                logger.error(f"[SPAWNER] Error in cleanup worker: {e}")
                
    async def _cleanup_idle_agents(self) -> int:
        """Cleanup idle agents that have exceeded timeout"""
        cleaned_count = 0
        current_time = datetime.now()
        
        agents_to_remove = []
        
        for agent_id, agent in self.agent_pool.items():
            # Check if agent is idle and past timeout
            idle_time = current_time - agent.last_activity
            max_idle = timedelta(minutes=agent.config.get('idle_timeout', 30))
            
            if (agent.status == AgentStatus.IDLE and idle_time > max_idle) or \
               (agent.status == AgentStatus.ERROR and agent.error_count > 5):
                agents_to_remove.append(agent_id)
                
        # Remove idle agents
        for agent_id in agents_to_remove:
            reason = "idle_timeout" if self.agent_pool[agent_id].status == AgentStatus.IDLE else "error_threshold"
            await self.terminate_agent(agent_id, reason)
            cleaned_count += 1
            
        if cleaned_count > 0:
            logger.info(f"[SPAWNER] Cleaned up {cleaned_count} idle/error agents")
            
        return cleaned_count
        
    async def update_agent_activity(self, agent_id: str, task_info: Optional[Dict[str, Any]] = None):
        """Update agent activity timestamp and task info"""
        if agent_id in self.agent_pool:
            agent = self.agent_pool[agent_id]
            agent.last_activity = datetime.now()
            agent.task_count += 1
            
            if task_info:
                agent.metrics.update(task_info)
                
            # Send heartbeat
            await self._send_heartbeat(agent)
            
    async def set_agent_status(self, agent_id: str, status: str):
        """Set agent status"""
        if agent_id in self.agent_pool:
            try:
                status_enum = AgentStatus(status)
                self.agent_pool[agent_id].status = status_enum
                await self._send_heartbeat(self.agent_pool[agent_id])
            except ValueError:
                logger.warning(f"[SPAWNER] Invalid agent status: {status}")
                
    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific agent"""
        if agent_id not in self.agent_pool:
            return None
            
        agent = self.agent_pool[agent_id]
        return {
            'agent_id': agent.agent_id,
            'agent_type': agent.agent_type.value,
            'purpose': agent.purpose,
            'page_context': agent.page_context,
            'status': agent.status.value,
            'created_at': agent.created_at.isoformat(),
            'last_activity': agent.last_activity.isoformat(),
            'task_count': agent.task_count,
            'error_count': agent.error_count,
            'capabilities': agent.config.get('capabilities', []),
            'metrics': agent.metrics
        }
        
    def get_agents_by_type(self, agent_type: str) -> List[Dict[str, Any]]:
        """Get all agents of a specific type"""
        try:
            type_enum = AgentType(agent_type)
            return [
                self.get_agent_info(agent_id)
                for agent_id, agent in self.agent_pool.items()
                if agent.agent_type == type_enum
            ]
        except ValueError:
            return []
            
    def get_agents_by_page(self, page_context: str) -> List[Dict[str, Any]]:
        """Get all agents for a specific page context"""
        return [
            self.get_agent_info(agent_id)
            for agent_id, agent in self.agent_pool.items()
            if agent.page_context == page_context
        ]
        
    def get_spawning_stats(self) -> Dict[str, Any]:
        """Get spawning service statistics"""
        active_by_type = {}
        for agent in self.agent_pool.values():
            agent_type = agent.agent_type.value
            if agent_type not in active_by_type:
                active_by_type[agent_type] = 0
            active_by_type[agent_type] += 1
            
        return {
            'total_spawned': self.stats['total_spawned'],
            'active_agents': len(self.agent_pool),
            'terminated_agents': self.stats['terminated_agents'],
            'spawn_requests': self.stats['spawn_requests'],
            'spawn_failures': self.stats['spawn_failures'],
            'cleanup_runs': self.stats['cleanup_runs'],
            'queue_size': self.spawn_queue.qsize(),
            'max_agents': self.max_agents,
            'capacity_used': len(self.agent_pool) / self.max_agents * 100,
            'active_by_type': active_by_type,
            'supported_types': [t.value for t in AgentType]
        }
        
    async def handle_agent_error(self, agent_id: str, error_info: Dict[str, Any]):
        """Handle agent error"""
        if agent_id in self.agent_pool:
            agent = self.agent_pool[agent_id]
            agent.error_count += 1
            agent.status = AgentStatus.ERROR
            
            # Notify ZAI Prime about the error
            await self.zai_prime.global_event_stream.put({
                'type': 'agent:error',
                'source': 'agent_spawning_service',
                'data': {
                    'agent_id': agent_id,
                    'error_info': error_info,
                    'error_count': agent.error_count,
                    'agent_type': agent.agent_type.value
                }
            })
            
            # If too many errors, terminate the agent
            if agent.error_count > 5:
                await self.terminate_agent(agent_id, "error_threshold_exceeded")
                
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Get information about all active agents"""
        return [
            self.get_agent_info(agent_id)
            for agent_id in self.agent_pool.keys()
        ]