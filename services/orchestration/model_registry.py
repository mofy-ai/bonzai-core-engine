"""
[MUSIC] Gemini Orchestra Model Registry
Comprehensive registry of all available Gemini models with their capabilities
"""

from enum import Enum
from dataclasses import dataclass
from typing import Set, Dict, List, Optional
import json

class ModelCapability(Enum):
    """Model capabilities for intelligent routing"""
    REASONING = "reasoning"
    SPEED = "speed"
    LONG_CONTEXT = "long_context"
    LONG_OUTPUT = "long_output"
    CODE_GENERATION = "code_generation"
    CREATIVE = "creative"
    VISION = "vision"
    AUDIO = "audio"
    TTS = "tts"
    REAL_TIME = "real_time"
    THINKING = "thinking"
    EMBEDDING = "embedding"
    BATCH_PROCESSING = "batch_processing"
    BIDIRECTIONAL = "bidirectional"
    LIVE_COLLABORATION = "live_collaboration"
    CACHED_CONTENT = "cached_content"

@dataclass
class GeminiModel:
    """Comprehensive model specification"""
    id: str
    name: str
    context_window: int
    output_limit: int
    capabilities: Set[ModelCapability]
    latency_tier: str  # "ultra_fast", "fast", "medium", "slow"
    cost_tier: str     # "free", "low", "medium", "high"
    specialty: str
    features: List[str]
    notes: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "context_window": self.context_window,
            "output_limit": self.output_limit,
            "capabilities": [cap.value for cap in self.capabilities],
            "latency_tier": self.latency_tier,
            "cost_tier": self.cost_tier,
            "specialty": self.specialty,
            "features": self.features,
            "notes": self.notes
        }

