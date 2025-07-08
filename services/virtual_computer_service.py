"""
[BEAR] Virtual Computer Service - MUMA Scout Agent Operations
Orchestrates Scrapybara/E2B virtual computers for autonomous agent workflows
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import os

# Import existing services
from .enhanced_scrapybara_integration import EnhancedScrapybaraManager, ComputerActionRequest, ComputerAction
from .enhanced_code_execution import EnhancedMamaBearCodeExecution, CodeExecutionResult
# from .mama_bear_scrapybara_integration import MamaBearScrapybaraAgent  # Disabled for now

logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    RESEARCHING = "researching"
    CODING = "coding"
    BROWSING = "browsing"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    ERROR = "error"

class VirtualEnvironmentType(Enum):
    SCRAPYBARA_BROWSER = "scrapybara_browser"
    SCRAPYBARA_UBUNTU = "scrapybara_ubuntu"
    E2B_CODE_INTERPRETER = "e2b_code_interpreter"
    HYBRID_WORKSPACE = "hybrid_workspace"

@dataclass
class AgentWorkspace:
    """Represents an agent's virtual workspace"""
    workspace_id: str
    agent_name: str
    user_id: str
    task_description: str
    status: AgentStatus = AgentStatus.IDLE
    environments: List[Dict[str, Any]] = field(default_factory=list)
    file_tree: Dict[str, Any] = field(default_factory=dict)
    timeline: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    progress: float = 0.0
    current_step: str = ""
    output_files: List[str] = field(default_factory=list)

@dataclass
class AgentActivity:
    """Represents an activity in the agent timeline"""
    activity_id: str
    timestamp: datetime
    activity_type: str
    description: str
    details: Optional[str] = None
    status: str = "running"
    environment_id: Optional[str] = None
    files_affected: List[str] = field(default_factory=list)
    output: Optional[str] = None
    error: Optional[str] = None

