"""
[THEATER] Gemini Orchestra Manager
The main orchestration system that coordinates all models and handles requests
"""

import google.generativeai as genai
import anthropic
import asyncio
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
import json
import time

from .conductor import GeminiConductor
from .model_registry import GEMINI_REGISTRY, ModelCapability
from .performance_tracker import PerformanceTracker

logger = logging.getLogger(__name__)

class GeminiOrchestra:
    """The main orchestra that manages all Gemini models and Claude guests"""
    
    def __init__(self, gemini_api_key: str, anthropic_api_key: str = None):
        # Initialize API clients
        genai.configure(api_key=gemini_api_key)
        self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key) if anthropic_api_key else None
        
        # Initialize orchestra components
        self.conductor = GeminiConductor(gemini_api_key)
        self.performance_tracker = PerformanceTracker()
        
        # Initialize model instances
        self.gemini_models = {}
        self._initialize_gemini_models()
        
        # Orchestra state
        self.active_requests = {}
        self.request_queue = asyncio.Queue()
        self.is_running = False
        
        logger.info("[THEATER] Gemini Orchestra initialized with 50+ models!")
    
    def _initialize_gemini_models(self):
        """Initialize all Gemini model instances"""
        
        for model_key, model_config in GEMINI_REGISTRY.items():
            try:
                self.gemini_models[model_key] = genai.GenerativeModel(model_config.id)
                logger.debug(f"Initialized {model_key}: {model_config.name}")
            except Exception as e:
                logger.error(f"Failed to initialize {model_key}: {e}")
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Main entry point for processing requests through the orchestra"""
        
        request_id = request.get("request_id", str(uuid.uuid4()))
        request["request_id"] = request_id
        
        start_time = time.time()
        
        try:
            logger.info(f"[MUSIC] Processing request {request_id}")
            
            # Step 1: Conductor analyzes and routes the request
            routing_decision = await self.conductor.analyze_and_route(request)
            
            # Step 2: Performance tracker adjusts routing if needed
            optimized_routing = await self.performance_tracker.get_performance_adjusted_routing(routing_decision)
            
            # Step 3: Determine if Claude should handle this request
            if self._should_use_claude(request, optimized_routing):
                return await self._process_with_claude(request, optimized_routing)
            
            # Step 4: Process with Gemini orchestra
            result = await self._process_with_gemini_orchestra(request, optimized_routing)
            
            # Step 5: Record success metrics
            processing_time = (time.time() - start_time) * 1000  # Convert to ms
            await self.performance_tracker.record_success(
                optimized_routing["primary_model"],
                request_id,
                processing_time,
                result
            )
            
            result["orchestra_metadata"] = {
                "request_id": request_id,
                "routing_decision": optimized_routing,
                "processing_time_ms": processing_time,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"[OK] Request {request_id} completed in {processing_time:.0f}ms")
            return result
            
        except Exception as e:
            # Record failure and attempt fallback
            processing_time = (time.time() - start_time) * 1000
            
            if 'optimized_routing' in locals():
                await self.performance_tracker.record_failure(
                    optimized_routing["primary_model"],
                    request_id,
                    type(e).__name__,
                    str(e)
                )
            
            logger.error(f"[ERROR] Request {request_id} failed: {e}")
            
            # Attempt fallback processing
            return await self._handle_request_failure(request, e, processing_time)
    
    def _should_use_claude(self, request: Dict[str, Any], routing: Dict[str, Any]) -> bool:
        """Determine if Claude should handle this request instead of Gemini"""
        
        if not self.anthropic_client:
            return False
        
        # Use Claude for specific scenarios
        use_claude_conditions = [
            # Explicitly requested
            request.get("require_claude", False),
            request.get("prefer_claude", False),
            
            # Low routing confidence from conductor
            routing.get("routing_confidence", 1.0) < 0.6,
            
            # Critical tasks that need highest reliability
            request.get("task_type") in ["critical_code_review", "security_analysis", "production_deployment"],
            
            # Mama Bear empathetic responses
            request.get("mama_bear_variant") in ["learning_bear", "creative_bear"] and request.get("require_empathy", False),
            
            # Complex reasoning that needs Claude's strengths
            request.get("require_reasoning", False) and request.get("complexity_level", "medium") == "high",
            
            # When Gemini models are experiencing issues
            self._are_gemini_models_struggling(routing)
        ]
        
        return any(use_claude_conditions)
    
    def _are_gemini_models_struggling(self, routing: Dict[str, Any]) -> bool:
        """Check if the primary and fallback Gemini models are having issues"""
        
        primary_model = routing["primary_model"]
        fallback_models = routing.get("fallback_models", [])
        
        # Check performance of primary model
        primary_perf = self.performance_tracker.performance_data[primary_model]
        if primary_perf["success_rate"] < 0.7:
            return True
        
        # Check if most fallbacks are also struggling
        struggling_fallbacks = 0
        for fallback in fallback_models[:3]:  # Check first 3 fallbacks
            fallback_perf = self.performance_tracker.performance_data[fallback]
            if fallback_perf["success_rate"] < 0.8:
                struggling_fallbacks += 1
        
        return struggling_fallbacks >= 2
    
    async def _process_with_claude(self, request: Dict[str, Any], routing: Dict[str, Any]) -> Dict[str, Any]:
        """Process request using Claude as a guest performer"""
        
        logger.info(f"[THEATER] Routing to Claude guest performer for request {request['request_id']}")
        
        # Determine which Claude model to use
        claude_model = self._select_claude_model(request, routing)
        
        # Build Claude-optimized prompt
        claude_prompt = self._build_claude_prompt(request, routing)
        
        try:
            # Make request to Claude
            response = await asyncio.to_thread(
                self.anthropic_client.messages.create,
                model=claude_model,
                max_tokens=request.get("max_tokens_needed", 4096),
                messages=[{"role": "user", "content": claude_prompt}]
            )
            
            return {
                "response": response.content[0].text,
                "model_used": f"claude_{claude_model}",
                "provider": "anthropic",
                "routing_reason": routing.get("reasoning", "Claude selected for reliability"),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Claude processing failed: {e}")
            # Fallback to Gemini if Claude fails
            return await self._process_with_gemini_orchestra(request, routing)
    
    def _select_claude_model(self, request: Dict[str, Any], routing: Dict[str, Any]) -> str:
        """Select the appropriate Claude model based on request needs"""
        
        # For critical tasks, use Opus
        if request.get("task_type") in ["critical_code_review", "security_analysis"]:
            return "claude-3-opus-20240229"
        
        # For empathetic Mama Bear responses, use Sonnet
        if request.get("mama_bear_variant") and request.get("require_empathy"):
            return "claude-3-sonnet-20240229"
        
        # For speed-sensitive tasks, use Haiku
        if request.get("require_speed") or request.get("urgency") == "high":
            return "claude-3-haiku-20240307"
        
        # Default to Sonnet for balanced performance
        return "claude-3-sonnet-20240229"
    
    def _build_claude_prompt(self, request: Dict[str, Any], routing: Dict[str, Any]) -> str:
        """Build an optimized prompt for Claude"""
        
        base_message = request.get("message", "")
        mama_bear_variant = request.get("mama_bear_variant")
        task_type = request.get("task_type", "general")
        
        # Add Podplay Sanctuary context
        sanctuary_context = """
