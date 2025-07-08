# [ART] Agent Creation Workbench - Mama Bear's autonomous agent design & deployment system

import asyncio
import json
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import logging
import os

from .enhanced_gemini_scout_orchestration import enhanced_scout_orchestrator
from .intelligent_execution_router import get_intelligent_router

@dataclass
class AgentTemplate:
    """Base template for agent creation"""
    id: str
    name: str
    type: str  # research, ui_design, api, security, custom
    description: str
    capabilities: List[str]
    default_config: Dict[str, Any]
    created_at: str
    version: str = "1.0.0"

@dataclass
class AgentInstance:
    """Deployed agent instance"""
    id: str
    template_id: str
    name: str
    status: str  # active, paused, stopped, error
    config: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    created_at: str
    deployed_at: Optional[str] = None
    last_activity: Optional[str] = None
    owner_id: str = ""

class AgentCreationWorkbench:
    """[BEAR] Mama Bear's Agent Creation & Management System"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.agents_storage_path = os.path.join(os.getcwd(), "data", "agents")
        self.templates_storage_path = os.path.join(os.getcwd(), "data", "agent_templates")
        
        # Ensure storage directories exist
        os.makedirs(self.agents_storage_path, exist_ok=True)
        os.makedirs(self.templates_storage_path, exist_ok=True)
        
        # Initialize default templates
        self._initialize_default_templates()
        
        # Track active agents
        self.active_agents: Dict[str, AgentInstance] = {}
        self._load_active_agents()

    def _initialize_default_templates(self):
        """Initialize default agent templates"""
        default_templates = [
            AgentTemplate(
                id="research_agent_v1",
                name="Research Specialist",
                type="research",
                description="Deep research agent with web scraping, data analysis, and report generation",
                capabilities=[
                    "web_research",
                    "data_analysis", 
                    "report_generation",
                    "fact_checking",
                    "source_validation"
                ],
                default_config={
                    "max_research_depth": 5,
                    "sources_required": 3,
                    "fact_check_enabled": True,
                    "output_format": "markdown",
                    "research_timeout": 300
                },
                created_at=datetime.now().isoformat()
            ),
            AgentTemplate(
                id="ui_design_agent_v1",
                name="UI/UX Designer",
                type="ui_design",
                description="Intelligent UI designer with modern frameworks and accessibility focus",
                capabilities=[
                    "component_design",
                    "responsive_layouts",
                    "accessibility_compliance",
                    "design_systems",
                    "user_experience_optimization"
                ],
                default_config={
                    "framework_preference": "react",
                    "accessibility_level": "WCAG_AA",
                    "design_system": "material_design",
                    "responsive_breakpoints": ["mobile", "tablet", "desktop"],
                    "performance_first": True
                },
                created_at=datetime.now().isoformat()
            ),
            AgentTemplate(
                id="api_specialist_v1",
                name="API Development Specialist",
                type="api",
                description="REST/GraphQL API development with security and performance optimization",
                capabilities=[
                    "api_design",
                    "endpoint_implementation",
                    "authentication_setup",
                    "performance_optimization",
                    "documentation_generation"
                ],
                default_config={
                    "api_style": "REST",
                    "authentication": "JWT",
                    "rate_limiting": True,
                    "documentation": "OpenAPI",
                    "validation": "strict"
                },
                created_at=datetime.now().isoformat()
            ),
            AgentTemplate(
                id="security_analyst_v1",
                name="Security Analyst",
                type="security",
                description="Application security analysis, vulnerability detection, and hardening",
                capabilities=[
                    "vulnerability_scanning",
                    "security_analysis",
                    "penetration_testing",
                    "compliance_checking",
                    "security_recommendations"
                ],
                default_config={
                    "scan_depth": "comprehensive",
                    "compliance_standards": ["OWASP", "SOC2"],
                    "automated_fixes": False,
                    "report_detail": "high",
                    "continuous_monitoring": True
                },
                created_at=datetime.now().isoformat()
            )
        ]
        
        # Save default templates
        for template in default_templates:
            self._save_template(template)

    async def create_custom_agent(self, 
                                user_id: str,
                                agent_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        [ART] Create a custom agent using Mama Bear intelligence
        """
        try:
            # Use Mama Bear to analyze and enhance the agent specification
            enhanced_spec = await self._enhance_agent_spec_with_mama_bear(agent_spec)
            
            # Create unique agent template
            template = AgentTemplate(
                id=str(uuid.uuid4()),
                name=enhanced_spec.get('name', 'Custom Agent'),
                type='custom',
                description=enhanced_spec.get('description', ''),
                capabilities=enhanced_spec.get('capabilities', []),
                default_config=enhanced_spec.get('config', {}),
                created_at=datetime.now().isoformat()
            )
            
            # Save template
            self._save_template(template)
            
            # Generate implementation code
            implementation = await self._generate_agent_implementation(template)
            
            return {
                'success': True,
                'template': asdict(template),
                'implementation': implementation,
                'recommendations': enhanced_spec.get('recommendations', [])
            }
            
        except Exception as e:
            self.logger.error(f"Custom agent creation failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    async def deploy_agent(self, 
                         template_id: str,
                         user_id: str,
                         deployment_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        [LAUNCH] Deploy an agent instance from template
        """
        try:
            # Load template
            template = self._load_template(template_id)
            if not template:
                return {
                    'success': False,
                    'error': f'Template {template_id} not found'
                }
            
            # Create agent instance
            agent_instance = AgentInstance(
                id=str(uuid.uuid4()),
                template_id=template_id,
                name=deployment_config.get('name', template.name),
                status='deploying',
                config={**template.default_config, **deployment_config.get('config', {})},
                performance_metrics={
                    'tasks_completed': 0,
                    'success_rate': 0.0,
                    'avg_response_time': 0.0,
                    'uptime': 0.0
                },
                created_at=datetime.now().isoformat(),
                owner_id=user_id
            )
            
            # Deploy agent (simulate deployment process)
            deployment_result = await self._deploy_agent_instance(agent_instance, template)
            
            if deployment_result['success']:
                agent_instance.status = 'active'
                agent_instance.deployed_at = datetime.now().isoformat()
                agent_instance.last_activity = datetime.now().isoformat()
                
                # Store active agent
                self.active_agents[agent_instance.id] = agent_instance
                self._save_agent_instance(agent_instance)
                
                return {
                    'success': True,
                    'agent': asdict(agent_instance),
                    'deployment_info': deployment_result['info']
                }
            else:
                agent_instance.status = 'error'
                return {
                    'success': False,
                    'error': deployment_result['error']
                }
                
        except Exception as e:
            self.logger.error(f"Agent deployment failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    async def manage_agent(self, 
                         agent_id: str,
                         action: str,
                         user_id: str) -> Dict[str, Any]:
        """
        [TOOL] Manage agent lifecycle (start, stop, pause, update)
        """
        try:
            if agent_id not in self.active_agents:
                return {
                    'success': False,
                    'error': f'Agent {agent_id} not found'
                }
            
            agent = self.active_agents[agent_id]
            
            # Verify ownership
            if agent.owner_id != user_id:
                return {
                    'success': False,
                    'error': 'Access denied: not agent owner'
                }
            
            if action == 'stop':
                agent.status = 'stopped'
            elif action == 'pause':
                agent.status = 'paused'
            elif action == 'start':
                agent.status = 'active'
                agent.last_activity = datetime.now().isoformat()
            elif action == 'restart':
                agent.status = 'active'
                agent.last_activity = datetime.now().isoformat()
            else:
                return {
                    'success': False,
                    'error': f'Unknown action: {action}'
                }
            
            # Update agent
            self._save_agent_instance(agent)
            
            return {
                'success': True,
                'agent': asdict(agent),
                'action_performed': action
            }
            
        except Exception as e:
            self.logger.error(f"Agent management failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_agent_templates(self, template_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get available agent templates"""
        templates = []
        
        try:
            for filename in os.listdir(self.templates_storage_path):
                if filename.endswith('.json'):
                    template = self._load_template(filename[:-5])  # Remove .json
                    if template and (not template_type or template.type == template_type):
                        templates.append(asdict(template))
                        
        except Exception as e:
            self.logger.error(f"Failed to load templates: {str(e)}")
        
        return templates

    def get_user_agents(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all agents owned by user"""
        user_agents = []
        
        for agent in self.active_agents.values():
            if agent.owner_id == user_id:
                user_agents.append(asdict(agent))
        
        return user_agents

    async def get_agent_performance(self, agent_id: str) -> Dict[str, Any]:
        """Get detailed performance metrics for agent"""
        if agent_id not in self.active_agents:
            return {'error': 'Agent not found'}
        
        agent = self.active_agents[agent_id]
        
        # Calculate real-time metrics
        performance = {
            **agent.performance_metrics,
            'current_status': agent.status,
            'uptime_hours': self._calculate_uptime(agent),
            'last_activity': agent.last_activity,
            'deployment_age_hours': self._calculate_deployment_age(agent)
        }
        
        return performance

    # Helper methods
    async def _enhance_agent_spec_with_mama_bear(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Use Mama Bear to enhance agent specification"""
        try:
            prompt = f"""
            Analyze and enhance this agent specification:
            {json.dumps(spec, indent=2)}
            
            Please provide:
            1. Enhanced capabilities list
            2. Optimized configuration settings
            3. Implementation recommendations
            4. Performance optimization suggestions
            """
            
            response = await enhanced_scout_orchestrator.process_request(
                prompt=prompt,
                request_type="agent_design",
                context={"spec": spec}
            )
            
            # Parse Mama Bear's response
            enhanced_spec = {
                **spec,
                'capabilities': response.get('enhanced_capabilities', spec.get('capabilities', [])),
                'config': response.get('optimized_config', spec.get('config', {})),
                'recommendations': response.get('recommendations', [])
            }
            
            return enhanced_spec
            
        except Exception as e:
            self.logger.error(f"Mama Bear enhancement failed: {str(e)}")
            return spec

    async def _generate_agent_implementation(self, template: AgentTemplate) -> Dict[str, Any]:
        """Generate implementation code for agent"""
        try:
            prompt = f"""
            Generate implementation code for this agent template:
            Name: {template.name}
            Type: {template.type}
            Capabilities: {template.capabilities}
            Config: {template.default_config}
            
            Generate:
            1. Main agent class
            2. Required methods
            3. Configuration handling
            4. Error handling
            5. Performance monitoring
            """
            
            response = await enhanced_scout_orchestrator.process_request(
                prompt=prompt,
                request_type="code_generation",
                context={"template": asdict(template)}
            )
            
            return {
                'main_class': response.get('main_class', ''),
                'methods': response.get('methods', []),
                'dependencies': response.get('dependencies', []),
                'setup_instructions': response.get('setup_instructions', [])
            }
            
        except Exception as e:
            self.logger.error(f"Implementation generation failed: {str(e)}")
            return {'error': str(e)}

    async def _deploy_agent_instance(self, agent: AgentInstance, template: AgentTemplate) -> Dict[str, Any]:
        """Deploy agent instance (simulated)"""
        try:
            # Simulate deployment process
            await asyncio.sleep(1)  # Simulate deployment time
            
            return {
                'success': True,
                'info': {
                    'deployment_id': f"deploy_{agent.id[:8]}",
                    'endpoint': f"/agents/{agent.id}",
                    'health_check': f"/agents/{agent.id}/health",
                    'metrics': f"/agents/{agent.id}/metrics"
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _save_template(self, template: AgentTemplate):
        """Save agent template to storage"""
        try:
            template_path = os.path.join(self.templates_storage_path, f"{template.id}.json")
            with open(template_path, 'w') as f:
                json.dump(asdict(template), f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save template: {str(e)}")

    def _load_template(self, template_id: str) -> Optional[AgentTemplate]:
        """Load agent template from storage"""
        try:
            template_path = os.path.join(self.templates_storage_path, f"{template_id}.json")
            if os.path.exists(template_path):
                with open(template_path, 'r') as f:
                    data = json.load(f)
                return AgentTemplate(**data)
        except Exception as e:
            self.logger.error(f"Failed to load template: {str(e)}")
        return None

    def _save_agent_instance(self, agent: AgentInstance):
        """Save agent instance to storage"""
        try:
            agent_path = os.path.join(self.agents_storage_path, f"{agent.id}.json")
            with open(agent_path, 'w') as f:
                json.dump(asdict(agent), f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save agent instance: {str(e)}")

    def _load_active_agents(self):
        """Load active agents from storage"""
        try:
            for filename in os.listdir(self.agents_storage_path):
                if filename.endswith('.json'):
                    agent_path = os.path.join(self.agents_storage_path, filename)
                    with open(agent_path, 'r') as f:
                        data = json.load(f)
                    agent = AgentInstance(**data)
                    if agent.status in ['active', 'paused']:
                        self.active_agents[agent.id] = agent
        except Exception as e:
            self.logger.error(f"Failed to load active agents: {str(e)}")

    def _calculate_uptime(self, agent: AgentInstance) -> float:
        """Calculate agent uptime in hours"""
        if not agent.deployed_at:
            return 0.0
        
        deployed = datetime.fromisoformat(agent.deployed_at)
        now = datetime.now()
        return (now - deployed).total_seconds() / 3600

    def _calculate_deployment_age(self, agent: AgentInstance) -> float:
        """Calculate deployment age in hours"""
        created = datetime.fromisoformat(agent.created_at)
        now = datetime.now()
        return (now - created).total_seconds() / 3600

# Global instance
agent_workbench = AgentCreationWorkbench()
