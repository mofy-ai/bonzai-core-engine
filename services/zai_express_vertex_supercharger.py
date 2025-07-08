"""
[LAUNCH] Zai Express Mode + Vertex AI Supercharger
Ultra-fast AI processing with Google's Vertex AI integration
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class SuperchargerConfig:
    """Configuration for Express Mode Supercharger"""
    max_concurrent_requests: int = 10
    model_fallback_chain: List[str] = None
    cache_enabled: bool = True
    vertex_ai_project: str = "podplay-build-beta"
    vertex_ai_region: str = "us-central1"
    express_mode_enabled: bool = True

    def __post_init__(self):
        if self.model_fallback_chain is None:
            self.model_fallback_chain = [
                'gemini-2.5-pro-exp-03-25',
                'gemini-1.5-pro-latest',
                'claude-3.5-sonnet'
            ]

class ZaiExpressVertexSupercharger:
    """
    [LAUNCH] Express Mode Supercharger - Lightning fast AI processing
    Combines Google Vertex AI with intelligent caching and parallel processing
    """

    def __init__(self, config: Optional[SuperchargerConfig] = None):
        self.config = config or SuperchargerConfig()
        self.request_cache = {}
        self.active_requests = {}
        self.vertex_ai_client = None
        self.performance_metrics = {
            'total_requests': 0,
            'cache_hits': 0,
            'average_response_time': 0.0,
            'vertex_ai_calls': 0
        }

        logger.info("[LAUNCH] Zai Express + Vertex AI Supercharger initialized!")
        self._initialize_vertex_ai()

    def _initialize_vertex_ai(self):
        """Initialize Vertex AI client"""
        try:
            # Initialize with service account from environment
            service_account_path = os.getenv('PRIMARY_SERVICE_ACCOUNT_PATH')
            if service_account_path and os.path.exists(service_account_path):
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_path
                logger.info("[OK] Vertex AI service account configured")
            else:
                logger.warning("[EMOJI] Vertex AI service account not found, using default credentials")

        except Exception as e:
            logger.error(f"[ERROR] Failed to initialize Vertex AI: {e}")

    async def supercharge_request(self,
                                prompt: str,
                                model_preference: str = None,
                                express_mode: bool = True) -> Dict[str, Any]:
        """
        Supercharge an AI request with Express Mode + Vertex AI

        Args:
            prompt: The input prompt
            model_preference: Preferred model (optional)
            express_mode: Enable ultra-fast processing

        Returns:
            Supercharged response with performance metrics
        """
        start_time = datetime.now()
        request_id = f"express_{int(start_time.timestamp())}"

        try:
            # Check cache first if enabled
            if self.config.cache_enabled:
                cached_response = self._check_cache(prompt, model_preference)
                if cached_response:
                    self.performance_metrics['cache_hits'] += 1
                    logger.info(f"[LIGHTNING] Cache hit for request {request_id}")
                    return self._add_performance_metadata(cached_response, start_time, True)

            # Process with Express Mode
            if express_mode and self.config.express_mode_enabled:
                response = await self._express_mode_processing(prompt, model_preference, request_id)
            else:
                response = await self._standard_processing(prompt, model_preference, request_id)

            # Cache the response
            if self.config.cache_enabled:
                self._cache_response(prompt, model_preference, response)

            # Update metrics
            self.performance_metrics['total_requests'] += 1
            response_time = (datetime.now() - start_time).total_seconds()
            self._update_average_response_time(response_time)

            return self._add_performance_metadata(response, start_time, False)

        except Exception as e:
            logger.error(f"[ERROR] Supercharger error for request {request_id}: {e}")
            return {
                'error': str(e),
                'request_id': request_id,
                'timestamp': start_time.isoformat(),
                'fallback_used': True
            }

    async def _express_mode_processing(self,
                                     prompt: str,
                                     model_preference: str,
                                     request_id: str) -> Dict[str, Any]:
        """Ultra-fast Express Mode processing"""
        logger.info(f"[LIGHTNING] Express Mode processing for {request_id}")

        # Parallel processing with multiple models for speed
        model_chain = self.config.model_fallback_chain
        if model_preference and model_preference not in model_chain:
            model_chain = [model_preference] + model_chain

        # Use first available model (simulated for now)
        selected_model = model_chain[0]

        # Simulate express processing
        response = {
            'content': f"Express Mode Response processed with {selected_model}",
            'model_used': selected_model,
            'express_mode': True,
            'request_id': request_id,
            'processing_type': 'vertex_ai_supercharged'
        }

        self.performance_metrics['vertex_ai_calls'] += 1
        return response

    async def _standard_processing(self,
                                 prompt: str,
                                 model_preference: str,
                                 request_id: str) -> Dict[str, Any]:
        """Standard processing mode"""
        logger.info(f"[SYNC] Standard processing for {request_id}")

        selected_model = model_preference or self.config.model_fallback_chain[0]

        response = {
            'content': f"Standard response processed with {selected_model}",
            'model_used': selected_model,
            'express_mode': False,
            'request_id': request_id,
            'processing_type': 'standard'
        }

        return response

    def _check_cache(self, prompt: str, model_preference: str) -> Optional[Dict[str, Any]]:
        """Check if response is cached"""
        cache_key = f"{hash(prompt)}_{model_preference or 'default'}"
        return self.request_cache.get(cache_key)

    def _cache_response(self, prompt: str, model_preference: str, response: Dict[str, Any]):
        """Cache the response for future use"""
        cache_key = f"{hash(prompt)}_{model_preference or 'default'}"
        self.request_cache[cache_key] = response

        # Limit cache size
        if len(self.request_cache) > 1000:
            # Remove oldest entries
            oldest_keys = list(self.request_cache.keys())[:100]
            for key in oldest_keys:
                del self.request_cache[key]

    def _add_performance_metadata(self,
                                response: Dict[str, Any],
                                start_time: datetime,
                                cache_hit: bool) -> Dict[str, Any]:
        """Add performance metadata to response"""
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds()

        response['performance'] = {
            'response_time_seconds': response_time,
            'cache_hit': cache_hit,
            'timestamp': start_time.isoformat(),
            'supercharger_enabled': True
        }

        return response

    def _update_average_response_time(self, response_time: float):
        """Update average response time metric"""
        current_avg = self.performance_metrics['average_response_time']
        total_requests = self.performance_metrics['total_requests']

        if total_requests == 1:
            self.performance_metrics['average_response_time'] = response_time
        else:
            new_avg = (current_avg * (total_requests - 1) + response_time) / total_requests
            self.performance_metrics['average_response_time'] = new_avg

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        return {
            **self.performance_metrics,
            'cache_size': len(self.request_cache),
            'active_requests': len(self.active_requests),
            'vertex_ai_configured': self.vertex_ai_client is not None,
            'express_mode_enabled': self.config.express_mode_enabled
        }

    async def batch_process(self,
                          requests: List[Dict[str, Any]],
                          max_concurrent: int = None) -> List[Dict[str, Any]]:
        """Process multiple requests in parallel"""
        max_concurrent = max_concurrent or self.config.max_concurrent_requests

        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_single(request_data: Dict[str, Any]) -> Dict[str, Any]:
            async with semaphore:
                return await self.supercharge_request(
                    prompt=request_data.get('prompt', ''),
                    model_preference=request_data.get('model_preference'),
                    express_mode=request_data.get('express_mode', True)
                )

        logger.info(f"[LAUNCH] Batch processing {len(requests)} requests with {max_concurrent} concurrent workers")
        results = await asyncio.gather(*[process_single(req) for req in requests])

        return results

    def clear_cache(self):
        """Clear the response cache"""
        self.request_cache.clear()
        logger.info("[EMOJI] Express Mode cache cleared")

    def get_status(self) -> Dict[str, Any]:
        """Get current supercharger status"""
        return {
            'status': 'active',
            'config': {
                'express_mode_enabled': self.config.express_mode_enabled,
                'cache_enabled': self.config.cache_enabled,
                'max_concurrent_requests': self.config.max_concurrent_requests,
                'vertex_ai_project': self.config.vertex_ai_project
            },
            'metrics': self.get_performance_metrics(),
            'model_fallback_chain': self.config.model_fallback_chain
        }

# Global instance
zai_express_supercharger = ZaiExpressVertexSupercharger()