class VirtualComputerService:
    """
    Orchestrates virtual computers for autonomous agent operations
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        if config is None:
            config = {}
        
        self.config = config
        
        # Initialize virtual computer managers
        self.scrapybara_manager = EnhancedScrapybaraManager(config)
        self.code_executor = EnhancedMamaBearCodeExecution()
        # self.mama_bear_agent = MamaBearScrapybaraAgent(config)  # Disabled for now
        self.mama_bear_agent = None  # Temporary fallback
        
        # Workspace management
        self.active_workspaces: Dict[str, AgentWorkspace] = {}
        self.environment_pool: Dict[str, Dict[str, Any]] = {}
        
        # Agent capabilities mapping
        self.agent_capabilities = {
            "Research Scout": {
                "primary_env": VirtualEnvironmentType.SCRAPYBARA_BROWSER,
                "secondary_env": VirtualEnvironmentType.E2B_CODE_INTERPRETER,
                "capabilities": ["web_research", "data_analysis", "report_generation"]
            },
            "Code Assistant": {
                "primary_env": VirtualEnvironmentType.E2B_CODE_INTERPRETER,
                "secondary_env": VirtualEnvironmentType.SCRAPYBARA_UBUNTU,
                "capabilities": ["code_generation", "testing", "debugging", "deployment"]
            },
            "Creative AI": {
                "primary_env": VirtualEnvironmentType.SCRAPYBARA_BROWSER,
                "secondary_env": VirtualEnvironmentType.E2B_CODE_INTERPRETER,
                "capabilities": ["content_creation", "design", "image_generation"]
            },
            "Automation Engine": {
                "primary_env": VirtualEnvironmentType.SCRAPYBARA_UBUNTU,
                "secondary_env": VirtualEnvironmentType.E2B_CODE_INTERPRETER,
                "capabilities": ["workflow_automation", "api_integration", "monitoring"]
            },
            "Performance Optimizer": {
                "primary_env": VirtualEnvironmentType.E2B_CODE_INTERPRETER,
                "secondary_env": VirtualEnvironmentType.SCRAPYBARA_UBUNTU,
                "capabilities": ["performance_analysis", "optimization", "benchmarking"]
            },
            "Deployment Scout": {
                "primary_env": VirtualEnvironmentType.SCRAPYBARA_UBUNTU,
                "secondary_env": VirtualEnvironmentType.E2B_CODE_INTERPRETER,
                "capabilities": ["infrastructure_setup", "deployment", "monitoring"]
            }
        }
        
        logger.info("[COMPUTER] Virtual Computer Service initialized with multi-environment support")
    
    async def create_agent_workspace(self, agent_name: str, user_id: str, 
                                   task_description: str) -> Dict[str, Any]:
        """Create a new virtual workspace for an agent"""
        try:
            workspace_id = f"workspace_{uuid.uuid4().hex[:12]}"
            
            # Get agent capabilities
            agent_config = self.agent_capabilities.get(agent_name, {
                "primary_env": VirtualEnvironmentType.SCRAPYBARA_BROWSER,
                "secondary_env": VirtualEnvironmentType.E2B_CODE_INTERPRETER,
                "capabilities": ["general_purpose"]
            })
            
            # Create virtual environments
            environments = await self._create_agent_environments(
                workspace_id, agent_name, agent_config
            )
            
            # Initialize file tree
            file_tree = {
                "name": f"{agent_name.lower().replace(' ', '_')}_workspace",
                "type": "folder",
                "children": [
                    {
                        "name": "src",
                        "type": "folder",
                        "children": []
                    },
                    {
                        "name": "data",
                        "type": "folder", 
                        "children": []
                    },
                    {
                        "name": "output",
                        "type": "folder",
                        "children": []
                    },
                    {
                        "name": "README.md",
                        "type": "file",
                        "content": f"# {agent_name} Workspace\n\nTask: {task_description}\nCreated: {datetime.now().isoformat()}"
                    }
                ]
            }
            
            # Create workspace
            workspace = AgentWorkspace(
                workspace_id=workspace_id,
                agent_name=agent_name,
                user_id=user_id,
                task_description=task_description,
                environments=environments,
                file_tree=file_tree,
                status=AgentStatus.PLANNING
            )
            
            self.active_workspaces[workspace_id] = workspace
            
            # Add initial timeline entry
            await self._add_timeline_activity(
                workspace_id,
                "workspace_created",
                f"Created virtual workspace for {agent_name}",
                f"Initialized {len(environments)} virtual environments"
            )
            
            logger.info(f"[LAUNCH] Created workspace {workspace_id} for {agent_name}")
            
            return {
                "success": True,
                "workspace_id": workspace_id,
                "agent_name": agent_name,
                "environments": environments,
                "file_tree": file_tree,
                "capabilities": agent_config["capabilities"]
            }
            
        except Exception as e:
            logger.error(f"Error creating agent workspace: {e}")
            return {"success": False, "error": str(e)}
    
    async def start_agent_execution(self, workspace_id: str) -> Dict[str, Any]:
        """Start autonomous agent execution"""
        try:
            if workspace_id not in self.active_workspaces:
                return {"success": False, "error": "Workspace not found"}
            
            workspace = self.active_workspaces[workspace_id]
            workspace.status = AgentStatus.EXECUTING
            workspace.last_activity = datetime.now()
            
            # Start autonomous execution based on agent type
            execution_plan = await self._create_execution_plan(workspace)
            
            # Execute plan asynchronously
            asyncio.create_task(self._execute_agent_plan(workspace_id, execution_plan))
            
            await self._add_timeline_activity(
                workspace_id,
                "execution_started",
                f"Started autonomous execution for {workspace.agent_name}",
                f"Executing {len(execution_plan)} planned steps"
            )
            
            return {
                "success": True,
                "workspace_id": workspace_id,
                "execution_plan": execution_plan,
                "status": workspace.status.value
            }
            
        except Exception as e:
            logger.error(f"Error starting agent execution: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_workspace_status(self, workspace_id: str) -> Dict[str, Any]:
        """Get current workspace status and timeline"""
        try:
            if workspace_id not in self.active_workspaces:
                return {"success": False, "error": "Workspace not found"}
            
            workspace = self.active_workspaces[workspace_id]
            
            # Get environment status
            env_status = []
            for env in workspace.environments:
                status = await self._get_environment_status(env["environment_id"])
                env_status.append({
                    "environment_id": env["environment_id"],
                    "type": env["type"],
                    "status": status
                })
            
            return {
                "success": True,
                "workspace_id": workspace_id,
                "agent_name": workspace.agent_name,
                "status": workspace.status.value,
                "progress": workspace.progress,
                "current_step": workspace.current_step,
                "timeline": [
                    {
                        "id": activity.activity_id,
                        "timestamp": activity.timestamp.isoformat(),
                        "type": activity.activity_type,
                        "description": activity.description,
                        "details": activity.details,
                        "status": activity.status,
                        "files_affected": activity.files_affected
                    }
                    for activity in workspace.timeline[-10:]  # Last 10 activities
                ],
                "file_tree": workspace.file_tree,
                "environments": env_status,
                "output_files": workspace.output_files
            }
            
        except Exception as e:
            logger.error(f"Error getting workspace status: {e}")
            return {"success": False, "error": str(e)}
    
    async def execute_agent_command(self, workspace_id: str, command: str, 
                                  environment_type: str = "auto") -> Dict[str, Any]:
        """Execute a command in the agent's virtual environment"""
        try:
            if workspace_id not in self.active_workspaces:
                return {"success": False, "error": "Workspace not found"}
            
            workspace = self.active_workspaces[workspace_id]
            
            # Select appropriate environment
            if environment_type == "auto":
                env = workspace.environments[0]  # Use primary environment
            else:
                env = next((e for e in workspace.environments if e["type"] == environment_type), None)
                if not env:
                    return {"success": False, "error": f"Environment type {environment_type} not found"}
            
            # Execute command based on environment type
            if env["type"] == VirtualEnvironmentType.E2B_CODE_INTERPRETER.value:
                result = await self._execute_code_command(env["environment_id"], command, workspace.user_id)
            elif env["type"] in [VirtualEnvironmentType.SCRAPYBARA_UBUNTU.value, VirtualEnvironmentType.SCRAPYBARA_BROWSER.value]:
                result = await self._execute_scrapybara_command(env["environment_id"], command)
            else:
                return {"success": False, "error": f"Unsupported environment type: {env['type']}"}
            
            # Add to timeline
            await self._add_timeline_activity(
                workspace_id,
                "command_executed",
                f"Executed command: {command[:50]}...",
                f"Environment: {env['type']}, Result: {result.get('success', False)}"
            )
            
            return {
                "success": True,
                "command": command,
                "environment": env["type"],
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error executing agent command: {e}")
            return {"success": False, "error": str(e)}
    
    async def update_workspace_files(self, workspace_id: str, file_path: str, 
                                   content: str, operation: str = "create") -> Dict[str, Any]:
        """Update files in the workspace"""
        try:
            if workspace_id not in self.active_workspaces:
                return {"success": False, "error": "Workspace not found"}
            
            workspace = self.active_workspaces[workspace_id]
            
            # Update file tree
            await self._update_file_tree(workspace, file_path, content, operation)
            
            # Add to timeline
            await self._add_timeline_activity(
                workspace_id,
                "file_updated",
                f"{operation.capitalize()} file: {file_path}",
                f"File size: {len(content)} characters",
                files_affected=[file_path]
            )
            
            return {
                "success": True,
                "file_path": file_path,
                "operation": operation,
                "file_tree": workspace.file_tree
            }
            
        except Exception as e:
            logger.error(f"Error updating workspace files: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_virtual_computer_stats(self) -> Dict[str, Any]:
        """Get statistics about virtual computer usage"""
        try:
            active_workspaces = len(self.active_workspaces)
            total_environments = sum(len(ws.environments) for ws in self.active_workspaces.values())
            
            # Environment type breakdown
            env_types = {}
            for workspace in self.active_workspaces.values():
                for env in workspace.environments:
                    env_type = env["type"]
                    env_types[env_type] = env_types.get(env_type, 0) + 1
            
            # Agent status breakdown
            agent_statuses = {}
            for workspace in self.active_workspaces.values():
                status = workspace.status.value
                agent_statuses[status] = agent_statuses.get(status, 0) + 1
            
            return {
                "success": True,
                "stats": {
                    "active_workspaces": active_workspaces,
                    "total_environments": total_environments,
                    "environment_types": env_types,
                    "agent_statuses": agent_statuses,
                    "service_uptime": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting virtual computer stats: {e}")
            return {"success": False, "error": str(e)}
    
    # Private helper methods
    
    async def _create_agent_environments(self, workspace_id: str, agent_name: str, 
                                       agent_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create virtual environments for the agent"""
        environments = []
        
        try:
            # Create primary environment
            primary_env_type = agent_config["primary_env"]
            primary_env = await self._create_environment(workspace_id, primary_env_type, "primary")
            environments.append(primary_env)
            
            # Create secondary environment
            secondary_env_type = agent_config["secondary_env"]
            secondary_env = await self._create_environment(workspace_id, secondary_env_type, "secondary")
            environments.append(secondary_env)
            
            return environments
            
        except Exception as e:
            logger.error(f"Error creating agent environments: {e}")
            return []
    
    async def _create_environment(self, workspace_id: str, env_type: VirtualEnvironmentType, 
                                role: str) -> Dict[str, Any]:
        """Create a single virtual environment"""
        env_id = f"{workspace_id}_{role}_{uuid.uuid4().hex[:8]}"
        
        if env_type == VirtualEnvironmentType.SCRAPYBARA_BROWSER:
            # Create Scrapybara browser instance
            result = await self.scrapybara_manager.start_browser({
                "workspace_id": workspace_id,
                "role": role,
                "extensions": ["ublock_origin", "json_viewer"]
            })
            
        elif env_type == VirtualEnvironmentType.SCRAPYBARA_UBUNTU:
            # Create Scrapybara Ubuntu instance
            result = await self.scrapybara_manager.start_ubuntu({
                "workspace_id": workspace_id,
                "role": role,
                "packages": ["python3", "nodejs", "curl", "wget", "git"]
            })
            
        elif env_type == VirtualEnvironmentType.E2B_CODE_INTERPRETER:
            # Create E2B code interpreter
            result = {"instance_id": env_id, "type": "e2b_code_interpreter"}
            
        else:
            raise ValueError(f"Unsupported environment type: {env_type}")
        
        return {
            "environment_id": env_id,
            "type": env_type.value,
            "role": role,
            "instance_id": result.get("instance_id", env_id),
            "status": "running",
            "created_at": datetime.now().isoformat()
        }
    
    async def _create_execution_plan(self, workspace: AgentWorkspace) -> List[Dict[str, Any]]:
        """Create execution plan based on agent type and task"""
        agent_name = workspace.agent_name
        task = workspace.task_description
        
        # Base plan structure
        base_plan = [
            {"step": 1, "action": "analyze_task", "description": f"Analyze task requirements: {task}"},
            {"step": 2, "action": "setup_environment", "description": "Configure virtual environments"},
            {"step": 3, "action": "execute_main_task", "description": "Execute primary task logic"},
            {"step": 4, "action": "generate_output", "description": "Generate results and documentation"},
            {"step": 5, "action": "finalize", "description": "Finalize workspace and cleanup"}
        ]
        
        # Customize plan based on agent type
        if agent_name == "Research Scout":
            base_plan[2] = {"step": 3, "action": "research_and_analyze", "description": "Conduct web research and data analysis"}
        elif agent_name == "Code Assistant":
            base_plan[2] = {"step": 3, "action": "code_and_test", "description": "Generate, test, and debug code"}
        elif agent_name == "Creative AI":
            base_plan[2] = {"step": 3, "action": "create_content", "description": "Generate creative content and designs"}
        
        return base_plan
    
    async def _execute_agent_plan(self, workspace_id: str, execution_plan: List[Dict[str, Any]]):
        """Execute the agent plan asynchronously"""
        try:
            workspace = self.active_workspaces[workspace_id]
            
            for step in execution_plan:
                workspace.current_step = step["description"]
                workspace.progress = (step["step"] - 1) / len(execution_plan)
                
                await self._add_timeline_activity(
                    workspace_id,
                    "step_started",
                    f"Step {step['step']}: {step['description']}",
                    f"Action: {step['action']}"
                )
                
                # Simulate step execution
                await asyncio.sleep(2)  # Simulate work
                
                await self._add_timeline_activity(
                    workspace_id,
                    "step_completed",
                    f"Completed step {step['step']}",
                    f"Successfully executed {step['action']}"
                )
            
            workspace.status = AgentStatus.COMPLETED
            workspace.progress = 1.0
            workspace.current_step = "Task completed"
            
            await self._add_timeline_activity(
                workspace_id,
                "execution_completed",
                f"Agent {workspace.agent_name} completed task",
                "All steps executed successfully"
            )
            
        except Exception as e:
            workspace = self.active_workspaces[workspace_id]
            workspace.status = AgentStatus.ERROR
            await self._add_timeline_activity(
                workspace_id,
                "execution_error",
                f"Error in agent execution: {str(e)}",
                "Agent execution failed"
            )
            logger.error(f"Error executing agent plan: {e}")
    
    async def _add_timeline_activity(self, workspace_id: str, activity_type: str, 
                                   description: str, details: Optional[str] = None,
                                   files_affected: Optional[List[str]] = None):
        """Add activity to workspace timeline"""
        if workspace_id not in self.active_workspaces:
            return
        
        workspace = self.active_workspaces[workspace_id]
        
        activity = AgentActivity(
            activity_id=f"activity_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.now(),
            activity_type=activity_type,
            description=description,
            details=details,
            files_affected=files_affected or []
        )
        
        workspace.timeline.append(activity)
        workspace.last_activity = datetime.now()
        
        # Keep only last 50 activities
        if len(workspace.timeline) > 50:
            workspace.timeline = workspace.timeline[-50:]
    
    async def _execute_code_command(self, env_id: str, command: str, user_id: str) -> Dict[str, Any]:
        """Execute code command in E2B environment"""
        try:
            result = await self.code_executor.execute_code_safely(command, user_id)
            return {
                "success": result.success,
                "output": result.output,
                "error": result.error,
                "execution_time": result.execution_time
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _execute_scrapybara_command(self, env_id: str, command: str) -> Dict[str, Any]:
        """Execute command in Scrapybara environment"""
        try:
            # Mock implementation - replace with actual Scrapybara API call
            return {
                "success": True,
                "output": f"Command executed: {command}",
                "execution_time": 0.5
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_environment_status(self, env_id: str) -> str:
        """Get status of virtual environment"""
        # Mock implementation
        return "running"
    
    async def _update_file_tree(self, workspace: AgentWorkspace, file_path: str, 
                              content: str, operation: str):
        """Update the workspace file tree"""
        # Simple implementation - in production, this would be more sophisticated
        if operation == "create":
            workspace.output_files.append(file_path)


# Global service instance
virtual_computer_service = VirtualComputerService()


# Integration functions
async def initialize_virtual_computer_service(config: Dict[str, Any]) -> VirtualComputerService:
    """Initialize the virtual computer service"""
    service = VirtualComputerService(config)
    logger.info("[COMPUTER] Virtual Computer Service initialized")
    return service


async def get_virtual_computer_service() -> VirtualComputerService:
    """Get the global virtual computer service instance"""
    return virtual_computer_service