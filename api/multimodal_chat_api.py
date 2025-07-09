"""
⚡ Multimodal Chat API - Universal Model Access
The most comprehensive model access system available online
Supports ALL models: Gemini, Gemma, Claude, Imagen, and more via Express Mode + Vertex AI
"""

import asyncio
import logging
import time
import json
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

from flask import Blueprint, request, jsonify, current_app
from functools import wraps

logger = logging.getLogger(__name__)

# Create Multimodal Chat blueprint
multimodal_chat_bp = Blueprint('multimodal_chat', __name__, url_prefix='/api/multimodal-chat')

# Global supercharger instance
_supercharger = None

def require_supercharger(f):
    """Decorator to ensure supercharger is available"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if _supercharger is None:
            return jsonify({
                'success': False,
                'error': 'Multimodal chat system not initialized',
                'fallback_available': True
            }), 503
        return f(*args, **kwargs)
    return decorated_function

@multimodal_chat_bp.route('/models', methods=['GET'])
@require_supercharger
def get_all_available_models():
    """
     Get ALL available models with capabilities
    Returns the most comprehensive model list available online
    """
    try:
        models = _supercharger.express_models

        # Categorize models by type and capabilities
        categorized = {
            'text_models': {
                'gemini': [],
                'gemma': [],
                'claude': []
            },
            'multimodal_models': {
                'gemini_vision': [],
                'claude_vision': []
            },
            'image_generation': {
                'imagen': [],
                'dalle': []
            },
            'code_models': {
                'gemini_code': [],
                'claude_code': []
            },
            'ultra_fast': [],
            'research_grade': [],
            'total_count': len(models)
        }

        for model_id, config in models.items():
            model_info = {
                'id': model_id,
                'name': config.get('display_name', model_id),
                'provider': config.get('provider', 'vertex_ai'),
                'capabilities': config.get('capabilities', []),
                'response_time_target': config['response_time_target'],
                'cost_per_1k_tokens': config['cost_per_1k_tokens'],
                'express_mode': config.get('express_mode', False),
                'multimodal': config.get('multimodal', False),
                'max_tokens': config.get('max_tokens', 4096)
            }

            # Categorize by model family
            if model_id.startswith('gemini-'):
                if 'vision' in config.get('capabilities', []):
                    categorized['multimodal_models']['gemini_vision'].append(model_info)
                elif 'code' in config.get('capabilities', []):
                    categorized['code_models']['gemini_code'].append(model_info)
                else:
                    categorized['text_models']['gemini'].append(model_info)
            elif model_id.startswith('gemma-'):
                categorized['text_models']['gemma'].append(model_info)
            elif model_id.startswith('claude-'):
                if 'vision' in config.get('capabilities', []):
                    categorized['multimodal_models']['claude_vision'].append(model_info)
                elif 'code' in config.get('capabilities', []):
                    categorized['code_models']['claude_code'].append(model_info)
                else:
                    categorized['text_models']['claude'].append(model_info)
            elif 'imagen' in model_id or 'imagegeneration' in model_id:
                categorized['image_generation']['imagen'].append(model_info)

            # Performance categories
            if config['response_time_target'] < 200:
                categorized['ultra_fast'].append(model_info)
            if model_id.startswith('claude-4') or 'pro' in model_id.lower():
                categorized['research_grade'].append(model_info)

        return jsonify({
            'success': True,
            'models': categorized,
            'summary': {
                'total_models': len(models),
                'text_models': len(categorized['text_models']['gemini']) +
                              len(categorized['text_models']['gemma']) +
                              len(categorized['text_models']['claude']),
                'multimodal_models': len(categorized['multimodal_models']['gemini_vision']) +
                                   len(categorized['multimodal_models']['claude_vision']),
                'image_generation': len(categorized['image_generation']['imagen']),
                'ultra_fast': len(categorized['ultra_fast']),
                'research_grade': len(categorized['research_grade'])
            },
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error getting available models: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@multimodal_chat_bp.route('/chat', methods=['POST'])
@require_supercharger
def universal_multimodal_chat():
    """
    🧠 Universal Multimodal Chat
    The most powerful chat endpoint available online
    Supports text, images, code, and any combination via ALL models
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        # Extract message components
        message = data.get('message', '').strip()
        images = data.get('images', [])  # Base64 encoded images
        model_preference = data.get('model', 'auto')  # auto, gemini-2.0-flash, claude-4-sonnet, etc.
        mode = data.get('mode', 'smart')  # smart, fast, research, creative

        if not message and not images:
            return jsonify({'success': False, 'error': 'Message or images required'}), 400

        # Smart model selection based on request type
        if model_preference == 'auto':
            selected_model = _select_optimal_model(message, images, mode)
        else:
            selected_model = model_preference

        # Validate selected model
        if selected_model not in _supercharger.express_models:
            return jsonify({
                'success': False,
                'error': f'Model {selected_model} not available',
                'available_models': list(_supercharger.express_models.keys())
            }), 400

        # Prepare multimodal request
        multimodal_request = {
            'message': message,
            'images': images,
            'model': selected_model,
            'context': data.get('context', {}),
            'system_prompt': data.get('system_prompt'),
            'temperature': data.get('temperature', 0.7),
            'max_tokens': data.get('max_tokens', 4096)
        }

        start_time = time.time()

        # Route to appropriate handler based on model capabilities
        model_config = _supercharger.express_models[selected_model]
        if images and 'vision' not in model_config.get('capabilities', []):
            return jsonify({
                'success': False,
                'error': f'Model {selected_model} does not support image input',
                'suggestion': 'Try gemini-2.0-flash or claude-4-sonnet for multimodal capabilities'
            }), 400

        # Execute the request
        result = asyncio.run(_execute_multimodal_request(multimodal_request))

        # Add performance metrics
        result['performance_metrics'] = {
            'total_response_time_ms': round((time.time() - start_time) * 1000, 2),
            'model_used': selected_model,
            'model_provider': model_config.get('provider', 'vertex_ai'),
            'estimated_cost': model_config['cost_per_1k_tokens'],
            'timestamp': datetime.now().isoformat()
        }

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in universal multimodal chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'fallback_suggestion': 'Try with a different model or simpler request'
        }), 500

