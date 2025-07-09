from flask import Blueprint, request, jsonify
import asyncio
import logging
from services.revolutionary_mcp_service import revolutionary_mcp_service

logger = logging.getLogger(__name__)

# Create Blueprint for Revolutionary MCP API
revolutionary_mcp_bp = Blueprint('revolutionary_mcp', __name__, url_prefix='/api/revolutionary-mcp')

@revolutionary_mcp_bp.route('/status', methods=['GET'])
def get_mcp_status():
    """Get Revolutionary MCP Client status"""
    try:
        status = revolutionary_mcp_service.get_connection_status()
        return jsonify({
            'success': True,
            'status': status
        })
    except Exception as e:
        logger.error(f"Error getting MCP status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@revolutionary_mcp_bp.route('/agents/search', methods=['POST'])
def search_agents():
    """Search agents across all MCP marketplaces"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        filters = data.get('filters', {})

        # Convert to async
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            agents = loop.run_until_complete(
                revolutionary_mcp_service.search_agents(query, filters)
            )

            # Convert agents to dictionaries
            agent_dicts = []
            for agent in agents:
                agent_dicts.append({
                    'id': agent.id,
                    'name': agent.name,
                    'description': agent.description,
                    'author': agent.author,
                    'category': agent.category,
                    'rating': agent.rating,
                    'downloads': agent.downloads,
                    'logo': agent.logo,
                    'source': agent.source,
                    'capabilities': agent.capabilities,
                    'configuration': agent.configuration
                })

            return jsonify({
                'success': True,
                'agents': agent_dicts,
                'total': len(agent_dicts)
            })
        finally:
            loop.close()

    except Exception as e:
        logger.error(f"Error searching agents: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@revolutionary_mcp_bp.route('/agents/suggestions', methods=['POST'])
def get_mama_bear_suggestions():
    """Get Mama Bear's intelligent agent suggestions"""
    try:
        data = request.get_json()
        project_context = data.get('project_context', '')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            suggestions = loop.run_until_complete(
                revolutionary_mcp_service.get_mama_bear_suggestions(project_context)
            )

            # Convert to dictionaries
            suggestion_dicts = []
            for agent in suggestions:
                suggestion_dicts.append({
                    'id': agent.id,
                    'name': agent.name,
                    'description': agent.description,
                    'author': agent.author,
                    'category': agent.category,
                    'rating': agent.rating,
                    'downloads': agent.downloads,
                    'logo': agent.logo,
                    'source': agent.source,
                    'capabilities': agent.capabilities,
                    'relevance_score': getattr(agent, 'relevance_score', 0)
                })

            return jsonify({
                'success': True,
                'suggestions': suggestion_dicts,
                'message': f' Mama Bear analyzed "{project_context}" and found {len(suggestion_dicts)} relevant agents'
            })
        finally:
            loop.close()

    except Exception as e:
        logger.error(f"Error getting Mama Bear suggestions: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@revolutionary_mcp_bp.route('/agents/install', methods=['POST'])
def install_agent():
    """Install an agent from a marketplace"""
    try:
        data = request.get_json()
        agent_id = data.get('agent_id')
        source = data.get('source')

        if not agent_id or not source:
            return jsonify({'success': False, 'error': 'agent_id and source are required'}), 400

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(
                revolutionary_mcp_service.install_agent(agent_id, source)
            )

            return jsonify({
                'success': True,
                'result': result
            })
        finally:
            loop.close()

    except Exception as e:
        logger.error(f"Error installing agent: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@revolutionary_mcp_bp.route('/agents/create', methods=['POST'])
def create_custom_agent():
    """Create a custom agent using Mama Bear's AI"""
    try:
        data = request.get_json()
        config = data.get('config', {})

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            custom_agent = loop.run_until_complete(
                revolutionary_mcp_service.create_custom_agent(config)
            )

            agent_dict = {
                'id': custom_agent.id,
                'name': custom_agent.name,
                'description': custom_agent.description,
                'author': custom_agent.author,
                'category': custom_agent.category,
                'rating': custom_agent.rating,
                'downloads': custom_agent.downloads,
                'logo': custom_agent.logo,
                'source': custom_agent.source,
                'capabilities': custom_agent.capabilities,
                'configuration': custom_agent.configuration
            }

            return jsonify({
                'success': True,
                'agent': agent_dict,
                'message': ' Mama Bear successfully created your custom agent!'
            })
        finally:
            loop.close()

    except Exception as e:
        logger.error(f"Error creating custom agent: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@revolutionary_mcp_bp.route('/connections/test', methods=['POST'])
def test_mcp_connections():
    """Test connections to all MCP marketplaces"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Re-initialize connections
            loop.run_until_complete(revolutionary_mcp_service.initialize())

            status = revolutionary_mcp_service.get_connection_status()

            return jsonify({
                'success': True,
                'message': 'MCP connections tested successfully',
                'status': status
            })
        finally:
            loop.close()

    except Exception as e:
        logger.error(f"Error testing MCP connections: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@revolutionary_mcp_bp.route('/docker/connect', methods=['POST'])
def connect_docker_mcp():
    """Connect to Docker MCP Toolkit specifically"""
    try:
        data = request.get_json()
        docker_url = data.get('url', 'tcp:host.docker.internal:8811')

        logger.info(f"🐳 Attempting to connect to Docker MCP: {docker_url}")

        # Test Docker MCP connection with socat
        import subprocess
        import json

        # Test the Docker MCP connection
        test_command = [
            'docker', 'run', '-i', '--rm', 'alpine/socat',
            'STDIO', docker_url
        ]

        try:
            # Send a test message to Docker MCP
            result = subprocess.run(
                test_command,
                input='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"revolutionary-mcp","version":"1.0.0"}}}\n',
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return jsonify({
                    'success': True,
                    'message': '🐳 Successfully connected to Docker MCP Toolkit!',
                    'response': result.stdout
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f'Docker MCP connection failed: {result.stderr}'
                })

        except subprocess.TimeoutExpired:
            return jsonify({
                'success': False,
                'error': 'Docker MCP connection timeout - make sure Docker Desktop is running'
            })
        except FileNotFoundError:
            return jsonify({
                'success': False,
                'error': 'Docker not found - please install Docker Desktop'
            })

    except Exception as e:
        logger.error(f"Error connecting to Docker MCP: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Initialize the service when the module loads
try:
    # Service will be initialized on first use to avoid event loop conflicts
    logger.info(" Revolutionary MCP Service ready for initialization!")
except Exception as e:
    logger.error(f"Failed to prepare Revolutionary MCP Service: {e}")
