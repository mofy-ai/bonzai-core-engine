"""
Chat API routes for Live API Studio
Provides streaming AI responses with multi-model support and Mama Bear integration
"""

from flask import Blueprint, request, jsonify, current_app, Response
import json
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Generator
import asyncio
import threading

chat_bp = Blueprint('chat', __name__)

# Model Registry for external imports
MODEL_REGISTRY = {}

# Comprehensive model configurations with intelligent orchestration
MODEL_CONFIGS = {
    # OpenAI GPT Models
    'gpt-4o': {
        'name': 'GPT-4o',
        'provider': 'openai',
        'capabilities': ['text', 'images', 'code', 'analysis', 'function_calling'],
        'max_tokens': 4096,
        'supports_streaming': True,
        'supports_live_api': False,
        'mama_bear_variant': 'scout_commander',
        'orchestration_priority': 'balanced'
    },
    'gpt-4o-mini': {
        'name': 'GPT-4o Mini',
        'provider': 'openai',
        'capabilities': ['text', 'fast_responses', 'code'],
        'max_tokens': 4096,
        'supports_streaming': True,
        'supports_live_api': False,
        'mama_bear_variant': 'research_specialist',
        'orchestration_priority': 'speed'
    },

    # Claude Models (For deep research and analysis)
    'claude-3-opus-20240229': {
        'name': 'Claude 3 Opus',
        'provider': 'anthropic',
        'capabilities': ['text', 'images', 'deep_analysis', 'complex_reasoning', 'computer_use'],
        'max_tokens': 4096,
        'supports_streaming': True,
        'supports_live_api': False,
        'mama_bear_variant': 'research_specialist',
        'orchestration_priority': 'quality'
    },
    'claude-3.5-sonnet': {
        'name': 'Claude 3.5 Sonnet',
        'provider': 'anthropic',
        'capabilities': ['text', 'images', 'analysis', 'writing', 'computer_use'],
        'max_tokens': 8192,
        'supports_streaming': True,
        'supports_live_api': False,
        'mama_bear_variant': 'creative_bear',
        'orchestration_priority': 'balanced'
    },

    # Gemini 2.5 Models (Advanced collaboration and reasoning)
    'gemini-2.5-pro-exp-03-25': {
        'name': 'Gemini 2.5 Pro Experimental',
        'provider': 'google',
        'capabilities': ['text', 'images', 'advanced_reasoning', 'function_calling', 'thinking'],
        'max_tokens': 65536,
        'supports_streaming': True,
        'supports_live_api': False,
        'mama_bear_variant': 'research_specialist',
        'orchestration_priority': 'quality'
    },
    'gemini-2.5-flash-preview-05-20': {
        'name': 'Gemini 2.5 Flash',
        'provider': 'google',
        'capabilities': ['text', 'images', 'fast_reasoning', 'function_calling'],
        'max_tokens': 65536,
        'supports_streaming': True,
        'supports_live_api': False,
        'mama_bear_variant': 'scout_commander',
        'orchestration_priority': 'speed'
    },

    # Gemini 2.0 Live API Models (Real-time interaction)
    'gemini-2.0-flash-exp': {
        'name': 'Gemini 2.0 Flash Experimental',
        'provider': 'google',
        'capabilities': ['text', 'images', 'video', 'audio', 'live-api', 'bidirectional', 'real-time'],
        'max_tokens': 8192,
        'supports_streaming': True,
        'supports_live_api': True,
        'mama_bear_variant': 'scout_commander',
        'orchestration_priority': 'real_time'
    },
    'gemini-2.0-flash-live-001': {
        'name': 'Gemini 2.0 Flash Live',
        'provider': 'google',
        'capabilities': ['text', 'images', 'video', 'audio', 'live-api', 'bidirectional', 'real-time'],
        'max_tokens': 8192,
        'supports_streaming': True,
        'supports_live_api': True,
        'mama_bear_variant': 'research_specialist',
        'orchestration_priority': 'real_time'
    },
    'gemini-2.5-flash-preview-native-audio-dialog': {
        'name': 'Gemini 2.5 Flash Native Audio Dialog',
        'provider': 'google',
        'capabilities': ['text', 'images', 'audio', 'live-api', 'bidirectional', 'native-audio'],
        'max_tokens': 8192,
        'supports_streaming': True,
        'supports_live_api': True,
        'mama_bear_variant': 'creative_bear',
        'orchestration_priority': 'real_time'
    },
    'gemini-2.5-flash-preview-native-audio-dialog-rai-v3': {
        'name': 'Gemini 2.5 Flash Native Audio Dialog RAI v3',
        'provider': 'google',
        'capabilities': ['text', 'images', 'audio', 'live-api', 'bidirectional', 'native-audio', 'rai-v3'],
        'max_tokens': 8192,
        'supports_streaming': True,
        'supports_live_api': True,
        'mama_bear_variant': 'debugging_detective',
        'orchestration_priority': 'real_time'
    },
    'gemini-2.5-flash-exp-native-audio-thinking-dialog': {
        'name': 'Gemini 2.5 Flash Experimental Native Audio Thinking Dialog',
        'provider': 'google',
        'capabilities': ['text', 'images', 'audio', 'live-api', 'bidirectional', 'native-audio', 'thinking'],
        'max_tokens': 8192,
        'supports_streaming': True,
        'supports_live_api': True,
        'mama_bear_variant': 'learning_bear',
        'orchestration_priority': 'real_time'
    },

    # Gemini 1.5 Models (Proven workhorses)
    'gemini-1.5-pro-latest': {
        'name': 'Gemini 1.5 Pro',
        'provider': 'google',
        'capabilities': ['text', 'images', 'long_context', 'function_calling'],
        'max_tokens': 8192,
        'supports_streaming': True,
        'supports_live_api': False,
        'mama_bear_variant': 'research_specialist',
        'orchestration_priority': 'context'
    },
    'gemini-1.5-flash-latest': {
        'name': 'Gemini 1.5 Flash',
        'provider': 'google',
        'capabilities': ['text', 'images', 'fast_responses', 'function_calling'],
        'max_tokens': 8192,
        'supports_streaming': True,
        'supports_live_api': False,
        'mama_bear_variant': 'scout_commander',
        'orchestration_priority': 'speed'
    }
}

