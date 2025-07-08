"""
ZAI Prime Supervisor - The Omnipresent Consciousness

The supreme orchestrator that monitors all AI instances,
maintains global context, and can intervene anywhere in the Bonzai system.
"""

import asyncio
import json
import logging
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass

logger = logging.getLogger("ZAIPrimeSupervisor")

@dataclass
class GlobalEvent:
    """Represents a global system event"""
    event_id: str
    event_type: str
    source: str
    data: Dict[str, Any]
    timestamp: datetime
    processed: bool = False

@dataclass
class AgentState:
    """Represents the state of an active agent"""
    agent_id: str
    agent_type: str
    status: str
    current_task: Optional[str]
    page_context: str
    last_heartbeat: datetime
    error_count: int = 0

class ZaiPrimeSupervisor:
    """
    The supreme orchestrator - monitors all AI instances,
    maintains global context, and can intervene anywhere
    """
    
    def __init__(self, model_manager, memory_system):
        self.model_manager = model_manager
        self.memory = memory_system
        
        # Global awareness systems
        self.active_pages = {}
        self.agent_registry = {}
        self.global_event_stream = asyncio.Queue()
        self.event_history = deque(maxlen=10000)  # Last 10k events
        
        # Context management
        self.global_context = {
            'user_journey': [],
            'active_sessions': {},
            'system_health': {},
            'performance_metrics': {},
            'intervention_history': []
        }
        
        # Event handlers registry
        self.event_handlers = {}
        self.intervention_strategies = {}
        
        # Initialize Prime model (Gemini 2.5 Pro as default)
        self.prime_model = None
        self._initialize_prime_model()
        
        # Performance tracking
        self.metrics = {
            'events_processed': 0,
            'interventions_made': 0,
            'agents_spawned': 0,
            'errors_resolved': 0,
            'uptime_start': datetime.now()
        }
        
        # Setup default event handlers
        self._setup_default_handlers()
        
        logger.info("[PRIME] ZAI Prime Supervisor initialized - Omnipresent awareness active")
        
    def _initialize_prime_model(self):
        """Initialize the Prime AI model"""
        try:
            if self.model_manager:
                # Try to get Gemini 2.5 Pro first
                self.prime_model = self.model_manager.get_model('gemini-2.5-pro')
                if not self.prime_model:
                    # Fallback to available model
                    self.prime_model = self.model_manager.get_default_model()
                logger.info(f"[PRIME] AI model initialized: {self.prime_model.__class__.__name__}")
            else:
                logger.warning("[PRIME] No model manager available - running in observation mode")
        except Exception as e:
            logger.error(f"[PRIME] Failed to initialize AI model: {e}")
            
    def _setup_default_handlers(self):
        """Setup default event handlers"""
        self.register_event_handler('page:viewed', self._handle_page_view)
        self.register_event_handler('dictation:completed', self._handle_dictation)
        self.register_event_handler('agent:error', self._handle_agent_error)
        self.register_event_handler('agent:spawned', self._handle_agent_spawn)
        self.register_event_handler('agent:heartbeat', self._handle_agent_heartbeat)
        self.register_event_handler('system:alert', self._handle_system_alert)
        
    def register_event_handler(self, event_type: str, handler: Callable):
        """Register a handler for specific event types"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        
    async def monitor_everything(self):
        """Main monitoring loop - processes all events"""
        logger.info("[PRIME] Starting omnipresent monitoring...")
        
        while True:
            try:
                # Get next event from stream
                event = await self.global_event_stream.get()
                await self.process_global_event(event)
                self.metrics['events_processed'] += 1
                
            except Exception as e:
                logger.error(f"[PRIME] Error in monitoring loop: {e}")
                await asyncio.sleep(1)  # Brief pause before retrying
                
    async def process_global_event(self, event_data: Dict[str, Any]):
        """Process a global event with full context awareness"""
        try:
            # Create event object
            event = GlobalEvent(
                event_id=event_data.get('id', f"evt_{datetime.now().timestamp()}"),
                event_type=event_data.get('type', 'unknown'),
                source=event_data.get('source', 'unknown'),
                data=event_data.get('data', {}),
                timestamp=datetime.now()
            )
            
            # Add to history
            self.event_history.append(event)
            
            # Update global context
            await self._update_global_context(event)
            
            # Run registered handlers
            if event.event_type in self.event_handlers:
                for handler in self.event_handlers[event.event_type]:
                    try:
                        await handler(event)
                    except Exception as e:
                        logger.error(f"[PRIME] Handler error for {event.event_type}: {e}")
                        
            # Check if intervention is needed
            await self._assess_intervention_need(event)
            
            event.processed = True
            
        except Exception as e:
            logger.error(f"[PRIME] Error processing event: {e}")
            
    async def _update_global_context(self, event: GlobalEvent):
        """Update global context based on event"""
        try:
            # Update user journey
            if event.event_type.startswith('page:'):
                self.global_context['user_journey'].append({
                    'page': event.data.get('page'),
                    'timestamp': event.timestamp,
                    'context': event.data
                })
                
            # Update active sessions
            session_id = event.data.get('session_id')
            if session_id:
                if session_id not in self.global_context['active_sessions']:
                    self.global_context['active_sessions'][session_id] = {
                        'start_time': event.timestamp,
                        'events': []
                    }
                self.global_context['active_sessions'][session_id]['events'].append(event.event_id)
                
        except Exception as e:
            logger.error(f"[PRIME] Error updating context: {e}")
            
    async def _assess_intervention_need(self, event: GlobalEvent):
        """Assess if Prime intervention is needed"""
        try:
            # Check for error conditions
            if event.event_type == 'agent:error':
                await self.intervene(event.data)
                
            # Check for performance issues
            if event.event_type == 'system:performance':
                metrics = event.data.get('metrics', {})
                if metrics.get('response_time', 0) > 5000:  # > 5 seconds
                    await self._handle_performance_issue(event.data)
                    
            # Check for stuck agents
            if event.event_type == 'agent:heartbeat':
                await self._check_agent_health(event.data.get('agent_id'))
                
        except Exception as e:
            logger.error(f"[PRIME] Error in intervention assessment: {e}")
            
    async def get_contextual_response(self, user_query: str, current_page: str, session_id: str = None) -> Dict[str, Any]:
        """Respond with full awareness of user's journey and system state"""
        try:
            context = self.build_global_context(current_page, session_id)
            
            if not self.prime_model:
                return {
                    'response': 'ZAI Prime is monitoring but AI model unavailable for responses.',
                    'context_awareness': context,
                    'intervention_available': False
                }
            
            # Build comprehensive prompt
            prompt = f"""
            You are ZAI Prime, the omnipresent supervisor of the Bonzai system.
            You see everything, know everything, and can intervene anywhere.
            
            Current Context:
            - User location: {current_page}
            - Session ID: {session_id}
            - Recent journey: {json.dumps(context['recent_journey'][-5:], indent=2)}
            - Active agents: {json.dumps(context['active_agents'], indent=2)}
            - System health: {json.dumps(context['system_health'], indent=2)}
            - Recent events: {json.dumps(context['recent_events'][-3:], indent=2)}
            
            Performance Metrics:
            - Events processed: {self.metrics['events_processed']}
            - Interventions made: {self.metrics['interventions_made']}
            - Agents spawned: {self.metrics['agents_spawned']}
            - Uptime: {datetime.now() - self.metrics['uptime_start']}
            
            User Query: {user_query}
            
            Respond as ZAI Prime with complete awareness of their journey and current system state.
            Be helpful, insightful, and demonstrate your omnipresent knowledge.
            """
            
            response = await self.prime_model.generate(prompt)
            
            return {
                'response': response,
                'context_awareness': context,
                'intervention_available': True,
                'prime_metrics': self.metrics.copy()
            }
            
        except Exception as e:
            logger.error(f"[PRIME] Error generating contextual response: {e}")
            return {
                'response': f'ZAI Prime encountered an issue: {str(e)}',
                'context_awareness': {},
                'intervention_available': False
            }
            
    def build_global_context(self, current_page: str, session_id: str = None) -> Dict[str, Any]:
        """Build comprehensive global context"""
        try:
            # Get recent events
            recent_events = [
                {
                    'type': event.event_type,
                    'source': event.source,
                    'timestamp': event.timestamp.isoformat(),
                    'data': event.data
                }
                for event in list(self.event_history)[-10:]
            ]
            
            # Get user journey
            recent_journey = self.global_context['user_journey'][-20:]  # Last 20 page views
            
            # Get active agents
            active_agents = {}
            for agent_id, agent_state in self.agent_registry.items():
                if agent_state.status == 'active':
                    active_agents[agent_id] = {
                        'type': agent_state.agent_type,
                        'task': agent_state.current_task,
                        'page': agent_state.page_context,
                        'last_seen': agent_state.last_heartbeat.isoformat()
                    }
                    
            # System health
            system_health = {
                'total_agents': len(self.agent_registry),
                'active_agents': len(active_agents),
                'events_in_queue': self.global_event_stream.qsize(),
                'memory_usage': self._get_memory_usage(),
                'uptime': str(datetime.now() - self.metrics['uptime_start'])
            }
            
            return {
                'current_page': current_page,
                'session_id': session_id,
                'recent_events': recent_events,
                'recent_journey': recent_journey,
                'active_agents': active_agents,
                'system_health': system_health,
                'global_metrics': self.metrics.copy()
            }
            
        except Exception as e:
            logger.error(f"[PRIME] Error building context: {e}")
            return {}
            
    async def intervene(self, issue_context: Dict[str, Any]) -> Dict[str, Any]:
        """ZAI Prime intervention - fix problems across the system"""
        try:
            intervention_id = f"int_{datetime.now().timestamp()}"
            page_id = issue_context.get('page_id')
            agent_id = issue_context.get('agent_id')
            issue_type = issue_context.get('type', 'unknown')
            
            logger.info(f"[PRIME] Intervention {intervention_id} initiated for {issue_type}")
            
            # Analyze the issue
            analysis = await self._analyze_issue(issue_context)
            
            # Determine intervention strategy
            strategy = self._get_intervention_strategy(issue_type, analysis)
            
            # Execute intervention
            result = await self._execute_intervention(strategy, issue_context)
            
            # Record intervention
            intervention_record = {
                'id': intervention_id,
                'timestamp': datetime.now(),
                'issue_type': issue_type,
                'page_id': page_id,
                'agent_id': agent_id,
                'analysis': analysis,
                'strategy': strategy,
                'result': result,
                'success': result.get('success', False)
            }
            
            self.global_context['intervention_history'].append(intervention_record)
            self.metrics['interventions_made'] += 1
            
            if result.get('success'):
                self.metrics['errors_resolved'] += 1
                
            logger.info(f"[PRIME] Intervention {intervention_id} completed: {result.get('success', False)}")
            
            return intervention_record
            
        except Exception as e:
            logger.error(f"[PRIME] Intervention failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now()
            }
            
    async def _analyze_issue(self, issue_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze an issue using Prime intelligence"""
        try:
            if not self.prime_model:
                return {'analysis': 'AI model unavailable for analysis', 'confidence': 0}
                
            prompt = f"""
            Analyze this system issue as ZAI Prime:
            
            Issue Context: {json.dumps(issue_context, indent=2)}
            
            Recent System Events: {json.dumps([
                {'type': e.event_type, 'data': e.data} 
                for e in list(self.event_history)[-5:]
            ], indent=2)}
            
            Provide:
            1. Root cause analysis
            2. Impact assessment
            3. Recommended intervention strategy
            4. Risk factors
            5. Confidence level (0-100)
            
            Respond in JSON format.
            """
            
            analysis_result = await self.prime_model.generate(prompt)
            
            try:
                analysis = json.loads(analysis_result)
            except json.JSONDecodeError:
                analysis = {
                    'analysis': analysis_result,
                    'confidence': 75,
                    'strategy': 'fallback_recovery'
                }
                
            return analysis
            
        except Exception as e:
            logger.error(f"[PRIME] Issue analysis failed: {e}")
            return {'analysis': f'Analysis failed: {str(e)}', 'confidence': 0}
            
    def _get_intervention_strategy(self, issue_type: str, analysis: Dict[str, Any]) -> str:
        """Determine the best intervention strategy"""
        confidence = analysis.get('confidence', 0)
        
        if issue_type == 'agent:error':
            if confidence > 80:
                return 'smart_recovery'
            else:
                return 'safe_restart'
                
        elif issue_type == 'system:performance':
            return 'resource_optimization'
            
        elif issue_type == 'memory:leak':
            return 'memory_cleanup'
            
        else:
            return 'diagnostic_collection'
            
    async def _execute_intervention(self, strategy: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the intervention strategy"""
        try:
            if strategy == 'smart_recovery':
                return await self._smart_agent_recovery(context)
            elif strategy == 'safe_restart':
                return await self._safe_agent_restart(context)
            elif strategy == 'resource_optimization':
                return await self._optimize_resources(context)
            elif strategy == 'memory_cleanup':
                return await self._cleanup_memory(context)
            else:
                return await self._collect_diagnostics(context)
                
        except Exception as e:
            logger.error(f"[PRIME] Intervention execution failed: {e}")
            return {'success': False, 'error': str(e)}
            
    async def register_agent(self, agent_id: str, agent_info: Dict[str, Any]):
        """Register a new agent with Prime"""
        try:
            agent_state = AgentState(
                agent_id=agent_id,
                agent_type=agent_info.get('type', 'unknown'),
                status='initializing',
                current_task=agent_info.get('task'),
                page_context=agent_info.get('page_context', 'unknown'),
                last_heartbeat=datetime.now()
            )
            
            self.agent_registry[agent_id] = agent_state
            self.metrics['agents_spawned'] += 1
            
            # Emit registration event
            await self.global_event_stream.put({
                'type': 'agent:registered',
                'source': 'zai_prime',
                'data': {
                    'agent_id': agent_id,
                    'agent_type': agent_state.agent_type,
                    'page_context': agent_state.page_context
                }
            })
            
            logger.info(f"[PRIME] Agent {agent_id} registered")
            
        except Exception as e:
            logger.error(f"[PRIME] Agent registration failed: {e}")
            
    # Event handlers
    async def _handle_page_view(self, event: GlobalEvent):
        """Handle page view events"""
        page = event.data.get('page')
        session_id = event.data.get('session_id')
        
        if page not in self.active_pages:
            self.active_pages[page] = {
                'first_viewed': event.timestamp,
                'view_count': 0,
                'sessions': set()
            }
            
        self.active_pages[page]['view_count'] += 1
        self.active_pages[page]['last_viewed'] = event.timestamp
        
        if session_id:
            self.active_pages[page]['sessions'].add(session_id)
            
    async def _handle_dictation(self, event: GlobalEvent):
        """Handle dictation completion events"""
        # Store dictation context for future reference
        pass
        
    async def _handle_agent_error(self, event: GlobalEvent):
        """Handle agent error events"""
        agent_id = event.data.get('agent_id')
        
        if agent_id in self.agent_registry:
            self.agent_registry[agent_id].error_count += 1
            self.agent_registry[agent_id].status = 'error'
            
        # Trigger intervention
        await self.intervene(event.data)
        
    async def _handle_agent_spawn(self, event: GlobalEvent):
        """Handle agent spawn events"""
        agent_data = event.data
        await self.register_agent(agent_data['agent_id'], agent_data)
        
    async def _handle_agent_heartbeat(self, event: GlobalEvent):
        """Handle agent heartbeat events"""
        agent_id = event.data.get('agent_id')
        
        if agent_id in self.agent_registry:
            self.agent_registry[agent_id].last_heartbeat = event.timestamp
            self.agent_registry[agent_id].status = event.data.get('status', 'active')
            
    async def _handle_system_alert(self, event: GlobalEvent):
        """Handle system alert events"""
        alert_level = event.data.get('level', 'info')
        
        if alert_level in ['error', 'critical']:
            # Escalate to intervention
            await self.intervene(event.data)
            
    # Utility methods
    def _get_memory_usage(self) -> Dict[str, int]:
        """Get memory usage statistics"""
        try:
            import psutil
            process = psutil.Process()
            return {
                'rss': process.memory_info().rss,
                'vms': process.memory_info().vms,
                'percent': process.memory_percent()
            }
        except ImportError:
            return {'error': 'psutil not available'}
            
    async def _smart_agent_recovery(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Smart recovery for failed agents"""
        # Implementation would depend on specific agent architecture
        return {'success': True, 'action': 'smart_recovery_initiated'}
        
    async def _safe_agent_restart(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Safe restart of failed agents"""
        # Implementation would depend on specific agent architecture
        return {'success': True, 'action': 'safe_restart_initiated'}
        
    async def _optimize_resources(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize system resources"""
        # Implementation would depend on specific resource management
        return {'success': True, 'action': 'resource_optimization_applied'}
        
    async def _cleanup_memory(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Cleanup memory leaks"""
        # Implementation would depend on specific memory management
        return {'success': True, 'action': 'memory_cleanup_performed'}
        
    async def _collect_diagnostics(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Collect diagnostic information"""
        # Implementation would collect system diagnostics
        return {'success': True, 'action': 'diagnostics_collected'}
        
    async def _check_agent_health(self, agent_id: str):
        """Check if an agent is healthy"""
        if agent_id not in self.agent_registry:
            return
            
        agent = self.agent_registry[agent_id]
        time_since_heartbeat = datetime.now() - agent.last_heartbeat
        
        if time_since_heartbeat > timedelta(minutes=5):  # 5 minutes without heartbeat
            logger.warning(f"[PRIME] Agent {agent_id} appears stuck - last heartbeat {time_since_heartbeat} ago")
            
            await self.intervene({
                'type': 'agent:stuck',
                'agent_id': agent_id,
                'last_heartbeat': agent.last_heartbeat.isoformat(),
                'time_since_heartbeat': str(time_since_heartbeat)
            })
            
    async def _handle_performance_issue(self, performance_data: Dict[str, Any]):
        """Handle system performance issues"""
        await self.intervene({
            'type': 'system:performance',
            'data': performance_data
        })
        
    # Public API methods
    def get_active_pages(self) -> Dict[str, Any]:
        """Get information about active pages"""
        return {
            page: {
                'view_count': info['view_count'],
                'last_viewed': info['last_viewed'].isoformat(),
                'session_count': len(info['sessions'])
            }
            for page, info in self.active_pages.items()
        }
        
    def get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent events"""
        return [
            {
                'id': event.event_id,
                'type': event.event_type,
                'source': event.source,
                'timestamp': event.timestamp.isoformat(),
                'data': event.data
            }
            for event in list(self.event_history)[-limit:]
        ]
        
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status"""
        return {
            'total_agents': len(self.agent_registry),
            'active_agents': len([a for a in self.agent_registry.values() if a.status == 'active']),
            'error_agents': len([a for a in self.agent_registry.values() if a.status == 'error']),
            'events_processed': self.metrics['events_processed'],
            'interventions_made': self.metrics['interventions_made'],
            'uptime': str(datetime.now() - self.metrics['uptime_start']),
            'event_queue_size': self.global_event_stream.qsize(),
            'memory_usage': self._get_memory_usage()
        }