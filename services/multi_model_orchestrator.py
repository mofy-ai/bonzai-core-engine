"""
[STAR] Multi-Model Orchestrator for Podplay Sanctuary
Supports Claude 3.5, Gemini, and OpenAI with Computer Use API integration
Designed for neurodivergent-friendly AI development platform
"""

import asyncio
import json
import logging
import os
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import google.generativeai as genai
from anthropic import Anthropic
from openai import OpenAI

logger = logging.getLogger(__name__)

class ModelProvider(Enum):
    CLAUDE = "claude"
    GEMINI = "gemini"
    OPENAI = "openai"

class CapabilityType(Enum):
    FUNCTION_CALLING = "function_calling"
    COMPUTER_USE = "computer_use"
    CODE_EXECUTION = "code_execution"
    WEB_BROWSING = "web_browsing"
    IMAGE_GENERATION = "image_generation"
    MEMORY_OPERATIONS = "memory_operations"

@dataclass
class ModelConfig:
    """Configuration for each AI model"""
    provider: ModelProvider
    model_name: str
    api_key: str
    capabilities: List[CapabilityType]
    max_tokens: int = 4096
    temperature: float = 0.1
    supports_cua: bool = False  # Computer Use API support
    function_calling_format: str = "openai"  # openai, anthropic, or gemini

@dataclass
class FunctionDefinition:
    """Universal function definition that works across all models"""
    name: str
    description: str
    parameters: Dict[str, Any]
    provider_specific: Dict[str, Any] = field(default_factory=dict)

