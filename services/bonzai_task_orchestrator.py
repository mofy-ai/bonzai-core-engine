"""
Bonzai Task Orchestrator Service
Routes tasks to appropriate agents, manages queues, and aggregates responses
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict, deque
import heapq
from concurrent.futures import ThreadPoolExecutor
import threading

# Import agent registry for service discovery
from .bonzai_agent_registry import get_registry, AgentCapability

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING = "pending"
    QUEUED = "queued"
    ASSIGNED = "assigned"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"

class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5

class ExecutionStrategy(Enum):
    SINGLE = "single"           # Route to single best agent
    PARALLEL = "parallel"       # Execute on multiple agents in parallel
    SEQUENTIAL = "sequential"   # Execute on agents in sequence
    CONSENSUS = "consensus"     # Get consensus from multiple agents
    FALLBACK = "fallback"      # Try agents until one succeeds

@dataclass
class TaskRequest:
    """Represents an incoming task request"""
    id: str
    type: str
    description: str
    requirements: List[str]
    priority: TaskPriority
    payload: Dict[str, Any]
    strategy: ExecutionStrategy
    timeout: int  # seconds
    created_at: datetime
    user_id: Optional[str] = None
    callback_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TaskAssignment:
    """Represents a task assignment to an agent"""
    task_id: str
    agent_id: str
    assigned_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: TaskStatus = TaskStatus.ASSIGNED
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@dataclass 
class TaskResult:
    """Aggregated result from task execution"""
    task_id: str
    status: TaskStatus
    assignments: List[TaskAssignment]
    aggregated_result: Optional[Dict[str, Any]]
    execution_time: float
    created_at: datetime
    completed_at: Optional[datetime]
    metadata: Dict[str, Any]

class TaskQueue:
    """Priority queue for tasks"""
    
    def __init__(self):
        self._queue = []
        self._task_map = {}
        self._lock = threading.Lock()
        self._counter = 0
        
    def push(self, task: TaskRequest):
        """Add task to queue with priority"""
        with self._lock:
            # Use counter to break ties and maintain FIFO for same priority
            self._counter += 1
            entry = (task.priority.value, self._counter, task.id, task)
            heapq.heappush(self._queue, entry)
            self._task_map[task.id] = task
            
    def pop(self) -> Optional[TaskRequest]:
        """Get highest priority task"""
        with self._lock:
            while self._queue:
                priority, counter, task_id, task = heapq.heappop(self._queue)
                if task_id in self._task_map:
                    del self._task_map[task_id]
                    return task
            return None
            
    def remove(self, task_id: str) -> bool:
        """Remove specific task from queue"""
        with self._lock:
            if task_id in self._task_map:
                del self._task_map[task_id]
                return True
            return False
            
    def size(self) -> int:
        """Get queue size"""
        with self._lock:
            return len(self._task_map)
            
    def get_tasks(self) -> List[TaskRequest]:
        """Get all tasks in queue"""
        with self._lock:
            return list(self._task_map.values())

class BonzaiTaskOrchestrator:
    """Main task orchestration service"""
    
    def __init__(self, max_workers: int = 10):
        self.registry = get_registry()
        self.task_queue = TaskQueue()
        self.active_tasks: Dict[str, TaskRequest] = {}
        self.task_results: Dict[str, TaskResult] = {}
        self.task_assignments: Dict[str, List[TaskAssignment]] = defaultdict(list)
        
        # Worker pool for concurrent execution
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.max_workers = max_workers
        
        # Performance tracking
        self.metrics = {
            "tasks_received": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "tasks_timeout": 0,
            "average_execution_time": 0,
            "queue_size": 0,
            "active_tasks": 0
        }
        
        # Agent performance tracking
        self.agent_performance: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "tasks_assigned": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "average_response_time": 0,
            "success_rate": 1.0
        })
        
        # Start background workers
        self._running = True
        self._start_workers()
        
        logger.info("[OK] Bonzai Task Orchestrator initialized with %d workers", max_workers)
    
    def _start_workers(self):
        """Start background worker tasks"""
        # Task processor
        asyncio.create_task(self._process_queue())
        
        # Timeout monitor
        asyncio.create_task(self._monitor_timeouts())
        
        # Metrics updater
        asyncio.create_task(self._update_metrics())
    
    async def submit_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a new task for orchestration"""
        try:
            # Create task request
            task = TaskRequest(
                id=str(uuid.uuid4()),
                type=task_data.get("type", "general"),
                description=task_data.get("description", ""),
                requirements=task_data.get("requirements", []),
                priority=TaskPriority[task_data.get("priority", "NORMAL").upper()],
                payload=task_data.get("payload", {}),
                strategy=ExecutionStrategy[task_data.get("strategy", "SINGLE").upper()],
                timeout=task_data.get("timeout", 300),  # 5 min default
                created_at=datetime.now(),
                user_id=task_data.get("user_id"),
                callback_url=task_data.get("callback_url"),
                metadata=task_data.get("metadata", {})
            )
            
            # Add to queue
            self.task_queue.push(task)
            self.metrics["tasks_received"] += 1
            
            # Initialize result tracking
            self.task_results[task.id] = TaskResult(
                task_id=task.id,
                status=TaskStatus.QUEUED,
                assignments=[],
                aggregated_result=None,
                execution_time=0,
                created_at=task.created_at,
                completed_at=None,
                metadata={}
            )
            
            logger.info(f"[OK] Task {task.id} submitted: {task.description[:50]}...")
            
            return {
                "success": True,
                "task_id": task.id,
                "status": TaskStatus.QUEUED.value,
                "priority": task.priority.value,
                "estimated_wait": self._estimate_wait_time(task.priority)
            }
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to submit task: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _process_queue(self):
        """Background task to process queued tasks"""
        while self._running:
            try:
                # Check if we have capacity
                if len(self.active_tasks) < self.max_workers:
                    task = self.task_queue.pop()
                    if task:
                        self.active_tasks[task.id] = task
                        self.task_results[task.id].status = TaskStatus.PROCESSING
                        
                        # Process task asynchronously
                        asyncio.create_task(self._execute_task(task))
                
                await asyncio.sleep(0.1)  # Small delay to prevent busy waiting
                
            except Exception as e:
                logger.error(f"[ERROR] Queue processing error: {str(e)}")
                await asyncio.sleep(1)
    
    async def _execute_task(self, task: TaskRequest):
        """Execute a task based on its strategy"""
        start_time = datetime.now()
        
        try:
            # Find suitable agents
            agents = self._find_suitable_agents(task)
            
            if not agents:
                raise Exception("No suitable agents found for task requirements")
            
            # Execute based on strategy
            if task.strategy == ExecutionStrategy.SINGLE:
                result = await self._execute_single(task, agents[0])
            elif task.strategy == ExecutionStrategy.PARALLEL:
                result = await self._execute_parallel(task, agents)
            elif task.strategy == ExecutionStrategy.SEQUENTIAL:
                result = await self._execute_sequential(task, agents)
            elif task.strategy == ExecutionStrategy.CONSENSUS:
                result = await self._execute_consensus(task, agents)
            elif task.strategy == ExecutionStrategy.FALLBACK:
                result = await self._execute_fallback(task, agents)
            else:
                raise Exception(f"Unknown execution strategy: {task.strategy}")
            
            # Update task result
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            task_result = self.task_results[task.id]
            task_result.status = TaskStatus.COMPLETED
            task_result.aggregated_result = result
            task_result.execution_time = execution_time
            task_result.completed_at = end_time
            
            # Update metrics
            self.metrics["tasks_completed"] += 1
            self._update_average_execution_time(execution_time)
            
            # Trigger callback if specified
            if task.callback_url:
                await self._trigger_callback(task, task_result)
            
            logger.info(f"[OK] Task {task.id} completed in {execution_time:.2f}s")
            
        except asyncio.TimeoutError:
            self._handle_task_timeout(task)
        except Exception as e:
            self._handle_task_failure(task, str(e))
        finally:
            # Remove from active tasks
            self.active_tasks.pop(task.id, None)
    
    def _find_suitable_agents(self, task: TaskRequest) -> List[str]:
        """Find agents that can handle the task requirements"""
        suitable_agents = []
        
        # Get all agents
        all_agents = self.registry.agents.values()
        
        for agent in all_agents:
            # Check if agent is active
            if agent.status.value != "active":
                continue
                
            # Check if agent has all required capabilities
            agent_capabilities = {cap.name for cap in agent.capabilities}
            if all(req in agent_capabilities for req in task.requirements):
                # Score agent based on performance
                score = self._calculate_agent_score(agent.id, task)
                suitable_agents.append((score, agent.id))
        
        # Sort by score (descending)
        suitable_agents.sort(key=lambda x: x[0], reverse=True)
        
        # Return agent IDs
        return [agent_id for _, agent_id in suitable_agents]
    
    def _calculate_agent_score(self, agent_id: str, task: TaskRequest) -> float:
        """Calculate agent suitability score for a task"""
        base_score = 1.0
        
        # Factor in agent performance
        perf = self.agent_performance[agent_id]
        success_rate = perf["success_rate"]
        
        # Factor in current load (if available)
        agent_load = self._get_agent_load(agent_id)
        load_factor = 1.0 - (agent_load / 10.0)  # Penalize heavily loaded agents
        
        # Factor in task priority
        priority_factor = 1.0
        if task.priority == TaskPriority.CRITICAL:
            priority_factor = 2.0
        elif task.priority == TaskPriority.HIGH:
            priority_factor = 1.5
        
        return base_score * success_rate * load_factor * priority_factor
    
    def _get_agent_load(self, agent_id: str) -> int:
        """Get current load on an agent"""
        # Count active assignments
        load = 0
        for assignments in self.task_assignments.values():
            for assignment in assignments:
                if assignment.agent_id == agent_id and assignment.status == TaskStatus.PROCESSING:
                    load += 1
        return load
    
    async def _execute_single(self, task: TaskRequest, agent_id: str) -> Dict[str, Any]:
        """Execute task on a single agent"""
        assignment = TaskAssignment(
            task_id=task.id,
            agent_id=agent_id,
            assigned_at=datetime.now()
        )
        self.task_assignments[task.id].append(assignment)
        
        # Simulate agent execution (in production, this would call the actual agent)
        assignment.started_at = datetime.now()
        assignment.status = TaskStatus.PROCESSING
        
        try:
            result = await self._call_agent(agent_id, task)
            assignment.completed_at = datetime.now()
            assignment.status = TaskStatus.COMPLETED
            assignment.result = result
            
            # Update agent performance
            self._update_agent_performance(agent_id, success=True, 
                                         response_time=(assignment.completed_at - assignment.started_at).total_seconds())
            
            return result
            
        except Exception as e:
            assignment.status = TaskStatus.FAILED
            assignment.error = str(e)
            self._update_agent_performance(agent_id, success=False)
            raise
    
    async def _execute_parallel(self, task: TaskRequest, agent_ids: List[str]) -> Dict[str, Any]:
        """Execute task on multiple agents in parallel"""
        # Limit parallel execution
        max_parallel = min(len(agent_ids), 5)
        selected_agents = agent_ids[:max_parallel]
        
        # Create assignments
        assignments = []
        for agent_id in selected_agents:
            assignment = TaskAssignment(
                task_id=task.id,
                agent_id=agent_id,
                assigned_at=datetime.now()
            )
            self.task_assignments[task.id].append(assignment)
            assignments.append(assignment)
        
        # Execute in parallel
        tasks = []
        for assignment in assignments:
            agent_task = asyncio.create_task(
                self._execute_agent_assignment(assignment, task)
            )
            tasks.append(agent_task)
        
        # Wait for all to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Aggregate results
        successful_results = []
        for i, result in enumerate(results):
            if not isinstance(result, Exception):
                successful_results.append(result)
        
        if not successful_results:
            raise Exception("All parallel agents failed")
        
        # Aggregate based on task type
        return self._aggregate_results(successful_results, task)
    
    async def _execute_sequential(self, task: TaskRequest, agent_ids: List[str]) -> Dict[str, Any]:
        """Execute task on agents sequentially, passing results forward"""
        result = task.payload
        
        for agent_id in agent_ids[:3]:  # Limit to 3 agents
            assignment = TaskAssignment(
                task_id=task.id,
                agent_id=agent_id,
                assigned_at=datetime.now()
            )
            self.task_assignments[task.id].append(assignment)
            
            try:
                # Pass previous result as input
                task_copy = TaskRequest(**asdict(task))
                task_copy.payload = result
                
                result = await self._execute_agent_assignment(assignment, task_copy)
                
            except Exception as e:
                logger.warning(f"Sequential execution failed at agent {agent_id}: {str(e)}")
                # Continue with next agent
        
        return result
    
    async def _execute_consensus(self, task: TaskRequest, agent_ids: List[str]) -> Dict[str, Any]:
        """Get consensus from multiple agents"""
        # Execute on multiple agents
        results = await self._execute_parallel(task, agent_ids[:3])
        
        # For now, return the aggregated result
        # In production, this would implement actual consensus logic
        return results
    
    async def _execute_fallback(self, task: TaskRequest, agent_ids: List[str]) -> Dict[str, Any]:
        """Try agents until one succeeds"""
        last_error = None
        
        for agent_id in agent_ids:
            assignment = TaskAssignment(
                task_id=task.id,
                agent_id=agent_id,
                assigned_at=datetime.now()
            )
            self.task_assignments[task.id].append(assignment)
            
            try:
                result = await self._execute_agent_assignment(assignment, task)
                return result
            except Exception as e:
                last_error = e
                logger.warning(f"Fallback: Agent {agent_id} failed: {str(e)}")
                continue
        
        raise Exception(f"All fallback agents failed. Last error: {last_error}")
    
    async def _execute_agent_assignment(self, assignment: TaskAssignment, task: TaskRequest) -> Dict[str, Any]:
        """Execute a specific agent assignment"""
        assignment.started_at = datetime.now()
        assignment.status = TaskStatus.PROCESSING
        
        try:
            result = await self._call_agent(assignment.agent_id, task)
            assignment.completed_at = datetime.now()
            assignment.status = TaskStatus.COMPLETED
            assignment.result = result
            
            # Update performance
            response_time = (assignment.completed_at - assignment.started_at).total_seconds()
            self._update_agent_performance(assignment.agent_id, success=True, response_time=response_time)
            
            return result
            
        except Exception as e:
            assignment.status = TaskStatus.FAILED
            assignment.error = str(e)
            assignment.completed_at = datetime.now()
            self._update_agent_performance(assignment.agent_id, success=False)
            raise
    
    async def _call_agent(self, agent_id: str, task: TaskRequest) -> Dict[str, Any]:
        """Call an agent to execute a task"""
        # Get agent details
        agent = self.registry.get_agent(agent_id)
        if not agent:
            raise Exception(f"Agent {agent_id} not found")
        
        # Simulate agent execution
        # In production, this would make actual API calls to the agent
        await asyncio.sleep(0.5)  # Simulate processing time
        
        # Return simulated result
        return {
            "agent_id": agent_id,
            "agent_name": agent.name,
            "task_type": task.type,
            "result": {
                "status": "success",
                "data": f"Processed by {agent.name}",
                "metadata": {
                    "processing_time": 0.5,
                    "capabilities_used": task.requirements
                }
            }
        }
    
    def _aggregate_results(self, results: List[Dict[str, Any]], task: TaskRequest) -> Dict[str, Any]:
        """Aggregate results from multiple agents"""
        # Basic aggregation - can be customized based on task type
        aggregated = {
            "aggregation_type": task.strategy.value,
            "agent_count": len(results),
            "results": results,
            "summary": {
                "all_successful": all(r.get("result", {}).get("status") == "success" for r in results),
                "task_type": task.type
            }
        }
        
        # Task-specific aggregation
        if task.type == "research":
            # Combine research findings
            aggregated["combined_findings"] = []
            for result in results:
                if "data" in result.get("result", {}):
                    aggregated["combined_findings"].append(result["result"]["data"])
        
        return aggregated
    
    def _update_agent_performance(self, agent_id: str, success: bool, response_time: float = 0):
        """Update agent performance metrics"""
        perf = self.agent_performance[agent_id]
        perf["tasks_assigned"] += 1
        
        if success:
            perf["tasks_completed"] += 1
        else:
            perf["tasks_failed"] += 1
        
        # Update success rate
        if perf["tasks_assigned"] > 0:
            perf["success_rate"] = perf["tasks_completed"] / perf["tasks_assigned"]
        
        # Update average response time
        if response_time > 0 and success:
            current_avg = perf["average_response_time"]
            completed = perf["tasks_completed"]
            perf["average_response_time"] = ((current_avg * (completed - 1)) + response_time) / completed
    
    def _update_average_execution_time(self, execution_time: float):
        """Update average execution time metric"""
        completed = self.metrics["tasks_completed"]
        current_avg = self.metrics["average_execution_time"]
        self.metrics["average_execution_time"] = ((current_avg * (completed - 1)) + execution_time) / completed
    
    def _estimate_wait_time(self, priority: TaskPriority) -> float:
        """Estimate wait time based on queue and priority"""
        # Simple estimation based on queue size
        queue_size = self.task_queue.size()
        active_tasks = len(self.active_tasks)
        
        # Base wait time
        base_wait = (queue_size + active_tasks) * self.metrics.get("average_execution_time", 5)
        
        # Adjust for priority
        priority_factor = {
            TaskPriority.CRITICAL: 0.1,
            TaskPriority.HIGH: 0.3,
            TaskPriority.NORMAL: 1.0,
            TaskPriority.LOW: 2.0,
            TaskPriority.BACKGROUND: 5.0
        }
        
        return base_wait * priority_factor.get(priority, 1.0)
    
    def _handle_task_timeout(self, task: TaskRequest):
        """Handle task timeout"""
        logger.warning(f"Task {task.id} timed out")
        
        task_result = self.task_results[task.id]
        task_result.status = TaskStatus.TIMEOUT
        task_result.completed_at = datetime.now()
        
        self.metrics["tasks_timeout"] += 1
        
        # Cancel any pending assignments
        for assignment in self.task_assignments[task.id]:
            if assignment.status in [TaskStatus.ASSIGNED, TaskStatus.PROCESSING]:
                assignment.status = TaskStatus.CANCELLED
    
    def _handle_task_failure(self, task: TaskRequest, error: str):
        """Handle task failure"""
        logger.error(f"Task {task.id} failed: {error}")
        
        task_result = self.task_results[task.id]
        task_result.status = TaskStatus.FAILED
        task_result.completed_at = datetime.now()
        task_result.metadata["error"] = error
        
        self.metrics["tasks_failed"] += 1
    
    async def _trigger_callback(self, task: TaskRequest, result: TaskResult):
        """Trigger callback URL with task result"""
        # In production, this would make an HTTP POST to the callback URL
        logger.info(f"Would trigger callback to {task.callback_url} with result")
    
    async def _monitor_timeouts(self):
        """Monitor tasks for timeouts"""
        while self._running:
            try:
                current_time = datetime.now()
                
                for task_id, task in list(self.active_tasks.items()):
                    elapsed = (current_time - task.created_at).total_seconds()
                    
                    if elapsed > task.timeout:
                        self._handle_task_timeout(task)
                        self.active_tasks.pop(task_id, None)
                
                await asyncio.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logger.error(f"Timeout monitor error: {str(e)}")
                await asyncio.sleep(5)
    
    async def _update_metrics(self):
        """Update metrics periodically"""
        while self._running:
            try:
                self.metrics["queue_size"] = self.task_queue.size()
                self.metrics["active_tasks"] = len(self.active_tasks)
                
                await asyncio.sleep(10)  # Update every 10 seconds
                
            except Exception as e:
                logger.error(f"Metrics update error: {str(e)}")
                await asyncio.sleep(10)
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        if task_id not in self.task_results:
            return None
        
        result = self.task_results[task_id]
        
        return {
            "task_id": task_id,
            "status": result.status.value,
            "created_at": result.created_at.isoformat(),
            "completed_at": result.completed_at.isoformat() if result.completed_at else None,
            "execution_time": result.execution_time,
            "assignments": [
                {
                    "agent_id": a.agent_id,
                    "status": a.status.value,
                    "started_at": a.started_at.isoformat() if a.started_at else None,
                    "completed_at": a.completed_at.isoformat() if a.completed_at else None,
                    "error": a.error
                }
                for a in self.task_assignments.get(task_id, [])
            ],
            "result": result.aggregated_result
        }
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        return {
            "queue_size": self.task_queue.size(),
            "active_tasks": len(self.active_tasks),
            "max_workers": self.max_workers,
            "available_capacity": self.max_workers - len(self.active_tasks),
            "priorities": {
                priority.name: sum(1 for task in self.task_queue.get_tasks() if task.priority == priority)
                for priority in TaskPriority
            }
        }
    
    def get_orchestrator_metrics(self) -> Dict[str, Any]:
        """Get orchestrator performance metrics"""
        return {
            **self.metrics,
            "agent_performance": dict(self.agent_performance),
            "success_rate": self.metrics["tasks_completed"] / max(self.metrics["tasks_received"], 1),
            "failure_rate": self.metrics["tasks_failed"] / max(self.metrics["tasks_received"], 1),
            "timeout_rate": self.metrics["tasks_timeout"] / max(self.metrics["tasks_received"], 1)
        }
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending or active task"""
        # Remove from queue if pending
        if self.task_queue.remove(task_id):
            if task_id in self.task_results:
                self.task_results[task_id].status = TaskStatus.CANCELLED
                self.task_results[task_id].completed_at = datetime.now()
            return True
        
        # Cancel if active
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            self._handle_task_failure(task, "Cancelled by user")
            self.active_tasks.pop(task_id, None)
            
            # Update result status
            if task_id in self.task_results:
                self.task_results[task_id].status = TaskStatus.CANCELLED
            
            return True
        
        return False
    
    def shutdown(self):
        """Gracefully shutdown the orchestrator"""
        logger.info("Shutting down Task Orchestrator...")
        self._running = False
        self.executor.shutdown(wait=True)

# Create global orchestrator instance
task_orchestrator = BonzaiTaskOrchestrator(max_workers=20)

# Helper functions for easy integration
def get_orchestrator():
    """Get the global task orchestrator instance"""
    return task_orchestrator

async def submit_task(task_data: Dict[str, Any]) -> Dict[str, Any]:
    """Submit a task to the orchestrator"""
    return await task_orchestrator.submit_task(task_data)

def get_task_result(task_id: str) -> Optional[Dict[str, Any]]:
    """Get result of a specific task"""
    return task_orchestrator.get_task_status(task_id)

def get_queue_info() -> Dict[str, Any]:
    """Get current queue information"""
    return task_orchestrator.get_queue_status()

def get_metrics() -> Dict[str, Any]:
    """Get orchestrator metrics"""
    return task_orchestrator.get_orchestrator_metrics()