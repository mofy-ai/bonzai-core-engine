# backend/services/enhanced_gemini_scout_orchestration.py
"""
[TARGET] Enhanced Mama Bear Scout with Complete Gemini 2.5 Model Orchestration
Autonomous quota management and intelligent routing for production workflows
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import google.generativeai as genai
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

class WorkflowStage(Enum):
    PLANNING = "planning"
    ENVIRONMENT = "environment" 
    CODING = "coding"
    TESTING = "testing"
    DEPLOYMENT = "deployment"

class ModelTier(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    FALLBACK = "fallback"
    EMERGENCY = "emergency"

@dataclass
class QuotaStatus:
    model_id: str
    requests_per_minute: int = 60
    requests_per_day: int = 1500
    current_minute_count: int = 0
    current_day_count: int = 0
    last_reset_minute: datetime = field(default_factory=datetime.now)
    last_reset_day: datetime = field(default_factory=datetime.now)
    consecutive_errors: int = 0
    last_error_time: Optional[datetime] = None
    is_healthy: bool = True
    cooldown_until: Optional[datetime] = None
    
    @property
    def minute_quota_available(self) -> float:
        return max(0, self.requests_per_minute - self.current_minute_count) / self.requests_per_minute
    
    @property
    def day_quota_available(self) -> float:
        return max(0, self.requests_per_day - self.current_day_count) / self.requests_per_day
    
    @property
    def overall_health_score(self) -> float:
        if not self.is_healthy or self.cooldown_until and self.cooldown_until > datetime.now():
            return 0.0
        health = min(self.minute_quota_available, self.day_quota_available)
        error_penalty = max(0, 1 - (self.consecutive_errors * 0.2))
        return health * error_penalty

class EnhancedGeminiScoutOrchestrator:
    """
    [TARGET] Complete Gemini 2.5 Scout Orchestration System
    Handles autonomous quota management and intelligent model routing
    """
    
    def __init__(self, gemini_api_key: str):
        self.api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        
        # Complete Gemini 2.5 Model Configuration
        self.gemini_models = self._initialize_complete_model_registry()
        
        # Quota management
        self.quota_status: Dict[str, QuotaStatus] = {}
        self.request_history = deque(maxlen=10000)
        
        # Scout workflow state
        self.active_workflows: Dict[str, Dict] = {}
        self.model_performance_cache = defaultdict(list)
        
        # Autonomous routing configuration
        self.routing_preferences = self._configure_routing_preferences()
        
        # Initialize quota tracking
        self._initialize_quota_tracking()
        
        logger.info("[TARGET] Enhanced Gemini Scout Orchestrator initialized with complete model coverage")
    
    def _initialize_complete_model_registry(self) -> Dict[str, Dict[str, Any]]:
        """Initialize complete Gemini 2.5 model registry with Scout-specific configurations"""
        
        return {
            # PRIMARY TIER - Latest and most capable
            "gemini-2.5-pro-preview-06-05": {
                "tier": ModelTier.PRIMARY,
                "context_window": 1048576,
                "output_limit": 65536,
                "rpm_limit": 60,
                "rpd_limit": 1500,
                "specialties": ["orchestration", "complex_planning", "architecture"],
                "scout_roles": ["master_planner", "architect", "orchestrator"],
                "workflow_stages": [WorkflowStage.PLANNING, WorkflowStage.DEPLOYMENT],
                "cost_tier": "high",
                "latency": "medium"
            },
            
            "gemini-2.5-pro-preview-05-06": {
                "tier": ModelTier.PRIMARY,
                "context_window": 1048576,
                "output_limit": 65536,
                "rpm_limit": 60,
                "rpd_limit": 1500,
                "specialties": ["strategic_planning", "system_design"],
                "scout_roles": ["strategic_planner", "system_architect"],
                "workflow_stages": [WorkflowStage.PLANNING, WorkflowStage.ENVIRONMENT],
                "cost_tier": "high",
                "latency": "medium"
            },
            
            "gemini-2.5-pro-preview-03-25": {
                "tier": ModelTier.SECONDARY,
                "context_window": 1048576,
                "output_limit": 65536,
                "rpm_limit": 60,
                "rpd_limit": 1500,
                "specialties": ["batch_processing", "bulk_operations"],
                "scout_roles": ["batch_processor", "bulk_generator"],
                "workflow_stages": [WorkflowStage.CODING, WorkflowStage.TESTING],
                "cost_tier": "high",
                "latency": "slow"
            },
            
            # SECONDARY TIER - Fast and efficient
            "gemini-2.5-flash-preview-05-20": {
                "tier": ModelTier.SECONDARY,
                "context_window": 1048576,
                "output_limit": 65536,
                "rpm_limit": 120,
                "rpd_limit": 3000,
                "specialties": ["rapid_development", "code_generation"],
                "scout_roles": ["rapid_developer", "code_generator"],
                "workflow_stages": [WorkflowStage.CODING, WorkflowStage.TESTING],
                "cost_tier": "medium",
                "latency": "fast"
            },
            
            "gemini-2.5-flash-preview-04-17": {
                "tier": ModelTier.SECONDARY,
                "context_window": 1048576,
                "output_limit": 65536,
                "rpm_limit": 120,
                "rpd_limit": 3000,
                "specialties": ["fast_prototyping", "quick_iteration"],
                "scout_roles": ["prototyper", "iterator"],
                "workflow_stages": [WorkflowStage.ENVIRONMENT, WorkflowStage.CODING],
                "cost_tier": "medium",
                "latency": "fast"
            },
            
            # SPECIALIZED TIER - Thinking and reasoning
            "gemini-2.5-flash-preview-04-17-thinking": {
                "tier": ModelTier.FALLBACK,
                "context_window": 1048576,
                "output_limit": 65536,
                "rpm_limit": 60,
                "rpd_limit": 1500,
                "specialties": ["complex_reasoning", "debugging", "optimization"],
                "scout_roles": ["debugger", "optimizer", "problem_solver"],
                "workflow_stages": [WorkflowStage.TESTING, WorkflowStage.DEPLOYMENT],
                "cost_tier": "medium",
                "latency": "slow"
            },
            
            # EMERGENCY TIER - Fallback options
            "gemini-1.5-pro": {
                "tier": ModelTier.EMERGENCY,
                "context_window": 2000000,  # Largest context window
                "output_limit": 8192,
                "rpm_limit": 60,
                "rpd_limit": 1500,
                "specialties": ["large_context", "emergency_fallback"],
                "scout_roles": ["context_master", "emergency_backup"],
                "workflow_stages": [WorkflowStage.PLANNING, WorkflowStage.CODING],
                "cost_tier": "medium",
                "latency": "medium"
            },
            
            "gemini-1.5-flash": {
                "tier": ModelTier.EMERGENCY,
                "context_window": 1000000,
                "output_limit": 8192,
                "rpm_limit": 120,
                "rpd_limit": 3000,
                "specialties": ["emergency_speed", "basic_tasks"],
                "scout_roles": ["emergency_responder", "basic_assistant"],
                "workflow_stages": [WorkflowStage.ENVIRONMENT, WorkflowStage.TESTING],
                "cost_tier": "low",
                "latency": "ultra_fast"
            }
        }
    
    def _configure_routing_preferences(self) -> Dict[str, List[str]]:
        """Configure stage-specific model routing preferences"""
        return {
            WorkflowStage.PLANNING.value: [
                "gemini-2.5-pro-preview-06-05",  # Master orchestrator
                "gemini-2.5-pro-preview-05-06",  # Strategic planner
                "gemini-1.5-pro"  # Emergency large context
            ],
            WorkflowStage.ENVIRONMENT.value: [
                "gemini-2.5-flash-preview-04-17",  # Fast prototyping
                "gemini-2.5-pro-preview-05-06",   # System architect
                "gemini-1.5-flash"  # Emergency speed
            ],
            WorkflowStage.CODING.value: [
                "gemini-2.5-flash-preview-05-20",  # Rapid development
                "gemini-2.5-pro-preview-03-25",   # Batch processing
                "gemini-2.5-flash-preview-04-17", # Fast prototyping
                "gemini-1.5-pro"  # Large context backup
            ],
            WorkflowStage.TESTING.value: [
                "gemini-2.5-flash-preview-04-17-thinking",  # Complex reasoning
                "gemini-2.5-flash-preview-05-20",          # Rapid testing
                "gemini-2.5-pro-preview-03-25",           # Batch testing
                "gemini-1.5-flash"  # Emergency
            ],
            WorkflowStage.DEPLOYMENT.value: [
                "gemini-2.5-pro-preview-06-05",            # Master orchestrator
                "gemini-2.5-flash-preview-04-17-thinking", # Complex reasoning
                "gemini-1.5-pro"  # Emergency backup
            ]
        }
    
    def _initialize_quota_tracking(self):
        """Initialize quota tracking for all models"""
        for model_id, config in self.gemini_models.items():
            self.quota_status[model_id] = QuotaStatus(
                model_id=model_id,
                requests_per_minute=config["rpm_limit"],
                requests_per_day=config["rpd_limit"]
            )
    
    def _update_quota_tracking(self, model_id: str, success: bool = True):
        """Update quota tracking after a request"""
        if model_id not in self.quota_status:
            return
        
        status = self.quota_status[model_id]
        now = datetime.now()
        
        # Reset counters if needed
        if now - status.last_reset_minute >= timedelta(minutes=1):
            status.current_minute_count = 0
            status.last_reset_minute = now
        
        if now - status.last_reset_day >= timedelta(days=1):
            status.current_day_count = 0
            status.last_reset_day = now
        
        # Update counts
        status.current_minute_count += 1
        status.current_day_count += 1
        
        # Update health status
        if success:
            status.consecutive_errors = 0
            status.is_healthy = True
            status.cooldown_until = None
        else:
            status.consecutive_errors += 1
            status.last_error_time = now
            
            # Set cooldown for problematic models
            if status.consecutive_errors >= 3:
                status.is_healthy = False
                status.cooldown_until = now + timedelta(minutes=5)
        
        # Log performance data
        self.model_performance_cache[model_id].append({
            'timestamp': now,
            'success': success,
            'minute_quota': status.minute_quota_available,
            'day_quota': status.day_quota_available
        })
        
        # Keep only recent performance data
        if len(self.model_performance_cache[model_id]) > 1000:
            self.model_performance_cache[model_id] = self.model_performance_cache[model_id][-500:]
    
    def get_best_model_for_stage(self, stage: WorkflowStage) -> Optional[str]:
        """Get the best available model for a specific workflow stage"""
        stage_preferences = self.routing_preferences.get(stage.value, [])
        
        # Score and rank available models
        model_scores = []
        for model_id in stage_preferences:
            if model_id not in self.quota_status:
                continue
                
            status = self.quota_status[model_id]
            health_score = status.overall_health_score
            
            if health_score > 0:
                model_scores.append((model_id, health_score))
        
        # Sort by health score (descending)
        model_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return the best available model
        if model_scores:
            best_model = model_scores[0][0]
            logger.info(f"[TARGET] Selected {best_model} for {stage.value} (health: {model_scores[0][1]:.2f})")
            return best_model
        
        logger.warning(f"[ERROR] No healthy models available for {stage.value}")
        return None
    
    async def execute_workflow_stage(self, stage: WorkflowStage, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific workflow stage with the best available model"""
        model_id = self.get_best_model_for_stage(stage)
        if not model_id:
            return {
                'success': False,
                'error': f'No models available for {stage.value}',
                'stage': stage.value
            }
        
        try:
            # Get model configuration
            model_config = self.gemini_models[model_id]
            
            # Configure the model
            model = genai.GenerativeModel(model_id)
            
            # Create enhanced prompt with stage-specific instructions
            enhanced_prompt = self._create_stage_prompt(stage, prompt, context, model_config)
            
            # Execute the request
            start_time = time.time()
            response = await model.generate_content_async(enhanced_prompt)
            duration = time.time() - start_time
            
            # Update quota tracking
            self._update_quota_tracking(model_id, success=True)
            
            result = {
                'success': True,
                'content': response.text,
                'stage': stage.value,
                'model_used': model_id,
                'duration': duration,
                'metadata': {
                    'model_tier': model_config['tier'].value,
                    'specialties': model_config['specialties'],
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            logger.info(f"[OK] {stage.value} completed with {model_id} in {duration:.2f}s")
            return result
            
        except Exception as e:
            # Update quota tracking for failure
            self._update_quota_tracking(model_id, success=False)
            
            logger.error(f"[ERROR] {stage.value} failed with {model_id}: {e}")
            
            # Try fallback model if available
            fallback_model = self._get_fallback_model(stage, model_id)
            if fallback_model:
                logger.info(f"[SYNC] Retrying {stage.value} with fallback model {fallback_model}")
                return await self._execute_with_fallback(stage, prompt, context, fallback_model)
            
            return {
                'success': False,
                'error': str(e),
                'stage': stage.value,
                'failed_model': model_id
            }
    
    def _create_stage_prompt(self, stage: WorkflowStage, prompt: str, context: Dict[str, Any], model_config: Dict[str, Any]) -> str:
        """Create stage-specific enhanced prompts"""
        
        stage_instructions = {
            WorkflowStage.PLANNING: """
[TARGET] PLANNING PHASE - Master Orchestrator
Your role: Strategic planner and project architect
Focus: Create comprehensive project roadmap with technical specifications

Requirements:
- Analyze project scope and complexity
- Define technology stack and architecture
- Create detailed implementation phases
- Identify potential challenges and solutions
- Estimate timeline and resources needed
""",
            WorkflowStage.ENVIRONMENT: """
[TOOLS] ENVIRONMENT PHASE - Infrastructure Setup
Your role: DevOps engineer and environment architect
Focus: Configure development and deployment environments

Requirements:
- Set up development environment
- Configure build tools and dependencies
- Prepare deployment infrastructure
- Establish CI/CD pipeline foundations
- Ensure security and performance optimization
""",
            WorkflowStage.CODING: """
[LAPTOP] CODING PHASE - Full-Stack Developer
Your role: Senior full-stack developer
Focus: Implement the complete application with best practices

Requirements:
- Write clean, maintainable, and efficient code
- Follow coding standards and patterns
- Implement proper error handling
- Add comprehensive logging
- Create reusable components and modules
""",
            WorkflowStage.TESTING: """
[LAB] TESTING PHASE - Quality Assurance Engineer
Your role: Senior QA engineer and testing specialist
Focus: Comprehensive testing and quality validation

Requirements:
- Create unit tests for all components
- Implement integration tests
- Perform end-to-end testing scenarios
- Validate performance and security
- Document test results and coverage
""",
            WorkflowStage.DEPLOYMENT: """
[LAUNCH] DEPLOYMENT PHASE - Release Engineer
Your role: Release manager and deployment specialist
Focus: Production deployment and monitoring setup

Requirements:
- Deploy to production environment
- Configure monitoring and alerting
- Set up backup and recovery systems
- Validate deployment success
- Document deployment procedures
"""
        }
        
        enhanced_prompt = f"""
{stage_instructions.get(stage, '')}

CONTEXT:
{json.dumps(context, indent=2)}

TASK:
{prompt}

MODEL CAPABILITIES:
- Specialties: {', '.join(model_config['specialties'])}
- Context Window: {model_config['context_window']:,} tokens
- Tier: {model_config['tier'].value}

Please provide a detailed, actionable response that leverages your specific capabilities for this {stage.value} phase.
"""
        
        return enhanced_prompt
    
    def _get_fallback_model(self, stage: WorkflowStage, failed_model: str) -> Optional[str]:
        """Get a fallback model for the stage, excluding the failed one"""
        stage_preferences = self.routing_preferences.get(stage.value, [])
        
        for model_id in stage_preferences:
            if model_id != failed_model and model_id in self.quota_status:
                status = self.quota_status[model_id]
                if status.overall_health_score > 0:
                    return model_id
        
        # Try emergency tier models
        for model_id, config in self.gemini_models.items():
            if (config['tier'] == ModelTier.EMERGENCY and 
                model_id != failed_model and 
                model_id in self.quota_status):
                status = self.quota_status[model_id]
                if status.overall_health_score > 0:
                    return model_id
        
        return None
    
    async def _execute_with_fallback(self, stage: WorkflowStage, prompt: str, context: Dict[str, Any], fallback_model: str) -> Dict[str, Any]:
        """Execute stage with a specific fallback model"""
        try:
            model_config = self.gemini_models[fallback_model]
            model = genai.GenerativeModel(fallback_model)
            
            enhanced_prompt = self._create_stage_prompt(stage, prompt, context, model_config)
            
            start_time = time.time()
            response = await model.generate_content_async(enhanced_prompt)
            duration = time.time() - start_time
            
            self._update_quota_tracking(fallback_model, success=True)
            
            return {
                'success': True,
                'content': response.text,
                'stage': stage.value,
                'model_used': fallback_model,
                'duration': duration,
                'is_fallback': True,
                'metadata': {
                    'model_tier': model_config['tier'].value,
                    'specialties': model_config['specialties'],
                    'timestamp': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            self._update_quota_tracking(fallback_model, success=False)
            
            return {
                'success': False,
                'error': str(e),
                'stage': stage.value,
                'failed_fallback_model': fallback_model
            }
    
    async def execute_full_workflow(self, description: str, preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a complete Scout workflow from planning to deployment"""
        workflow_id = f"scout_{int(datetime.now().timestamp())}"
        
        # Initialize workflow tracking
        self.active_workflows[workflow_id] = {
            'description': description,
            'preferences': preferences or {},
            'started_at': datetime.now(),
            'stages': {},
            'current_stage': None,
            'status': 'running'
        }
        
        workflow_context = {
            'description': description,
            'preferences': preferences or {},
            'workflow_id': workflow_id,
            'completed_stages': {}
        }
        
        stages = [
            WorkflowStage.PLANNING,
            WorkflowStage.ENVIRONMENT,
            WorkflowStage.CODING,
            WorkflowStage.TESTING,
            WorkflowStage.DEPLOYMENT
        ]
        
        results = {}
        
        try:
            for stage in stages:
                logger.info(f"[TARGET] Starting {stage.value} phase for workflow {workflow_id}")
                
                # Update current stage
                self.active_workflows[workflow_id]['current_stage'] = stage.value
                
                # Create stage-specific prompt
                stage_prompt = self._create_workflow_stage_prompt(stage, description, workflow_context)
                
                # Execute stage
                result = await self.execute_workflow_stage(stage, stage_prompt, workflow_context)
                
                # Store results
                results[stage.value] = result
                self.active_workflows[workflow_id]['stages'][stage.value] = result
                
                if result['success']:
                    workflow_context['completed_stages'][stage.value] = result
                    logger.info(f"[OK] {stage.value} completed successfully")
                else:
                    logger.error(f"[ERROR] {stage.value} failed: {result.get('error', 'Unknown error')}")
                    # Continue with other stages even if one fails
            
            # Mark workflow as completed
            self.active_workflows[workflow_id]['status'] = 'completed'
            self.active_workflows[workflow_id]['completed_at'] = datetime.now()
            
            return {
                'success': True,
                'workflow_id': workflow_id,
                'results': results,
                'metadata': {
                    'started_at': self.active_workflows[workflow_id]['started_at'].isoformat(),
                    'completed_at': self.active_workflows[workflow_id]['completed_at'].isoformat(),
                    'total_stages': len(stages),
                    'successful_stages': sum(1 for r in results.values() if r['success']),
                    'models_used': list(set(r.get('model_used') for r in results.values() if r.get('model_used')))
                }
            }
            
        except Exception as e:
            self.active_workflows[workflow_id]['status'] = 'failed'
            self.active_workflows[workflow_id]['error'] = str(e)
            
            logger.error(f"[ERROR] Workflow {workflow_id} failed: {e}")
            
            return {
                'success': False,
                'workflow_id': workflow_id,
                'error': str(e),
                'partial_results': results
            }
    
    def _create_workflow_stage_prompt(self, stage: WorkflowStage, description: str, context: Dict[str, Any]) -> str:
        """Create comprehensive prompts for each workflow stage"""
        
        base_context = f"""
PROJECT DESCRIPTION: {description}
PREFERENCES: {json.dumps(context.get('preferences', {}), indent=2)}
"""
        
        if context.get('completed_stages'):
            base_context += f"\nCOMPLETED STAGES:\n{json.dumps(context['completed_stages'], indent=2)}"
        
        stage_prompts = {
            WorkflowStage.PLANNING: f"""
{base_context}

Create a comprehensive project plan including:
1. Technology stack analysis and recommendations
2. Project architecture and structure
3. Development phases and timeline
4. Required dependencies and tools
5. Potential challenges and mitigation strategies
6. Resource requirements and team structure
7. Success metrics and testing strategy

Provide actionable, detailed specifications that can guide the entire development process.
""",
            
            WorkflowStage.ENVIRONMENT: f"""
{base_context}

Set up the complete development environment including:
1. Development environment configuration
2. Required tools and dependencies installation
3. Project structure and scaffolding
4. Build system configuration
5. Development server setup
6. Environment variables and configuration
7. Git repository initialization
8. CI/CD pipeline foundation

Provide specific commands and configurations for environment setup.
""",
            
            WorkflowStage.CODING: f"""
{base_context}

Implement the complete application including:
1. Core application logic and features
2. User interface components and styling
3. Backend API and database integration
4. Authentication and authorization
5. Error handling and validation
6. Performance optimization
7. Security implementation
8. Documentation and code comments

Provide production-ready, well-structured code with best practices.
""",
            
            WorkflowStage.TESTING: f"""
{base_context}

Create comprehensive testing suite including:
1. Unit tests for all components and functions
2. Integration tests for API endpoints
3. End-to-end testing scenarios
4. Performance and load testing
5. Security testing and validation
6. Accessibility testing
7. Cross-browser compatibility testing
8. Test automation and CI integration

Provide complete test coverage with detailed test scenarios.
""",
            
            WorkflowStage.DEPLOYMENT: f"""
{base_context}

Deploy the application to production including:
1. Production environment setup
2. Build optimization and minification
3. Deployment configuration and scripts
4. SSL certificate and domain configuration
5. Monitoring and logging setup
6. Backup and recovery procedures
7. Performance monitoring
8. Security hardening and compliance

Provide complete deployment instructions and monitoring setup.
"""
        }
        
        return stage_prompts.get(stage, f"{base_context}\n\nExecute {stage.value} phase tasks.")
    
    def get_orchestration_status(self) -> Dict[str, Any]:
        """Get current orchestration status and model health"""
        healthy_models = sum(1 for status in self.quota_status.values() if status.is_healthy)
        
        model_status = {}
        for model_id, status in self.quota_status.items():
            config = self.gemini_models[model_id]
            model_status[model_id] = {
                'id': model_id,
                'name': model_id.replace('-', ' ').title(),
                'tier': config['tier'].value,
                'health_score': status.overall_health_score,
                'quota_usage': {
                    'minute': f"{status.current_minute_count}/{status.requests_per_minute}",
                    'day': f"{status.current_day_count}/{status.requests_per_day}"
                },
                'performance': {
                    'success_rate': self._calculate_success_rate(model_id),
                    'consecutive_errors': status.consecutive_errors
                },
                'specialties': config['specialties'],
                'is_healthy': status.is_healthy,
                'cooldown_until': status.cooldown_until.isoformat() if status.cooldown_until else None
            }
        
        return {
            'active_workflows': len(self.active_workflows),
            'total_models': len(self.gemini_models),
            'healthy_models': healthy_models,
            'model_status': model_status,
            'routing_preferences': self.routing_preferences
        }
    
    def _calculate_success_rate(self, model_id: str) -> float:
        """Calculate recent success rate for a model"""
        recent_performance = self.model_performance_cache.get(model_id, [])
        if not recent_performance:
            return 1.0  # Default to 100% for new models
        
        # Look at last 10 requests
        recent = recent_performance[-10:]
        if not recent:
            return 1.0
        
        success_count = sum(1 for p in recent if p['success'])
        return success_count / len(recent)
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific workflow"""
        if workflow_id not in self.active_workflows:
            return None
        
        workflow = self.active_workflows[workflow_id]
        
        # Calculate progress
        total_stages = 5  # Planning, Environment, Coding, Testing, Deployment
        completed_stages = sum(1 for stage in workflow['stages'].values() if stage.get('success'))
        progress = (completed_stages / total_stages) * 100
        
        # Prepare stage information
        stages = []
        stage_names = ['planning', 'environment', 'coding', 'testing', 'deployment']
        
        for stage_name in stage_names:
            stage_info = workflow['stages'].get(stage_name, {})
            stages.append({
                'name': stage_name,
                'status': 'completed' if stage_info.get('success') else 'failed' if stage_name in workflow['stages'] else 'pending',
                'model_used': stage_info.get('model_used'),
                'duration': stage_info.get('duration'),
                'completed_at': stage_info.get('metadata', {}).get('timestamp')
            })
        
        return {
            'workflow_id': workflow_id,
            'status': workflow['status'],
            'progress': progress,
            'stages': stages,
            'metadata': {
                'started_at': workflow['started_at'].isoformat(),
                'models_used': list(set(s.get('model_used') for s in workflow['stages'].values() if s.get('model_used'))),
                'total_requests': len(workflow['stages']),
                'quota_switches': self._count_quota_switches(workflow)
            },
            'current_stage': workflow.get('current_stage')
        }
    
    def _count_quota_switches(self, workflow: Dict[str, Any]) -> int:
        """Count how many times models were switched due to quota issues"""
        models_used = [s.get('model_used') for s in workflow['stages'].values() if s.get('model_used')]
        fallbacks_used = sum(1 for s in workflow['stages'].values() if s.get('is_fallback'))
        return fallbacks_used

# Global instance for the application
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize with API key from environment
gemini_api_key = os.getenv('GEMINI_API_KEY_PRIMARY') or os.getenv('GOOGLE_API_KEY')
if not gemini_api_key:
    logger.warning("[EMOJI] No Gemini API key found in environment variables")
    enhanced_scout_orchestrator = None
else:
    enhanced_scout_orchestrator = EnhancedGeminiScoutOrchestrator(gemini_api_key)