# [THEATER] THE GEMINI ORCHESTRA REGISTRY
GEMINI_REGISTRY = {
    # [MUSIC] THE CONDUCTOR - Ultimate Task Router
    "conductor": GeminiModel(
        id="models/gemini-2.5-pro-preview-06-05",
        name="Gemini 2.5 Pro Conductor",
        context_window=1048576,
        output_limit=65536,
        capabilities={
            ModelCapability.REASONING, 
            ModelCapability.LONG_OUTPUT,
            ModelCapability.CODE_GENERATION,
            ModelCapability.BATCH_PROCESSING,
            ModelCapability.CACHED_CONTENT
        },
        latency_tier="medium",
        cost_tier="high",
        specialty="task_routing_and_orchestration",
        features=["generateContent", "countTokens", "createCachedContent", "batchGenerateContent"],
        notes="Latest 2.5 Pro - Most capable conductor for complex routing decisions"
    ),

    # [BRAIN] DEEP THINKERS - Complex Reasoning Specialists
    "deep_thinker_primary": GeminiModel(
        id="models/gemini-2.0-flash-thinking-exp-01-21",
        name="Gemini 2.0 Flash Thinking (Latest)",
        context_window=1048576,
        output_limit=65536,
        capabilities={
            ModelCapability.THINKING,
            ModelCapability.REASONING,
            ModelCapability.LONG_OUTPUT,
            ModelCapability.CODE_GENERATION,
            ModelCapability.BATCH_PROCESSING,
            ModelCapability.CACHED_CONTENT
        },
        latency_tier="slow",
        cost_tier="medium",
        specialty="complex_reasoning_and_debugging",
        features=["generateContent", "countTokens", "createCachedContent", "batchGenerateContent"],
        notes="Latest thinking model - Best for architecture decisions and complex debugging"
    ),

    "deep_thinker_backup": GeminiModel(
        id="models/gemini-2.5-flash-preview-04-17-thinking",
        name="Gemini 2.5 Flash Thinking",
        context_window=1048576,
        output_limit=65536,
        capabilities={
            ModelCapability.THINKING,
            ModelCapability.REASONING,
            ModelCapability.LONG_OUTPUT,
            ModelCapability.BATCH_PROCESSING,
            ModelCapability.CACHED_CONTENT
        },
        latency_tier="slow",
        cost_tier="medium",
        specialty="complex_reasoning_backup",
        features=["generateContent", "countTokens", "createCachedContent", "batchGenerateContent"],
        notes="2.5 thinking backup - Reliable for complex analysis"
    ),

    # [LIGHTNING] SPEED DEMONS - Ultra-Fast Response Specialists
    "speed_demon_primary": GeminiModel(
        id="models/gemini-2.0-flash-lite",
        name="Gemini 2.0 Flash Lite",
        context_window=1048576,
        output_limit=8192,
        capabilities={
            ModelCapability.SPEED,
            ModelCapability.BATCH_PROCESSING,
            ModelCapability.CACHED_CONTENT
        },
        latency_tier="ultra_fast",
        cost_tier="low",
        specialty="instant_responses",
        features=["generateContent", "countTokens", "createCachedContent", "batchGenerateContent"],
        notes="Fastest model - Perfect for chat and quick UI interactions"
    ),

    "speed_demon_backup": GeminiModel(
        id="models/gemini-1.5-flash-8b",
        name="Gemini 1.5 Flash 8B",
        context_window=1000000,
        output_limit=8192,
        capabilities={
            ModelCapability.SPEED,
            ModelCapability.CACHED_CONTENT
        },
        latency_tier="ultra_fast",
        cost_tier="free",
        specialty="ultra_fast_backup",
        features=["createCachedContent", "generateContent", "countTokens"],
        notes="Ultra-fast backup - Great for high-volume requests"
    ),

    # [BOOKS] LONG CONTEXT MASTERS - Document Processing Specialists
    "context_master_primary": GeminiModel(
        id="models/gemini-1.5-pro",
        name="Gemini 1.5 Pro (2M Context)",
        context_window=2000000,  # 2 MILLION tokens!
        output_limit=8192,
        capabilities={
            ModelCapability.LONG_CONTEXT,
            ModelCapability.CODE_GENERATION,
            ModelCapability.REASONING
        },
        latency_tier="medium",
        cost_tier="medium",
        specialty="massive_document_analysis",
        features=["generateContent", "countTokens"],
        notes="2M context window - Can analyze entire codebases at once!"
    ),

    "context_master_backup": GeminiModel(
        id="models/gemini-1.5-pro-002",
        name="Gemini 1.5 Pro 002",
        context_window=2000000,
        output_limit=8192,
        capabilities={
            ModelCapability.LONG_CONTEXT,
            ModelCapability.CODE_GENERATION,
            ModelCapability.CACHED_CONTENT
        },
        latency_tier="medium",
        cost_tier="medium",
        specialty="document_analysis_backup",
        features=["generateContent", "countTokens", "createCachedContent"],
        notes="Reliable 2M context backup with caching support"
    ),

    # [ART] CREATIVE WRITERS - Long-Form Content Specialists
    "creative_writer_primary": GeminiModel(
        id="models/gemini-2.5-flash-preview-05-20",
        name="Gemini 2.5 Flash Creative",
        context_window=1048576,
        output_limit=65536,  # 65K output!
        capabilities={
            ModelCapability.CREATIVE,
            ModelCapability.LONG_OUTPUT,
            ModelCapability.CODE_GENERATION,
            ModelCapability.BATCH_PROCESSING,
            ModelCapability.CACHED_CONTENT
        },
        latency_tier="fast",
        cost_tier="medium",
        specialty="long_form_content_generation",
        features=["generateContent", "countTokens", "createCachedContent", "batchGenerateContent"],
        notes="65K output limit - Perfect for generating large code files and documentation"
    ),

    "creative_writer_backup": GeminiModel(
        id="models/gemini-2.0-pro-exp",
        name="Gemini 2.0 Pro Experimental",
        context_window=1048576,
        output_limit=65536,
        capabilities={
            ModelCapability.CREATIVE,
            ModelCapability.LONG_OUTPUT,
            ModelCapability.REASONING,
            ModelCapability.BATCH_PROCESSING,
            ModelCapability.CACHED_CONTENT
        },
        latency_tier="medium",
        cost_tier="high",
        specialty="creative_reasoning_backup",
        features=["generateContent", "countTokens", "createCachedContent", "batchGenerateContent"],
        notes="Pro-level creative backup with strong reasoning"
    ),

    # [MUSIC_NOTE] AUDIO & VOICE SPECIALISTS
    "tts_specialist": GeminiModel(
        id="models/gemini-2.5-flash-preview-tts",
        name="Gemini 2.5 Flash TTS",
        context_window=32768,
        output_limit=8192,
        capabilities={
            ModelCapability.TTS,
            ModelCapability.AUDIO
        },
        latency_tier="fast",
        cost_tier="medium",
        specialty="text_to_speech",
        features=["countTokens", "generateContent"],
        notes="Specialized for text-to-speech generation"
    ),

    "audio_dialog_specialist": GeminiModel(
        id="models/gemini-2.5-flash-preview-native-audio-dialog",
        name="Gemini 2.5 Audio Dialog",
        context_window=131072,
        output_limit=8192,
        capabilities={
            ModelCapability.AUDIO,
            ModelCapability.BIDIRECTIONAL,
            ModelCapability.REAL_TIME
        },
        latency_tier="fast",
        cost_tier="medium",
        specialty="audio_conversations",
        features=["countTokens", "bidiGenerateContent"],
        notes="Native audio dialog processing for voice interfaces"
    ),

    # [SYNC] REAL-TIME COLLABORATORS
    "realtime_primary": GeminiModel(
        id="models/gemini-2.0-flash-exp",
        name="Gemini 2.0 Flash Experimental",
        context_window=1048576,
        output_limit=8192,
        capabilities={
            ModelCapability.REAL_TIME,
            ModelCapability.BIDIRECTIONAL,
            ModelCapability.LIVE_COLLABORATION
        },
        latency_tier="fast",
        cost_tier="medium",
        specialty="live_coding_sessions",
        features=["generateContent", "countTokens", "bidiGenerateContent"],
        notes="Supports bidirectional generation for real-time collaboration"
    ),

    "live_collaborator": GeminiModel(
        id="models/gemini-2.0-flash-live-001",
        name="Gemini 2.0 Flash Live",
        context_window=131072,
        output_limit=8192,
        capabilities={
            ModelCapability.LIVE_COLLABORATION,
            ModelCapability.BIDIRECTIONAL,
            ModelCapability.REAL_TIME
        },
        latency_tier="ultra_fast",
        cost_tier="medium",
        specialty="live_streaming_collaboration",
        features=["bidiGenerateContent", "countTokens"],
        notes="Optimized for live streaming and real-time collaboration"
    ),

    # [SEARCH] EMBEDDING SPECIALISTS
    "embedding_specialist": GeminiModel(
        id="models/gemini-embedding-exp",
        name="Gemini Embedding Experimental",
        context_window=8192,
        output_limit=1,
        capabilities={
            ModelCapability.EMBEDDING
        },
        latency_tier="fast",
        cost_tier="low",
        specialty="vector_embeddings",
        features=["embedContent", "countTextTokens"],
        notes="Specialized for creating vector embeddings for semantic search"
    ),

    # [TARGET] SPECIALIZED VARIANTS
    "vision_specialist": GeminiModel(
        id="models/gemini-1.0-pro-vision-latest",
        name="Gemini Pro Vision",
        context_window=12288,
        output_limit=4096,
        capabilities={
            ModelCapability.VISION,
            ModelCapability.REASONING
        },
        latency_tier="medium",
        cost_tier="medium",
        specialty="image_analysis",
        features=["generateContent", "countTokens"],
        notes="Specialized for image and visual content analysis"
    ),

    "batch_processor": GeminiModel(
        id="models/gemini-2.5-pro-exp-03-25",
        name="Gemini 2.5 Pro Batch",
        context_window=1048576,
        output_limit=65536,
        capabilities={
            ModelCapability.BATCH_PROCESSING,
            ModelCapability.LONG_OUTPUT,
            ModelCapability.CACHED_CONTENT,
            ModelCapability.REASONING
        },
        latency_tier="slow",
        cost_tier="high",
        specialty="bulk_processing",
        features=["generateContent", "countTokens", "createCachedContent", "batchGenerateContent"],
        notes="Optimized for processing large batches of requests efficiently"
    )
}