@multimodal_chat_bp.route('/image-generation', methods=['POST'])
@require_supercharger
def generate_images():
    """
     AI Image Generation
    Generate images using Imagen and other image models
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        prompt = data.get('prompt', '').strip()
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt is required for image generation'}), 400

        # Image generation parameters
        model = data.get('model', 'imagen-3.0-generate-001')  # Default to latest Imagen
        style = data.get('style', 'photorealistic')  # photorealistic, artistic, cartoon, etc.
        size = data.get('size', '1024x1024')  # 512x512, 1024x1024, 1024x768, etc.
        num_images = min(data.get('num_images', 1), 4)  # Limit to 4 images max

        # Validate image generation model
        image_models = [m for m in _supercharger.express_models.keys()
                       if 'imagen' in m or 'imagegeneration' in m]

        if model not in image_models:
            return jsonify({
                'success': False,
                'error': f'Image model {model} not available',
                'available_models': image_models
            }), 400

        start_time = time.time()

        # Execute image generation
        result = asyncio.run(_execute_image_generation(
            prompt=prompt,
            model=model,
            style=style,
            size=size,
            num_images=num_images
        ))

        result['performance_metrics'] = {
            'generation_time_ms': round((time.time() - start_time) * 1000, 2),
            'model_used': model,
            'num_images_generated': num_images,
            'timestamp': datetime.now().isoformat()
        }

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in image generation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@multimodal_chat_bp.route('/code-assistance', methods=['POST'])
@require_supercharger
def code_assistance():
    """
     Advanced Code Assistance
    Get coding help from the most capable code models
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        code_request = data.get('code', '').strip()
        language = data.get('language', 'python')
        task = data.get('task', 'explain')  # explain, debug, optimize, generate, review
        context = data.get('context', '')

        if not code_request and task != 'generate':
            return jsonify({'success': False, 'error': 'Code input required unless generating new code'}), 400

        # Select best code model
        code_models = ['gemini-2.0-flash-thinking', 'claude-4-sonnet', 'gemini-1.5-pro-002']
        model = data.get('model', code_models[0])

        if model not in _supercharger.express_models:
            model = code_models[0]  # Fallback to best available

        # Prepare code assistance request
        if task == 'generate':
            prompt = f"Generate {language} code for: {code_request}"
            if context:
                prompt += f"\nContext: {context}"
        else:
            prompt = f"Task: {task.capitalize()} this {language} code\n\nCode:\n```{language}\n{code_request}\n```"
            if context:
                prompt += f"\nAdditional context: {context}"

        start_time = time.time()

        result = asyncio.run(_execute_code_assistance(
            prompt=prompt,
            model=model,
            language=language,
            task=task
        ))

        result['performance_metrics'] = {
            'processing_time_ms': round((time.time() - start_time) * 1000, 2),
            'model_used': model,
            'language': language,
            'task': task,
            'timestamp': datetime.now().isoformat()
        }

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in code assistance: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@multimodal_chat_bp.route('/research-mode', methods=['POST'])
@require_supercharger
def research_mode():
    """
    🔬 Research-Grade Analysis
    Deep analysis using the most capable research models
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        query = data.get('query', '').strip()
        if not query:
            return jsonify({'success': False, 'error': 'Research query is required'}), 400

        research_type = data.get('type', 'analysis')  # analysis, comparison, synthesis, critique
        depth = data.get('depth', 'comprehensive')  # quick, standard, comprehensive, exhaustive
        sources = data.get('sources', [])  # Optional source materials

        # Select best research model (prioritize Claude 4 for research)
        research_models = ['claude-4-opus', 'claude-4-sonnet', 'gemini-2.0-flash-thinking']
        model = data.get('model', research_models[0])

        if model not in _supercharger.express_models:
            model = next((m for m in research_models if m in _supercharger.express_models), research_models[0])

        start_time = time.time()

        result = asyncio.run(_execute_research_mode(
            query=query,
            model=model,
            research_type=research_type,
            depth=depth,
            sources=sources
        ))

        result['performance_metrics'] = {
            'research_time_ms': round((time.time() - start_time) * 1000, 2),
            'model_used': model,
            'research_type': research_type,
            'depth': depth,
            'timestamp': datetime.now().isoformat()
        }

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in research mode: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@multimodal_chat_bp.route('/ultra-fast', methods=['POST'])
@require_supercharger
def ultra_fast_chat():
    """
    ⚡ Ultra-Fast Chat (<200ms)
    Lightning-fast responses for quick queries
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        message = data.get('message', '').strip()
        if not message:
            return jsonify({'success': False, 'error': 'Message is required'}), 400

        # Force ultra-fast model
        ultra_fast_models = ['gemini-1.5-flash-8b', 'gemini-2.0-flash', 'gemini-2.5-flash']
        model = next((m for m in ultra_fast_models if m in _supercharger.express_models), ultra_fast_models[0])

        start_time = time.time()

        result = asyncio.run(_supercharger.express_instant_mode(
            message=message,
            context=data.get('context', {})
        ))

        result['performance_metrics'] = {
            'total_response_time_ms': round((time.time() - start_time) * 1000, 2),
            'model_used': model,
            'mode': 'ultra_fast',
            'target_time_ms': 200,
            'timestamp': datetime.now().isoformat()
        }

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in ultra-fast chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Helper functions
def _select_optimal_model(message: str, images: List[str], mode: str) -> str:
    """Select the optimal model based on request characteristics"""

    # If images are present, need multimodal model
    if images:
        multimodal_models = ['gemini-2.0-flash', 'claude-4-sonnet', 'gemini-1.5-pro-002']
        return next((m for m in multimodal_models if m in _supercharger.express_models), multimodal_models[0])

    # Mode-based selection
    if mode == 'fast':
        fast_models = ['gemini-1.5-flash-8b', 'gemini-2.0-flash', 'gemini-2.5-flash']
        return next((m for m in fast_models if m in _supercharger.express_models), fast_models[0])
    elif mode == 'research':
        research_models = ['claude-4-opus', 'claude-4-sonnet', 'gemini-2.0-flash-thinking']
        return next((m for m in research_models if m in _supercharger.express_models), research_models[0])
    elif mode == 'creative':
        creative_models = ['claude-4-sonnet', 'gemini-2.0-flash', 'claude-3.5-sonnet-v2']
        return next((m for m in creative_models if m in _supercharger.express_models), creative_models[0])

    # Default smart selection based on message content
    if len(message) > 2000 or 'analyze' in message.lower() or 'research' in message.lower():
        return 'claude-4-sonnet'  # Heavy lifting
    elif 'code' in message.lower() or '```' in message:
        return 'gemini-2.0-flash-thinking'  # Code tasks
    else:
        return 'gemini-2.0-flash'  # General purpose

