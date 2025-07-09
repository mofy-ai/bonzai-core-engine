"""
 Virtual Computer API - MUMA Scout Agent Operations
API endpoints for managing virtual computer workspaces and agent operations
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from flask import Blueprint, request, jsonify
from flask_socketio import emit, join_room, leave_room

# Import the virtual computer service
from backend.services.virtual_computer_service import (
    virtual_computer_service,
    VirtualComputerService,
    AgentStatus,
    VirtualEnvironmentType
)

logger = logging.getLogger(__name__)

# Create blueprint
virtual_computer_bp = Blueprint('virtual_computer', __name__, url_prefix='/api/virtual-computer')

# Global SocketIO instance (will be set during initialization)
socketio = None

def init_virtual_computer_api(socketio_instance):
    """Initialize the virtual computer API with SocketIO"""
    global socketio
    socketio = socketio_instance
    logger.info("🖥️ Virtual Computer API initialized with SocketIO support")

@virtual_computer_bp.route('/workspaces', methods=['POST'])
async def create_workspace():
    """Create a new agent workspace"""
    try:
        data = request.get_json()
        
        agent_name = data.get('agent_name')
        user_id = data.get('user_id')
        task_description = data.get('task_description')
        
        if not all([agent_name, user_id, task_description]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: agent_name, user_id, task_description'
            }), 400
        
        # Create workspace
        result = await virtual_computer_service.create_agent_workspace(
            agent_name, user_id, task_description
        )
        
        if result['success']:
            workspace_id = result['workspace_id']
            
            # Emit workspace created event
            if socketio:
                socketio.emit('workspace_created', {
                    'workspace_id': workspace_id,
                    'agent_name': agent_name,
                    'status': 'created'
                }, room=f'user_{user_id}')
            
            logger.info(f" Created workspace {workspace_id} for {agent_name}")
            
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error creating workspace: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@virtual_computer_bp.route('/workspaces/<workspace_id>/start', methods=['POST'])
async def start_workspace_execution(workspace_id: str):
    """Start autonomous agent execution"""
    try:
        result = await virtual_computer_service.start_agent_execution(workspace_id)
        
        if result['success']:
            # Emit execution started event
            if socketio:
                socketio.emit('execution_started', {
                    'workspace_id': workspace_id,
                    'status': 'executing'
                }, room=f'workspace_{workspace_id}')
            
            logger.info(f"▶️ Started execution for workspace {workspace_id}")
            
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error starting workspace execution: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@virtual_computer_bp.route('/workspaces/<workspace_id>/status', methods=['GET'])
async def get_workspace_status(workspace_id: str):
    """Get workspace status and timeline"""
    try:
        result = await virtual_computer_service.get_workspace_status(workspace_id)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error getting workspace status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@virtual_computer_bp.route('/workspaces/<workspace_id>/execute', methods=['POST'])
async def execute_command(workspace_id: str):
    """Execute a command in the workspace"""
    try:
        data = request.get_json()
        
        command = data.get('command')
        environment_type = data.get('environment_type', 'auto')
        
        if not command:
            return jsonify({
                'success': False,
                'error': 'Missing required field: command'
            }), 400
        
        result = await virtual_computer_service.execute_agent_command(
            workspace_id, command, environment_type
        )
        
        if result['success']:
            # Emit command executed event
            if socketio:
                socketio.emit('command_executed', {
                    'workspace_id': workspace_id,
                    'command': command,
                    'result': result['result']
                }, room=f'workspace_{workspace_id}')
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@virtual_computer_bp.route('/workspaces/<workspace_id>/files', methods=['POST'])
async def update_workspace_file(workspace_id: str):
    """Update a file in the workspace"""
    try:
        data = request.get_json()
        
        file_path = data.get('file_path')
        content = data.get('content')
        operation = data.get('operation', 'create')
        
        if not all([file_path, content]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: file_path, content'
            }), 400
        
        result = await virtual_computer_service.update_workspace_files(
            workspace_id, file_path, content, operation
        )
        
        if result['success']:
            # Emit file updated event
            if socketio:
                socketio.emit('file_updated', {
                    'workspace_id': workspace_id,
                    'file_path': file_path,
                    'operation': operation,
                    'file_tree': result['file_tree']
                }, room=f'workspace_{workspace_id}')
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error updating workspace file: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@virtual_computer_bp.route('/workspaces/<workspace_id>/files/<path:file_path>', methods=['GET'])
async def get_workspace_file(workspace_id: str, file_path: str):
    """Get a file from the workspace"""
    try:
        # Mock implementation - in production, retrieve from actual workspace
        result = {
            'success': True,
            'file_path': file_path,
            'content': f'// File content for {file_path}\n// Generated by {workspace_id}',
            'last_modified': datetime.now().isoformat()
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error getting workspace file: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@virtual_computer_bp.route('/stats', methods=['GET'])
async def get_virtual_computer_stats():
    """Get virtual computer service statistics"""
    try:
        result = await virtual_computer_service.get_virtual_computer_stats()
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error getting virtual computer stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@virtual_computer_bp.route('/environments/types', methods=['GET'])
def get_environment_types():
    """Get available virtual environment types"""
    try:
        environment_types = [
            {
                'type': 'scrapybara_browser',
                'name': 'Scrapybara Browser',
                'description': 'Web browsing and automation environment',
                'capabilities': ['web_browsing', 'form_filling', 'data_extraction']
            },
            {
                'type': 'scrapybara_ubuntu',
                'name': 'Scrapybara Ubuntu',
                'description': 'Full Ubuntu environment with development tools',
                'capabilities': ['command_line', 'file_operations', 'package_management']
            },
            {
                'type': 'e2b_code_interpreter',
                'name': 'E2B Code Interpreter',
                'description': 'Secure code execution environment',
                'capabilities': ['code_execution', 'package_installation', 'file_management']
            },
            {
                'type': 'hybrid_workspace',
                'name': 'Hybrid Workspace',
                'description': 'Combined environment with multiple capabilities',
                'capabilities': ['web_browsing', 'code_execution', 'file_operations']
            }
        ]
        
        return jsonify({
            'success': True,
            'environment_types': environment_types
        })
        
    except Exception as e:
        logger.error(f"Error getting environment types: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# SocketIO event handlers
def register_socketio_events(socketio_instance):
    """Register SocketIO events for real-time workspace updates"""
    
    @socketio_instance.on('join_workspace')
    def handle_join_workspace(data):
        """Join a workspace room for real-time updates"""
        workspace_id = data.get('workspace_id')
        user_id = data.get('user_id')
        
        if workspace_id and user_id:
            join_room(f'workspace_{workspace_id}')
            join_room(f'user_{user_id}')
            
            emit('joined_workspace', {
                'workspace_id': workspace_id,
                'status': 'connected'
            })
            
            logger.info(f"👤 User {user_id} joined workspace {workspace_id}")
    
    @socketio_instance.on('leave_workspace')
    def handle_leave_workspace(data):
        """Leave a workspace room"""
        workspace_id = data.get('workspace_id')
        user_id = data.get('user_id')
        
        if workspace_id and user_id:
            leave_room(f'workspace_{workspace_id}')
            leave_room(f'user_{user_id}')
            
            emit('left_workspace', {
                'workspace_id': workspace_id,
                'status': 'disconnected'
            })
            
            logger.info(f"👤 User {user_id} left workspace {workspace_id}")
    
    @socketio_instance.on('workspace_heartbeat')
    def handle_workspace_heartbeat(data):
        """Handle workspace heartbeat for keeping connections alive"""
        workspace_id = data.get('workspace_id')
        
        if workspace_id:
            emit('heartbeat_response', {
                'workspace_id': workspace_id,
                'timestamp': datetime.now().isoformat(),
                'status': 'alive'
            })

# Background task for sending live updates
async def send_workspace_updates():
    """Background task to send live workspace updates"""
    while True:
        try:
            # Get all active workspaces
            stats = await virtual_computer_service.get_virtual_computer_stats()
            
            if stats['success'] and socketio:
                # Send updates to all connected clients
                socketio.emit('workspace_stats_update', {
                    'stats': stats['stats'],
                    'timestamp': datetime.now().isoformat()
                })
            
            # Wait 5 seconds before next update
            await asyncio.sleep(5)
            
        except Exception as e:
            logger.error(f"Error in workspace updates background task: {e}")
            await asyncio.sleep(10)  # Wait longer on error

# Initialize function for the API
def integrate_virtual_computer_api(app, socketio_instance):
    """Integrate virtual computer API with Flask app and SocketIO"""
    global socketio
    socketio = socketio_instance
    
    # Register blueprint
    app.register_blueprint(virtual_computer_bp)
    
    # Register SocketIO events
    register_socketio_events(socketio_instance)
    
    # Start background task for live updates (only if event loop is running)
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(send_workspace_updates())
    except RuntimeError:
        # No event loop running, skip background task for now
        logger.warning(" No event loop running, skipping background workspace updates")
    
    logger.info("🔗 Virtual Computer API integrated with Flask app and SocketIO")

# Export the blueprint and integration function
__all__ = ['virtual_computer_bp', 'integrate_virtual_computer_api', 'init_virtual_computer_api']