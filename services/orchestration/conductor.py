"""
[MUSIC] Gemini Orchestra Conductor
The maestro that analyzes requests and routes them to the perfect specialist
"""

import google.generativeai as genai
from typing import Dict, Any, List, Optional
import json
import asyncio
import logging
from datetime import datetime

from .model_registry import GEMINI_REGISTRY, ModelCapability, MAMA_BEAR_MODEL_PREFERENCES

logger = logging.getLogger(__name__)

class GeminiConductor:
    """The maestro that orchestrates all other models"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.conductor_model = genai.GenerativeModel(
            GEMINI_REGISTRY["conductor"].id
        )
        self.routing_history = []
        
    async def analyze_and_route(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Use the conductor model to analyze and route requests"""
        
        # Extract key request parameters
        message = request.get("message", "")
        task_type = request.get("task_type", "general")
        mama_bear_variant = request.get("mama_bear_variant", None)
        context_size = request.get("context_size", 0)
        urgency = request.get("urgency", "normal")
        require_speed = request.get("require_speed", False)
        require_creativity = request.get("require_creativity", False)
        require_reasoning = request.get("require_reasoning", False)
        max_tokens_needed = request.get("max_tokens_needed", 1000)
        
        # Build the routing prompt
        routing_prompt = self._build_routing_prompt(
            message, task_type, mama_bear_variant, context_size,
            urgency, require_speed, require_creativity, require_reasoning,
            max_tokens_needed
        )
        
        try:
            # Get routing decision from conductor
            response = await self.conductor_model.generate_content_async(routing_prompt)
            routing_decision = self._parse_routing_response(response.text)
            
            # Add metadata
            routing_decision["timestamp"] = datetime.now().isoformat()
            routing_decision["request_id"] = request.get("request_id", "unknown")
            
            # Store in history for learning
            self.routing_history.append({
                "request": request,
                "routing": routing_decision,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"Conductor routed request to: {routing_decision['primary_model']}")
            return routing_decision
            
        except Exception as e:
            logger.error(f"Conductor routing failed: {e}")
            # Fallback to simple rule-based routing
            return self._fallback_routing(request)
    
    def _build_routing_prompt(self, message: str, task_type: str, mama_bear_variant: Optional[str],
                            context_size: int, urgency: str, require_speed: bool,
                            require_creativity: bool, require_reasoning: bool,
                            max_tokens_needed: int) -> str:
        """Build the comprehensive routing prompt for the conductor"""
        
        # Get available models summary
        models_summary = self._get_models_summary()
        
        # Get Mama Bear preferences if applicable
        mama_bear_prefs = ""
        if mama_bear_variant and mama_bear_variant in MAMA_BEAR_MODEL_PREFERENCES:
            preferred_models = MAMA_BEAR_MODEL_PREFERENCES[mama_bear_variant]
            mama_bear_prefs = f"\nMama Bear Variant '{mama_bear_variant}' prefers: {', '.join(preferred_models)}"
        
        return f"""
[MUSIC] GEMINI ORCHESTRA CONDUCTOR ANALYSIS

You are the conductor of a sophisticated AI orchestra with 50+ specialized Gemini models.
Your job is to analyze this request and route it to the perfect specialist(s).

[INFO] REQUEST ANALYSIS:
Message: "{message}"
Task Type: {task_type}
Context Size: {context_size} tokens
Urgency: {urgency}
Speed Required: {require_speed}
Creativity Required: {require_creativity}
Reasoning Required: {require_reasoning}
Max Output Tokens: {max_tokens_needed}
{mama_bear_prefs}

[THEATER] AVAILABLE ORCHESTRA SECTIONS:

{models_summary}

[TARGET] ROUTING CRITERIA:
1. **Task Complexity**: Simple queries → Speed Demons, Complex analysis → Deep Thinkers
2. **Context Size**: Large documents (>100K tokens) → Context Masters (2M context!)
3. **Output Length**: Long content (>8K tokens) → Creative Writers (65K output!)
4. **Speed Requirements**: Urgent requests → Ultra-fast models (Flash Lite)
5. **Reasoning Depth**: Architecture/debugging → Thinking models
6. **Real-time Needs**: Live collaboration → Bidirectional models
7. **Audio/Voice**: TTS/voice → Audio specialists
8. **Cost Optimization**: High-volume → Cheaper models when possible

[MUSIC] SPECIAL CONSIDERATIONS:
- Neurodivergent users need gentle, encouraging responses
- Mama Bear variants have personality preferences
- Podplay Sanctuary requires empathetic, caring AI interactions
- Code generation should prioritize accessibility and clean patterns
- Always consider cognitive load reduction

[CHART] RETURN FORMAT (JSON only):
{{
    "primary_model": "model_key_from_registry",
    "fallback_models": ["backup1", "backup2"],
    "reasoning": "detailed explanation of why these models were chosen",
    "estimated_tokens": {max_tokens_needed},
    "routing_confidence": 0.95,
    "special_instructions": "any model-specific prompting guidance",
    "orchestra_section": "which section this belongs to",
    "performance_prediction": {{
        "latency_estimate": "fast/medium/slow",
        "cost_estimate": "low/medium/high",
        "success_probability": 0.95
    }},
    "mama_bear_personality": "caring guidance for response tone"
}}

Analyze the request and provide the optimal routing decision as JSON.
"""

    def _get_models_summary(self) -> str:
        """Generate a concise summary of available models for the conductor"""
        
        summary = """
[BRAIN] DEEP THINKERS (Complex Reasoning):
- deep_thinker_primary: Gemini 2.0 Flash Thinking (Latest) - Architecture, debugging, complex analysis
- deep_thinker_backup: Gemini 2.5 Flash Thinking - Reliable complex reasoning backup

[LIGHTNING] SPEED DEMONS (Ultra-Fast):
- speed_demon_primary: Gemini 2.0 Flash Lite - Instant chat responses, UI interactions
- speed_demon_backup: Gemini 1.5 Flash 8B - Ultra-fast backup for high volume

[BOOKS] CONTEXT MASTERS (2M Context!):
- context_master_primary: Gemini 1.5 Pro - 2 MILLION token context for massive documents
- context_master_backup: Gemini 1.5 Pro 002 - Reliable 2M context with caching

[ART] CREATIVE WRITERS (65K Output!):
- creative_writer_primary: Gemini 2.5 Flash Creative - 65K output for large code generation
- creative_writer_backup: Gemini 2.0 Pro Experimental - Pro-level creative backup

[MUSIC_NOTE] AUDIO SPECIALISTS:
- tts_specialist: Gemini 2.5 Flash TTS - Text-to-speech generation
- audio_dialog_specialist: Gemini 2.5 Audio Dialog - Voice conversations

[SYNC] REAL-TIME COLLABORATORS:
- realtime_primary: Gemini 2.0 Flash Experimental - Live coding sessions
- live_collaborator: Gemini 2.0 Flash Live - Real-time streaming collaboration

[TARGET] SPECIALISTS:
- embedding_specialist: Gemini Embedding - Vector embeddings for search
- vision_specialist: Gemini Pro Vision - Image and visual analysis
- batch_processor: Gemini 2.5 Pro Batch - Bulk processing optimization
"""
        return summary
    
    def _parse_routing_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the conductor's routing response"""
        try:
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response_text[start_idx:end_idx]
            routing_decision = json.loads(json_str)
            
            # Validate required fields
            required_fields = ["primary_model", "fallback_models", "reasoning", "routing_confidence"]
            for field in required_fields:
                if field not in routing_decision:
                    raise ValueError(f"Missing required field: {field}")
            
            # Ensure models exist in registry
            if routing_decision["primary_model"] not in GEMINI_REGISTRY:
                raise ValueError(f"Unknown primary model: {routing_decision['primary_model']}")
            
            for fallback in routing_decision["fallback_models"]:
                if fallback not in GEMINI_REGISTRY:
                    logger.warning(f"Unknown fallback model: {fallback}")
            
            return routing_decision
            
        except Exception as e:
            logger.error(f"Failed to parse routing response: {e}")
            logger.debug(f"Raw response: {response_text}")
            raise
    
    def _fallback_routing(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Simple rule-based fallback routing when conductor fails"""
        
        message = request.get("message", "")
        require_speed = request.get("require_speed", False)
        require_creativity = request.get("require_creativity", False)
        require_reasoning = request.get("require_reasoning", False)
        context_size = request.get("context_size", 0)
        max_tokens_needed = request.get("max_tokens_needed", 1000)
        
        # Simple routing logic
        if require_speed or "quick" in message.lower() or "fast" in message.lower():
            primary = "speed_demon_primary"
            fallbacks = ["speed_demon_backup"]
            reasoning = "Speed required - using fastest models"
            
        elif context_size > 100000:  # Large context
            primary = "context_master_primary"
            fallbacks = ["context_master_backup"]
            reasoning = "Large context detected - using 2M context models"
            
        elif max_tokens_needed > 8192:  # Long output
            primary = "creative_writer_primary"
            fallbacks = ["creative_writer_backup"]
            reasoning = "Long output required - using 65K output models"
            
        elif require_reasoning or "debug" in message.lower() or "analyze" in message.lower():
            primary = "deep_thinker_primary"
            fallbacks = ["deep_thinker_backup"]
            reasoning = "Complex reasoning required - using thinking models"
            
        elif require_creativity or "create" in message.lower() or "generate" in message.lower():
            primary = "creative_writer_primary"
            fallbacks = ["creative_writer_backup"]
            reasoning = "Creative task detected - using creative models"
            
        else:
            # Default to balanced model
            primary = "conductor"
            fallbacks = ["speed_demon_primary", "creative_writer_primary"]
            reasoning = "General task - using conductor model"
        
        return {
            "primary_model": primary,
            "fallback_models": fallbacks,
            "reasoning": reasoning,
            "estimated_tokens": max_tokens_needed,
            "routing_confidence": 0.7,
            "special_instructions": "Fallback routing used - conductor unavailable",
            "orchestra_section": "fallback",
            "performance_prediction": {
                "latency_estimate": "medium",
                "cost_estimate": "medium",
                "success_probability": 0.8
            },
            "mama_bear_personality": "gentle and encouraging",
            "timestamp": datetime.now().isoformat(),
            "fallback_used": True
        }
    
    async def get_routing_analytics(self) -> Dict[str, Any]:
        """Get analytics on routing decisions for optimization"""
        
        if not self.routing_history:
            return {"message": "No routing history available"}
        
        # Analyze routing patterns
        model_usage = {}
        confidence_scores = []
        
        for entry in self.routing_history:
            routing = entry["routing"]
            primary_model = routing["primary_model"]
            
            model_usage[primary_model] = model_usage.get(primary_model, 0) + 1
            confidence_scores.append(routing.get("routing_confidence", 0))
        
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        
        return {
            "total_requests": len(self.routing_history),
            "model_usage": model_usage,
            "average_confidence": avg_confidence,
            "most_used_model": max(model_usage.items(), key=lambda x: x[1])[0],
            "routing_patterns": self._analyze_routing_patterns()
        }
    
    def _analyze_routing_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in routing decisions for optimization"""
        
        patterns = {
            "speed_requests": 0,
            "creative_requests": 0,
            "reasoning_requests": 0,
            "context_heavy_requests": 0,
            "mama_bear_requests": 0
        }
        
        for entry in self.routing_history:
            request = entry["request"]
            
            if request.get("require_speed"):
                patterns["speed_requests"] += 1
            if request.get("require_creativity"):
                patterns["creative_requests"] += 1
            if request.get("require_reasoning"):
                patterns["reasoning_requests"] += 1
            if request.get("context_size", 0) > 50000:
                patterns["context_heavy_requests"] += 1
            if request.get("mama_bear_variant"):
                patterns["mama_bear_requests"] += 1
        
        return patterns