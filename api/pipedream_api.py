# backend/api/pipedream_api.py
"""
🔗 Pipedream API Endpoints - REST API for Workflow Automation
Production-ready endpoints for Pipedream Integration Studio
"""

from flask import Blueprint, request, jsonify, Response
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import json

from services.pipedream_integration_service import get_pipedream_service

logger = logging.getLogger(__name__)

# Create Blueprint
pipedream_bp = Blueprint('pipedream', __name__)

@pipedream_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Get service (don't await here since this is a sync function)
        service_status = {
            'service': 'Pipedream Integration API',
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'endpoints': [
                '/workflows',
                '/workflows/create',
                '/workflows/natural-language',
                '/workflows/{id}/execute',
                '/workflows/{id}/pause',
                '/workflows/{id}/resume',
                '/workflows/{id}/delete',
                '/templates',
                '/analytics',
                '/services'
            ]
        }

        return jsonify(service_status)

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'service': 'Pipedream Integration API',
            'status': 'error',
            'error': str(e)
        }), 500

@pipedream_bp.route('/workflows', methods=['GET'])
def get_workflows():
    """Get all workflows"""
    try:
        user_id = request.args.get('user_id', 'default_user')

        async def fetch_workflows():
            service = await get_pipedream_service()
            if not service:
                return []
            return await service.get_workflows(user_id)

        # Run async function
        workflows = asyncio.run(fetch_workflows())

        return jsonify({
            'success': True,
            'workflows': workflows,
            'total': len(workflows),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error fetching workflows: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pipedream_bp.route('/workflows/create', methods=['POST'])
def create_workflow():
    """Create a new workflow"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No workflow data provided'
            }), 400

        user_id = data.get('user_id', 'default_user')
        workflow_spec = data.get('workflow_spec', {})

        if not workflow_spec:
            return jsonify({
                'success': False,
                'error': 'Workflow specification required'
            }), 400

        async def create_workflow_async():
            service = await get_pipedream_service()
            if not service:
                return {
                    'success': False,
                    'error': 'Pipedream service not available'
                }
            return await service.create_workflow(workflow_spec, user_id)

        # Run async function
        result = asyncio.run(create_workflow_async())

        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"Error creating workflow: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pipedream_bp.route('/workflows/natural-language', methods=['POST'])
def create_workflow_from_natural_language():
    """Create workflow from natural language description"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No request data provided'
            }), 400

        request_text = data.get('request', '')
        user_id = data.get('user_id', 'default_user')

        if not request_text:
            return jsonify({
                'success': False,
                'error': 'Request text is required'
            }), 400

        async def create_nl_workflow_async():
            service = await get_pipedream_service()
            if not service:
                return {
                    'success': False,
                    'error': 'Pipedream service not available'
                }
            return await service.create_workflow_from_natural_language(request_text, user_id)

        # Run async function
        result = asyncio.run(create_nl_workflow_async())

        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"Error creating workflow from natural language: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pipedream_bp.route('/workflows/<workflow_id>/execute', methods=['POST'])
def execute_workflow(workflow_id):
    """Execute a workflow manually"""
    try:
        data = request.get_json() or {}
        input_data = data.get('input_data', {})

        async def execute_workflow_async():
            service = await get_pipedream_service()
            if not service:
                return {
                    'success': False,
                    'error': 'Pipedream service not available'
                }
            return await service.execute_workflow(workflow_id, input_data)

        # Run async function
        result = asyncio.run(execute_workflow_async())

        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"Error executing workflow {workflow_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pipedream_bp.route('/workflows/<workflow_id>/pause', methods=['POST'])