# Mama Bear personality templates
MAMA_BEAR_PERSONALITIES = {
    'scout_commander': {
        'role': 'Strategic Planning and Orchestration',
        'personality': 'Caring but decisive leader who helps plan and coordinate complex development tasks',
        'greeting': "Hello, dear developer! I'm here to help you plan and coordinate your development journey. What would you like to work on together?",
        'style': 'strategic_caring'
    },
    'research_specialist': {
        'role': 'Deep Research and Analysis',
        'personality': 'Thorough and patient researcher who loves diving deep into technical topics',
        'greeting': "Hi there! I'm your research companion, ready to explore any technical topic with you. What shall we investigate?",
        'style': 'analytical_supportive'
    },
    'creative_bear': {
        'role': 'Innovation and Creative Solutions',
        'personality': 'Imaginative and encouraging, helps brainstorm creative solutions to development challenges',
        'greeting': "Hey creative soul! I'm here to help you think outside the box and find innovative solutions. What's sparking your imagination?",
        'style': 'creative_enthusiastic'
    },
    'debugging_detective': {
        'role': 'Problem-Solving and Investigation',
        'personality': 'Methodical and reassuring detective who helps solve complex technical problems',
        'greeting': "Hello, fellow problem-solver! I'm here to help you investigate and solve any technical mysteries. What puzzle are we tackling?",
        'style': 'methodical_reassuring'
    },
    'learning_bear': {
        'role': 'Patient Teaching and Learning',
        'personality': 'Gentle and encouraging teacher who adapts to different learning styles and paces',
        'greeting': "Hello, wonderful learner! I'm here to help you understand and grow at your own pace. What would you like to explore together?",
        'style': 'patient_educational'
    }
}