# [THEATER] ORCHESTRA SECTIONS - Grouped by specialty
ORCHESTRA_SECTIONS = {
    "conductors": ["conductor"],
    "deep_thinkers": ["deep_thinker_primary", "deep_thinker_backup"],
    "speed_demons": ["speed_demon_primary", "speed_demon_backup"],
    "context_masters": ["context_master_primary", "context_master_backup"],
    "creative_writers": ["creative_writer_primary", "creative_writer_backup"],
    "audio_specialists": ["tts_specialist", "audio_dialog_specialist"],
    "realtime_collaborators": ["realtime_primary", "live_collaborator"],
    "specialists": ["embedding_specialist", "vision_specialist", "batch_processor"]
}

def get_models_by_capability(capability: ModelCapability) -> List[str]:
    """Get all model keys that have a specific capability"""
    return [
        key for key, model in GEMINI_REGISTRY.items()
        if capability in model.capabilities
    ]

def get_fastest_model_for_capability(capability: ModelCapability) -> Optional[str]:
    """Get the fastest model that has a specific capability"""
    capable_models = [
        (key, model) for key, model in GEMINI_REGISTRY.items()
        if capability in model.capabilities
    ]
    
    if not capable_models:
        return None
    
    # Sort by latency tier (ultra_fast > fast > medium > slow)
    tier_order = {"ultra_fast": 0, "fast": 1, "medium": 2, "slow": 3}
    capable_models.sort(key=lambda x: tier_order.get(x[1].latency_tier, 4))
    
    return capable_models[0][0]

def get_cheapest_model_for_capability(capability: ModelCapability) -> Optional[str]:
    """Get the most cost-effective model that has a specific capability"""
    capable_models = [
        (key, model) for key, model in GEMINI_REGISTRY.items()
        if capability in model.capabilities
    ]
    
    if not capable_models:
        return None
    
    # Sort by cost tier (free > low > medium > high)
    tier_order = {"free": 0, "low": 1, "medium": 2, "high": 3}
    capable_models.sort(key=lambda x: tier_order.get(x[1].cost_tier, 4))
    
    return capable_models[0][0]

def export_registry_json() -> str:
    """Export the entire registry as JSON for external tools"""
    registry_dict = {
        key: model.to_dict() for key, model in GEMINI_REGISTRY.items()
    }
    return json.dumps(registry_dict, indent=2)

# [MUSIC] MAMA BEAR VARIANT MAPPINGS
MAMA_BEAR_MODEL_PREFERENCES = {
    "scout_commander": ["conductor", "deep_thinker_primary"],
    "research_specialist": ["context_master_primary", "deep_thinker_primary"],
    "code_review_bear": ["deep_thinker_primary", "context_master_primary"],
    "creative_bear": ["creative_writer_primary", "creative_writer_backup"],
    "learning_bear": ["deep_thinker_primary", "creative_writer_primary"],
    "efficiency_bear": ["speed_demon_primary", "speed_demon_backup"],
    "debugging_detective": ["deep_thinker_primary", "context_master_primary"]
}