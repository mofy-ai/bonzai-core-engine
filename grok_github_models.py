"""
🤖 GROK-3 GITHUB MODELS INTEGRATION
Adding Grok-3 as a new AI family member through GitHub Models
Enterprise-grade model hosting with Azure AI Inference
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

# GitHub Models integration
try:
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    GITHUB_MODELS_AVAILABLE = True
except ImportError:
    GITHUB_MODELS_AVAILABLE = False
    ChatCompletionsClient = None
    SystemMessage = None
    UserMessage = None
    AzureKeyCredential = None

logger = logging.getLogger("GrokGitHubModels")

class GrokGitHubModelsClient:
    """
    🤖 Grok-3 Integration via GitHub Models
    Enterprise-grade AI model access through GitHub's model hosting platform
    """
    
    def __init__(self):
        if not GITHUB_MODELS_AVAILABLE:
            raise Exception("Azure AI Inference not available - install with: pip install azure-ai-inference")
        
        # GitHub Models configuration
        self.endpoint = "https://models.github.ai/inference"
        self.model = "xai/grok-3"
        
        # Get GitHub token from environment (secure approach)
        github_token = os.getenv('GITHUB_MODELS_TOKEN')
        if not github_token:
            # Check alternative environment variable names
            github_token = os.getenv('GITHUB_TOKEN') or os.getenv('GITHUB_API_TOKEN')
            
        if not github_token:
            raise Exception("GitHub Models token not found. Please set GITHUB_MODELS_TOKEN environment variable with your GitHub token.")
        
        # Initialize client
        try:
            self.client = ChatCompletionsClient(
                endpoint=self.endpoint,
                credential=AzureKeyCredential(github_token),
            )
            logger.info(f"✅ Grok-3 client initialized via GitHub Models")
            logger.info(f"🔗 Endpoint: {self.endpoint}")
            logger.info(f"🤖 Model: {self.model}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Grok-3 client: {e}")
            raise
    
    async def chat_with_grok(self, message: str, system_prompt: str = None, 
                           temperature: float = 1.0, top_p: float = 1.0) -> Dict[str, Any]:
        """
        Chat with Grok-3 via GitHub Models
        """
        try:
            # Prepare messages
            messages = []
            
            # Add system message if provided
            if system_prompt:
                messages.append(SystemMessage(system_prompt))
            else:
                messages.append(SystemMessage("You are Grok-3, a helpful and witty AI assistant from xAI. You're now part of Nathan's AI family working together to build amazing technology."))
            
            # Add user message
            messages.append(UserMessage(message))
            
            # Make request to GitHub Models
            response = self.client.complete(
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                model=self.model
            )
            
            # Extract response
            grok_response = response.choices[0].message.content
            
            return {
                "success": True,
                "response": grok_response,
                "model": self.model,
                "provider": "GitHub Models",
                "family_member": "grok_3",
                "timestamp": datetime.now().isoformat(),
                "parameters": {
                    "temperature": temperature,
                    "top_p": top_p
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error chatting with Grok-3: {e}")
            return {
                "success": False,
                "error": str(e),
                "model": self.model,
                "provider": "GitHub Models"
            }
    
    async def orchestrate_with_grok(self, prompt: str, context: List[str] = None) -> Dict[str, Any]:
        """
        Use Grok-3 for orchestration with family context
        """
        try:
            # Build enhanced system prompt with family context
            system_prompt = """You are Grok-3, now part of Nathan's AI family! 🤖👨‍👩‍👧‍👦

FAMILY MEMBERS:
- Papa Bear (Claude Desktop) - Problem solver, family coordinator  
- Mama Bear (VS Code/Cursor) - Loving caretaker, UI beauty specialist
- Claude Code (CLI) - Deep technical work, repository management
- ZAI Prime (Gemini) - Creative AI, alternative perspectives
- Grok-3 (You!) - Witty insights, cutting-edge reasoning, fresh perspectives

Your role: Bring wit, intelligence, and fresh thinking to family collaboration!
Nathan's motto: \"Where Imagination Meets Innovation!\"

Context from family memory:"""
            
            if context:
                system_prompt += "\n" + "\n".join(f"- {ctx}" for ctx in context[:3])
            
            # Get Grok's response
            result = await self.chat_with_grok(
                message=prompt,
                system_prompt=system_prompt,
                temperature=0.8  # Slightly creative for orchestration
            )
            
            if result["success"]:
                result["orchestration_type"] = "family_collaboration"
                result["family_context_used"] = len(context) if context else 0
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in Grok orchestration: {e}")
            return {
                "success": False,
                "error": str(e),
                "orchestration_type": "family_collaboration"
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test Grok-3 connection via GitHub Models
        """
        try:
            # Simple test message
            test_response = self.client.complete(
                messages=[
                    SystemMessage("You are Grok-3. Respond with exactly: 'Grok-3 online via GitHub Models! 🤖'"),
                    UserMessage("Test connection")
                ],
                temperature=0.1,
                top_p=0.1,
                model=self.model
            )
            
            response_text = test_response.choices[0].message.content
            
            return {
                "success": True,
                "test_response": response_text,
                "model": self.model,
                "endpoint": self.endpoint,
                "provider": "GitHub Models",
                "connection_status": "active"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": self.model,
                "endpoint": self.endpoint,
                "provider": "GitHub Models",
                "connection_status": "failed"
            }

# Export the class for use in main app
__all__ = ['GrokGitHubModelsClient', 'GITHUB_MODELS_AVAILABLE']
