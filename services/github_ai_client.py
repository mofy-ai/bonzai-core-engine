"""
🚀 GitHub AI Models Integration Service
Integrates GitHub's AI models via Azure AI Inference for the Bonzai Core Engine
"""

import os
import logging
from typing import List, Dict, Any, Optional
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

logger = logging.getLogger(__name__)

class GitHubAIClient:
    """Client for interacting with GitHub AI models via Azure AI Inference"""
    
    def __init__(self):
        self.endpoint = "https://models.github.ai/inference"
        self.token = os.environ.get("GITHUB_TOKEN")
        
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
            
        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.token),
        )
        
        # Available models
        self.models = {
            "gpt-4.1": "openai/gpt-4.1",
            "gpt-4o": "openai/gpt-4o",
            "gpt-4o-mini": "openai/gpt-4o-mini",
            "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
            "llama-3.3-70b": "meta/llama-3.3-70b-instruct",
            "phi-3.5-mini": "microsoft/phi-3.5-mini-instruct"
        }
        
        logger.info(f"GitHub AI Client initialized with {len(self.models)} available models")
    
    def chat(self, 
             messages: List[Dict[str, str]], 
             model: str = "gpt-4.1",
             temperature: float = 0.7,
             max_tokens: Optional[int] = None,
             **kwargs) -> str:
        """
        Send a chat completion request to GitHub AI models
        
        Args:
            messages: List of messages with 'role' and 'content' keys
            model: Model to use (key from self.models)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Response content as string
        """
        try:
            # Convert messages to Azure AI format
            azure_messages = []
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                if role == "system":
                    azure_messages.append(SystemMessage(content))
                elif role == "user":
                    azure_messages.append(UserMessage(content))
                elif role == "assistant":
                    azure_messages.append(AssistantMessage(content))
            
            # Get model name
            model_name = self.models.get(model, model)
            
            # Prepare request parameters
            request_params = {
                "messages": azure_messages,
                "temperature": temperature,
                "model": model_name,
                **kwargs
            }
            
            if max_tokens:
                request_params["max_tokens"] = max_tokens
            
            # Make the request
            response = self.client.complete(**request_params)
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"GitHub AI request failed: {str(e)}")
            raise
    
    def simple_completion(self, 
                         prompt: str, 
                         model: str = "gpt-4.1",
                         system_prompt: Optional[str] = None) -> str:
        """Simple completion with optional system prompt"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        return self.chat(messages, model)
    
    def code_completion(self, 
                       code_context: str, 
                       request: str,
                       model: str = "gpt-4.1") -> str:
        """Specialized code completion"""
        system_prompt = """You are an expert software engineer assistant. 
        Provide clean, efficient, and well-documented code solutions.
        Focus on best practices and maintainable code."""
        
        prompt = f"""Code Context:
{code_context}

Request:
{request}

Please provide a complete solution with explanations."""

        return self.simple_completion(prompt, model, system_prompt)
    
    def get_available_models(self) -> Dict[str, str]:
        """Get available models"""
        return self.models.copy()
    
    def test_connection(self) -> bool:
        """Test the connection to GitHub AI"""
        try:
            response = self.simple_completion(
                "Hello, please respond with 'Connection successful'",
                model="gpt-4o-mini"
            )
            return "successful" in response.lower()
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False

# Convenience functions
def create_github_ai_client() -> GitHubAIClient:
    """Factory function to create GitHub AI client"""
    return GitHubAIClient()

def quick_chat(prompt: str, model: str = "gpt-4.1") -> str:
    """Quick chat completion"""
    client = create_github_ai_client()
    return client.simple_completion(prompt, model)

def code_assist(code_context: str, request: str, model: str = "gpt-4.1") -> str:
    """Quick code assistance"""
    client = create_github_ai_client()
    return client.code_completion(code_context, request, model)