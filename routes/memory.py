"""
Memory API routes for Mem0 integration
Provides persistent context and relationship management for AI conversations
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import uuid
import json
import os
from typing import Dict, List, Optional

memory_bp = Blueprint('memory', __name__)

# In-memory storage for development (replace with Mem0 in production)
memory_store = {}
context_store = {}

@memory_bp.route('/context', methods=['GET'])
def get_context():
    """Get conversation context for a user/session"""
    try:
        user_id = request.args.get('user_id', 'default')
        session_id = request.args.get('session_id', 'default')
        
        context_key = f"{user_id}:{session_id}"
        context = context_store.get(context_key, {
            'messages': [],
            'relationships': {},
            'preferences': {},
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        })
        
        return jsonify({
            'success': True,
            'context': context
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting context: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@memory_bp.route('/context', methods=['POST'])
def save_context():
    """Save conversation context with Mem0 integration"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default')
        session_id = data.get('session_id', 'default')
        context = data.get('context', {})
        
        context_key = f"{user_id}:{session_id}"
        
        # Update context with timestamp
        context['updated_at'] = datetime.utcnow().isoformat()
        if 'created_at' not in context:
            context['created_at'] = datetime.utcnow().isoformat()
        
        # Store context
        context_store[context_key] = context
        
        # TODO: Integrate with Mem0 for persistent storage
        # mem0_client.add_memory(user_id, context)
        
        return jsonify({
            'success': True,
            'message': 'Context saved successfully',
            'context_id': context_key
        })
        
    except Exception as e:
        current_app.logger.error(f"Error saving context: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@memory_bp.route('/relationships', methods=['GET'])
def get_relationships():
    """Get AI relationship data for persistent personalities"""
    try:
        user_id = request.args.get('user_id', 'default')
        
        relationships = memory_store.get(f"relationships:{user_id}", {
            'mama_bear_variants': {
                'scout_commander': {'trust_level': 0.5, 'interaction_count': 0},
                'research_specialist': {'trust_level': 0.5, 'interaction_count': 0},
                'code_review_bear': {'trust_level': 0.5, 'interaction_count': 0},
                'creative_bear': {'trust_level': 0.5, 'interaction_count': 0},
                'learning_bear': {'trust_level': 0.5, 'interaction_count': 0},
                'efficiency_bear': {'trust_level': 0.5, 'interaction_count': 0},
                'debugging_detective': {'trust_level': 0.5, 'interaction_count': 0}
            },
            'preferences': {
                'communication_style': 'caring_technical',
                'complexity_preference': 'moderate',
                'learning_style': 'visual_kinesthetic'
            }
        })
        
        return jsonify({
            'success': True,
            'relationships': relationships
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting relationships: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@memory_bp.route('/relationships', methods=['POST'])
def update_relationships():
    """Update AI relationship data based on interactions"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default')
        variant = data.get('variant')
        interaction_data = data.get('interaction_data', {})
        
        relationships_key = f"relationships:{user_id}"
        relationships = memory_store.get(relationships_key, {
            'mama_bear_variants': {},
            'preferences': {}
        })
        
        # Update specific variant relationship
        if variant and variant in relationships.get('mama_bear_variants', {}):
            variant_data = relationships['mama_bear_variants'][variant]
            variant_data['interaction_count'] = variant_data.get('interaction_count', 0) + 1
            
            # Adjust trust level based on interaction success
            if interaction_data.get('helpful', True):
                variant_data['trust_level'] = min(1.0, variant_data.get('trust_level', 0.5) + 0.1)
            
            variant_data['last_interaction'] = datetime.utcnow().isoformat()
        
        # Update preferences based on interaction patterns
        if interaction_data.get('preferences'):
            relationships['preferences'].update(interaction_data['preferences'])
        
        memory_store[relationships_key] = relationships
        
        return jsonify({
            'success': True,
            'message': 'Relationships updated successfully'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error updating relationships: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@memory_bp.route('/search', methods=['POST'])
def search_memory():
    """Search through stored memories and context"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        user_id = data.get('user_id', 'default')
        
        # Simple search implementation (replace with Mem0 semantic search)
        results = []
        
        # Search through context store
        for context_key, context in context_store.items():
            if user_id in context_key:
                for message in context.get('messages', []):
                    if query.lower() in message.get('content', '').lower():
                        results.append({
                            'type': 'message',
                            'content': message.get('content', ''),
                            'timestamp': message.get('timestamp'),
                            'context_id': context_key
                        })
        
        return jsonify({
            'success': True,
            'results': results[:10]  # Limit to 10 results
        })
        
    except Exception as e:
        current_app.logger.error(f"Error searching memory: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@memory_bp.route('/stats', methods=['GET'])
def get_memory_stats():
    """Get memory usage and relationship statistics"""
    try:
        user_id = request.args.get('user_id', 'default')
        
        # Calculate stats
        user_contexts = [k for k in context_store.keys() if user_id in k]
        total_messages = sum(len(context_store[k].get('messages', [])) for k in user_contexts)
        
        relationships_key = f"relationships:{user_id}"
        relationships = memory_store.get(relationships_key, {})
        
        stats = {
            'total_contexts': len(user_contexts),
            'total_messages': total_messages,
            'relationship_strength': {
                variant: data.get('trust_level', 0.5)
                for variant, data in relationships.get('mama_bear_variants', {}).items()
            },
            'memory_usage': {
                'contexts': len(context_store),
                'relationships': len([k for k in memory_store.keys() if k.startswith('relationships:')])
            }
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting memory stats: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@memory_bp.route('/health', methods=['GET'])
def memory_health():
    """Health check endpoint for memory system"""
    try:
        return jsonify({
            'success': True,
            'status': 'healthy',
            'service': 'memory',
            'timestamp': datetime.utcnow().isoformat(),
            'store_count': len(memory_store),
            'context_count': len(context_store)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@memory_bp.route('/store', methods=['GET'])
def get_memory_store():
    """Get current memory store statistics"""
    try:
        return jsonify({
            'success': True,
            'store': {
                'total_memories': len(memory_store),
                'total_contexts': len(context_store),
                'memory_keys': list(memory_store.keys())[:10],  # First 10 keys for preview
                'context_keys': list(context_store.keys())[:10]
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@memory_bp.route('/store', methods=['POST']) 
def store_memory():
    """Store a new memory entry"""
    try:
        data = request.get_json()
        memory_id = data.get('id', str(uuid.uuid4()))
        user_id = data.get('user_id', 'default')
        content = data.get('content', '')
        
        memory_key = f"{user_id}:{memory_id}"
        memory_store[memory_key] = {
            'id': memory_id,
            'user_id': user_id,
            'content': content,
            'created_at': datetime.utcnow().isoformat(),
            'metadata': data.get('metadata', {})
        }
        
        return jsonify({
            'success': True,
            'memory_id': memory_id,
            'message': 'Memory stored successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Error handlers
@memory_bp.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 'Bad request - invalid data provided'
    }), 400

@memory_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Memory resource not found'
    }), 404

@memory_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500