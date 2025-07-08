"""
Theme API routes
Provides theme management, customization, and accessibility options
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import uuid
import json
from typing import Dict, List, Optional

themes_bp = Blueprint('themes', __name__)

# Mock theme data
theme_store = {
    'cozy-cabin': {
        'id': 'cozy-cabin',
        'name': 'Cozy Cabin',
        'description': 'Warm, earthy tones for a comfortable coding environment',
        'category': 'comfort',
        'colors': {
            'primary': '#8B4513',
            'secondary': '#CD853F',
            'accent': '#DEB887',
            'background': '#FFF8DC',
            'text': '#2F4F4F',
            'border': '#D2B48C'
        },
        'accessibility': {
            'high_contrast': False,
            'reduced_motion': False,
            'large_text': False,
            'color_blind_friendly': True
        },
        'created_at': '2024-01-15T10:00:00Z',
        'updated_at': '2024-01-20T14:30:00Z',
        'usage_count': 127,
        'rating': 4.6
    },
    'forest-sanctuary': {
        'id': 'forest-sanctuary',
        'name': 'Forest Sanctuary', 
        'description': 'Natural greens and browns for a calming atmosphere',
        'category': 'nature',
        'colors': {
            'primary': '#228B22',
            'secondary': '#32CD32',
            'accent': '#90EE90',
            'background': '#F0FFF0',
            'text': '#006400',
            'border': '#8FBC8F'
        },
        'accessibility': {
            'high_contrast': False,
            'reduced_motion': False,
            'large_text': False,
            'color_blind_friendly': True
        },
        'created_at': '2024-01-12T09:30:00Z',
        'updated_at': '2024-01-19T16:15:00Z',
        'usage_count': 89,
        'rating': 4.8
    },
    'midnight-focus': {
        'id': 'midnight-focus',
        'name': 'Midnight Focus',
        'description': 'Dark theme optimized for extended coding sessions',
        'category': 'dark',
        'colors': {
            'primary': '#4169E1',
            'secondary': '#6495ED',
            'accent': '#87CEEB',
            'background': '#191970',
            'text': '#E6E6FA',
            'border': '#483D8B'
        },
        'accessibility': {
            'high_contrast': True,
            'reduced_motion': True,
            'large_text': False,
            'color_blind_friendly': True
        },
        'created_at': '2024-01-18T20:00:00Z',
        'updated_at': '2024-01-20T22:45:00Z',
        'usage_count': 203,
        'rating': 4.9
    },
    'sunrise-energy': {
        'id': 'sunrise-energy',
        'name': 'Sunrise Energy',
        'description': 'Bright, energizing colors to boost productivity',
        'category': 'energetic',
        'colors': {
            'primary': '#FF6347',
            'secondary': '#FF7F50',
            'accent': '#FFA07A',
            'background': '#FFFAF0',
            'text': '#8B0000',
            'border': '#F4A460'
        },
        'accessibility': {
            'high_contrast': False,
            'reduced_motion': False,
            'large_text': False,
            'color_blind_friendly': False
        },
        'created_at': '2024-01-20T06:00:00Z',
        'updated_at': '2024-01-20T06:00:00Z',
        'usage_count': 12,
        'rating': 4.2
    }
}

user_theme_preferences = {
    'default': {
        'current_theme': 'cozy-cabin',
        'accessibility_settings': {
            'high_contrast': False,
            'reduced_motion': False,
            'large_text': False,
            'color_blind_friendly': True
        },
        'custom_overrides': {},
        'last_updated': '2024-01-20T15:30:00Z'
    }
}

@themes_bp.route('/health', methods=['GET'])
def themes_health():
    """Health check endpoint for themes system"""
    try:
        return jsonify({
            'success': True,
            'status': 'healthy',
            'service': 'themes',
            'timestamp': datetime.utcnow().isoformat(),
            'total_themes': len(theme_store),
            'active_users': len(user_theme_preferences)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@themes_bp.route('/themes', methods=['GET'])
def get_themes():
    """Get all available themes with optional filtering"""
    try:
        category_filter = request.args.get('category')
        accessibility_filter = request.args.get('accessibility')
        
        themes = list(theme_store.values())
        
        if category_filter:
            themes = [t for t in themes if t['category'] == category_filter]
        
        if accessibility_filter:
            themes = [t for t in themes if t['accessibility'].get(accessibility_filter, False)]
        
        # Sort by rating descending
        themes.sort(key=lambda x: x['rating'], reverse=True)
        
        return jsonify({
            'success': True,
            'themes': themes,
            'total': len(themes)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@themes_bp.route('/themes/<theme_id>', methods=['GET'])
def get_theme(theme_id):
    """Get a specific theme by ID"""
    try:
        theme = theme_store.get(theme_id)
        if not theme:
            return jsonify({
                'success': False,
                'error': 'Theme not found'
            }), 404
        
        return jsonify({
            'success': True,
            'theme': theme
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@themes_bp.route('/themes', methods=['POST'])
def create_theme():
    """Create a new custom theme"""
    try:
        data = request.get_json()
        
        theme_id = data.get('id', str(uuid.uuid4())[:12])
        
        theme = {
            'id': theme_id,
            'name': data.get('name', f'Custom Theme {theme_id}'),
            'description': data.get('description', 'Custom user-created theme'),
            'category': data.get('category', 'custom'),
            'colors': data.get('colors', {}),
            'accessibility': data.get('accessibility', {
                'high_contrast': False,
                'reduced_motion': False,
                'large_text': False,
                'color_blind_friendly': False
            }),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'usage_count': 0,
            'rating': 0.0,
            'is_custom': True,
            'created_by': data.get('user_id', 'anonymous')
        }
        
        theme_store[theme_id] = theme
        
        return jsonify({
            'success': True,
            'theme': theme,
            'message': 'Theme created successfully'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@themes_bp.route('/themes/<theme_id>', methods=['PUT'])
def update_theme(theme_id):
    """Update an existing theme"""
    try:
        theme = theme_store.get(theme_id)
        if not theme:
            return jsonify({
                'success': False,
                'error': 'Theme not found'
            }), 404
        
        data = request.get_json()
        
        # Update allowed fields
        for field in ['name', 'description', 'category', 'colors', 'accessibility']:
            if field in data:
                theme[field] = data[field]
        
        theme['updated_at'] = datetime.utcnow().isoformat()
        
        return jsonify({
            'success': True,
            'theme': theme,
            'message': 'Theme updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@themes_bp.route('/themes/<theme_id>', methods=['DELETE'])
def delete_theme(theme_id):
    """Delete a custom theme"""
    try:
        theme = theme_store.get(theme_id)
        if not theme:
            return jsonify({
                'success': False,
                'error': 'Theme not found'
            }), 404
        
        # Only allow deletion of custom themes
        if not theme.get('is_custom', False):
            return jsonify({
                'success': False,
                'error': 'Cannot delete built-in themes'
            }), 403
        
        del theme_store[theme_id]
        
        return jsonify({
            'success': True,
            'message': 'Theme deleted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@themes_bp.route('/user/<user_id>/preferences', methods=['GET'])
def get_user_preferences(user_id):
    """Get user theme preferences"""
    try:
        preferences = user_theme_preferences.get(user_id, {
            'current_theme': 'cozy-cabin',
            'accessibility_settings': {
                'high_contrast': False,
                'reduced_motion': False,
                'large_text': False,
                'color_blind_friendly': False
            },
            'custom_overrides': {},
            'last_updated': datetime.utcnow().isoformat()
        })
        
        return jsonify({
            'success': True,
            'preferences': preferences
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@themes_bp.route('/user/<user_id>/preferences', methods=['PUT'])
def update_user_preferences(user_id):
    """Update user theme preferences"""
    try:
        data = request.get_json()
        
        preferences = user_theme_preferences.get(user_id, {})
        
        # Update preferences
        if 'current_theme' in data:
            if data['current_theme'] not in theme_store:
                return jsonify({
                    'success': False,
                    'error': 'Theme not found'
                }), 404
            preferences['current_theme'] = data['current_theme']
            # Increment usage count
            theme_store[data['current_theme']]['usage_count'] += 1
        
        if 'accessibility_settings' in data:
            preferences['accessibility_settings'] = data['accessibility_settings']
        
        if 'custom_overrides' in data:
            preferences['custom_overrides'] = data['custom_overrides']
        
        preferences['last_updated'] = datetime.utcnow().isoformat()
        user_theme_preferences[user_id] = preferences
        
        return jsonify({
            'success': True,
            'preferences': preferences,
            'message': 'Preferences updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@themes_bp.route('/categories', methods=['GET'])
def get_theme_categories():
    """Get available theme categories"""
    try:
        categories = {}
        
        for theme in theme_store.values():
            category = theme['category']
            if category not in categories:
                categories[category] = {
                    'name': category.replace('_', ' ').title(),
                    'count': 0,
                    'themes': []
                }
            categories[category]['count'] += 1
            categories[category]['themes'].append({
                'id': theme['id'],
                'name': theme['name'],
                'rating': theme['rating']
            })
        
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@themes_bp.route('/accessibility', methods=['GET'])
def get_accessibility_options():
    """Get available accessibility features"""
    try:
        accessibility_features = {
            'high_contrast': {
                'name': 'High Contrast',
                'description': 'Increased contrast between text and background for better readability',
                'available_themes': len([t for t in theme_store.values() if t['accessibility']['high_contrast']])
            },
            'reduced_motion': {
                'name': 'Reduced Motion',
                'description': 'Minimized animations and transitions for users sensitive to motion',
                'available_themes': len([t for t in theme_store.values() if t['accessibility']['reduced_motion']])
            },
            'large_text': {
                'name': 'Large Text',
                'description': 'Larger font sizes for improved readability',
                'available_themes': len([t for t in theme_store.values() if t['accessibility']['large_text']])
            },
            'color_blind_friendly': {
                'name': 'Color Blind Friendly',
                'description': 'Color schemes optimized for users with color vision deficiencies',
                'available_themes': len([t for t in theme_store.values() if t['accessibility']['color_blind_friendly']])
            }
        }
        
        return jsonify({
            'success': True,
            'accessibility_features': accessibility_features
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@themes_bp.route('/themes/<theme_id>/rate', methods=['POST'])
def rate_theme(theme_id):
    """Rate a theme"""
    try:
        theme = theme_store.get(theme_id)
        if not theme:
            return jsonify({
                'success': False,
                'error': 'Theme not found'
            }), 404
        
        data = request.get_json()
        rating = data.get('rating', 0)
        
        if not (1 <= rating <= 5):
            return jsonify({
                'success': False,
                'error': 'Rating must be between 1 and 5'
            }), 400
        
        # Simple rating calculation (in production, would store individual ratings)
        current_rating = theme['rating']
        usage_count = theme['usage_count']
        
        # Weighted average with new rating
        new_rating = ((current_rating * usage_count) + rating) / (usage_count + 1)
        theme['rating'] = round(new_rating, 1)
        theme['usage_count'] += 1
        
        return jsonify({
            'success': True,
            'theme': theme,
            'message': 'Rating submitted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
