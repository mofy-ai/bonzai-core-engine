"""
[LAUNCH] ZAI MULTI-PROVIDER MODEL CONFIGURATION SYSTEM
Provider-Agnostic AI Orchestration Platform

This implements Nathan's vision of separating ZAI's capabilities from specific models,
allowing users to choose their preferred AI provider like a "pizza menu"
"""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
import json
import yaml

class ProviderType(Enum):
    GOOGLE_VERTEX = "google_vertex"
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    XAI = "xai"
    CUSTOM = "custom"
    MULTI_PROVIDER = "multi"

class ModelRole(Enum):
    CHAT = "chat"
    RESEARCH = "research"
    BUILD = "build"
    CREATIVE = "creative"
    ANALYSIS = "analysis"
    CODING = "coding"
    REASONING = "reasoning"

@dataclass
class ModelConfig:
    """Configuration for a specific model"""
    provider: ProviderType
    model_name: str
    role: ModelRole
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    pricing_tier: Optional[str] = None

@dataclass
class ProviderCredentials:
    """Provider-specific credentials"""
    provider: ProviderType
    api_key: Optional[str] = None
    project_id: Optional[str] = None
    region: Optional[str] = None
    endpoint: Optional[str] = None
    
class ZAIModelRegistry:
    """
    The heart of Nathan's vision - a registry that maps ZAI capabilities
    to user-chosen models from any provider
    """
    
    # Pre-defined model sets for each provider
    PROVIDER_MODELS = {
        ProviderType.GOOGLE_VERTEX: {
            "gemini-2.5-pro": {"tier": "premium", "strengths": ["reasoning", "research"]},
            "gemini-2.5-flash": {"tier": "fast", "strengths": ["chat", "quick_responses"]},
            "gemini-2.0-flash": {"tier": "efficient", "strengths": ["coding", "analysis"]},
            "gemini-1.5-pro": {"tier": "standard", "strengths": ["creative", "general"]},
            "gemini-1.5-flash": {"tier": "budget", "strengths": ["simple_tasks"]},
        },
        
        ProviderType.ANTHROPIC: {
            "claude-4-opus": {"tier": "premium", "strengths": ["reasoning", "complex_tasks"]},
            "claude-4-sonnet": {"tier": "balanced", "strengths": ["chat", "research"]},
            "claude-3.5-sonnet": {"tier": "standard", "strengths": ["coding", "analysis"]},
            "claude-3.5-haiku": {"tier": "fast", "strengths": ["creative", "quick_responses"]},
        },
        
        ProviderType.OPENAI: {
            "gpt-4o": {"tier": "premium", "strengths": ["reasoning", "multimodal"]},
            "gpt-4-turbo": {"tier": "balanced", "strengths": ["chat", "research"]},
            "gpt-4": {"tier": "standard", "strengths": ["coding", "analysis"]},
            "gpt-3.5-turbo": {"tier": "budget", "strengths": ["simple_tasks", "chat"]},
        },
        
        ProviderType.XAI: {
            "grok-2": {"tier": "premium", "strengths": ["creative", "unconventional"]},
            "grok-1.5": {"tier": "standard", "strengths": ["chat", "research"]},
            "grok-mini": {"tier": "budget", "strengths": ["quick_responses"]},
        }
    }
    
    # Pre-defined configuration templates (The "Pizza Menu" Options!)
    CONFIGURATION_TEMPLATES = {
        "google_power_user": {
            "name": "Google Ecosystem Powerhouse",
            "description": "Full Google Vertex AI integration with latest Gemini models",
            "provider": ProviderType.GOOGLE_VERTEX,
            "models": {
                ModelRole.CHAT: "gemini-2.5-pro",
                ModelRole.RESEARCH: "gemini-2.5-flash", 
                ModelRole.BUILD: "gemini-2.0-flash",
                ModelRole.CREATIVE: "gemini-1.5-pro",
                ModelRole.ANALYSIS: "gemini-2.5-pro",
                ModelRole.CODING: "gemini-2.0-flash",
                ModelRole.REASONING: "gemini-2.5-pro"
            }
        },
        
        "anthropic_claude_lover": {
            "name": "Anthropic Claude Excellence",
            "description": "Claude 4 powered development environment - Nathan's favorite!",
            "provider": ProviderType.ANTHROPIC,
            "models": {
                ModelRole.CHAT: "claude-4-opus",
                ModelRole.RESEARCH: "claude-4-sonnet",
                ModelRole.BUILD: "claude-3.5-sonnet",
                ModelRole.CREATIVE: "claude-3.5-haiku",
                ModelRole.ANALYSIS: "claude-4-opus",
                ModelRole.CODING: "claude-3.5-sonnet",
                ModelRole.REASONING: "claude-4-opus"
            }
        },
        
        "openai_classic": {
            "name": "OpenAI GPT Suite",
            "description": "Tried and tested GPT models for reliable performance",
            "provider": ProviderType.OPENAI,
            "models": {
                ModelRole.CHAT: "gpt-4o",
                ModelRole.RESEARCH: "gpt-4-turbo",
                ModelRole.BUILD: "gpt-4",
                ModelRole.CREATIVE: "gpt-4o",
                ModelRole.ANALYSIS: "gpt-4-turbo",
                ModelRole.CODING: "gpt-4",
                ModelRole.REASONING: "gpt-4o"
            }
        },
        
        "xai_innovator": {
            "name": "XAI Grok Innovation",
            "description": "Cutting-edge Grok models for unconventional solutions",
            "provider": ProviderType.XAI,
            "models": {
                ModelRole.CHAT: "grok-2",
                ModelRole.RESEARCH: "grok-2",
                ModelRole.BUILD: "grok-1.5",
                ModelRole.CREATIVE: "grok-2",
                ModelRole.ANALYSIS: "grok-1.5",
                ModelRole.CODING: "grok-1.5",
                ModelRole.REASONING: "grok-2"
            }
        },
        
        "enterprise_mix": {
            "name": "Enterprise Multi-Provider Optimization",
            "description": "Best model for each task across all providers",
            "provider": ProviderType.MULTI_PROVIDER,
            "models": {
                ModelRole.CHAT: ("anthropic", "claude-4-opus"),        # Best reasoning
                ModelRole.RESEARCH: ("google_vertex", "gemini-2.5-pro"), # Best search integration
                ModelRole.BUILD: ("openai", "gpt-4"),                   # Best coding
                ModelRole.CREATIVE: ("xai", "grok-2"),                  # Most innovative  
                ModelRole.ANALYSIS: ("anthropic", "claude-4-opus"),     # Best analysis
                ModelRole.CODING: ("openai", "gpt-4"),                  # Best for code
                ModelRole.REASONING: ("anthropic", "claude-4-opus")     # Best reasoning
            }
        },
        
        "budget_optimizer": {
            "name": "Cost-Optimized Performance",
            "description": "Maximum capability per dollar spent",
            "provider": ProviderType.MULTI_PROVIDER,
            "models": {
                ModelRole.CHAT: ("anthropic", "claude-3.5-haiku"),
                ModelRole.RESEARCH: ("google_vertex", "gemini-2.5-flash"),
                ModelRole.BUILD: ("openai", "gpt-3.5-turbo"),
                ModelRole.CREATIVE: ("xai", "grok-mini"),
                ModelRole.ANALYSIS: ("google_vertex", "gemini-2.0-flash"),
                ModelRole.CODING: ("openai", "gpt-3.5-turbo"),
                ModelRole.REASONING: ("anthropic", "claude-3.5-sonnet")
            }
        }
    }
    
    def __init__(self):
        self.user_configs = {}
        self.active_config = None
        
    def create_custom_config(self, 
                           user_id: str, 
                           config_name: str,
                           model_mapping: Dict[ModelRole, Union[str, tuple]],
                           provider: ProviderType = ProviderType.MULTI_PROVIDER) -> Dict:
        """
        Create a custom model configuration for a user
        This is where users can build their own "pizza menu" selection
        """
        config = {
            "name": config_name,
            "user_id": user_id,
            "provider": provider,
            "models": model_mapping,
            "created_at": "2025-06-29",  # Current date
            "custom": True
        }
        
        self.user_configs[f"{user_id}_{config_name}"] = config
        return config
    
    def get_template_config(self, template_name: str) -> Dict:
        """Get a pre-defined configuration template"""
        return self.CONFIGURATION_TEMPLATES.get(template_name)
    
    def list_available_templates(self) -> Dict[str, str]:
        """List all available configuration templates"""
        return {
            name: config["description"] 
            for name, config in self.CONFIGURATION_TEMPLATES.items()
        }
    
    def get_provider_models(self, provider: ProviderType) -> Dict[str, Dict]:
        """Get available models for a specific provider"""
        return self.PROVIDER_MODELS.get(provider, {})
    
    def validate_config(self, config: Dict) -> tuple[bool, List[str]]:
        """Validate a model configuration"""
        errors = []
        
        if "models" not in config:
            errors.append("Configuration must include 'models' mapping")
            return False, errors
            
        required_roles = [ModelRole.CHAT, ModelRole.RESEARCH, ModelRole.BUILD]
        
        for role in required_roles:
            if role not in config["models"]:
                errors.append(f"Missing required role: {role}")
                
        return len(errors) == 0, errors
    
    def export_config(self, config_key: str, format: str = "yaml") -> str:
        """Export a configuration to YAML or JSON"""
        config = self.user_configs.get(config_key)
        if not config:
            raise ValueError(f"Configuration '{config_key}' not found")
            
        if format.lower() == "yaml":
            return yaml.dump(config, default_flow_style=False)
        else:
            return json.dumps(config, indent=2)