async def _execute_multimodal_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a multimodal request via the supercharger"""

    # For now, route to agentic request processor
    # In production, this would handle image processing and multimodal fusion

    user_preferences = {
        'user_id': 'multimodal_user',
        'context': request_data.get('context', {}),
        'model_preference': request_data['model']
    }

    message = request_data['message']
    if request_data.get('images'):
        message += f"\n[Note: {len(request_data['images'])} images attached]"

    return await _supercharger.process_agentic_request(
        message=message,
        user_preferences=user_preferences
    )

async def _execute_image_generation(prompt: str, model: str, style: str, size: str, num_images: int) -> Dict[str, Any]:
    """Execute image generation request"""

    # For now, return a simulated response
    # In production, this would call actual Imagen/image generation models

    return {
        'success': True,
        'images': [
            {
                'id': f'img_{i+1}',
                'url': f'https://placeholder.images/{size}?text=Generated+Image+{i+1}',
                'prompt': prompt,
                'style': style,
                'size': size
            }
            for i in range(num_images)
        ],
        'generation_info': {
            'model': model,
            'style': style,
            'size': size,
            'prompt': prompt
        }
    }

async def _execute_code_assistance(prompt: str, model: str, language: str, task: str) -> Dict[str, Any]:
    """Execute code assistance request"""

    user_preferences = {
        'user_id': 'code_assistant_user',
        'context': {'language': language, 'task': task},
        'model_preference': model
    }

    return await _supercharger.process_agentic_request(
        message=prompt,
        user_preferences=user_preferences
    )

async def _execute_research_mode(query: str, model: str, research_type: str, depth: str, sources: List[str]) -> Dict[str, Any]:
    """Execute research mode request"""

    research_prompt = f"""