def pause_workflow(workflow_id):
    """Pause a workflow"""
    try:
        async def pause_workflow_async():
            service = await get_pipedream_service()
            if not service:
                return {
                    'success': False,
                    'error': 'Pipedream service not available'
                }
            return await service.pause_workflow(workflow_id)

        # Run async function
        result = asyncio.run(pause_workflow_async())

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error pausing workflow {workflow_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pipedream_bp.route('/workflows/<workflow_id>/resume', methods=['POST'])
def resume_workflow(workflow_id):
    """Resume a paused workflow"""
    try:
        async def resume_workflow_async():
            service = await get_pipedream_service()
            if not service:
                return {
                    'success': False,
                    'error': 'Pipedream service not available'
                }
            return await service.resume_workflow(workflow_id)

        # Run async function
        result = asyncio.run(resume_workflow_async())

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error resuming workflow {workflow_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pipedream_bp.route('/workflows/<workflow_id>/delete', methods=['DELETE'])
def delete_workflow(workflow_id):
    """Delete a workflow"""
    try:
        async def delete_workflow_async():
            service = await get_pipedream_service()
            if not service:
                return {
                    'success': False,
                    'error': 'Pipedream service not available'
                }
            return await service.delete_workflow(workflow_id)

        # Run async function
        result = asyncio.run(delete_workflow_async())

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error deleting workflow {workflow_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pipedream_bp.route('/templates', methods=['GET'])
def get_workflow_templates():
    """Get available workflow templates"""
    try:
        async def fetch_templates():
            service = await get_pipedream_service()
            if not service:
                return []
            return await service.get_workflow_templates()

        # Run async function
        templates = asyncio.run(fetch_templates())

        return jsonify({
            'success': True,
            'templates': templates,
            'total': len(templates),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error fetching templates: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pipedream_bp.route('/analytics', methods=['GET'])
def get_analytics():
    """Get workflow analytics and insights"""
    try:
        timeframe = request.args.get('timeframe', '7d')

        async def fetch_analytics():
            service = await get_pipedream_service()
            if not service:
                return {}
            return await service.get_analytics(timeframe)

        # Run async function
        analytics = asyncio.run(fetch_analytics())

        return jsonify({
            'success': True,
            'analytics': analytics,
            'timeframe': timeframe,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error fetching analytics: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pipedream_bp.route('/services', methods=['GET'])
def get_available_services():
    """Get list of available integration services"""
    try:
        async def fetch_services():
            service = await get_pipedream_service()
            if not service:
                return []
            return await service.get_available_services()

        # Run async function
        services = asyncio.run(fetch_services())

        return jsonify({
            'success': True,
            'services': services,
            'total': len(services),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error fetching services: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pipedream_bp.route('/status', methods=['GET'])
def get_service_status():
    """Get Pipedream service status"""
    try:
        async def get_status():
            service = await get_pipedream_service()
            if not service:
                return {
                    'service': 'Pipedream Integration Service',
                    'status': 'unavailable',
                    'error': 'Service not initialized'
                }
            return service.get_service_status()

        # Run async function
        status = asyncio.run(get_status())

        return jsonify(status)

    except Exception as e:
        logger.error(f"Error getting service status: {e}")
        return jsonify({
            'service': 'Pipedream Integration Service',
            'status': 'error',
            'error': str(e)
        }), 500

# Natural Language Assistant Endpoint (Mama Bear Integration)
@pipedream_bp.route('/assistant/chat', methods=['POST'])
def pipedream_assistant_chat():
    """Chat with Pipedream assistant for workflow guidance"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400

        message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')

        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400

        # Check if this is a workflow creation request
        workflow_keywords = ['create', 'build', 'make', 'workflow', 'automation', 'integrate']
        is_workflow_request = any(keyword in message.lower() for keyword in workflow_keywords)

        if is_workflow_request:
            # Try to create workflow from natural language
            async def create_from_nl():
                service = await get_pipedream_service()
                if not service:
                    return {
                        'success': False,
                        'error': 'Pipedream service not available'
                    }
                return await service.create_workflow_from_natural_language(message, user_id)

            result = asyncio.run(create_from_nl())

            if result.get('success'):
                response = f"✅ I've created your workflow! Here's what I built:\n\n" \
                          f"**{result.get('workflow_id', 'Workflow')}**\n" \
                          f"🔗 Pipedream URL: {result.get('pipedream_url', 'N/A')}\n\n" \
                          f"Your workflow is now live and ready to automate your process!"
            else:
                response = f"I understand you want to create a workflow, but I encountered an issue: {result.get('error', 'Unknown error')}\n\n" \
                          f"Let me suggest some alternatives:\n" \
                          f"• Try being more specific about the trigger and actions\n" \
                          f"• Check out our workflow templates for inspiration\n" \
                          f"• Use the visual workflow builder for complex automations"
        else:
            # General assistant response
            response = f"🐻 **Mama Bear Pipedream Assistant**\n\n" \
                      f"I can help you with workflow automation! Here are some things I can do:\n\n" \
                      f"🔧 **Create Workflows**: Just describe what you want to automate\n" \
                      f"📊 **Analytics**: Get insights on your workflow performance\n" \
                      f"🎯 **Templates**: Browse pre-built workflow templates\n" \
                      f"🔗 **Integrations**: Connect 2000+ services and apps\n\n" \
                      f"Try saying: *'Create a workflow that sends me a Slack message when someone stars my GitHub repo'*"

        return jsonify({
            'success': True,
            'response': response,
            'is_workflow_request': is_workflow_request,
            'timestamp': datetime.now().isoformat(),
            'assistant': 'mama_bear_pipedream'
        })

    except Exception as e:
        logger.error(f"Error in Pipedream assistant chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Webhook endpoint for Pipedream callbacks
@pipedream_bp.route('/webhook', methods=['POST'])
def pipedream_webhook():
    """Handle webhooks from Pipedream workflows"""
    try:
        data = request.get_json()
        headers = dict(request.headers)

        # Log webhook received
        logger.info(f"📥 Pipedream webhook received: {data}")

        # Here you could process the webhook data
        # Update workflow execution status, trigger notifications, etc.

        return jsonify({
            'success': True,
            'message': 'Webhook processed successfully',
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error processing Pipedream webhook: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def integrate_pipedream_api_with_app(app):
    """Integrate Pipedream API with Flask app"""
    try:
        # Register the blueprint
        app.register_blueprint(pipedream_bp, url_prefix='/api/pipedream')
        logger.info("✅ Pipedream API endpoints registered")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to integrate Pipedream API: {e}")
        return False