class ZAIProviderRouter:
    """
    Routes requests to the appropriate provider based on user configuration
    This is the orchestration layer that Nathan envisioned
    """
    
    def __init__(self, user_config: Dict, credentials: Dict[ProviderType, ProviderCredentials]):
        self.config = user_config
        self.credentials = credentials
        self.registry = ZAIModelRegistry()
        
    def get_model_for_task(self, task_type: ModelRole) -> tuple[ProviderType, str]:
        """
        Get the optimal model for a specific task based on user preferences
        This is where ZAI's orchestration magic happens!
        """
        model_mapping = self.config.get("models", {})
        
        if task_type not in model_mapping:
            # Fallback to chat model
            task_type = ModelRole.CHAT
            
        model_config = model_mapping[task_type]
        
        if isinstance(model_config, tuple):
            # Multi-provider config: (provider, model)
            provider_str, model_name = model_config
            provider = ProviderType(provider_str)
        else:
            # Single provider config
            provider = ProviderType(self.config["provider"])
            model_name = model_config
            
        return provider, model_name
    
    def route_request(self, task_type: ModelRole, request_data: Dict) -> Dict:
        """
        Route a request to the appropriate provider and model
        Returns the configuration needed for the request
        """
        provider, model_name = self.get_model_for_task(task_type)
        provider_creds = self.credentials.get(provider)
        
        if not provider_creds:
            raise ValueError(f"No credentials configured for provider: {provider}")
            
        return {
            "provider": provider,
            "model": model_name,
            "credentials": provider_creds,
            "task_type": task_type,
            "request_data": request_data
        }

