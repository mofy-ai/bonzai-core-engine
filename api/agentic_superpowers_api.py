# backend/api/agentic_superpowers_api.py
"""
 MAMA BEAR AGENTIC SUPERPOWERS API - PRODUCTION READY
💥 Express Mode + Autonomous AI Agent Endpoints
"""

from flask import Blueprint, request, jsonify
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

from services.zai_agentic_superpowers_v3 import ZaiAgenticSuperpowersV3

logger = logging.getLogger(__name__)

# Create Blueprint
agentic_superpowers_bp = Blueprint('agentic_superpowers', __name__)

# Initialize service (will be configured in app.py)
agentic_service: ZaiAgenticSuperpowersV3 = None

def init_agentic_service(config: Dict[str, Any]):
    """Initialize the agentic superpowers service"""
    global agentic_service
    agentic_service = ZaiAgenticSuperpowersV3(config)
    logger.info(" Agentic Superpowers API initialized!")

@agentic_superpowers_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        if agentic_service is None:
            return jsonify({
                "status": "error",
                "message": "Agentic service not initialized"
            }), 503

        return jsonify({
            "status": "healthy",
            "service": "Mama Bear Agentic Superpowers V3.0",
            "timestamp": datetime.now().isoformat(),
            "express_mode_enabled": True,
            "autonomous_capabilities": True
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@agentic_superpowers_bp.route('/status', methods=['GET'])
def get_status():
    """Get detailed service status and metrics"""
    try:
        if agentic_service is None:
            return jsonify({"error": "Service not initialized"}), 503

        status = asyncio.run(agentic_service.get_status())
        return jsonify(status)
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return jsonify({"error": str(e)}), 500

@agentic_superpowers_bp.route('/interact', methods=['POST'])
def process_interaction():
    """
    🧠 PROCESS USER INTERACTION WITH FULL AGENTIC CAPABILITIES

    Expected payload:
    {
        "user_input": "string",
        "user_id": "string",
        "context": {},
        "allow_autonomous_actions": true
    }
    """
    try:
        if agentic_service is None:
            return jsonify({"error": "Service not initialized"}), 503

        data = request.get_json()

        if not data or 'user_input' not in data:
            return jsonify({"error": "user_input is required"}), 400

        user_input = data['user_input']
        user_id = data.get('user_id', 'anonymous')
        context = data.get('context', {})
        allow_autonomous = data.get('allow_autonomous_actions', True)

        # Process interaction asynchronously
        result = asyncio.run(
            agentic_service.process_user_interaction(
                user_input=user_input,
                user_id=user_id,
                context=context,
                allow_autonomous_actions=allow_autonomous
            )
        )

        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Interaction processing failed: {e}")
        return jsonify({"error": str(e)}), 500

@agentic_superpowers_bp.route('/capability-level', methods=['POST'])
def set_capability_level():
    """
    ⚙️ SET AGENTIC CAPABILITY LEVEL

    Expected payload:
    {
        "level": "OBSERVER|ASSISTANT|COLLABORATOR|LEADER|AUTONOMOUS",
        "user_id": "string"
    }
    """
    try:
        if agentic_service is None:
            return jsonify({"error": "Service not initialized"}), 503

        data = request.get_json()

        if not data or 'level' not in data:
            return jsonify({"error": "level is required"}), 400

        level = data['level']
        user_id = data.get('user_id', 'anonymous')

        # Update capability level (simplified for this example)
        from services.zai_agentic_superpowers_v3 import AgenticCapabilityLevel

        try:
            new_level = AgenticCapabilityLevel[level]
            agentic_service.capability_level = new_level

            return jsonify({
                "success": True,
                "capability_level": new_level.name,
                "description": {
                    "OBSERVER": "Just watches and suggests",
                    "ASSISTANT": "Actively helps but asks permission",
                    "COLLABORATOR": "Works alongside user as equal partner",
                    "LEADER": "Takes initiative and leads tasks",
                    "AUTONOMOUS": "Fully autonomous operation"
                }.get(level, "Unknown level"),
                "timestamp": datetime.now().isoformat()
            })

        except KeyError:
            return jsonify({
                "error": f"Invalid capability level: {level}. Valid options: OBSERVER, ASSISTANT, COLLABORATOR, LEADER, AUTONOMOUS"
            }), 400

    except Exception as e:
        logger.error(f"Capability level setting failed: {e}")
        return jsonify({"error": str(e)}), 500

@agentic_superpowers_bp.route('/personality', methods=['GET', 'POST'])
def manage_personality():
    """
     MANAGE MAMA BEAR'S AGENTIC PERSONALITY
    """
    try:
        if agentic_service is None:
            return jsonify({"error": "Service not initialized"}), 503

        if request.method == 'GET':
            # Get current personality
            personality = agentic_service.personality
            return jsonify({
                "personality": {
                    "caring_level": personality.caring_level,
                    "proactivity": personality.proactivity,
                    "autonomy_preference": personality.autonomy_preference,
                    "learning_eagerness": personality.learning_eagerness,
                    "risk_tolerance": personality.risk_tolerance,
                    "collaboration_style": personality.collaboration_style,
                    "communication_tone": personality.communication_tone,
                    "initiative_taking": personality.initiative_taking,
                    "user_trust_level": personality.user_trust_level
                }
            })

        elif request.method == 'POST':
            # Update personality
            data = request.get_json()
            personality = agentic_service.personality

            # Update provided personality traits
            for trait, value in data.items():
                if hasattr(personality, trait):
                    setattr(personality, trait, value)

            return jsonify({
                "success": True,
                "message": "Personality updated successfully",
                "updated_personality": {
                    "caring_level": personality.caring_level,
                    "proactivity": personality.proactivity,
                    "autonomy_preference": personality.autonomy_preference,
                    "user_trust_level": personality.user_trust_level
                }
            })

    except Exception as e:
        logger.error(f"Personality management failed: {e}")
        return jsonify({"error": str(e)}), 500

@agentic_superpowers_bp.route('/metrics', methods=['GET'])
def get_metrics():
    """ GET AGENTIC PERFORMANCE METRICS"""
    try:
        if agentic_service is None:
            return jsonify({"error": "Service not initialized"}), 503

        metrics = agentic_service.metrics

        return jsonify({
            "metrics": metrics,
            "performance_summary": {
                "total_decisions": metrics["decisions_made"],
                "success_rate": (
                    metrics["successful_outcomes"] / max(metrics["decisions_made"], 1) * 100
                ),
                "avg_response_time_ms": metrics["avg_response_time"],
                "express_mode_usage": metrics["express_mode_calls"],
                "learning_events": metrics["learning_events"],
                "user_satisfaction": metrics["user_satisfaction"]
            },
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Metrics retrieval failed: {e}")
        return jsonify({"error": str(e)}), 500

@agentic_superpowers_bp.route('/memory', methods=['GET'])
def get_memory_state():
    """🧠 GET CURRENT MEMORY STATE"""
    try:
        if agentic_service is None:
            return jsonify({"error": "Service not initialized"}), 503

        return jsonify({
            "working_memory_size": len(agentic_service.working_memory),
            "working_memory_recent": list(agentic_service.working_memory)[-5:],
            "long_term_memory_keys": list(agentic_service.long_term_memory.keys()),
            "decision_history_count": len(agentic_service.decision_history),
            "recent_decisions": agentic_service.decision_history[-3:] if agentic_service.decision_history else [],
            "predictive_patterns_count": len(agentic_service.predictive_patterns),
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Memory state retrieval failed: {e}")
        return jsonify({"error": str(e)}), 500

@agentic_superpowers_bp.route('/test', methods=['POST'])
def test_agentic_capabilities():
    """
     TEST AGENTIC CAPABILITIES

    Expected payload:
    {
        "test_scenario": "string",
        "capability_level": "string",
        "user_id": "string"
    }
    """
    try:
        if agentic_service is None:
            return jsonify({"error": "Service not initialized"}), 503

        data = request.get_json()
        test_scenario = data.get('test_scenario', 'general_interaction')
        capability_level = data.get('capability_level', 'COLLABORATOR')
        user_id = data.get('user_id', 'test_user')

        # Run test interaction
        test_input = f"Test scenario: {test_scenario}. Please demonstrate your agentic capabilities at {capability_level} level."

        result = asyncio.run(
            agentic_service.process_user_interaction(
                user_input=test_input,
                user_id=user_id,
                context={"test_mode": True, "scenario": test_scenario},
                allow_autonomous_actions=True
            )
        )

        return jsonify({
            "test_results": {
                "scenario": test_scenario,
                "capability_level": capability_level,
                "response": result["response"],
                "agentic_metadata": result["agentic_metadata"],
                "performance": {
                    "processing_time_ms": result["agentic_metadata"]["processing_time_ms"],
                    "confidence": result["agentic_metadata"]["confidence"],
                    "autonomous_actions": len(result["agentic_metadata"].get("autonomous_actions_taken", []))
                }
            },
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Agentic capabilities test failed: {e}")
        return jsonify({"error": str(e)}), 500
