# Intelligent Execution Router API - E2B/Scrapybara routing with Mama Bear intelligence

from flask import Blueprint, request, jsonify
from typing import Dict, Any
import asyncio
import logging
from datetime import datetime

from services.intelligent_execution_router import get_intelligent_router
from services.enhanced_code_execution import mama_bear_code_executor
from services.enhanced_scrapybara_integration import enhanced_scrapybara_service

# Create blueprint for execution router API
execution_router_bp = Blueprint('execution_router', __name__, url_prefix='/api/execution')

logger = logging.getLogger(__name__)

@execution_router_bp.route('/analyze', methods=['POST'])
async def analyze_task():
    """
    🔍 Analyze task complexity and get routing recommendation
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['code', 'task_type']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Get Mama Bear's analysis
        intelligent_router = get_intelligent_router()
        analysis = await intelligent_router.analyze_task_complexity(
            task_description=f"{data['task_type']}: {data['code']}",
            code_snippets=[data['code']],
            user_context=data.get('user_preferences', {})
        )
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Task analysis failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@execution_router_bp.route('/route', methods=['POST'])
async def route_execution():
    """
    🚀 Route code execution to optimal platform (E2B or Scrapybara)
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['code', 'task_type', 'user_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Get routing decision from Mama Bear
        intelligent_router = get_intelligent_router()
        routing_decision = await intelligent_router.route_execution(
            task_description=f"{data['task_type']}: {data['code']}",
            code_snippets=[data['code']],
            user_id=data['user_id'],
            user_context=data.get('user_preferences', {})
        )
        
        # Execute based on routing decision
        if routing_decision['platform'] == 'e2b':
            result = await _execute_on_e2b(
                code=data['code'],
                user_id=data['user_id'],
                language=data.get('language', 'python'),
                timeout=data.get('timeout', 30)
            )
        else:  # scrapybara
            result = await _execute_on_scrapybara(
                code=data['code'],
                user_id=data['user_id'],
                task_context=data.get('task_context', {}),
                timeout=data.get('timeout', 300)
            )
        
        # Log execution metrics for learning
        intelligent_router = get_intelligent_router()
        await intelligent_router.log_execution_result(
            routing_decision=routing_decision,
            execution_result=result,
            user_id=data['user_id']
        )
        
        return jsonify({
            'success': True,
            'routing_decision': routing_decision,
            'execution_result': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Execution routing failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@execution_router_bp.route('/e2b/execute', methods=['POST'])
async def execute_on_e2b():
    """
    ⚡ Direct E2B execution for quick validation tasks
    """
    try:
        data = request.get_json()
        
        result = await _execute_on_e2b(
            code=data['code'],
            user_id=data['user_id'],
            language=data.get('language', 'python'),
            timeout=data.get('timeout', 30)
        )
        
        return jsonify({
            'success': True,
            'result': result,
            'platform': 'e2b',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"E2B execution failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@execution_router_bp.route('/scrapybara/execute', methods=['POST'])
async def execute_on_scrapybara():
    """
    🔧 Direct Scrapybara execution for complex VM tasks
    """
    try:
        data = request.get_json()
        
        result = await _execute_on_scrapybara(
            code=data['code'],
            user_id=data['user_id'],
            task_context=data.get('task_context', {}),
            timeout=data.get('timeout', 300)
        )
        
        return jsonify({
            'success': True,
            'result': result,
            'platform': 'scrapybara',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Scrapybara execution failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@execution_router_bp.route('/sessions', methods=['GET'])
async def get_active_sessions():
    """
    📊 Get information about active execution sessions
    """
    try:
        user_id = request.args.get('user_id')
        
        sessions = {
            'e2b': {},
            'scrapybara': {}
        }
        
        # Get E2B session info
        if user_id:
            sessions['e2b'] = await mama_bear_code_executor.get_session_info(user_id)
        
        # Get Scrapybara session info
        sessions['scrapybara'] = await enhanced_scrapybara_service.get_session_status()
        
        return jsonify({
            'success': True,
            'sessions': sessions,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get session info: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@execution_router_bp.route('/metrics', methods=['GET'])
async def get_execution_metrics():
    """
    📈 Get execution metrics and cost analytics
    """
    try:
        user_id = request.args.get('user_id')
        time_range = request.args.get('time_range', '24h')
        
        intelligent_router = get_intelligent_router()
        metrics = await intelligent_router.get_execution_metrics(
            user_id=user_id,
            time_range=time_range
        )
        
        return jsonify({
            'success': True,
            'metrics': metrics,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get metrics: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@execution_router_bp.route('/cleanup', methods=['POST'])
async def cleanup_sessions():
    """
    🧹 Clean up execution sessions
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        platform = data.get('platform', 'all')
        
        results = {}
        
        if platform in ['all', 'e2b']:
            await mama_bear_code_executor.cleanup_session(user_id)
            results['e2b'] = 'cleaned'
        
        if platform in ['all', 'scrapybara']:
            await enhanced_scrapybara_service.cleanup_session()
            results['scrapybara'] = 'cleaned'
        
        return jsonify({
            'success': True,
            'cleanup_results': results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Session cleanup failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Helper functions for execution routing
async def _execute_on_e2b(code: str, user_id: str, language: str = 'python', timeout: int = 30):
    """Execute code on E2B platform"""
    return await mama_bear_code_executor.execute_code_safely(
        code=code,
        user_id=user_id,
        language=language,
        timeout=timeout
    )

async def _execute_on_scrapybara(code: str, user_id: str, task_context: Dict[str, Any], timeout: int = 300):
    """Execute code on Scrapybara platform"""
    return await enhanced_scrapybara_service.execute_complex_task(
        task_description=f"Execute code: {code}",
        context=task_context,
        timeout=timeout
    )