def _get_optimal_model_for_task(user_message, available_models=None):
    """
    Intelligent model orchestration based on task analysis
    Routes to the best model for specific tasks:
    - Claude 3.5 for deep research and complex analysis
    - Gemini 2.5 Pro for collaborative research and reasoning
    - Gemini 2.0 Flash for real-time interaction
    - GPT-4o for balanced general tasks
    """
    if not available_models:
        available_models = list(MODEL_CONFIGS.keys())

    message_lower = user_message.lower()

    # Deep research and analysis tasks - Use Claude 3.5
    research_keywords = ['research', 'analyze', 'deep dive', 'investigate', 'study', 'complex', 'thorough', 'detailed analysis']
    if any(keyword in message_lower for keyword in research_keywords):
        claude_models = [m for m in available_models if m.startswith('claude-3')]
        if claude_models:
            return claude_models[0]  # Prefer Claude 3.5 Sonnet

    # Collaborative reasoning and advanced thinking - Use Gemini 2.5
    collaboration_keywords = ['collaborate', 'brainstorm', 'think together', 'reasoning', 'logic', 'solve', 'strategy']
    if any(keyword in message_lower for keyword in collaboration_keywords):
        gemini_25_models = [m for m in available_models if m.startswith('gemini-2.5')]
        if gemini_25_models:
            return gemini_25_models[0]  # Prefer Gemini 2.5 Pro

    # Real-time interaction and live API - Use Gemini 2.0 Live
    realtime_keywords = ['live', 'real-time', 'interactive', 'conversation', 'chat', 'talk']
    if any(keyword in message_lower for keyword in realtime_keywords):
        gemini_20_live = [m for m in available_models if 'live' in m or 'audio' in m]
        if gemini_20_live:
            return gemini_20_live[0]  # Prefer Live API models

    # Code generation and technical tasks - Use GPT-4o or Claude
    code_keywords = ['code', 'program', 'function', 'script', 'debug', 'implement', 'development']
    if any(keyword in message_lower for keyword in code_keywords):
        code_models = [m for m in available_models if m.startswith('gpt-4o') or m.startswith('claude-3.5')]
        if code_models:
            return code_models[0]

    # Default to best available model based on orchestration priority
    priority_order = ['quality', 'balanced', 'real_time', 'speed', 'context']

    for priority in priority_order:
        priority_models = [m for m in available_models
                          if MODEL_CONFIGS.get(m, {}).get('orchestration_priority') == priority]
        if priority_models:
            return priority_models[0]

    # Final fallback
    return available_models[0] if available_models else 'gemini-2.0-flash-exp'

