"""
[SEARCH] Task Analyzer
Analyzes incoming requests to extract key characteristics for optimal routing
"""

import re
import logging
from typing import Dict, Any, List, Set, Optional, Tuple
from datetime import datetime
import json

from .model_registry import ModelCapability

logger = logging.getLogger(__name__)

class TaskAnalyzer:
    """Analyzes tasks to determine optimal model routing"""
    
    def __init__(self):
        self.analysis_patterns = self._initialize_patterns()
        self.complexity_indicators = self._initialize_complexity_indicators()
        self.mama_bear_patterns = self._initialize_mama_bear_patterns()
        
    def _initialize_patterns(self) -> Dict[str, List[str]]:
        """Initialize regex patterns for task classification"""
        
        return {
            "speed_required": [
                r"\b(quick|fast|urgent|immediate|asap|now|hurry)\b",
                r"\b(real.?time|live|instant)\b",
                r"\b(chat|message|respond)\b"
            ],
            
            "creativity_required": [
                r"\b(create|generate|design|build|make|write)\b",
                r"\b(creative|innovative|original|unique)\b",
                r"\b(brainstorm|ideate|imagine)\b",
                r"\b(story|poem|article|content)\b"
            ],
            
            "reasoning_required": [
                r"\b(analyze|debug|solve|figure out|understand)\b",
                r"\b(why|how|explain|reason|logic)\b",
                r"\b(complex|difficult|challenging)\b",
                r"\b(architecture|design pattern|algorithm)\b"
            ],
            
            "long_context": [
                r"\b(entire|whole|complete|full)\b.{0,20}\b(file|document|codebase)\b",
                r"\b(review|analyze|summarize)\b.{0,30}\b(large|big|massive)\b",
                r"\b(multiple files|many files|all files)\b"
            ],
            
            "long_output": [
                r"\b(detailed|comprehensive|complete|thorough)\b",
                r"\b(generate|create|write)\b.{0,30}\b(large|long|extensive)\b",
                r"\b(documentation|tutorial|guide|manual)\b",
                r"\b(full implementation|complete code|entire)\b"
            ],
            
            "code_generation": [
                r"\b(code|function|class|component|module)\b",
                r"\b(implement|program|develop|build)\b",
                r"\b(javascript|python|react|typescript|html|css)\b",
                r"\b(api|endpoint|service|database)\b"
            ],
            
            "audio_tts": [
                r"\b(speak|voice|audio|sound|tts|text.to.speech)\b",
                r"\b(read aloud|narrate|pronounce)\b",
                r"\b(voice interface|audio response)\b"
            ],
            
            "real_time": [
                r"\b(live|real.?time|streaming|interactive)\b",
                r"\b(collaboration|pair programming|live coding)\b",
                r"\b(chat|conversation|dialog)\b"
            ],
            
            "vision_analysis": [
                r"\b(image|picture|photo|visual|diagram)\b",
                r"\b(analyze|describe|identify|recognize)\b.{0,20}\b(image|visual)\b",
                r"\b(screenshot|ui|interface|design)\b"
            ],
            
            "empathy_required": [
                r"\b(help|support|encourage|comfort)\b",
                r"\b(struggling|difficult|frustrated|overwhelmed)\b",
                r"\b(learning|understanding|confused)\b",
                r"\b(gentle|patient|kind|caring)\b"
            ]
        }
    
    def _initialize_complexity_indicators(self) -> Dict[str, List[str]]:
        """Initialize patterns that indicate task complexity"""
        
        return {
            "high_complexity": [
                r"\b(architecture|system design|scalability)\b",
                r"\b(optimization|performance|security)\b",
                r"\b(complex|sophisticated|advanced)\b",
                r"\b(multiple|various|several).{0,20}\b(components|systems|services)\b",
                r"\b(integration|orchestration|coordination)\b"
            ],
            
            "medium_complexity": [
                r"\b(feature|functionality|component)\b",
                r"\b(implement|develop|create)\b",
                r"\b(api|service|module)\b",
                r"\b(database|backend|frontend)\b"
            ],
            
            "low_complexity": [
                r"\b(simple|basic|quick|small)\b",
                r"\b(fix|update|change|modify)\b",
                r"\b(question|help|explain)\b",
                r"\b(chat|message|response)\b"
            ]
        }
    
    def _initialize_mama_bear_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for Mama Bear variant detection"""
        
        return {
            "scout_commander": [
                r"\b(plan|organize|coordinate|manage)\b",
                r"\b(strategy|roadmap|timeline|schedule)\b",
                r"\b(project|task|workflow|process)\b"
            ],
            
            "research_specialist": [
                r"\b(research|investigate|find|discover)\b",
                r"\b(information|data|facts|details)\b",
                r"\b(analyze|study|examine|explore)\b"
            ],
            
            "code_review_bear": [
                r"\b(review|check|validate|verify)\b",
                r"\b(code|implementation|solution)\b",
                r"\b(quality|best practices|standards)\b",
                r"\b(improve|optimize|refactor)\b"
            ],
            
            "creative_bear": [
                r"\b(creative|innovative|original|unique)\b",
                r"\b(brainstorm|ideate|imagine|design)\b",
                r"\b(art|design|creative writing|story)\b"
            ],
            
            "learning_bear": [
                r"\b(learn|understand|explain|teach)\b",
                r"\b(tutorial|guide|lesson|example)\b",
                r"\b(beginner|new|confused|help)\b",
                r"\b(step by step|simple|basic)\b"
            ],
            
            "efficiency_bear": [
                r"\b(optimize|efficient|fast|quick)\b",
                r"\b(automate|streamline|improve)\b",
                r"\b(productivity|workflow|process)\b",
                r"\b(time|speed|performance)\b"
            ],
            
            "debugging_detective": [
                r"\b(debug|fix|solve|troubleshoot)\b",
                r"\b(error|bug|issue|problem)\b",
                r"\b(broken|failing|not working)\b",
                r"\b(investigate|diagnose|analyze)\b"
            ]
        }
    
    async def analyze_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive analysis of an incoming request"""
        
        message = request.get("message", "")
        context = request.get("context", {})
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "original_request": request,
            "capabilities_needed": self._detect_capabilities(message),
            "complexity_level": self._assess_complexity(message),
            "urgency_level": self._assess_urgency(message, request),
            "estimated_tokens": self._estimate_token_requirements(message, request),
            "mama_bear_suggestions": self._suggest_mama_bear_variant(message),
            "task_classification": self._classify_task_type(message),
            "neurodivergent_considerations": self._analyze_neurodivergent_needs(message, request),
            "optimization_hints": self._generate_optimization_hints(message, request)
        }
        
        # Add derived recommendations
        analysis["routing_recommendations"] = self._generate_routing_recommendations(analysis)
        
        logger.debug(f"Task analysis complete: {len(analysis['capabilities_needed'])} capabilities detected")
        
        return analysis
    
    def _detect_capabilities(self, message: str) -> Set[ModelCapability]:
        """Detect required model capabilities from the message"""
        
        capabilities = set()
        message_lower = message.lower()
        
        # Check each capability pattern
        for capability_name, patterns in self.analysis_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    # Map pattern names to ModelCapability enum
                    capability_mapping = {
                        "speed_required": ModelCapability.SPEED,
                        "creativity_required": ModelCapability.CREATIVE,
                        "reasoning_required": ModelCapability.REASONING,
                        "long_context": ModelCapability.LONG_CONTEXT,
                        "long_output": ModelCapability.LONG_OUTPUT,
                        "code_generation": ModelCapability.CODE_GENERATION,
                        "audio_tts": ModelCapability.TTS,
                        "real_time": ModelCapability.REAL_TIME,
                        "vision_analysis": ModelCapability.VISION
                    }
                    
                    if capability_name in capability_mapping:
                        capabilities.add(capability_mapping[capability_name])
                    break
        
        return capabilities
    
    def _assess_complexity(self, message: str) -> str:
        """Assess the complexity level of the task"""
        
        message_lower = message.lower()
        
        # Count complexity indicators
        complexity_scores = {
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for complexity_level, patterns in self.complexity_indicators.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, message_lower, re.IGNORECASE))
                complexity_scores[complexity_level] += matches
        
        # Determine overall complexity
        max_score = max(complexity_scores.values())
        if max_score == 0:
            return "medium"  # Default
        
        for level, score in complexity_scores.items():
            if score == max_score:
                return level
        
        return "medium"
    
    def _assess_urgency(self, message: str, request: Dict[str, Any]) -> str:
        """Assess the urgency level of the request"""
        
        # Check explicit urgency in request
        explicit_urgency = request.get("urgency", "").lower()
        if explicit_urgency in ["high", "urgent", "critical"]:
            return "high"
        elif explicit_urgency in ["low", "normal", "standard"]:
            return explicit_urgency
        
        # Analyze message for urgency indicators
        message_lower = message.lower()
        
        high_urgency_patterns = [
            r"\b(urgent|asap|immediately|now|critical|emergency)\b",
            r"\b(deadline|due|time.sensitive)\b",
            r"\b(production|live|broken|down)\b"
        ]
        
        low_urgency_patterns = [
            r"\b(when you have time|no rush|eventually|later)\b",
            r"\b(research|explore|consider|think about)\b"
        ]
        
        for pattern in high_urgency_patterns:
            if re.search(pattern, message_lower):
                return "high"
        
        for pattern in low_urgency_patterns:
            if re.search(pattern, message_lower):
                return "low"
        
        return "normal"
    
    def _estimate_token_requirements(self, message: str, request: Dict[str, Any]) -> Dict[str, int]:
        """Estimate token requirements for input and output"""
        
        # Rough token estimation (1 token ≈ 4 characters for English)
        input_chars = len(message) + len(str(request.get("context", "")))
        estimated_input_tokens = input_chars // 4
        
        # Estimate output tokens based on task type and complexity
        base_output = 500  # Base response length
        
        # Adjust based on detected patterns
        message_lower = message.lower()
        
        if re.search(r"\b(detailed|comprehensive|complete|thorough)\b", message_lower):
            base_output *= 3
        elif re.search(r"\b(brief|short|quick|summary)\b", message_lower):
            base_output //= 2
        
        if re.search(r"\b(code|implementation|function|class)\b", message_lower):
            base_output *= 2
        
        if re.search(r"\b(documentation|tutorial|guide)\b", message_lower):
            base_output *= 4
        
        # Cap at reasonable limits
        estimated_output_tokens = min(base_output, 65536)  # Max output for 2.5 models
        
        return {
            "estimated_input": estimated_input_tokens,
            "estimated_output": estimated_output_tokens,
            "total_estimated": estimated_input_tokens + estimated_output_tokens
        }
    
    def _suggest_mama_bear_variant(self, message: str) -> List[Tuple[str, float]]:
        """Suggest appropriate Mama Bear variants with confidence scores"""
        
        message_lower = message.lower()
        variant_scores = {}
        
        # Score each variant based on pattern matches
        for variant, patterns in self.mama_bear_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, message_lower, re.IGNORECASE))
                score += matches
            
            if score > 0:
                # Normalize score (simple approach)
                confidence = min(score / 3.0, 1.0)  # Max confidence of 1.0
                variant_scores[variant] = confidence
        
        # Sort by confidence and return top suggestions
        sorted_variants = sorted(variant_scores.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_variants[:3]  # Top 3 suggestions
    
    def _classify_task_type(self, message: str) -> str:
        """Classify the type of task being requested"""
        
        message_lower = message.lower()
        
        task_patterns = {
            "code_generation": [
                r"\b(write|create|generate|implement)\b.{0,30}\b(code|function|class|component)\b",
                r"\b(build|develop|program)\b"
            ],
            "code_review": [
                r"\b(review|check|analyze|evaluate)\b.{0,20}\b(code|implementation)\b",
                r"\b(feedback|suggestions|improvements)\b"
            ],
            "debugging": [
                r"\b(debug|fix|solve|troubleshoot)\b",
                r"\b(error|bug|issue|problem|broken)\b"
            ],
            "explanation": [
                r"\b(explain|describe|what is|how does|why)\b",
                r"\b(understand|clarify|help me)\b"
            ],
            "research": [
                r"\b(research|find|search|investigate|discover)\b",
                r"\b(information|data|facts|details)\b"
            ],
            "creative_writing": [
                r"\b(write|create|compose)\b.{0,20}\b(story|article|content|text)\b",
                r"\b(creative|original|unique)\b"
            ],
            "planning": [
                r"\b(plan|organize|schedule|roadmap|strategy)\b",
                r"\b(project|task|workflow|process)\b"
            ],
            "analysis": [
                r"\b(analyze|examine|study|evaluate|assess)\b",
                r"\b(data|information|results|performance)\b"
            ]
        }
        
        # Score each task type
        task_scores = {}
        for task_type, patterns in task_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    score += 1
            task_scores[task_type] = score
        
        # Return highest scoring task type
        if task_scores:
            return max(task_scores.items(), key=lambda x: x[1])[0]
        
        return "general"
    
    def _analyze_neurodivergent_needs(self, message: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze specific neurodivergent considerations"""
        
        message_lower = message.lower()
        
        considerations = {
            "cognitive_load_indicators": [],
            "sensory_considerations": [],
            "communication_preferences": [],
            "support_needs": []
        }
        
        # Cognitive load indicators
        if re.search(r"\b(overwhelmed|confused|complex|difficult)\b", message_lower):
            considerations["cognitive_load_indicators"].append("high_cognitive_load")
        
        if re.search(r"\b(simple|basic|step by step|break down)\b", message_lower):
            considerations["cognitive_load_indicators"].append("needs_simplification")
        
        # Sensory considerations
        if re.search(r"\b(quiet|calm|gentle|soft)\b", message_lower):
            considerations["sensory_considerations"].append("prefers_gentle_tone")
        
        if re.search(r"\b(bright|loud|overwhelming|too much)\b", message_lower):
            considerations["sensory_considerations"].append("sensory_sensitivity")
        
        # Communication preferences
        if re.search(r"\b(direct|clear|specific|exact)\b", message_lower):
            considerations["communication_preferences"].append("prefers_direct_communication")
        
        if re.search(r"\b(patient|understanding|supportive)\b", message_lower):
            considerations["communication_preferences"].append("needs_patient_approach")
        
        # Support needs
        if re.search(r"\b(help|support|guidance|assistance)\b", message_lower):
            considerations["support_needs"].append("needs_guidance")
        
        if re.search(r"\b(learning|new|beginner|first time)\b", message_lower):
            considerations["support_needs"].append("learning_support")
        
        return considerations
    
    def _generate_optimization_hints(self, message: str, request: Dict[str, Any]) -> List[str]:
        """Generate optimization hints for model selection"""
        
        hints = []
        message_lower = message.lower()
        
        # Speed optimization hints
        if re.search(r"\b(quick|fast|urgent|immediate)\b", message_lower):
            hints.append("prioritize_speed_over_quality")
            hints.append("use_fastest_available_model")
        
        # Quality optimization hints
        if re.search(r"\b(important|critical|production|careful)\b", message_lower):
            hints.append("prioritize_quality_over_speed")
            hints.append("use_most_reliable_model")
        
        # Context optimization hints
        if len(message) > 5000:  # Long message
            hints.append("large_context_handling_needed")
        
        # Output optimization hints
        if re.search(r"\b(detailed|comprehensive|complete|full)\b", message_lower):
            hints.append("long_output_expected")
            hints.append("use_high_output_limit_model")
        
        # Cost optimization hints
        if re.search(r"\b(simple|basic|quick|small)\b", message_lower):
            hints.append("cost_optimization_possible")
            hints.append("use_efficient_model")
        
        return hints
    
    def _generate_routing_recommendations(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific routing recommendations based on analysis"""
        
        recommendations = {
            "preferred_capabilities": list(analysis["capabilities_needed"]),
            "complexity_routing": analysis["complexity_level"],
            "urgency_routing": analysis["urgency_level"],
            "suggested_mama_bear": analysis["mama_bear_suggestions"][0][0] if analysis["mama_bear_suggestions"] else None,
            "optimization_strategy": "balanced"
        }
        
        # Determine optimization strategy
        if analysis["urgency_level"] == "high":
            recommendations["optimization_strategy"] = "speed_first"
        elif analysis["complexity_level"] == "high":
            recommendations["optimization_strategy"] = "quality_first"
        elif "cost_optimization_possible" in analysis["optimization_hints"]:
            recommendations["optimization_strategy"] = "cost_first"
        
        # Add specific model recommendations
        if ModelCapability.SPEED in analysis["capabilities_needed"]:
            recommendations["model_preferences"] = ["speed_demon_primary", "speed_demon_backup"]
        elif ModelCapability.LONG_CONTEXT in analysis["capabilities_needed"]:
            recommendations["model_preferences"] = ["context_master_primary", "context_master_backup"]
        elif ModelCapability.LONG_OUTPUT in analysis["capabilities_needed"]:
            recommendations["model_preferences"] = ["creative_writer_primary", "creative_writer_backup"]
        elif ModelCapability.REASONING in analysis["capabilities_needed"]:
            recommendations["model_preferences"] = ["deep_thinker_primary", "deep_thinker_backup"]
        
        return recommendations
    
    async def batch_analyze_requests(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze multiple requests in batch for efficiency"""
        
        analyses = []
        
        for request in requests:
            try:
                analysis = await self.analyze_request(request)
                analyses.append(analysis)
            except Exception as e:
                logger.error(f"Failed to analyze request {request.get('request_id', 'unknown')}: {e}")
                analyses.append({
                    "error": str(e),
                    "original_request": request,
                    "analysis_failed": True
                })
        
        return analyses
    
    def get_analysis_statistics(self) -> Dict[str, Any]:
        """Get statistics about analysis patterns (for optimization)"""
        
        return {
            "total_patterns": sum(len(patterns) for patterns in self.analysis_patterns.values()),
            "capability_patterns": len(self.analysis_patterns),
            "complexity_patterns": len(self.complexity_indicators),
            "mama_bear_patterns": len(self.mama_bear_patterns),
            "supported_capabilities": [cap.value for cap in ModelCapability],
            "analysis_version": "1.0.0"
        }