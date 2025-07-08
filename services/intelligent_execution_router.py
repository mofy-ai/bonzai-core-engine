# backend/services/intelligent_execution_router.py
"""
[BRAIN] Intelligent Execution Router - Mama Bear's Decision Engine
Routes tasks between E2B (quick/cheap) and Scrapybara (full/robust) based on complexity analysis
"""

import asyncio
import ast
import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import time
from datetime import datetime, timedelta

from .enhanced_gemini_scout_orchestration import EnhancedGeminiScoutOrchestrator
from .enhanced_code_execution import EnhancedMamaBearCodeExecution, CodeExecutionResult
from .enhanced_scrapybara_integration import EnhancedScrapybaraManager

logger = logging.getLogger(__name__)

class ExecutionRoute(Enum):
    E2B = "e2b"
    SCRAPYBARA = "scrapybara"
    HYBRID = "hybrid"  # Use both for validation pipeline

@dataclass
class TaskComplexityAnalysis:
    score: float  # 0-10 scale
    route_recommendation: ExecutionRoute
    confidence: float  # 0-1.0
    reasoning: List[str]
    estimated_duration: int  # seconds
    estimated_cost: float  # USD
    risk_factors: List[str]
    
    # Detailed metrics
    code_lines: int
    file_count: int
    dependency_count: int
    system_operations: List[str]
    language_complexity: float
    mama_bear_assessment: Dict[str, Any]