# Example usage demonstrating Nathan's vision
def demonstrate_zai_multi_provider():
    """
    This demonstrates how Nathan's vision works in practice
    """
    registry = ZAIModelRegistry()
    
    print("[PIZZA] ZAI MODEL PROVIDER MENU [PIZZA]")
    print("=" * 50)
    
    # Show available templates
    templates = registry.list_available_templates()
    for name, desc in templates.items():
        print(f"[OK] {name}: {desc}")
    
    print("\n[TARGET] EXAMPLE: Nathan's Preferred Setup")
    print("=" * 50)
    
    # Nathan's preference: Anthropic Claude
    nathan_config = registry.get_template_config("anthropic_claude_lover")
    print(f"Config: {nathan_config['name']}")
    print(f"Description: {nathan_config['description']}")
    print("\nModel Assignments:")
    for role, model in nathan_config["models"].items():
        print(f"  {role.value}: {model}")
    
    print("\n[LAUNCH] EXAMPLE: Enterprise Multi-Provider")
    print("=" * 50)
    
    enterprise_config = registry.get_template_config("enterprise_mix")
    print(f"Config: {enterprise_config['name']}")
    print("\nOptimized Model Selection:")
    for role, (provider, model) in enterprise_config["models"].items():
        print(f"  {role.value}: {provider} → {model}")

if __name__ == "__main__":
    demonstrate_zai_multi_provider()