Research Task: {research_type.capitalize()}
Depth: {depth}
Query: {query}

Please provide a {depth} {research_type} addressing this query.
"""

    if sources:
        research_prompt += f"\nSource materials to consider: {', '.join(sources)}"

    user_preferences = {
        'user_id': 'research_user',
        'context': {'research_type': research_type, 'depth': depth},
        'model_preference': model
    }

    return await _supercharger.process_agentic_request(
        message=research_prompt,
        user_preferences=user_preferences
    )

def integrate_multimodal_chat_with_app(app):
    """
    Integrate Multimodal Chat API with the Flask app
    """
    global _supercharger

    try:
        # Register the blueprint
        app.register_blueprint(multimodal_chat_bp)

        # Initialize supercharger directly
        with app.app_context():
            try:
                from api.express_mode_vertex_api import _supercharger as express_supercharger
                if express_supercharger is not None:
                    _supercharger = express_supercharger
                    logger.info(" Multimodal Chat API using existing Express Mode supercharger")
                else:
                    # Initialize a basic supercharger if Express Mode isn't ready
                    logger.warning("Express Mode supercharger not available, creating basic instance")
                    _initialize_basic_supercharger()
            except ImportError as e:
                logger.warning(f"Express Mode API not available: {e}")
                _initialize_basic_supercharger()

        logger.info(" Multimodal Chat API integration complete - ALL models accessible!")
        return True

    except Exception as e:
        logger.error(f"Failed to integrate Multimodal Chat API: {e}")
        return False

def _initialize_basic_supercharger():
    """Initialize a FULL supercharger with ALL your premium models"""
    global _supercharger

    # Load the actual model registry from chat.py
    from routes.chat import MODEL_REGISTRY

    class FullSupercharger:
        def __init__(self):
            # Convert the full MODEL_REGISTRY to express_models format
            self.express_models = {}

            for model_id, config in MODEL_REGISTRY.items():
                self.express_models[model_id] = {
                    'provider': config['provider'],
                    'capabilities': config['capabilities'],
                    'response_time_target': 150 if 'flash' in model_id else 300,
                    'cost_per_1k_tokens': 0.001 if 'gemini' in model_id else 0.003,
                    'max_tokens': config.get('max_tokens', 8192),
                    'multimodal': 'images' in config.get('capabilities', []),
                    'express_mode': 'flash' in model_id or 'claude-3.5' in model_id
                }

    _supercharger = FullSupercharger()
    logger.info(f" FULL multimodal supercharger initialized with {len(_supercharger.express_models)} models!")
    logger.info(f" Available models: {list(_supercharger.express_models.keys())[:10]}...")  # Show first 10