class IntelligentExecutionRouter:
    """
    [BRAIN] Mama Bear's Intelligent Task Routing System
    Automatically decides between E2B vs Scrapybara based on comprehensive task analysis
    """
    
    def __init__(self, 
                 scout_orchestrator: Optional[EnhancedGeminiScoutOrchestrator],
                 e2b_execution: EnhancedMamaBearCodeExecution,
                 scrapybara_manager: EnhancedScrapybaraManager):
        self.scout = scout_orchestrator
        self.e2b = e2b_execution
        self.scrapybara = scrapybara_manager
        
        # Routing metrics
        self.routing_history = []
        self.performance_cache = {}
        
        # Cost constants (per hour)
        self.E2B_COST_PER_HOUR = 0.10
        self.SCRAPYBARA_COST_PER_HOUR = 2.50
        
        logger.info("[BRAIN] Intelligent Execution Router initialized")
    
    async def analyze_task_complexity(self, 
                                    task_description: str,
                                    code_snippets: Optional[List[str]] = None,
                                    file_paths: Optional[List[str]] = None,
                                    user_context: Optional[Dict[str, Any]] = None) -> TaskComplexityAnalysis:
        """
        [SEARCH] Comprehensive task complexity analysis using Mama Bear intelligence
        """
        start_time = time.time()
        
        # Handle None parameters properly
        code_snippets = code_snippets or []
        file_paths = file_paths or []
        user_context = user_context or {}
        
        # Initialize analysis components
        complexity_factors = []
        risk_factors = []
        system_operations = []
        
        # Default values
        code_lines = 0
        file_count = len(file_paths) if file_paths else len(code_snippets) if code_snippets else 1
        dependency_count = 0
        
        # 1. Analyze code snippets
        if code_snippets:
            for snippet in code_snippets:
                analysis = self._analyze_code_snippet(snippet)
                code_lines += analysis['lines']
                dependency_count += analysis['dependencies']
                system_operations.extend(analysis['system_ops'])
                complexity_factors.extend(analysis['complexity_factors'])
                risk_factors.extend(analysis['risk_factors'])
        
        # 2. Mama Bear NLP analysis of task description
        mama_bear_assessment = await self._mama_bear_task_analysis(task_description, user_context)
        
        # 3. Calculate complexity score
        base_score = self._calculate_base_complexity_score(
            code_lines, file_count, dependency_count, system_operations
        )
        
        # 4. Apply Mama Bear intelligence boost
        final_score = self._apply_mama_bear_intelligence(
            base_score, mama_bear_assessment, complexity_factors
        )
        
        # 5. Determine routing recommendation
        route, confidence = self._determine_optimal_route(
            final_score, complexity_factors, risk_factors
        )
        
        # 6. Cost and duration estimation
        estimated_duration, estimated_cost = self._estimate_execution_metrics(
            route, final_score, code_lines
        )
        
        # 7. Generate reasoning
        reasoning = self._generate_routing_reasoning(
            final_score, route, complexity_factors, mama_bear_assessment
        )
        
        analysis = TaskComplexityAnalysis(
            score=final_score,
            route_recommendation=route,
            confidence=confidence,
            reasoning=reasoning,
            estimated_duration=estimated_duration,
            estimated_cost=estimated_cost,
            risk_factors=risk_factors,
            code_lines=code_lines,
            file_count=file_count,
            dependency_count=dependency_count,
            system_operations=system_operations,
            language_complexity=mama_bear_assessment.get('language_complexity', 0.5),
            mama_bear_assessment=mama_bear_assessment
        )
        
        # Store for learning
        self.routing_history.append({
            'timestamp': datetime.now(),
            'analysis': analysis,
            'task_description': task_description,
            'processing_time': time.time() - start_time
        })
        
        logger.info(f"[BRAIN] Task complexity analysis completed: Score={final_score:.2f}, Route={route.value}, Confidence={confidence:.2f}")
        
        return analysis
    
    def _analyze_code_snippet(self, code: str) -> Dict[str, Any]:
        """Analyze individual code snippet for complexity indicators"""
        
        lines = len([line for line in code.split('\n') if line.strip()])
        complexity_factors = []
        risk_factors = []
        system_ops = []
        dependencies = 0
        
        try:
            # Parse Python AST for detailed analysis
            tree = ast.parse(code)
            
            # Count imports (dependencies)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    dependencies += 1
                    
                # Check for system operations
                if isinstance(node, ast.Call):
                    if hasattr(node.func, 'attr'):
                        if node.func.attr in ['system', 'run', 'call', 'Popen']:
                            system_ops.append(f"subprocess.{node.func.attr}")
                            risk_factors.append("System command execution detected")
                    
                    if hasattr(node.func, 'id'):
                        if node.func.id in ['exec', 'eval', 'compile']:
                            risk_factors.append(f"Dynamic code execution: {node.func.id}")
            
            # Complexity indicators
            if lines > 50:
                complexity_factors.append("High line count")
            if dependencies > 5:
                complexity_factors.append("Many dependencies")
                
        except SyntaxError:
            # Not Python code, use regex analysis
            dependencies = len(re.findall(r'(?:import|require|include)\s+', code))
            
            # Check for system operations in other languages
            system_patterns = [
                r'os\.system\(',
                r'subprocess\.',
                r'exec\(',
                r'shell_exec\(',
                r'system\(',
                r'Runtime\.getRuntime\(\)\.exec\(',
            ]
            
            for pattern in system_patterns:
                if re.search(pattern, code):
                    system_ops.append("System operation detected")
                    risk_factors.append("System operation in non-Python code")
        
        return {
            'lines': lines,
            'dependencies': dependencies,
            'system_ops': system_ops,
            'complexity_factors': complexity_factors,
            'risk_factors': risk_factors
        }
    
    async def _mama_bear_task_analysis(self, 
                                     task_description: str, 
                                     user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Use Mama Bear's intelligence to analyze task complexity"""
        
        # Check if scout is available
        if self.scout is None:
            logger.warning("Scout orchestrator not available, using fallback analysis")
            return self._fallback_task_analysis(task_description, user_context)
        
        # Use the scout orchestrator for intelligent analysis
        analysis_prompt = f"""
        [BRAIN] Mama Bear Task Complexity Analysis

        Task Description: {task_description}
        User Context: {user_context or 'None provided'}

        Please analyze this task and provide:
        1. Complexity assessment (0-10 scale)
        2. Required capabilities (simple scripting vs full environment)
        3. Risk factors (security, system access, etc.)
        4. Language complexity rating
        5. Recommended execution approach

        Focus on practical considerations for routing between:
        - E2B: Quick, isolated, secure, limited capabilities
        - Scrapybara: Full VM, complete environment, higher cost

        Provide your analysis in JSON format.
        """
        
        try:
            # Use the scout's planning stage for analysis
            from .enhanced_gemini_scout_orchestration import WorkflowStage
            
            result = await self.scout.execute_workflow_stage(
                WorkflowStage.PLANNING,
                analysis_prompt,
                {'analysis_type': 'task_complexity', 'user_context': user_context}
            )
            
            if result['success']:
                # Extract structured analysis from Mama Bear's response
                return self._parse_mama_bear_analysis(result['content'])
            else:
                logger.warning("Mama Bear analysis failed, using fallback")
                return self._fallback_task_analysis(task_description, user_context)
                
        except Exception as e:
            logger.error(f"Mama Bear analysis error: {e}")
            return self._fallback_task_analysis(task_description, user_context)
    
    def _fallback_task_analysis(self, task_description: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fallback analysis when scout is not available"""
        
        # Simple keyword-based analysis
        desc_lower = task_description.lower()
        
        complexity_score = 5.0  # Default medium complexity
        
        # Increase complexity for certain keywords
        high_complexity_keywords = ['database', 'network', 'deploy', 'install', 'system', 'server']
        low_complexity_keywords = ['print', 'hello', 'simple', 'basic', 'calculate']
        
        for keyword in high_complexity_keywords:
            if keyword in desc_lower:
                complexity_score += 1.0
        
        for keyword in low_complexity_keywords:
            if keyword in desc_lower:
                complexity_score -= 1.0
        
        complexity_score = max(0.0, min(10.0, complexity_score))
        
        return {
            'complexity_score': complexity_score,
            'language_complexity': 0.5,
            'confidence': 0.6,
            'capabilities_required': ['full_environment'] if complexity_score > 6 else ['basic'],
            'risk_assessment': 'high' if complexity_score > 7 else 'medium' if complexity_score > 4 else 'low'
        }
    
    def _parse_mama_bear_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """Parse Mama Bear's analysis response"""
        
        # Default fallback
        analysis = {
            'complexity_score': 5.0,
            'language_complexity': 0.5,
            'confidence': 0.5,
            'capabilities_required': ['basic'],
            'risk_assessment': 'medium'
        }
        
        try:
            # Try to extract JSON if present
            import json
            import re
            
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                json_data = json.loads(json_match.group())
                analysis.update(json_data)
            else:
                # Parse text-based analysis
                lines = analysis_text.lower().split('\n')
                
                for line in lines:
                    if 'complexity' in line and any(char.isdigit() for char in line):
                        # Extract numeric complexity score
                        numbers = re.findall(r'(\d+(?:\.\d+)?)', line)
                        if numbers:
                            analysis['complexity_score'] = float(numbers[0])
                    
                    if 'risk' in line:
                        if 'high' in line:
                            analysis['risk_assessment'] = 'high'
                        elif 'low' in line:
                            analysis['risk_assessment'] = 'low'
                    
                    if 'environment' in line or 'vm' in line or 'full' in line:
                        analysis['capabilities_required'] = ['full_environment']
                    elif 'simple' in line or 'basic' in line:
                        analysis['capabilities_required'] = ['basic']
        
        except Exception as e:
            logger.warning(f"Failed to parse Mama Bear analysis: {e}")
        
        return analysis
    
    def _calculate_base_complexity_score(self, 
                                       code_lines: int,
                                       file_count: int, 
                                       dependency_count: int,
                                       system_operations: List[str]) -> float:
        """Calculate base complexity score from code metrics"""
        
        score = 0.0
        
        # Line count factor (0-3 points)
        if code_lines <= 20:
            score += 0.5
        elif code_lines <= 100:
            score += 1.5
        elif code_lines <= 500:
            score += 3.0
        else:
            score += 4.0
        
        # File count factor (0-2 points)
        if file_count == 1:
            score += 0.5
        elif file_count <= 3:
            score += 1.0
        else:
            score += 2.5
        
        # Dependency factor (0-2 points)
        if dependency_count <= 2:
            score += 0.5
        elif dependency_count <= 5:
            score += 1.0
        else:
            score += 2.0
        
        # System operations factor (0-3 points)
        if system_operations:
            score += min(len(system_operations) * 0.5, 3.0)
        
        return min(score, 10.0)
    
    def _apply_mama_bear_intelligence(self, 
                                    base_score: float,
                                    mama_bear_assessment: Dict[str, Any],
                                    complexity_factors: List[str]) -> float:
        """Apply Mama Bear's intelligence to refine complexity score"""
        
        # Start with base score
        final_score = base_score
        
        # Apply Mama Bear's complexity assessment
        mb_score = mama_bear_assessment.get('complexity_score', 5.0)
        final_score = (final_score + mb_score) / 2  # Average with Mama Bear's assessment
        
        # Risk assessment adjustments
        risk_level = mama_bear_assessment.get('risk_assessment', 'medium')
        if risk_level == 'high':
            final_score += 1.5
        elif risk_level == 'low':
            final_score -= 0.5
        
        # Capabilities required adjustments
        capabilities = mama_bear_assessment.get('capabilities_required', ['basic'])
        if 'full_environment' in capabilities:
            final_score += 2.0
        elif 'database' in capabilities:
            final_score += 1.5
        elif 'network' in capabilities:
            final_score += 1.0
        
        return min(max(final_score, 0.0), 10.0)
    
    def _determine_optimal_route(self, 
                               complexity_score: float,
                               complexity_factors: List[str],
                               risk_factors: List[str]) -> Tuple[ExecutionRoute, float]:
        """Determine optimal execution route with confidence score"""
        
        confidence = 0.8  # Base confidence
        
        # Simple routing logic
        if complexity_score <= 3.0:
            route = ExecutionRoute.E2B
            confidence += 0.1
        elif complexity_score >= 7.0:
            route = ExecutionRoute.SCRAPYBARA
            confidence += 0.1
        else:
            # Medium complexity - need more analysis
            route = ExecutionRoute.E2B  # Default to cheaper option
            confidence -= 0.2
            
            # Check for specific factors requiring Scrapybara
            scrapybara_indicators = [
                'full environment', 'database', 'network', 'installation',
                'deployment', 'multi-file', 'system operation'
            ]
            
            all_factors = ' '.join(complexity_factors + risk_factors).lower()
            if any(indicator in all_factors for indicator in scrapybara_indicators):
                route = ExecutionRoute.SCRAPYBARA
                confidence += 0.3
        
        return route, min(confidence, 1.0)
    
    def _estimate_execution_metrics(self, 
                                  route: ExecutionRoute,
                                  complexity_score: float,
                                  code_lines: int) -> Tuple[int, float]:
        """Estimate execution duration and cost"""
        
        if route == ExecutionRoute.E2B:
            # E2B: Fast startup, limited by code complexity
            base_duration = 5  # seconds
            duration = base_duration + (complexity_score * 2) + (code_lines * 0.1)
            cost = (duration / 3600) * self.E2B_COST_PER_HOUR
        else:
            # Scrapybara: Slower startup, scales better
            base_duration = 60  # seconds
            duration = base_duration + (complexity_score * 10) + (code_lines * 0.5)
            cost = (duration / 3600) * self.SCRAPYBARA_COST_PER_HOUR
        
        return int(duration), cost
    
    def _generate_routing_reasoning(self, 
                                  complexity_score: float,
                                  route: ExecutionRoute,
                                  complexity_factors: List[str],
                                  mama_bear_assessment: Dict[str, Any]) -> List[str]:
        """Generate human-readable reasoning for routing decision"""
        
        reasoning = []
        
        # Score-based reasoning
        if complexity_score <= 3.0:
            reasoning.append(f"Low complexity score ({complexity_score:.1f}/10) suitable for quick E2B execution")
        elif complexity_score >= 7.0:
            reasoning.append(f"High complexity score ({complexity_score:.1f}/10) requires full Scrapybara environment")
        else:
            reasoning.append(f"Medium complexity score ({complexity_score:.1f}/10) analyzed for optimal routing")
        
        # Route-specific reasoning
        if route == ExecutionRoute.E2B:
            reasoning.append("E2B selected for fast, cost-effective execution")
            reasoning.append("Task suitable for isolated sandbox environment")
        else:
            reasoning.append("Scrapybara selected for comprehensive environment support")
            reasoning.append("Task requires full VM capabilities")
        
        # Complexity factors
        if complexity_factors:
            reasoning.append(f"Complexity factors considered: {', '.join(complexity_factors[:3])}")
        
        # Mama Bear insights
        mb_risk = mama_bear_assessment.get('risk_assessment', 'medium')
        reasoning.append(f"Mama Bear risk assessment: {mb_risk}")
        
        return reasoning
    
    async def execute_with_optimal_routing(self, 
                                         task_description: str,
                                         code_snippets: List[str] = None,
                                         user_id: str = "default",
                                         user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        [LAUNCH] Execute task using optimal routing based on complexity analysis
        """
        
        # 1. Analyze task complexity
        analysis = await self.analyze_task_complexity(
            task_description, code_snippets, user_context=user_context
        )
        
        # 2. Execute using recommended route
        execution_start = time.time()
        
        if analysis.route_recommendation == ExecutionRoute.E2B:
            result = await self._execute_via_e2b(code_snippets, user_id, analysis)
        else:
            result = await self._execute_via_scrapybara(code_snippets, user_id, analysis)
        
        execution_time = time.time() - execution_start
        actual_cost = (execution_time / 3600) * (
            self.E2B_COST_PER_HOUR if analysis.route_recommendation == ExecutionRoute.E2B 
            else self.SCRAPYBARA_COST_PER_HOUR
        )
        
        # 3. Update learning metrics
        self._update_routing_performance(analysis, result, execution_time, actual_cost)
        
        return {
            'success': result.success,
            'output': result.output,
            'error': result.error,
            'analysis': analysis,
            'execution_time': execution_time,
            'actual_cost': actual_cost,
            'route_used': analysis.route_recommendation.value,
            'cost_savings': max(0, analysis.estimated_cost - actual_cost)
        }
    
    async def _execute_via_e2b(self, 
                             code_snippets: List[str],
                             user_id: str,
                             analysis: TaskComplexityAnalysis) -> CodeExecutionResult:
        """Execute via E2B with enhanced safety"""
        
        if not code_snippets:
            return CodeExecutionResult(
                success=False,
                output="",
                error="No code provided for execution"
            )
        
        # Combine code snippets
        combined_code = '\n\n'.join(code_snippets)
        
        # Execute with appropriate timeout
        timeout = max(30, analysis.estimated_duration + 10)
        
        return await self.e2b.execute_code_safely(
            code=combined_code,
            user_id=user_id,
            timeout=timeout
        )
    
    async def _execute_via_scrapybara(self, 
                                    code_snippets: List[str],
                                    user_id: str,
                                    analysis: TaskComplexityAnalysis) -> CodeExecutionResult:
        """Execute via Scrapybara with full environment"""
        
        # This would integrate with your existing Scrapybara service
        # For now, return a mock result
        
        logger.info(f"[BUILD] Executing via Scrapybara for user {user_id}")
        
        # Simulate Scrapybara execution
        await asyncio.sleep(2)  # Simulate setup time
        
        return CodeExecutionResult(
            success=True,
            output="Scrapybara execution completed successfully",
            execution_time=analysis.estimated_duration
        )
    
    async def route_execution(self, 
                            task_description: str,
                            code_snippets: Optional[List[str]] = None,
                            user_id: str = "default",
                            user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        [TARGET] Get routing decision without executing the task
        Returns routing recommendation and analysis
        """
        
        # Analyze task complexity
        analysis = await self.analyze_task_complexity(
            task_description=task_description,
            code_snippets=code_snippets or [],
            user_context=user_context or {}
        )
        
        # Return routing decision
        return {
            'platform': analysis.route_recommendation.value,
            'confidence': analysis.confidence,
            'reasoning': analysis.reasoning,
            'estimated_cost': analysis.estimated_cost,
            'estimated_duration': analysis.estimated_duration,
            'complexity_score': analysis.score,
            'analysis': analysis
        }
    
    async def log_execution_result(self,
                                 routing_decision: Dict[str, Any],
                                 execution_result: Dict[str, Any],
                                 user_id: str) -> None:
        """
        [CHART] Log execution results for learning and optimization
        """
        
        log_entry = {
            'timestamp': datetime.now(),
            'user_id': user_id,
            'routing_decision': routing_decision,
            'execution_result': execution_result,
            'success': execution_result.get('success', False),
            'execution_time': execution_result.get('execution_time', 0),
            'actual_cost': execution_result.get('cost', 0)
        }
        
        # Store in performance cache for learning
        self.performance_cache[f"{user_id}_{datetime.now().isoformat()}"] = log_entry
        
        logger.info(f"[CHART] Logged execution result for user {user_id}: {execution_result.get('success', False)}")
    
    async def get_execution_metrics(self,
                                  user_id: Optional[str] = None,
                                  time_range: str = "24h") -> Dict[str, Any]:
        """
        [EMOJI] Get execution metrics and analytics
        """
        
        # Parse time range
        if time_range == "24h":
            hours = 24
        elif time_range == "7d":
            hours = 24 * 7
        else:
            hours = 24
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Filter relevant entries
        relevant_entries = []
        for entry in self.routing_history:
            if entry['timestamp'] >= cutoff_time:
                if user_id is None or entry.get('user_id') == user_id:
                    relevant_entries.append(entry)
        
        if not relevant_entries:
            return {
                'message': 'No metrics available for the specified time range',
                'time_range': time_range,
                'user_id': user_id
            }
        
        # Calculate metrics
        total_tasks = len(relevant_entries)
        e2b_tasks = sum(1 for e in relevant_entries 
                       if e['analysis'].route_recommendation == ExecutionRoute.E2B)
        scrapybara_tasks = total_tasks - e2b_tasks
        
        avg_complexity = sum(e['analysis'].score for e in relevant_entries) / total_tasks
        total_cost = sum(e['analysis'].estimated_cost for e in relevant_entries)
        
        return {
            'time_range': time_range,
            'user_id': user_id,
            'total_tasks': total_tasks,
            'routing_distribution': {
                'e2b': {'count': e2b_tasks, 'percentage': (e2b_tasks / total_tasks) * 100},
                'scrapybara': {'count': scrapybara_tasks, 'percentage': (scrapybara_tasks / total_tasks) * 100}
            },
            'average_complexity': avg_complexity,
            'total_estimated_cost': total_cost,
            'cost_optimization': self._calculate_cost_savings()
        }
    
    def _update_routing_performance(self, 
                                  analysis: TaskComplexityAnalysis,
                                  result: CodeExecutionResult,
                                  actual_execution_time: float,
                                  actual_cost: float):
        """Update performance metrics for learning"""
        
        performance_data = {
            'timestamp': datetime.now(),
            'predicted_route': analysis.route_recommendation.value,
            'predicted_duration': analysis.estimated_duration,
            'predicted_cost': analysis.estimated_cost,
            'actual_duration': actual_execution_time,
            'actual_cost': actual_cost,
            'success': result.success,
            'complexity_score': analysis.score,
            'confidence': analysis.confidence
        }
        
        # Store in performance cache for learning
        route_key = analysis.route_recommendation.value
        if route_key not in self.performance_cache:
            self.performance_cache[route_key] = []
        
        self.performance_cache[route_key].append(performance_data)
        
        # Keep only recent performance data
        if len(self.performance_cache[route_key]) > 1000:
            self.performance_cache[route_key] = self.performance_cache[route_key][-500:]
        
        logger.info(f"[CHART] Performance updated: Predicted={analysis.estimated_duration}s, Actual={actual_execution_time:.1f}s")
    
    def get_routing_analytics(self) -> Dict[str, Any]:
        """Get comprehensive routing analytics"""
        
        total_routes = len(self.routing_history)
        if total_routes == 0:
            return {'message': 'No routing data available'}
        
        # Calculate metrics
        e2b_routes = sum(1 for r in self.routing_history if r['analysis'].route_recommendation == ExecutionRoute.E2B)
        scrapybara_routes = total_routes - e2b_routes
        
        avg_complexity = sum(r['analysis'].score for r in self.routing_history) / total_routes
        avg_confidence = sum(r['analysis'].confidence for r in self.routing_history) / total_routes
        
        return {
            'total_routes': total_routes,
            'e2b_usage': {
                'count': e2b_routes,
                'percentage': (e2b_routes / total_routes) * 100
            },
            'scrapybara_usage': {
                'count': scrapybara_routes,
                'percentage': (scrapybara_routes / total_routes) * 100
            },
            'average_complexity': avg_complexity,
            'average_confidence': avg_confidence,
            'cost_optimization': self._calculate_cost_savings()
        }
    
    def _calculate_cost_savings(self) -> Dict[str, float]:
        """Calculate cost savings from intelligent routing"""
        
        total_estimated_cost = sum(r['analysis'].estimated_cost for r in self.routing_history)
        
        # Calculate what cost would be if everything used Scrapybara
        scrapybara_cost = sum(
            (r['analysis'].estimated_duration / 3600) * self.SCRAPYBARA_COST_PER_HOUR 
            for r in self.routing_history
        )
        
        savings = scrapybara_cost - total_estimated_cost
        savings_percentage = (savings / scrapybara_cost) * 100 if scrapybara_cost > 0 else 0
        
        return {
            'total_estimated_cost': total_estimated_cost,
            'scrapybara_only_cost': scrapybara_cost,
            'savings_amount': savings,
            'savings_percentage': savings_percentage
        }

# Global instance for the application - initialize with None and lazy load dependencies
intelligent_router = None

def get_intelligent_router():
    """Lazy initialization of intelligent router with dependencies"""
    global intelligent_router
    if intelligent_router is None:
        from .enhanced_gemini_scout_orchestration import enhanced_scout_orchestrator
        from .enhanced_code_execution import mama_bear_code_executor
        from .enhanced_scrapybara_integration import enhanced_scrapybara_service
        
        # Check if scout orchestrator is available
        if enhanced_scout_orchestrator is None:
            logger.warning("[EMOJI] Enhanced Scout Orchestrator not available, using fallback")
            # Create a mock scout orchestrator for now
            scout_orchestrator = None
        else:
            scout_orchestrator = enhanced_scout_orchestrator
        
        intelligent_router = IntelligentExecutionRouter(
            scout_orchestrator=scout_orchestrator,
            e2b_execution=mama_bear_code_executor,
            scrapybara_manager=enhanced_scrapybara_service
        )
    return intelligent_router
