"""
[AI][BEAR] OpenAI via Vertex AI Model Garden Service
Production-ready service for Podplay Sanctuary
"""

import os
import json
import logging
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
import asyncio

import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account
from google.cloud import aiplatform

logger = logging.getLogger(__name__)

@dataclass
class ModelMetrics:
    """Model performance metrics"""
    requests_count: int = 0
    total_tokens: int = 0
    average_latency: float = 0.0
    success_rate: float = 100.0
    last_request: Optional[datetime] = None

@dataclass
class ServiceStatus:
    """Service status information"""
    service: str = "OpenAI via Vertex AI Model Garden"
    status: str = "operational"
    vertex_enabled: bool = True
    openai_fallback_enabled: bool = True
    project_id: str = ""
    location: str = "us-central1"
    available_models: int = 5
    uptime: float = 0.0
    metrics: Dict[str, ModelMetrics] = None

class OpenAIVertexService:
    """
    [AI][BEAR] OpenAI via Vertex AI Model Garden Service

    Provides OpenAI-compatible API using Google Cloud Vertex AI
    """

    def __init__(self):
        """Initialize the service"""
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'podplay-build-alpha')
        self.location = os.getenv('VERTEX_AI_LOCATION', 'us-central1')
        self.service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

        # Service metrics
        self.start_time = time.time()
        self.metrics = {
            'gpt-4o': ModelMetrics(),
            'gpt-4o-mini': ModelMetrics(),
            'gpt-4': ModelMetrics(),
            'gpt-4-turbo': ModelMetrics(),
            'gpt-3.5-turbo': ModelMetrics()
        }

        # Model mapping (using Gemini as proxy until OpenAI models are available)
        self.model_mapping = {
            'gpt-4o': 'gemini-1.5-pro',
            'gpt-4o-mini': 'gemini-1.5-flash',
            'gpt-4': 'gemini-1.5-pro',
            'gpt-4-turbo': 'gemini-1.5-pro',
            'gpt-3.5-turbo': 'gemini-1.5-flash'
        }

        self.vertex_enabled = False
        self.initialize_vertex()

        # Initialize Mama Bear Agentic Superpowers V3.0
        self.agentic_superpowers = self._initialize_agentic_superpowers()

    def _initialize_agentic_superpowers(self):
        """Initialize Mama Bear Agentic Superpowers V3.0"""
        try:
            from .mama_bear_agentic_superpowers_v3 import MamaBearAgenticSuperpowersV3

            config = {
                'vertex_config': {
                    'project_id': self.project_id,
                    'location': self.location,
                    'service_account_path': self.service_account_path
                }
            }

            agentic_superpowers = MamaBearAgenticSuperpowersV3(config)
            logger.info("[BEAR][EMOJI] Mama Bear Agentic Superpowers V3.0 integrated!")
            return agentic_superpowers

        except Exception as e:
            logger.warning(f"Could not initialize agentic superpowers: {e}")
            return None

    def initialize_vertex(self):
        """Initialize Vertex AI with service account"""
        try:
            # Set up service account authentication if path is provided
            if self.service_account_path and os.path.exists(self.service_account_path):
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.service_account_path
                logger.info(f"Using service account: {self.service_account_path}")

            # Initialize Vertex AI
            vertexai.init(project=self.project_id, location=self.location)

            # Test connection with a simple model initialization
            test_model = GenerativeModel('gemini-1.5-flash')
            self.vertex_enabled = True

            logger.info(f"[OK] Vertex AI initialized successfully")
            logger.info(f"Project: {self.project_id}, Location: {self.location}")

        except Exception as e:
            logger.error(f"[ERROR] Failed to initialize Vertex AI: {e}")
            self.vertex_enabled = False

    def get_health_status(self) -> Dict[str, Any]:
        """Get service health status"""
        return {
            "status": "healthy" if self.vertex_enabled else "degraded",
            "vertex_ai": "enabled" if self.vertex_enabled else "disabled",
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": time.time() - self.start_time
        }

    def get_detailed_status(self) -> ServiceStatus:
        """Get detailed service status"""
        status = ServiceStatus(
            project_id=self.project_id,
            location=self.location,
            vertex_enabled=self.vertex_enabled,
            uptime=time.time() - self.start_time,
            metrics=self.metrics
        )

        if not self.vertex_enabled:
            status.status = "degraded"

        return status

    def list_models(self) -> List[Dict[str, Any]]:
        """List available OpenAI models"""
        models = []

        for openai_model, vertex_model in self.model_mapping.items():
            metrics = self.metrics.get(openai_model, ModelMetrics())

            models.append({
                "id": openai_model,
                "object": "model",
                "created": int(self.start_time),
                "owned_by": "openai-vertex",
                "vertex_model": vertex_model,
                "status": "available" if self.vertex_enabled else "unavailable",
                "requests": metrics.requests_count,
                "avg_latency": metrics.average_latency,
                "success_rate": metrics.success_rate
            })

        return models

    async def chat_completion(self,
                            messages: List[Dict[str, str]],
                            model: str = "gpt-4o",
                            temperature: float = 0.7,
                            max_tokens: int = 1000,
                            stream: bool = False) -> Dict[str, Any]:
        """
        Create chat completion using OpenAI-compatible API

        Args:
            messages: List of message objects with 'role' and 'content'
            model: OpenAI model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response

        Returns:
            OpenAI-compatible response
        """
        start_time = time.time()

        try:
            # Validate model
            if model not in self.model_mapping:
                raise ValueError(f"Model {model} not supported")

            if not self.vertex_enabled:
                raise Exception("Vertex AI not available")

            # Get corresponding Vertex AI model
            vertex_model_name = self.model_mapping[model]
            vertex_model = GenerativeModel(vertex_model_name)

            # Convert messages to Vertex AI format
            prompt = self._convert_messages_to_prompt(messages)

            # Generate response
            response = await asyncio.to_thread(
                vertex_model.generate_content,
                prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                }
            )

            # Calculate metrics
            latency = time.time() - start_time
            self._update_metrics(model, latency, success=True)

            # Format as OpenAI response
            return {
                "id": f"chatcmpl-{int(time.time() * 1000)}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": model,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response.text
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": len(prompt.split()) * 1.3,  # Rough estimation
                    "completion_tokens": len(response.text.split()) * 1.3,  # Rough estimation
                    "total_tokens": len((prompt + response.text).split()) * 1.3
                },
                "vertex_model": vertex_model_name,
                "latency": latency
            }

        except Exception as e:
            # Update metrics for failure
            latency = time.time() - start_time
            self._update_metrics(model, latency, success=False)

            logger.error(f"Chat completion error: {e}")
            raise

    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI messages format to simple prompt"""
        prompt_parts = []

        for message in messages:
            role = message.get('role', 'user')
            content = message.get('content', '')

            if role == 'system':
                prompt_parts.append(f"Instructions: {content}")
            elif role == 'user':
                prompt_parts.append(f"User: {content}")
            elif role == 'assistant':
                prompt_parts.append(f"Assistant: {content}")

        return "\n\n".join(prompt_parts)

    def _update_metrics(self, model: str, latency: float, success: bool = True):
        """Update model metrics"""
        if model not in self.metrics:
            self.metrics[model] = ModelMetrics()

        metrics = self.metrics[model]
        metrics.requests_count += 1
        metrics.last_request = datetime.now()

        # Update average latency
        if metrics.average_latency == 0:
            metrics.average_latency = latency
        else:
            metrics.average_latency = (metrics.average_latency + latency) / 2

        # Update success rate
        if success:
            # Calculate new success rate
            total_requests = metrics.requests_count
            successful_requests = int(metrics.success_rate / 100 * (total_requests - 1)) + 1
            metrics.success_rate = (successful_requests / total_requests) * 100
        else:
            # Calculate new success rate with failure
            total_requests = metrics.requests_count
            successful_requests = int(metrics.success_rate / 100 * (total_requests - 1))
            metrics.success_rate = (successful_requests / total_requests) * 100

    async def test_connection(self) -> Dict[str, Any]:
        """Test connection to Vertex AI"""
        try:
            # Simple test with gpt-4o-mini (fastest model)
            test_messages = [{"role": "user", "content": "Hello, please respond with just 'OK'"}]

            start_time = time.time()
            response = await self.chat_completion(
                messages=test_messages,
                model="gpt-4o-mini",
                max_tokens=10
            )
            latency = time.time() - start_time

            return {
                "status": "success",
                "latency": latency,
                "model_used": "gpt-4o-mini",
                "vertex_model": self.model_mapping["gpt-4o-mini"],
                "response_preview": response["choices"][0]["message"]["content"][:50]
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "vertex_enabled": self.vertex_enabled
            }

# Global service instance
_service_instance = None

def get_openai_vertex_service() -> OpenAIVertexService:
    """Get singleton service instance"""
    global _service_instance
    if _service_instance is None:
        _service_instance = OpenAIVertexService()
    return _service_instance