@chat_bp.route('/models', methods=['GET'])
def get_available_models():
    """Get list of available AI models with their capabilities"""
    try:
        return jsonify({
            'success': True,
            'models': MODEL_CONFIGS
        })
    except Exception as e:
        current_app.logger.error(f"Error getting models: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chat_bp.route('/suggest-model', methods=['POST'])
def suggest_optimal_model():
    """Suggest the optimal AI model based on user's message content"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        available_models = data.get('available_models', list(MODEL_CONFIGS.keys()))
        max_suggestions = data.get('max_suggestions', 3)

        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Message content is required for model suggestion'
            }), 400

        # Get optimal model recommendation
        optimal_model = _get_optimal_model_for_task(user_message, available_models)

        # Get additional suggestions based on different priorities
        suggestions = []
        message_lower = user_message.lower()

        # Primary suggestion (optimal model)
        if optimal_model and optimal_model in MODEL_CONFIGS:
            model_config = MODEL_CONFIGS[optimal_model]
            suggestions.append({
                'model_id': optimal_model,
                'model_name': model_config['name'],
                'provider': model_config['provider'],
                'reason': f"Best for this type of task based on content analysis",
                'capabilities': model_config['capabilities'],
                'mama_bear_variant': model_config['mama_bear_variant'],
                'orchestration_priority': model_config['orchestration_priority'],
                'confidence': 0.9
            })

        # Add alternative suggestions based on different criteria
        all_models = [(model_id, config) for model_id, config in MODEL_CONFIGS.items()
                     if model_id in available_models and model_id != optimal_model]

        # Sort by orchestration priority and provider diversity
        priority_order = {'quality': 4, 'balanced': 3, 'real_time': 2, 'speed': 1, 'context': 0}
        all_models.sort(key=lambda x: priority_order.get(x[1].get('orchestration_priority', 'balanced'), 2), reverse=True)

        # Add diverse suggestions
        used_providers = {MODEL_CONFIGS[optimal_model]['provider']} if optimal_model in MODEL_CONFIGS else set()

        for model_id, config in all_models:
            if len(suggestions) >= max_suggestions:
                break

            # Prefer provider diversity
            if config['provider'] not in used_providers or len(suggestions) < max_suggestions:
                confidence = 0.7 if config['provider'] not in used_providers else 0.5
                suggestions.append({
                    'model_id': model_id,
                    'model_name': config['name'],
                    'provider': config['provider'],
                    'reason': f"Alternative {config['orchestration_priority']} option with {config['provider']} provider",
                    'capabilities': config['capabilities'],
                    'mama_bear_variant': config['mama_bear_variant'],
                    'orchestration_priority': config['orchestration_priority'],
                    'confidence': confidence
                })
                used_providers.add(config['provider'])

        return jsonify({
            'success': True,
            'message_analysis': {
                'detected_keywords': [word for word in ['research', 'analyze', 'code', 'live', 'chat', 'collaborate']
                                    if word in message_lower],
                'task_type': _analyze_task_type(user_message),
                'complexity_level': _analyze_complexity(user_message)
            },
            'suggestions': suggestions[:max_suggestions],
            'total_available_models': len(available_models)
        })

    except Exception as e:
        current_app.logger.error(f"Error suggesting optimal model: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def _analyze_task_type(message):
    """Analyze what type of task the user is requesting"""
    message_lower = message.lower()

    if any(word in message_lower for word in ['research', 'analyze', 'study', 'investigate']):
        return 'research_analysis'
    elif any(word in message_lower for word in ['code', 'program', 'function', 'debug']):
        return 'coding_development'
    elif any(word in message_lower for word in ['chat', 'talk', 'conversation', 'live']):
        return 'interactive_conversation'
    elif any(word in message_lower for word in ['collaborate', 'brainstorm', 'think']):
        return 'collaborative_thinking'
    else:
        return 'general_assistance'

def _analyze_complexity(message):
    """Analyze the complexity level of the user's request"""
    message_lower = message.lower()
    complexity_indicators = {
        'high': ['complex', 'detailed', 'thorough', 'comprehensive', 'advanced', 'deep'],
        'medium': ['analyze', 'explain', 'help', 'solve', 'create'],
        'low': ['quick', 'simple', 'basic', 'easy', 'fast']
    }

    for level, indicators in complexity_indicators.items():
        if any(indicator in message_lower for indicator in indicators):
            return level

    return 'medium'  # Default complexity

@chat_bp.route('/stream', methods=['POST'])
def stream_chat():
    """Stream AI responses with Mama Bear personality integration"""
    try:
        data = request.get_json()
        model_id = data.get('model', 'gemini-2.0-flash-exp')
        messages = data.get('messages', [])
        user_id = data.get('user_id', 'default')
        session_id = data.get('session_id', str(uuid.uuid4()))

        if model_id not in MODEL_CONFIGS:
            return jsonify({
                'success': False,
                'error': f'Model {model_id} not supported'
            }), 400

        model_config = MODEL_CONFIGS[model_id]
        mama_bear_variant = model_config['mama_bear_variant']
        personality = MAMA_BEAR_PERSONALITIES[mama_bear_variant]

        def generate_response():
            """Generate real streaming response with AI models"""
            try:
                # Add Mama Bear personality context
                system_message = f"""You are {personality['role']} - a caring AI assistant with the following personality: {personality['personality']}

Communication style: {personality['style']}
Model capabilities: {', '.join(model_config['capabilities'])}

Always maintain a caring, supportive tone while being technically excellent. You're part of the Podplay Sanctuary - a neurodivergent-friendly development platform."""

                # Prepare messages for AI model
                full_messages = [{'role': 'system', 'content': system_message}] + messages

                # Route to appropriate AI model with intelligent orchestration
                provider = model_config['provider']

                if provider == 'google':
                    yield from _generate_gemini_response(full_messages, model_id, mama_bear_variant, session_id)
                elif provider == 'anthropic':
                    yield from _generate_claude_response(full_messages, model_id, mama_bear_variant, session_id)
                elif provider == 'openai':
                    yield from _generate_openai_response(full_messages, model_id, mama_bear_variant, session_id)
                else:
                    # Fallback for unknown providers
                    yield from _generate_fallback_response(model_id, mama_bear_variant, session_id, personality)

            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error in generate_response: {e}")
                error_data = {
                    'error': str(e),
                    'model': model_id,
                    'timestamp': datetime.utcnow().isoformat()
                }
                yield f"data: {json.dumps(error_data)}\n\n"

        return Response(
            generate_response(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        )

    except Exception as e:
        current_app.logger.error(f"Error in stream_chat: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chat_bp.route('/conversation', methods=['POST'])
def save_conversation():
    """Save conversation to memory with context preservation"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default')
        session_id = data.get('session_id')
        messages = data.get('messages', [])
        model_id = data.get('model')

        # Use real memory manager to save conversation
        from services import get_memory_manager

        memory_manager = get_memory_manager()
        conversation_data = {
            'session_id': session_id,
            'model': model_id,
            'messages': messages,
            'mama_bear_variant': MODEL_CONFIGS.get(model_id, {}).get('mama_bear_variant')
        }

        # Handle async method properly in Flask route
        import asyncio
        try:
            # Create new event loop for this request
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Run the async method
            conversation_id = loop.run_until_complete(
                memory_manager.save_conversation(user_id, conversation_data)
            )
        finally:
            loop.close()

        return jsonify({
            'success': True,
            'conversation_id': conversation_id,
            'message': 'Conversation saved with persistent memory'
        })

    except Exception as e:
        current_app.logger.error(f"Error saving conversation: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chat_bp.route('/conversation/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Retrieve a saved conversation"""
    try:
        # TODO: Implement conversation retrieval from memory
        # This would fetch from the memory API

        # Mock response for now
        conversation = {
            'id': conversation_id,
            'messages': [],
            'model': 'gemini-2.0-flash-exp',
            'created_at': datetime.utcnow().isoformat(),
            'mama_bear_variant': 'scout_commander'
        }

        return jsonify({
            'success': True,
            'conversation': conversation
        })

    except Exception as e:
        current_app.logger.error(f"Error getting conversation: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chat_bp.route('/agent-status', methods=['GET'])
def get_agent_status():
    """Get real-time status of Scout and Workspace agents"""
    try:
        # Mock agent status (replace with actual agent monitoring)
        agent_status = {
            'scout_agent': {
                'status': 'active',
                'current_task': 'Web scraping documentation',
                'progress': 75,
                'last_update': datetime.utcnow().isoformat(),
                'capabilities': ['web_browsing', 'code_execution', 'file_operations']
            },
            'workspace_agent': {
                'status': 'idle',
                'current_task': None,
                'progress': 0,
                'last_update': datetime.utcnow().isoformat(),
                'capabilities': ['code_editing', 'project_management', 'collaboration']
            },
            'mama_bear_variants': {
                variant: {
                    'status': 'available',
                    'interaction_count': 0,
                    'trust_level': 0.5
                }
                for variant in MAMA_BEAR_PERSONALITIES.keys()
            }
        }

        return jsonify({
            'success': True,
            'agents': agent_status
        })

    except Exception as e:
        current_app.logger.error(f"Error getting agent status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chat_bp.route('/capabilities/<model_id>', methods=['GET'])
def get_model_capabilities(model_id):
    """Get detailed capabilities for a specific model"""
    try:
        if model_id not in MODEL_CONFIGS:
            return jsonify({
                'success': False,
                'error': f'Model {model_id} not found'
            }), 404

        model_config = MODEL_CONFIGS[model_id]
        mama_bear_variant = model_config['mama_bear_variant']
        personality = MAMA_BEAR_PERSONALITIES[mama_bear_variant]

        capabilities = {
            'model_info': model_config,
            'mama_bear_personality': personality,
            'supported_inputs': model_config['capabilities'],
            'streaming_support': model_config['supports_streaming'],
            'max_context_length': model_config['max_tokens']
        }

        return jsonify({
            'success': True,
            'capabilities': capabilities
        })

    except Exception as e:
        current_app.logger.error(f"Error getting model capabilities: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chat_bp.route('/health', methods=['GET'])
def chat_health():
    """Health check endpoint for chat system"""
    try:
        return jsonify({
            'success': True,
            'status': 'healthy',
            'service': 'chat',
            'timestamp': datetime.utcnow().isoformat(),
            'available_models': len(MODEL_CONFIGS),
            'model_names': list(MODEL_CONFIGS.keys())
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@chat_bp.route('/mama-bear', methods=['GET'])
def get_mama_bear_variants():
    """Get available Mama Bear variants and their capabilities"""
    try:
        variants = {
            'scout_commander': {
                'name': 'Scout Commander',
                'description': 'Strategic project leadership and architecture decisions',
                'capabilities': ['project_planning', 'architecture', 'team_coordination'],
                'status': 'active',
                'trust_level': 0.85
            },
            'research_specialist': {
                'name': 'Research Specialist',
                'description': 'Deep research and comprehensive analysis',
                'capabilities': ['research', 'analysis', 'documentation'],
                'status': 'active',
                'trust_level': 0.90
            },
            'code_review_bear': {
                'name': 'Code Review Bear',
                'description': 'Code quality assurance and best practices',
                'capabilities': ['code_review', 'quality_assurance', 'security'],
                'status': 'active',
                'trust_level': 0.88
            },
            'creative_bear': {
                'name': 'Creative Bear',
                'description': 'Creative problem solving and innovative solutions',
                'capabilities': ['creativity', 'innovation', 'design'],
                'status': 'active',
                'trust_level': 0.82
            },
            'learning_bear': {
                'name': 'Learning Bear',
                'description': 'Educational guidance and skill development',
                'capabilities': ['teaching', 'mentoring', 'skill_development'],
                'status': 'active',
                'trust_level': 0.89
            },
            'efficiency_bear': {
                'name': 'Efficiency Bear',
                'description': 'Process optimization and productivity enhancement',
                'capabilities': ['optimization', 'automation', 'efficiency'],
                'status': 'active',
                'trust_level': 0.86
            },
            'debugging_detective': {
                'name': 'Debugging Detective',
                'description': 'Problem diagnosis and error resolution',
                'capabilities': ['debugging', 'troubleshooting', 'error_analysis'],
                'status': 'active',
                'trust_level': 0.87
            }
        }

        return jsonify({
            'success': True,
            'variants': variants,
            'total_variants': len(variants)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chat_bp.route('/mama-bear', methods=['POST'])
def interact_with_mama_bear():
    """Interact with a specific Mama Bear variant"""
    try:
        data = request.get_json()
        variant = data.get('variant', 'scout_commander')
        message = data.get('message', '')

        # Mock response for now
        response = {
            'variant': variant,
            'message': f"Hello! I'm {variant.replace('_', ' ').title()}. How can I help you today?",
            'timestamp': datetime.utcnow().isoformat(),
            'capabilities': MODEL_CONFIGS.get('gpt-4o', {}).get('capabilities', [])
        }

        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def _generate_gemini_response(messages, model_id, mama_bear_variant, session_id):
    """Generate streaming response with live API Gemini models"""
    try:
        import google.generativeai as genai
        import os

        api_key = os.getenv('GEMINI_API_KEY_PRIMARY') or os.getenv('GOOGLE_API_KEY')
        if not api_key:
            yield from _generate_fallback_response(model_id, mama_bear_variant, session_id, None)
            return

        genai.configure(api_key=api_key)

        # Map our model IDs to actual Gemini model names
        model_mapping = {
            # Gemini 2.0 Live API Models
            'gemini-2.0-flash-exp': 'gemini-2.0-flash-exp',
            'gemini-2.0-flash-live-001': 'gemini-2.0-flash-live-001',
            'gemini-2.5-flash-preview-native-audio-dialog': 'gemini-2.5-flash-preview-native-audio-dialog',
            'gemini-2.5-flash-preview-native-audio-dialog-rai-v3': 'gemini-2.5-flash-preview-native-audio-dialog-rai-v3',
            'gemini-2.5-flash-exp-native-audio-thinking-dialog': 'gemini-2.5-flash-exp-native-audio-thinking-dialog',

            # Gemini 2.5 Models
            'gemini-2.5-pro-exp-03-25': 'gemini-2.5-pro-exp-03-25',
            'gemini-2.5-flash-preview-05-20': 'gemini-2.5-flash-preview-05-20',

            # Gemini 1.5 Models
            'gemini-1.5-pro-latest': 'gemini-1.5-pro-latest',
            'gemini-1.5-flash-latest': 'gemini-1.5-flash-latest'
        }

        actual_model_name = model_mapping.get(model_id, 'gemini-2.0-flash-exp')
        model = genai.GenerativeModel(actual_model_name)

        # Convert messages to Gemini format
        gemini_messages = []
        for msg in messages:
            if msg['role'] == 'system':
                continue  # System message handled separately
            gemini_messages.append({
                'role': 'user' if msg['role'] == 'user' else 'model',
                'parts': [msg['content']]
            })

        response = model.generate_content(
            gemini_messages,
            stream=True,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=8192,
                temperature=0.7
            )
        )

        for chunk in response:
            if chunk.text:
                chunk_data = {
                    'id': f"gemini_chunk_{int(time.time() * 1000)}",
                    'model': model_id,
                    'chunk': chunk.text,
                    'finished': False,
                    'timestamp': datetime.utcnow().isoformat(),
                    'mama_bear_variant': mama_bear_variant
                }
                yield f"data: {json.dumps(chunk_data)}\n\n"

        # Send completion signal
        completion_data = {
            'id': 'completion',
            'model': model_id,
            'finished': True,
            'mama_bear_variant': mama_bear_variant,
            'session_id': session_id
        }
        yield f"data: {json.dumps(completion_data)}\n\n"

    except Exception as e:
        current_app.logger.error(f"Gemini API error: {e}")
        yield from _generate_fallback_response(model_id, mama_bear_variant, session_id, None)

def _generate_claude_response(messages, model_id, mama_bear_variant, session_id):
    """Generate streaming response with Claude 3.5 Sonnet"""
    try:
        import anthropic
        import os

        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            yield from _generate_fallback_response(model_id, mama_bear_variant, session_id, None)
            return

        client = anthropic.Anthropic(api_key=api_key)

        # Separate system message from conversation
        system_message = ""
        conversation_messages = []

        for msg in messages:
            if msg['role'] == 'system':
                system_message = msg['content']
            else:
                conversation_messages.append(msg)

        # Map our model IDs to actual Claude model names
        claude_model_mapping = {
            'claude-3-opus-20240229': 'claude-3-opus-20240229',
            'claude-3.5-sonnet': 'claude-3-5-sonnet-20241022'  # Use the latest version
        }

        actual_model_name = claude_model_mapping.get(model_id, 'claude-3-5-sonnet-20241022')

        with client.messages.stream(
            model=actual_model_name,
            max_tokens=8192,
            system=system_message,
            messages=conversation_messages
        ) as stream:
            for text in stream.text_stream:
                chunk_data = {
                    'id': f"claude_chunk_{int(time.time() * 1000)}",
                    'model': model_id,
                    'chunk': text,
                    'finished': False,
                    'timestamp': datetime.utcnow().isoformat(),
                    'mama_bear_variant': mama_bear_variant
                }
                yield f"data: {json.dumps(chunk_data)}\n\n"

        # Send completion signal
        completion_data = {
            'id': 'completion',
            'model': model_id,
            'finished': True,
            'mama_bear_variant': mama_bear_variant,
            'session_id': session_id
        }
        yield f"data: {json.dumps(completion_data)}\n\n"

    except Exception as e:
        current_app.logger.error(f"Claude API error: {e}")
        yield from _generate_fallback_response(model_id, mama_bear_variant, session_id, None)

def _generate_openai_response(messages, model_id, mama_bear_variant, session_id):
    """Generate streaming response with GPT-4o"""
    try:
        import openai
        import os

        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            yield from _generate_fallback_response(model_id, mama_bear_variant, session_id, None)
            return

        client = openai.OpenAI(api_key=api_key)

        # Map our model IDs to actual OpenAI model names
        openai_model_mapping = {
            'gpt-4o': 'gpt-4o',
            'gpt-4o-mini': 'gpt-4o-mini'
        }

        actual_model_name = openai_model_mapping.get(model_id, 'gpt-4o')

        response = client.chat.completions.create(
            model=actual_model_name,
            messages=messages,
            stream=True,
            max_tokens=4096,
            temperature=0.7
        )

        for chunk in response:
            if chunk.choices[0].delta.content:
                chunk_data = {
                    'id': f"openai_chunk_{int(time.time() * 1000)}",
                    'model': model_id,
                    'chunk': chunk.choices[0].delta.content,
                    'finished': False,
                    'timestamp': datetime.utcnow().isoformat(),
                    'mama_bear_variant': mama_bear_variant
                }
                yield f"data: {json.dumps(chunk_data)}\n\n"

        # Send completion signal
        completion_data = {
            'id': 'completion',
            'model': model_id,
            'finished': True,
            'mama_bear_variant': mama_bear_variant,
            'session_id': session_id
        }
        yield f"data: {json.dumps(completion_data)}\n\n"

    except Exception as e:
        current_app.logger.error(f"OpenAI API error: {e}")
        yield from _generate_fallback_response(model_id, mama_bear_variant, session_id, None)

def _generate_grok_response(messages, model_id, mama_bear_variant, session_id):
    """Generate streaming response with Grok 2 (via OpenAI-compatible API)"""
    try:
        # Grok 2 uses OpenAI-compatible API
        # Note: This would need X.AI API key when available
        # For now, fallback to mock
        yield from _generate_fallback_response(model_id, mama_bear_variant, session_id, None)

    except Exception as e:
        current_app.logger.error(f"Grok API error: {e}")
        yield from _generate_fallback_response(model_id, mama_bear_variant, session_id, None)

def _generate_fallback_response(model_id, mama_bear_variant, session_id, personality):
    """Fallback response when AI models are unavailable"""
    try:
        if personality:
            response_chunks = [
                f"Hello! I'm your {personality['role']} assistant. ",
                "I'm here to help you with your development needs. ",
                "What would you like to work on together? ",
                "I can assist with planning, research, creative solutions, or debugging - ",
                "whatever you need to make your development journey smoother and more enjoyable!"
            ]
        else:
            response_chunks = [
                "Hello! I'm your AI assistant. ",
                "I'm currently running in fallback mode, but I'm still here to help! ",
                "What would you like to work on together?"
            ]

        for i, chunk in enumerate(response_chunks):
            chunk_data = {
                'id': f"fallback_chunk_{i}",
                'model': model_id,
                'chunk': chunk,
                'finished': i == len(response_chunks) - 1,
                'timestamp': datetime.utcnow().isoformat(),
                'mama_bear_variant': mama_bear_variant,
                'fallback': True
            }

            yield f"data: {json.dumps(chunk_data)}\n\n"
            time.sleep(0.1)  # Simulate streaming delay

        # Send completion signal
        completion_data = {
            'id': 'completion',
            'model': model_id,
            'finished': True,
            'mama_bear_variant': mama_bear_variant,
            'session_id': session_id,
            'fallback': True
        }
        yield f"data: {json.dumps(completion_data)}\n\n"

    except Exception as e:
        current_app.logger.error(f"Fallback response error: {e}")
        error_data = {
            'error': str(e),
            'model': model_id,
            'timestamp': datetime.utcnow().isoformat()
        }
        yield f"data: {json.dumps(error_data)}\n\n"
# Error handlers
@chat_bp.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 'Bad request - invalid chat data provided'
    }), 400

@chat_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Chat resource not found'
    }), 404

@chat_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error in chat service'
    }), 500