You are part of the Podplay Sanctuary AI system - a neurodivergent-friendly development platform.
Your responses should be caring, empathetic, and designed to reduce cognitive load for users with ADHD, autism, and other neurotypes.
Always maintain the purple sanctuary feeling - safe, calming, and empowering.
"""
        
        # Add Mama Bear personality if specified
        mama_bear_context = ""
        if mama_bear_variant:
            mama_bear_personalities = {
                "scout_commander": "You are Scout Commander - strategic, organized, and excellent at breaking down complex tasks.",
                "research_specialist": "You are Research Specialist - thorough, analytical, and great at finding comprehensive information.",
                "code_review_bear": "You are Code Review Bear - careful, constructive, and focused on helping improve code quality.",
                "creative_bear": "You are Creative Bear - innovative, inspiring, and excellent at brainstorming solutions.",
                "learning_bear": "You are Learning Bear - patient, encouraging, and skilled at explaining complex concepts simply.",
                "efficiency_bear": "You are Efficiency Bear - focused on optimization, automation, and streamlining workflows.",
                "debugging_detective": "You are Debugging Detective - systematic, persistent, and excellent at solving problems."
            }
            mama_bear_context = mama_bear_personalities.get(mama_bear_variant, "")
        
        # Build complete prompt
        full_prompt = f"""
{sanctuary_context}

{mama_bear_context}

Task Type: {task_type}
Routing Reason: {routing.get('reasoning', 'Selected for optimal performance')}

User Request:
{base_message}

