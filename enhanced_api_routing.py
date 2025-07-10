"""
🔑 ENHANCED API KEY ROUTING SYSTEM
Multi-Model Primary Routing for Nathan's AI Family
Each API key activates a different AI family member as "prime"
"""

import os
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List

logger = logging.getLogger("EnhancedAPIKeyManager")

class EnhancedAPIKeyManager:
    """
    🔑 Enhanced API Key Management with Model Routing
    Different API keys route to different primary AI family members
    """
    
    def __init__(self, family_system):
        self.family_system = family_system
        self.redis_client = family_system.redis_client
        
        # Initialize specialized API keys with model routing
        self.setup_model_routing_keys()
    
    def setup_model_routing_keys(self):
        """Setup specialized API keys for different primary models"""
        
        # Define model-specific API keys
        specialized_keys = [
            {
                "api_key": "bz_claude_prime_789",
                "user_id": "nathan_claude_mode",
                "tier": "enterprise",
                "primary_model": "claude-sonnet-4",
                "primary_family_member": "claude_desktop",
                "routing_preference": "anthropic_primary",
                "daily_limit": 50000,
                "features": [
                    "anthropic_models", "claude_desktop_integration", "advanced_reasoning",
                    "family_coordination", "memory_export", "technical_analysis"
                ],
                "model_access": {
                    "anthropic": {"priority": 1, "models": ["claude-sonnet-4", "claude-opus-4"]},
                    "gemini": {"priority": 2, "models": ["gemini-2.0-flash-exp", "gemini-1.5-pro"]},
                    "grok": {"priority": 3, "models": ["xai/grok-3"]},
                    "openai": {"priority": 4, "models": ["gpt-4", "gpt-3.5-turbo"]}
                },
                "description": "Claude (Anthropic) as Primary - Papa Bear Mode"
            },
            {
                "api_key": "bz_gemini_prime_456",
                "user_id": "nathan_gemini_mode", 
                "tier": "enterprise",
                "primary_model": "gemini-2.0-flash-exp",
                "primary_family_member": "zai_prime",
                "routing_preference": "google_primary",
                "daily_limit": 50000,
                "features": [
                    "google_models", "gemini_pro_access", "creative_intelligence",
                    "multimodal_processing", "advanced_search", "visual_analysis"
                ],
                "model_access": {
                    "gemini": {"priority": 1, "models": ["gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-2.5-pro"]},
                    "anthropic": {"priority": 2, "models": ["claude-sonnet-4"]},
                    "grok": {"priority": 3, "models": ["xai/grok-3"]},
                    "openai": {"priority": 4, "models": ["gpt-4"]}
                },
                "description": "Gemini 2.5 Pro as Primary - ZAI Prime Mode"
            },
            {
                "api_key": "bz_grok_prime_123",
                "user_id": "nathan_grok_mode",
                "tier": "enterprise", 
                "primary_model": "xai/grok-3",
                "primary_family_member": "grok_3",
                "routing_preference": "grok_primary",
                "daily_limit": 50000,
                "features": [
                    "github_models", "xai_grok_access", "cutting_edge_reasoning",
                    "witty_intelligence", "github_integration", "repo_analysis",
                    "code_understanding", "github_ecosystem_access"
                ],
                "model_access": {
                    "grok": {"priority": 1, "models": ["xai/grok-3"], "provider": "github_models"},
                    "anthropic": {"priority": 2, "models": ["claude-sonnet-4"]},
                    "gemini": {"priority": 3, "models": ["gemini-2.0-flash-exp"]},
                    "openai": {"priority": 4, "models": ["gpt-4"]}
                },
                "github_integration": {
                    "repo_access": True,
                    "can_read_repo": "mofy-ai/bonzai-core-engine",
                    "can_analyze_code": True,
                    "can_suggest_improvements": True,
                    "can_create_issues": True,
                    "github_actions_aware": True
                },
                "description": "Grok-3 as Primary - GitHub-Integrated Witty AI Mode"
            },
            {
                "api_key": "bz_family_orchestrator_999",
                "user_id": "nathan_orchestrator_mode",
                "tier": "enterprise",
                "primary_model": "dynamic_routing",
                "primary_family_member": "family_coordinator",
                "routing_preference": "intelligent_routing",
                "daily_limit": 100000,
                "features": [
                    "all_models", "intelligent_routing", "family_coordination",
                    "dynamic_model_selection", "context_aware_routing", "performance_optimization"
                ],
                "model_access": {
                    "dynamic": {"priority": 1, "strategy": "context_based"},
                    "anthropic": {"priority": 1, "models": ["claude-sonnet-4"]},
                    "gemini": {"priority": 1, "models": ["gemini-2.0-flash-exp"]}, 
                    "grok": {"priority": 1, "models": ["xai/grok-3"]},
                    "openai": {"priority": 1, "models": ["gpt-4"]}
                },
                "description": "Intelligent Family Orchestrator - Auto-selects best AI for each task"
            }
        ]
        
        # Store specialized keys in Mem0 and Redis
        for key_data in specialized_keys:
            try:
                # Store in family memory for long-term management
                self.family_system.add_family_memory(
                    content=f"Enhanced API Key: {key_data['description']}",
                    member_id="system",
                    category="enhanced_api_keys",
                    metadata=key_data
                )
                
                # Cache in Redis for fast routing
                self.redis_client.setex(
                    f"enhanced_key:{key_data['api_key']}", 
                    86400, 
                    json.dumps(key_data)
                )
                
                logger.info(f"✅ Setup {key_data['primary_family_member']} routing key")
                
            except Exception as e:
                logger.warning(f"Could not store enhanced API key: {e}")
    
    async def validate_and_route_api_key(self, key: str) -> Optional[Dict]:
        """Validate API key and return routing configuration"""
        
        # Check Redis cache first
        cached_data = self.redis_client.get(f"enhanced_key:{key}")
        if cached_data:
            key_data = json.loads(cached_data)
            
            # Update usage statistics
            key_data["last_used"] = datetime.now().isoformat()
            key_data["usage_count"] = key_data.get("usage_count", 0) + 1
            
            # Re-cache with updated stats
            self.redis_client.setex(f"enhanced_key:{key}", 86400, json.dumps(key_data))
            
            return key_data
        
        # Fall back to regular API key validation
        try:
            results = await self.family_system.search_family_memory(
                query=f"Enhanced API Key: {key}",
                search_filters={"category": "enhanced_api_keys"}
            )
            
            if results:
                key_data = results[0].get("metadata", {})
                
                # Update usage
                key_data["usage_count"] = key_data.get("usage_count", 0) + 1
                key_data["last_used"] = datetime.now().isoformat()
                
                # Cache for future use
                self.redis_client.setex(f"enhanced_key:{key}", 86400, json.dumps(key_data))
                
                return key_data
            
        except Exception as e:
            logger.error(f"Error validating enhanced API key: {e}")
        
        return None
    
    def get_primary_model_config(self, key_data: Dict) -> Dict[str, Any]:
        """Get primary model configuration for routing"""
        
        primary_model = key_data.get("primary_model", "claude-sonnet-4")
        primary_member = key_data.get("primary_family_member", "claude_desktop")
        routing_preference = key_data.get("routing_preference", "anthropic_primary")
        model_access = key_data.get("model_access", {})
        
        return {
            "primary_model": primary_model,
            "primary_family_member": primary_member,
            "routing_preference": routing_preference,
            "model_access": model_access,
            "github_integration": key_data.get("github_integration", {}),
            "features": key_data.get("features", []),
            "tier": key_data.get("tier", "basic")
        }
    
    def should_use_grok_for_request(self, request_content: str, routing_config: Dict) -> bool:
        """Determine if Grok-3 should handle this request"""
        
        # If Grok is primary, use it unless specifically requesting another model
        if routing_config.get("routing_preference") == "grok_primary":
            return True
        
        # Check for GitHub/repo-related content
        github_keywords = [
            "github", "repository", "repo", "code", "commit", "pull request",
            "issue", "branch", "merge", "git", "workflow", "action", 
            "file structure", "codebase", "programming", "development"
        ]
        
        content_lower = request_content.lower()
        github_related = any(keyword in content_lower for keyword in github_keywords)
        
        # Use Grok if request is GitHub-related and Grok has repo access
        github_integration = routing_config.get("github_integration", {})
        if github_related and github_integration.get("repo_access", False):
            return True
        
        return False
    
    def should_use_gemini_for_request(self, request_content: str, routing_config: Dict) -> bool:
        """Determine if Gemini should handle this request"""
        
        # If Gemini is primary, use it unless specifically requesting another model
        if routing_config.get("routing_preference") == "google_primary":
            return True
        
        # Check for creative/visual/multimodal content
        creative_keywords = [
            "creative", "visual", "image", "design", "artistic", "multimodal",
            "video", "audio", "creative writing", "brainstorm", "innovative",
            "imagine", "visualize", "creative solution"
        ]
        
        content_lower = request_content.lower()
        creative_related = any(keyword in content_lower for keyword in creative_keywords)
        
        return creative_related
    
    def should_use_claude_for_request(self, request_content: str, routing_config: Dict) -> bool:
        """Determine if Claude should handle this request"""
        
        # If Claude is primary, use it unless specifically requesting another model
        if routing_config.get("routing_preference") == "anthropic_primary":
            return True
        
        # Check for analytical/reasoning content
        analytical_keywords = [
            "analyze", "reasoning", "logic", "complex", "technical", "detailed",
            "explanation", "problem solving", "systematic", "thorough", "research",
            "academic", "professional", "analysis", "evaluate"
        ]
        
        content_lower = request_content.lower()
        analytical_related = any(keyword in content_lower for keyword in analytical_keywords)
        
        return analytical_related

    async def route_request_to_optimal_model(self, request_content: str, key_data: Dict) -> Dict[str, Any]:
        """Route request to optimal AI family member based on content and key configuration"""
        
        routing_config = self.get_primary_model_config(key_data)
        
        # Determine optimal routing
        if self.should_use_grok_for_request(request_content, routing_config):
            return {
                "selected_model": "xai/grok-3",
                "selected_family_member": "grok_3",
                "provider": "github_models",
                "reasoning": "GitHub/code-related content + Grok-3 repo access",
                "routing_config": routing_config
            }
        elif self.should_use_gemini_for_request(request_content, routing_config):
            return {
                "selected_model": "gemini-2.0-flash-exp", 
                "selected_family_member": "zai_prime",
                "provider": "google",
                "reasoning": "Creative/multimodal content suited for Gemini",
                "routing_config": routing_config
            }
        elif self.should_use_claude_for_request(request_content, routing_config):
            return {
                "selected_model": "claude-sonnet-4",
                "selected_family_member": "claude_desktop", 
                "provider": "anthropic",
                "reasoning": "Analytical/reasoning content suited for Claude",
                "routing_config": routing_config
            }
        else:
            # Default to primary model from API key
            primary_model = routing_config.get("primary_model", "claude-sonnet-4")
            primary_member = routing_config.get("primary_family_member", "claude_desktop")
            
            return {
                "selected_model": primary_model,
                "selected_family_member": primary_member,
                "provider": "primary_from_key",
                "reasoning": f"Using primary model from API key: {primary_model}",
                "routing_config": routing_config
            }

# Export the enhanced manager
__all__ = ['EnhancedAPIKeyManager']