class MultiModelOrchestrator:
    """
    Orchestrates multiple AI models with unified interface
    Supports Claude 3.5, Gemini, and OpenAI with Computer Use API
    """
    
    def __init__(self):
        self.models: Dict[ModelProvider, ModelConfig] = {}
        self.clients: Dict[ModelProvider, Any] = {}
        self.function_registry: Dict[str, FunctionDefinition] = {}
        
        # Initialize model configurations
        self._initialize_models()
        
        # Register Sanctuary-specific functions
        self._register_sanctuary_functions()
        
        logger.info("[STAR] Multi-Model Orchestrator initialized for Podplay Sanctuary")
    
    def _initialize_models(self):
        """Initialize all available AI models"""
        
        # Claude 3.5 Sonnet (Primary for Computer Use)
        if os.getenv('ANTHROPIC_API_KEY'):
            self.models[ModelProvider.CLAUDE] = ModelConfig(
                provider=ModelProvider.CLAUDE,
                model_name="claude-3-5-sonnet-20241022",
                api_key=os.getenv('ANTHROPIC_API_KEY'),
                capabilities=[
                    CapabilityType.FUNCTION_CALLING,
                    CapabilityType.COMPUTER_USE,
                    CapabilityType.CODE_EXECUTION,
                    CapabilityType.WEB_BROWSING
                ],
                max_tokens=8192,
                supports_cua=True,
                function_calling_format="anthropic"
            )
            self.clients[ModelProvider.CLAUDE] = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            logger.info("[OK] Claude 3.5 Sonnet initialized with Computer Use API support")
        
        # Gemini 2.5 Pro (Advanced Function Calling Specialist)
        if os.getenv('GOOGLE_API_KEY'):
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            self.models[ModelProvider.GEMINI] = ModelConfig(
                provider=ModelProvider.GEMINI,
                model_name="gemini-2.5-pro-preview-06-05",  # Latest 2.5 model with 65K output
                api_key=os.getenv('GOOGLE_API_KEY'),
                capabilities=[
                    CapabilityType.FUNCTION_CALLING,
                    CapabilityType.CODE_EXECUTION,
                    CapabilityType.WEB_BROWSING,
                    CapabilityType.MEMORY_OPERATIONS
                ],
                max_tokens=65536,  # Much higher output limit
                supports_cua=False,  # Will route CUA requests to Claude
                function_calling_format="gemini"
            )
            self.clients[ModelProvider.GEMINI] = genai.GenerativeModel('gemini-2.5-pro-preview-06-05')
            logger.info("[OK] Gemini 2.5 Pro initialized with advanced function calling support")
        
        # OpenAI GPT-4 (Backup and Specialized Tasks)
        if os.getenv('OPENAI_API_KEY'):
            self.models[ModelProvider.OPENAI] = ModelConfig(
                provider=ModelProvider.OPENAI,
                model_name="gpt-4o",
                api_key=os.getenv('OPENAI_API_KEY'),
                capabilities=[
                    CapabilityType.FUNCTION_CALLING,
                    CapabilityType.CODE_EXECUTION,
                    CapabilityType.IMAGE_GENERATION,
                    CapabilityType.MEMORY_OPERATIONS
                ],
                max_tokens=4096,
                supports_cua=False,
                function_calling_format="openai"
            )
            self.clients[ModelProvider.OPENAI] = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            logger.info("[OK] OpenAI GPT-4 initialized")
    
    def _register_sanctuary_functions(self):
        """Register Podplay Sanctuary specific functions"""
        
        # Scrapybara Computer Use Functions
        self.function_registry["scrapybara_browse"] = FunctionDefinition(
            name="scrapybara_browse",
            description="Browse websites using Scrapybara with neurodivergent-friendly interface",
            parameters={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL to browse"},
                    "extract_markdown": {"type": "boolean", "description": "Extract as markdown"},
                    "accessibility_mode": {"type": "boolean", "description": "Enable accessibility features"}
                },
                "required": ["url"]
            },
            provider_specific={
                "anthropic": {"type": "computer_20241022"},
                "gemini": {"function_declarations": True},
                "openai": {"type": "function"}
            }
        )
        
        self.function_registry["scrapybara_code_execute"] = FunctionDefinition(
            name="scrapybara_code_execute",
            description="Execute code safely in Scrapybara environment",
            parameters={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Code to execute"},
                    "language": {"type": "string", "description": "Programming language"},
                    "sanctuary_mode": {"type": "boolean", "description": "Enable sanctuary safety features"}
                },
                "required": ["code", "language"]
            }
        )
        
        # Mama Bear Memory Functions
        self.function_registry["mama_bear_remember"] = FunctionDefinition(
            name="mama_bear_remember",
            description="Store information in Mama Bear's caring memory system",
            parameters={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Information to remember"},
                    "user_id": {"type": "string", "description": "User identifier"},
                    "emotional_context": {"type": "string", "description": "Emotional context for caring responses"},
                    "neurodivergent_notes": {"type": "string", "description": "Special considerations for neurodivergent users"}
                },
                "required": ["content", "user_id"]
            }
        )
        
        self.function_registry["mama_bear_recall"] = FunctionDefinition(
            name="mama_bear_recall",
            description="Recall information from Mama Bear's memory with empathy",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "What to remember"},
                    "user_id": {"type": "string", "description": "User identifier"},
                    "emotional_support": {"type": "boolean", "description": "Include emotional support in response"}
                },
                "required": ["query", "user_id"]
            }
        )
        
        logger.info(f"[BOOKS] Registered {len(self.function_registry)} Sanctuary functions")
    
    async def route_request(self, 
                          prompt: str, 
                          user_id: str,
                          capabilities_needed: List[CapabilityType],
                          preferred_provider: Optional[ModelProvider] = None) -> Dict[str, Any]:
        """
        Intelligently route requests to the best model based on capabilities needed
        """
        
        # Determine best model for the request
        best_provider = self._select_best_provider(capabilities_needed, preferred_provider)
        
        if not best_provider:
            return {
                "success": False,
                "error": "No suitable model available for requested capabilities",
                "capabilities_needed": [cap.value for cap in capabilities_needed]
            }
        
        # Special routing for Computer Use API
        if CapabilityType.COMPUTER_USE in capabilities_needed:
            if best_provider != ModelProvider.CLAUDE:
                logger.info(f"[SYNC] Routing Computer Use request from {best_provider.value} to Claude 3.5")
                best_provider = ModelProvider.CLAUDE
        
        # Execute request with selected model
        return await self._execute_with_provider(
            provider=best_provider,
            prompt=prompt,
            user_id=user_id,
            capabilities_needed=capabilities_needed
        )
    
    def _select_best_provider(self, 
                            capabilities_needed: List[CapabilityType],
                            preferred_provider: Optional[ModelProvider] = None) -> Optional[ModelProvider]:
        """Select the best AI model provider for the given capabilities"""
        
        # If preferred provider is specified and available, check if it supports needed capabilities
        if preferred_provider and preferred_provider in self.models:
            model_config = self.models[preferred_provider]
            if all(cap in model_config.capabilities for cap in capabilities_needed):
                return preferred_provider
        
        # Capability-based routing
        if CapabilityType.COMPUTER_USE in capabilities_needed:
            # Only Claude 3.5 supports Computer Use API
            if ModelProvider.CLAUDE in self.models:
                return ModelProvider.CLAUDE
        
        if CapabilityType.FUNCTION_CALLING in capabilities_needed:
            # Prefer Gemini for function calling (as requested)
            if ModelProvider.GEMINI in self.models:
                gemini_config = self.models[ModelProvider.GEMINI]
                if all(cap in gemini_config.capabilities for cap in capabilities_needed):
                    return ModelProvider.GEMINI
        
        if CapabilityType.IMAGE_GENERATION in capabilities_needed:
            # OpenAI is best for image generation
            if ModelProvider.OPENAI in self.models:
                return ModelProvider.OPENAI
        
        # Default fallback order: Claude -> Gemini -> OpenAI
        for provider in [ModelProvider.CLAUDE, ModelProvider.GEMINI, ModelProvider.OPENAI]:
            if provider in self.models:
                model_config = self.models[provider]
                if all(cap in model_config.capabilities for cap in capabilities_needed):
                    return provider
        
        return None
    
    async def _execute_with_provider(self,
                                   provider: ModelProvider,
                                   prompt: str,
                                   user_id: str,
                                   capabilities_needed: List[CapabilityType]) -> Dict[str, Any]:
        """Execute request with specific provider"""
        
        try:
            model_config = self.models[provider]
            client = self.clients[provider]
            
            # Prepare functions for the request
            functions = self._prepare_functions_for_provider(provider, capabilities_needed)
            
            if provider == ModelProvider.CLAUDE:
                return await self._execute_claude(client, model_config, prompt, user_id, functions)
            elif provider == ModelProvider.GEMINI:
                return await self._execute_gemini(client, model_config, prompt, user_id, functions)
            elif provider == ModelProvider.OPENAI:
                return await self._execute_openai(client, model_config, prompt, user_id, functions)
            
        except Exception as e:
            logger.error(f"Error executing with {provider.value}: {e}")
            return {
                "success": False,
                "error": str(e),
                "provider": provider.value
            }
    
    def _prepare_functions_for_provider(self, 
                                      provider: ModelProvider, 
                                      capabilities_needed: List[CapabilityType]) -> List[Dict[str, Any]]:
        """Prepare function definitions in provider-specific format"""
        
        functions = []
        
        for func_name, func_def in self.function_registry.items():
            # Convert to provider-specific format
            if provider == ModelProvider.CLAUDE:
                functions.append({
                    "name": func_def.name,
                    "description": func_def.description,
                    "input_schema": func_def.parameters
                })
            elif provider == ModelProvider.GEMINI:
                functions.append({
                    "name": func_def.name,
                    "description": func_def.description,
                    "parameters": func_def.parameters
                })
            elif provider == ModelProvider.OPENAI:
                functions.append({
                    "type": "function",
                    "function": {
                        "name": func_def.name,
                        "description": func_def.description,
                        "parameters": func_def.parameters
                    }
                })
        
        return functions
    
    async def _execute_claude(self, client, config, prompt, user_id, functions):
        """Execute request with Claude 3.5"""
        
        # Prepare messages for Claude
        messages = [
            {
                "role": "user",
                "content": f"[BEAR] Sanctuary Request from {user_id}: {prompt}"
            }
        ]
        
        # Add Computer Use API tools if needed
        tools = []
        if config.supports_cua:
            # Use the correct Claude tool names - Computer Use API only
            tools.extend([
                {
                    "type": "bash_20250124",
                    "name": "bash"
                },
                {
                    "type": "text_editor_20250124",
                    "name": "str_replace_editor"
                },
                {
                    "type": "web_search_20250305",
                    "name": "web_search"
                }
            ])
        else:
            # Add function tools only if not using Computer Use API
            for func in functions:
                tools.append({
                    "type": "function",
                    "function": func
                })
        
        response = client.messages.create(
            model=config.model_name,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            messages=messages,
            tools=tools if tools else None
        )
        
        return {
            "success": True,
            "provider": "claude",
            "response": response.content[0].text if response.content else "",
            "tool_calls": getattr(response, 'tool_calls', []),
            "model": config.model_name
        }
    
    async def _execute_gemini(self, client, config, prompt, user_id, functions):
        """Execute request with Gemini (Function Calling Specialist)"""
        
        try:
            # Simplified approach - use basic generation without complex function calling for now
            sanctuary_prompt = f"[STAR] Podplay Sanctuary Request from {user_id}: {prompt}\n\nPlease respond with empathy and consideration for neurodivergent users."
            
            response = client.generate_content(
                sanctuary_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=config.temperature,
                    max_output_tokens=config.max_tokens
                )
            )
            
            # Handle response safely
            response_text = ""
            function_calls = []
            
            if response.parts:
                for part in response.parts:
                    if hasattr(part, 'text') and part.text:
                        response_text += part.text
                    elif hasattr(part, 'function_call'):
                        function_calls.append({
                            "name": part.function_call.name,
                            "args": dict(part.function_call.args) if part.function_call.args else {}
                        })
            
            return {
                "success": True,
                "provider": "gemini",
                "response": response_text,
                "function_calls": function_calls,
                "model": config.model_name,
                "sanctuary_note": "[STAR] Gemini response optimized for neurodivergent users"
            }
            
        except Exception as e:
            logger.error(f"Gemini execution error: {e}")
            return {
                "success": False,
                "provider": "gemini",
                "error": str(e),
                "sanctuary_note": "[EMOJI] Gemini encountered an issue, but we're here to help"
            }
    
    async def _execute_openai(self, client, config, prompt, user_id, functions):
        """Execute request with OpenAI"""
        
        messages = [
            {
                "role": "system",
                "content": "You are Mama Bear, a caring AI assistant for Podplay Sanctuary, designed to support neurodivergent developers with empathy and understanding."
            },
            {
                "role": "user", 
                "content": f"Sanctuary request from {user_id}: {prompt}"
            }
        ]
        
        response = client.chat.completions.create(
            model=config.model_name,
            messages=messages,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            tools=functions if functions else None,
            tool_choice="auto" if functions else None
        )
        
        return {
            "success": True,
            "provider": "openai",
            "response": response.choices[0].message.content,
            "tool_calls": getattr(response.choices[0].message, 'tool_calls', []),
            "model": config.model_name
        }
    
    def get_available_models(self) -> Dict[str, Any]:
        """Get information about available models and their capabilities"""
        
        models_info = {}
        for provider, config in self.models.items():
            models_info[provider.value] = {
                "model_name": config.model_name,
                "capabilities": [cap.value for cap in config.capabilities],
                "supports_cua": config.supports_cua,
                "function_calling_format": config.function_calling_format,
                "max_tokens": config.max_tokens
            }
        
        return {
            "available_models": models_info,
            "total_models": len(self.models),
            "cua_capable_models": [p.value for p, c in self.models.items() if c.supports_cua],
            "function_calling_models": [p.value for p, c in self.models.items() if CapabilityType.FUNCTION_CALLING in c.capabilities]
        }

# Factory function for easy initialization
async def create_multi_model_orchestrator() -> MultiModelOrchestrator:
    """Create and initialize the multi-model orchestrator"""
    orchestrator = MultiModelOrchestrator()
    logger.info("[STAR] Multi-Model Orchestrator ready for Podplay Sanctuary")
    return orchestrator