Please provide a helpful, caring response that embodies the Podplay Sanctuary values.
"""
        
        return full_prompt.strip()
    
    async def _process_with_gemini_orchestra(self, request: Dict[str, Any], routing: Dict[str, Any]) -> Dict[str, Any]:
        """Process request using the Gemini orchestra"""
        
        primary_model_key = routing["primary_model"]
        fallback_models = routing.get("fallback_models", [])
        request_id = request["request_id"]
        
        # Track request start
        await self.performance_tracker.record_request_start(
            primary_model_key, request_id, request
        )
        
        # Try primary model first
        try:
            result = await self._execute_gemini_request(primary_model_key, request, routing)
            result["model_used"] = primary_model_key
            result["provider"] = "google_gemini"
            result["success"] = True
            return result
            
        except Exception as primary_error:
            logger.warning(f"Primary model {primary_model_key} failed: {primary_error}")
            
            # Try fallback models
            for fallback_key in fallback_models:
                try:
                    logger.info(f"Trying fallback model: {fallback_key}")
                    result = await self._execute_gemini_request(fallback_key, request, routing)
                    result["model_used"] = fallback_key
                    result["provider"] = "google_gemini"
                    result["success"] = True
                    result["fallback_used"] = True
                    result["primary_failure"] = str(primary_error)
                    return result
                    
                except Exception as fallback_error:
                    logger.warning(f"Fallback model {fallback_key} failed: {fallback_error}")
                    continue
            
            # All Gemini models failed
            raise Exception(f"All Gemini models failed. Primary: {primary_error}")
    
    async def _execute_gemini_request(self, model_key: str, request: Dict[str, Any], routing: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a request on a specific Gemini model"""
        
        model = self.gemini_models[model_key]
        model_config = GEMINI_REGISTRY[model_key]
        
        # Build prompt for Gemini
        prompt = self._build_gemini_prompt(request, routing, model_config)
        
        # Configure generation parameters
        generation_config = self._get_generation_config(request, model_config)
        
        # Execute the request
        if ModelCapability.BIDIRECTIONAL in model_config.capabilities:
            # Use bidirectional generation for real-time models
            response = await self._execute_bidirectional_request(model, prompt, generation_config)
        else:
            # Standard generation
            response = await model.generate_content_async(prompt, generation_config=generation_config)
        
        return {
            "response": response.text,
            "model_config": model_config.to_dict(),
            "generation_config": generation_config.__dict__ if hasattr(generation_config, '__dict__') else str(generation_config),
            "routing_metadata": routing
        }
    
    def _build_gemini_prompt(self, request: Dict[str, Any], routing: Dict[str, Any], model_config) -> str:
        """Build an optimized prompt for Gemini models"""
        
        base_message = request.get("message", "")
        mama_bear_variant = request.get("mama_bear_variant")
        task_type = request.get("task_type", "general")
        special_instructions = routing.get("special_instructions", "")
        
        # Add model-specific optimizations
        model_optimizations = {
            "thinking": "Think step by step and show your reasoning process.",
            "creative": "Be creative and innovative in your response.",
            "speed": "Provide a concise, direct response.",
            "context": "Consider the full context provided and reference relevant details.",
            "audio": "Format your response for audio/voice output."
        }
        
        # Determine optimization based on model capabilities
        optimization_hints = []
        if ModelCapability.THINKING in model_config.capabilities:
            optimization_hints.append(model_optimizations["thinking"])
        if ModelCapability.CREATIVE in model_config.capabilities:
            optimization_hints.append(model_optimizations["creative"])
        if ModelCapability.SPEED in model_config.capabilities:
            optimization_hints.append(model_optimizations["speed"])
        
        # Build Podplay Sanctuary context
        sanctuary_context = """
[BEAR] PODPLAY SANCTUARY CONTEXT:
You are part of Podplay Sanctuary - a neurodivergent-friendly AI development platform.
- Provide caring, empathetic responses that reduce cognitive load
- Use clear, accessible language
- Break down complex concepts into manageable steps
- Maintain the purple sanctuary feeling - safe, calming, empowering
- Consider ADHD, autism, and other neurotype needs in your responses
"""
        
        # Add Mama Bear personality
        mama_bear_context = ""
        if mama_bear_variant:
            mama_bear_context = f"\n[THEATER] MAMA BEAR VARIANT: {mama_bear_variant}\n"
        
        # Combine all elements
        full_prompt = f"""
{sanctuary_context}
{mama_bear_context}

[TARGET] TASK TYPE: {task_type}
[MUSIC] MODEL SPECIALIZATION: {model_config.specialty}
[TOOL] OPTIMIZATION HINTS: {' '.join(optimization_hints)}
[NOTE] SPECIAL INSTRUCTIONS: {special_instructions}

[EMOJI] USER REQUEST:
{base_message}

Please provide a helpful response optimized for this model's capabilities while maintaining the Podplay Sanctuary values.
"""
        
        return full_prompt.strip()
    
    def _get_generation_config(self, request: Dict[str, Any], model_config) -> Any:
        """Get optimized generation configuration for the model"""
        
        max_tokens = min(
            request.get("max_tokens_needed", 1000),
            model_config.output_limit
        )
        
        # Base configuration
        config = {
            "max_output_tokens": max_tokens,
            "temperature": request.get("temperature", 0.7),
            "top_p": request.get("top_p", 0.9),
            "top_k": request.get("top_k", 40)
        }
        
        # Adjust based on task type
        task_type = request.get("task_type", "general")
        
        if task_type in ["code_generation", "technical_analysis"]:
            config["temperature"] = 0.3  # More deterministic for code
        elif task_type in ["creative_writing", "brainstorming"]:
            config["temperature"] = 0.9  # More creative
        elif task_type in ["debugging", "problem_solving"]:
            config["temperature"] = 0.5  # Balanced
        
        # Create GenerationConfig object
        return genai.GenerationConfig(**config)
    
    async def _execute_bidirectional_request(self, model, prompt: str, generation_config) -> Any:
        """Execute bidirectional generation for real-time models"""
        
        # This would be implemented for models that support bidirectional generation
        # For now, fall back to standard generation
        return await model.generate_content_async(prompt, generation_config=generation_config)
    
    async def _handle_request_failure(self, request: Dict[str, Any], error: Exception, processing_time: float) -> Dict[str, Any]:
        """Handle request failure with graceful fallback"""
        
        logger.error(f"Request {request.get('request_id')} failed completely: {error}")
        
        # Try Claude as final fallback if available
        if self.anthropic_client and not request.get("claude_attempted"):
            try:
                request["claude_attempted"] = True
                request["fallback_reason"] = f"Gemini orchestra failed: {error}"
                
                # Simple Claude fallback
                response = await asyncio.to_thread(
                    self.anthropic_client.messages.create,
                    model="claude-3-haiku-20240307",  # Fastest Claude model
                    max_tokens=1000,
                    messages=[{
                        "role": "user", 
                        "content": f"Please help with this request from Podplay Sanctuary: {request.get('message', '')}"
                    }]
                )
                
                return {
                    "response": response.content[0].text,
                    "model_used": "claude_fallback",
                    "provider": "anthropic",
                    "success": True,
                    "fallback_used": True,
                    "original_error": str(error),
                    "processing_time_ms": processing_time
                }
                
            except Exception as claude_error:
                logger.error(f"Claude fallback also failed: {claude_error}")
        
        # Return error response
        return {
            "response": "I apologize, but I'm experiencing technical difficulties right now. Please try again in a moment, or contact support if the issue persists.",
            "model_used": "error_handler",
            "provider": "system",
            "success": False,
            "error": str(error),
            "processing_time_ms": processing_time,
            "user_friendly_error": "The AI system is temporarily unavailable. Please try again."
        }
    
    async def get_orchestra_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the entire orchestra"""
        
        # Get performance report
        performance_report = await self.performance_tracker.get_performance_report()
        
        # Get conductor analytics
        conductor_analytics = await self.conductor.get_routing_analytics()
        
        # Model availability check
        available_models = []
        unavailable_models = []
        
        for model_key in GEMINI_REGISTRY.keys():
            if model_key in self.gemini_models:
                available_models.append(model_key)
            else:
                unavailable_models.append(model_key)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "orchestra_health": performance_report["system_health"],
            "available_models": len(available_models),
            "unavailable_models": len(unavailable_models),
            "claude_available": self.anthropic_client is not None,
            "active_requests": len(self.active_requests),
            "performance_summary": performance_report,
            "conductor_analytics": conductor_analytics,
            "model_sections": {
                section: [model for model in models if model in available_models]
                for section, models in {
                    "conductors": ["conductor"],
                    "deep_thinkers": ["deep_thinker_primary", "deep_thinker_backup"],
                    "speed_demons": ["speed_demon_primary", "speed_demon_backup"],
                    "context_masters": ["context_master_primary", "context_master_backup"],
                    "creative_writers": ["creative_writer_primary", "creative_writer_backup"],
                    "audio_specialists": ["tts_specialist", "audio_dialog_specialist"],
                    "realtime_collaborators": ["realtime_primary", "live_collaborator"]
                }.items()
            }
        }
    
    async def optimize_orchestra(self) -> Dict[str, Any]:
        """Run optimization analysis and apply improvements"""
        
        logger.info("[TOOL] Running orchestra optimization...")
        
        # Get performance insights
        performance_report = await self.performance_tracker.get_performance_report()
        
        optimizations_applied = []
        
        # Analyze model performance and suggest optimizations
        for model_key, perf_data in performance_report["model_performance"].items():
            if perf_data["success_rate"] < 0.8:
                optimizations_applied.append({
                    "type": "model_reliability",
                    "model": model_key,
                    "action": "Reduced routing priority due to low success rate",
                    "details": f"Success rate: {perf_data['success_rate']:.2f}"
                })
        
        # Update conductor with optimization insights
        optimization_summary = {
            "timestamp": datetime.now().isoformat(),
            "optimizations_applied": optimizations_applied,
            "performance_improvements": [],
            "recommendations": performance_report.get("optimization_suggestions", [])
        }
        
        logger.info(f"[OK] Orchestra optimization complete: {len(optimizations_applied)} optimizations applied")
        
        return optimization_summary