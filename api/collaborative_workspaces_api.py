# backend/api/collaborative_workspaces_api.py
"""
 SUPERCHARGED COLLABORATIVE WORKSPACES API - PRODUCTION READY
✨ Express Mode + Real-time Collaboration + Agentic Control
"""

from flask import Blueprint, request, jsonify
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

from services.supercharged_collaborative_workspaces_v3 import SuperchargedCollaborativeWorkspacesV3

logger = logging.getLogger(__name__)

# Create Blueprint
collaborative_workspaces_bp = Blueprint('collaborative_workspaces', __name__)

# Initialize service (will be configured in app.py)
workspace_service: SuperchargedCollaborativeWorkspacesV3 = None

def init_workspace_service(config: Dict[str, Any]):
    """Initialize the collaborative workspaces service"""
    global workspace_service
    workspace_service = SuperchargedCollaborativeWorkspacesV3(config)
    logger.info(" Collaborative Workspaces API initialized!")

@collaborative_workspaces_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        if workspace_service is None:
            return jsonify({
                "status": "error",
                "message": "Collaborative workspaces service not initialized"
            }), 503

        return jsonify({
            "status": "healthy",
            "service": "Supercharged Collaborative Workspaces V3.0",
            "timestamp": datetime.now().isoformat(),
            "express_mode_enabled": True,
            "agentic_control_enabled": True,
            "real_time_collaboration": True
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@collaborative_workspaces_bp.route('/sessions', methods=['GET', 'POST'])
def manage_sessions():
    """
    GET: List all active collaborative sessions
    POST: Create new collaborative session
    """
    try:
        if workspace_service is None:
            return jsonify({"error": "Service not initialized"}), 503

        if request.method == 'GET':
            # Get all active sessions
            sessions = asyncio.run(workspace_service.get_active_sessions())
            return jsonify(sessions)

        elif request.method == 'POST':
            # Create new session
            data = request.get_json()

            if not data or 'session_name' not in data:
                return jsonify({"error": "session_name is required"}), 400

            session_name = data['session_name']
            mode = data.get('mode', 'pair_programming')
            creator_id = data.get('creator_id', 'anonymous')
            participants = data.get('participants', [])
            agentic_control_level = data.get('agentic_control_level', 0.5)

            # Import enum for mode validation
            from services.supercharged_collaborative_workspaces_v3 import CollaborationMode

            try:
                collaboration_mode = CollaborationMode(mode)
            except ValueError:
                return jsonify({
                    "error": f"Invalid mode: {mode}. Valid options: {[m.value for m in CollaborationMode]}"
                }), 400

            result = asyncio.run(
                workspace_service.create_collaborative_session(
                    session_name=session_name,
                    mode=collaboration_mode,
                    creator_id=creator_id,
                    initial_participants=participants,
                    agentic_control_level=agentic_control_level
                )
            )

            return jsonify({
                "success": True,
                "session": result,
                "timestamp": datetime.now().isoformat()
            })

    except Exception as e:
        logger.error(f"Session management failed: {e}")
        return jsonify({"error": str(e)}), 500

@collaborative_workspaces_bp.route('/sessions/<session_id>/join', methods=['POST'])
def join_session(session_id: str):
    """
    🤝 JOIN COLLABORATIVE SESSION

    Expected payload:
    {
        "user_id": "string",
        "role": "developer|mentor|observer"
    }
    """
    try:
        if workspace_service is None:
            return jsonify({"error": "Service not initialized"}), 503

        data = request.get_json()

        if not data or 'user_id' not in data:
            return jsonify({"error": "user_id is required"}), 400

        user_id = data['user_id']
        role = data.get('role', 'developer')

        result = asyncio.run(
            workspace_service.join_collaborative_session(
                session_id=session_id,
                user_id=user_id,
                role=role
            )
        )

        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Session join failed: {e}")
        return jsonify({"error": str(e)}), 500

@collaborative_workspaces_bp.route('/sessions/<session_id>/message', methods=['POST'])
def send_message(session_id: str):
    """
    💬 SEND MESSAGE TO COLLABORATIVE SESSION

    Expected payload:
    {
        "user_id": "string",
        "message": {
            "type": "text|code|action",
            "content": "string",
            "metadata": {}
        }
    }
    """
    try:
        if workspace_service is None:
            return jsonify({"error": "Service not initialized"}), 503

        data = request.get_json()

        if not data or 'user_id' not in data or 'message' not in data:
            return jsonify({"error": "user_id and message are required"}), 400

        user_id = data['user_id']
        message = data['message']

        result = asyncio.run(
            workspace_service.process_collaboration_message(
                session_id=session_id,
                user_id=user_id,
                message=message
            )
        )

        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Message processing failed: {e}")
        return jsonify({"error": str(e)}), 500

@collaborative_workspaces_bp.route('/sessions/<session_id>/agentic-takeover', methods=['POST'])
def initiate_agentic_takeover(session_id: str):
    """
     INITIATE AGENTIC TAKEOVER MODE

    Expected payload:
    {
        "user_id": "string",
        "task_description": "string",
        "takeover_level": "collaborative|leadership|autonomous"
    }
    """
    try:
        if workspace_service is None:
            return jsonify({"error": "Service not initialized"}), 503

        data = request.get_json()

        if not data or 'user_id' not in data or 'task_description' not in data:
            return jsonify({"error": "user_id and task_description are required"}), 400

        user_id = data['user_id']
        task_description = data['task_description']
        takeover_level = data.get('takeover_level', 'collaborative')

        if takeover_level not in ['collaborative', 'leadership', 'autonomous']:
            return jsonify({
                "error": "Invalid takeover_level. Valid options: collaborative, leadership, autonomous"
            }), 400

        result = asyncio.run(
            workspace_service.initiate_agentic_takeover(
                session_id=session_id,
                user_id=user_id,
                task_description=task_description,
                takeover_level=takeover_level
            )
        )

        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Agentic takeover failed: {e}")
        return jsonify({"error": str(e)}), 500

@collaborative_workspaces_bp.route('/sessions/<session_id>/metrics', methods=['GET'])
def get_session_metrics(session_id: str):
    """ GET SESSION METRICS AND INSIGHTS"""
    try:
        if workspace_service is None:
            return jsonify({"error": "Service not initialized"}), 503

        metrics = asyncio.run(workspace_service.get_session_metrics(session_id))

        return jsonify({
            "success": True,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Session metrics retrieval failed: {e}")
        return jsonify({"error": str(e)}), 500

@collaborative_workspaces_bp.route('/modes', methods=['GET'])
def get_collaboration_modes():
    """📋 GET AVAILABLE COLLABORATION MODES"""
    try:
        from services.supercharged_collaborative_workspaces_v3 import CollaborationMode

        modes = []
        for mode in CollaborationMode:
            modes.append({
                "value": mode.value,
                "name": mode.name,
                "description": {
                    "pair_programming": "Real-time collaborative coding with AI assistance",
                    "code_review": "AI-enhanced code review and feedback sessions",
                    "brainstorming": "Creative problem-solving with AI insights",
                    "debugging": "Collaborative debugging with AI detective assistance",
                    "learning": "Educational sessions with AI tutoring",
                    "research": "Research sessions with AI-powered information gathering",
                    "design": "Design sessions with AI creative assistance",
                    "agentic_takeover": "Full AI control for autonomous task completion"
                }.get(mode.value, "Advanced collaboration mode")
            })

        return jsonify({
            "collaboration_modes": modes,
            "default_mode": "pair_programming"
        })

    except Exception as e:
        logger.error(f"Collaboration modes retrieval failed: {e}")
        return jsonify({"error": str(e)}), 500

@collaborative_workspaces_bp.route('/express-agents', methods=['GET'])
def get_express_agents():
    """ GET AVAILABLE EXPRESS AGENTS"""
    try:
        from services.supercharged_collaborative_workspaces_v3 import ExpressAgentType

        agents = []
        for agent_type in ExpressAgentType:
            agents.append({
                "type": agent_type.value,
                "name": agent_type.name,
                "description": {
                    "coding_pair": "Specialized coding pair programming assistant",
                    "debug_detective": "Expert debugging and error analysis agent",
                    "research_wizard": "Advanced research and information gathering agent",
                    "design_genius": "Creative design and UI/UX specialist agent",
                    "integration_master": "System integration and architecture expert"
                }.get(agent_type.value, "Specialized AI agent"),
                "capabilities": {
                    "coding_pair": ["code_generation", "refactoring", "optimization"],
                    "debug_detective": ["error_analysis", "root_cause_analysis", "testing"],
                    "research_wizard": ["information_gathering", "trend_analysis", "documentation"],
                    "design_genius": ["ui_ux", "architecture", "creative_solutions"],
                    "integration_master": ["system_integration", "api_design", "workflow_optimization"]
                }.get(agent_type.value, ["general_assistance"])
            })

        return jsonify({
            "express_agents": agents,
            "total_agents": len(agents)
        })

    except Exception as e:
        logger.error(f"Express agents retrieval failed: {e}")
        return jsonify({"error": str(e)}), 500

@collaborative_workspaces_bp.route('/test', methods=['POST'])
def test_collaborative_features():
    """
     TEST COLLABORATIVE WORKSPACE FEATURES

    Expected payload:
    {
        "test_scenario": "string",
        "mode": "string",
        "participants": ["user1", "user2"]
    }
    """
    try:
        if workspace_service is None:
            return jsonify({"error": "Service not initialized"}), 503

        data = request.get_json()
        test_scenario = data.get('test_scenario', 'basic_collaboration')
        mode = data.get('mode', 'pair_programming')
        participants = data.get('participants', ['test_user_1', 'test_user_2'])

        # Create test session
        from services.supercharged_collaborative_workspaces_v3 import CollaborationMode

        try:
            collaboration_mode = CollaborationMode(mode)
        except ValueError:
            collaboration_mode = CollaborationMode.PAIR_PROGRAMMING

        test_session = asyncio.run(
            workspace_service.create_collaborative_session(
                session_name=f"Test Session - {test_scenario}",
                mode=collaboration_mode,
                creator_id="test_system",
                initial_participants=[{"user_id": p, "role": "developer"} for p in participants],
                agentic_control_level=0.7
            )
        )

        # Simulate test interaction
        test_message = {
            "type": "test",
            "content": f"Testing {test_scenario} in {mode} mode",
            "metadata": {"test": True}
        }

        message_result = asyncio.run(
            workspace_service.process_collaboration_message(
                session_id=test_session["session_id"],
                user_id=participants[0],
                message=test_message
            )
        )

        return jsonify({
            "test_results": {
                "scenario": test_scenario,
                "session_created": test_session,
                "message_processed": message_result,
                "test_status": "completed"
            },
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Collaborative features test failed: {e}")
        return jsonify({"error": str(e)}), 500
