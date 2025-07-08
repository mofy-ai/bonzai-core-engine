# backend/services/pipedream_fallback_service.py
"""
[LINK] Pipedream Fallback Service - Pattern-based workflow creation
Works without AI integration using intelligent pattern matching
"""

import os
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import uuid

logger = logging.getLogger(__name__)

class PipedreamFallbackService:
    """
    Fallback service for creating workflows without AI
    Uses intelligent pattern matching and templates
    """

    def __init__(self):
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> Dict[str, Any]:
        """Load workflow patterns for common use cases"""
        return {
            'github_slack': {
                'keywords': ['github', 'slack', 'notify', 'message'],
                'template': {
                    'name': 'GitHub to Slack Integration',
                    'description': 'Automatically notify Slack about GitHub events',
                    'trigger': {'type': 'webhook', 'source': 'github'},
                    'steps': [{
                        'type': 'slack_message',
                        'action': 'send_message',
                        'config': {
                            'channel': '#dev-notifications',
                            'message': '[STAR] GitHub Event: {{event.type}} in {{repository.name}}'
                        }
                    }],
                    'category': 'DevOps',
                    'tags': ['github', 'slack', 'devops', 'notifications']
                }
            },
            'github_star': {
                'keywords': ['github', 'star', 'starred', 'notification'],
                'template': {
                    'name': 'GitHub Star Notifications',
                    'description': 'Get notified when someone stars your repository',
                    'trigger': {'type': 'webhook', 'source': 'github', 'event': 'star'},
                    'steps': [{
                        'type': 'slack_message',
                        'action': 'send_message',
                        'config': {
                            'channel': '#general',
                            'message': '[STAR] {{sender.login}} starred {{repository.name}}!'
                        }
                    }],
                    'category': 'Notifications',
                    'tags': ['github', 'stars', 'notifications']
                }
            },
            'email_slack': {
                'keywords': ['email', 'slack', 'notify', 'forward'],
                'template': {
                    'name': 'Email to Slack Forwarder',
                    'description': 'Forward important emails to Slack',
                    'trigger': {'type': 'email', 'source': 'gmail'},
                    'steps': [{
                        'type': 'slack_message',
                        'action': 'send_message',
                        'config': {
                            'channel': '#email-alerts',
                            'message': '[EMOJI] New email: {{subject}} from {{sender}}'
                        }
                    }],
                    'category': 'Communication',
                    'tags': ['email', 'slack', 'communication']
                }
            },
            'schedule_reminder': {
                'keywords': ['schedule', 'reminder', 'daily', 'weekly'],
                'template': {
                    'name': 'Scheduled Reminder',
                    'description': 'Send regular reminders or reports',
                    'trigger': {'type': 'schedule', 'config': {'cron': '0 9 * * 1'}},
                    'steps': [{
                        'type': 'slack_message',
                        'action': 'send_message',
                        'config': {
                            'channel': '#reminders',
                            'message': '⏰ Weekly reminder: Time for your team standup!'
                        }
                    }],
                    'category': 'Productivity',
                    'tags': ['schedule', 'reminder', 'productivity']
                }
            }
        }

    def create_workflow_from_patterns(self, request: str, user_id: str = None) -> Dict[str, Any]:
        """Create workflow using pattern matching"""
        try:
            request_lower = request.lower()

            # Find matching patterns
            matched_patterns = []
            for pattern_name, pattern_data in self.patterns.items():
                keywords = pattern_data['keywords']
                matches = sum(1 for keyword in keywords if keyword in request_lower)
                if matches >= 2:  # At least 2 keywords must match
                    matched_patterns.append((pattern_name, matches, pattern_data))

            if matched_patterns:
                # Use the pattern with the most matches
                best_pattern = max(matched_patterns, key=lambda x: x[1])
                pattern_name, score, pattern_data = best_pattern

                workflow_spec = pattern_data['template'].copy()

                # Customize based on the request
                workflow_spec['description'] += f" (Created from: {request})"
                workflow_spec['tags'].append('pattern-matched')

                logger.info(f"[OK] Matched pattern '{pattern_name}' with score {score}")

                return {
                    'success': True,
                    'workflow_spec': workflow_spec,
                    'pattern_matched': pattern_name,
                    'confidence': score / len(pattern_data['keywords']) * 100,
                    'message': f"Created workflow using '{pattern_name}' pattern"
                }
            else:
                # Create a generic workflow
                workflow_spec = {
                    'name': 'Custom Workflow',
                    'description': f'Custom workflow created from: {request}',
                    'trigger': {'type': 'webhook', 'source': 'custom'},
                    'steps': [{
                        'type': 'log',
                        'action': 'log_message',
                        'config': {
                            'message': f'Workflow triggered: {request}'
                        }
                    }],
                    'category': 'Custom',
                    'tags': ['custom', 'manual']
                }

                return {
                    'success': True,
                    'workflow_spec': workflow_spec,
                    'pattern_matched': 'generic',
                    'confidence': 50,
                    'message': 'Created generic workflow - consider using specific keywords like "github", "slack", "email" for better automation'
                }

        except Exception as e:
            logger.error(f"[ERROR] Error in pattern matching: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# Global instance
_fallback_service = None

def get_fallback_service() -> PipedreamFallbackService:
    """Get the fallback service instance"""
    global _fallback_service
    if _fallback_service is None:
        _fallback_service = PipedreamFallbackService()
    return _fallback_service
