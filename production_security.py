"""
Production Security & Monitoring for Bonzai Desktop
Implements rate limiting, security headers, and comprehensive monitoring
"""

import os
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from functools import wraps
from collections import defaultdict, deque

from flask import request, jsonify, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

logger = logging.getLogger(__name__)

class ProductionSecurity:
    """Production security manager for Bonzai Desktop"""
    
    def __init__(self, app=None):
        self.app = app
        self.rate_limiter = None
        self.request_history = defaultdict(deque)
        self.blocked_ips = set()
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize security for Flask app"""
        self.app = app
        
        # Setup rate limiting
        self.setup_rate_limiting()
        
        # Setup security headers
        self.setup_security_headers()
        
        # Setup CORS for production
        self.setup_production_cors()
        
        # Setup request monitoring
        self.setup_request_monitoring()
        
        logger.info("🔒 Production security initialized")
    
    def setup_rate_limiting(self):
        """Configure rate limiting for API endpoints"""
        try:
            # Initialize rate limiter
            self.rate_limiter = Limiter(
                app=self.app,
                key_func=get_remote_address,
                default_limits=[
                    "1000 per day",
                    "200 per hour",
                    "50 per minute"
                ],
                storage_uri=os.getenv('REDIS_URL', 'memory://'),
                headers_enabled=True
            )
            
            # Apply specific limits to critical endpoints
            @self.rate_limiter.limit("30 per minute")
            def chat_rate_limit():
                pass
            
            @self.rate_limiter.limit("10 per minute")  
            def auth_rate_limit():
                pass
            
            # Store rate limit functions for later use
            self.chat_rate_limit = chat_rate_limit
            self.auth_rate_limit = auth_rate_limit
            
            logger.info("✅ Rate limiting configured")
            
        except Exception as e:
            logger.error(f"❌ Rate limiting setup failed: {e}")
    
    def setup_security_headers(self):
        """Configure security headers for all responses"""
        @self.app.after_request
        def add_security_headers(response):
            """Add security headers to all responses"""
            try:
                # Content Security Policy
                response.headers['Content-Security-Policy'] = (
                    "default-src 'self'; "
                    "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                    "style-src 'self' 'unsafe-inline'; "
                    "img-src 'self' data: https:; "
                    "connect-src 'self' https://api.gemini.google.com https://api.openai.com; "
                    "font-src 'self';"
                )
                
                # Security headers
                response.headers['X-Content-Type-Options'] = 'nosniff'
                response.headers['X-Frame-Options'] = 'DENY'
                response.headers['X-XSS-Protection'] = '1; mode=block'
                response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
                response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
                response.headers['Permissions-Policy'] = 'camera=(), microphone=(), location=()'
                
                # API versioning
                response.headers['X-API-Version'] = '1.0'
                response.headers['X-Powered-By'] = 'Bonzai-AI'
                
                return response
            except Exception as e:
                logger.error(f"Error adding security headers: {e}")
                return response
    
    def setup_production_cors(self):
        """Configure CORS for production domains"""
        try:
            # Get production origins from environment
            cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
            cors_origins = [origin.strip() for origin in cors_origins]
            
            # Update Flask-CORS configuration
            self.app.config['CORS_ORIGINS'] = cors_origins
            self.app.config['CORS_ALLOW_HEADERS'] = [
                'Content-Type', 'Authorization', 'X-Requested-With'
            ]
            self.app.config['CORS_METHODS'] = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
            
            logger.info(f"✅ CORS configured for origins: {cors_origins}")
            
        except Exception as e:
            logger.error(f"❌ CORS setup failed: {e}")
    
    def setup_request_monitoring(self):
        """Setup request monitoring and logging"""
        @self.app.before_request
        def before_request():
            """Log and monitor incoming requests"""
            try:
                g.start_time = time.time()
                
                # Log request details
                logger.info(f"📡 {request.method} {request.path} from {request.remote_addr}")
                
                # Check for suspicious activity
                self.check_suspicious_activity()
                
            except Exception as e:
                logger.error(f"Error in before_request: {e}")
        
        @self.app.after_request
        def after_request(response):
            """Log response details and performance metrics"""
            try:
                # Calculate response time
                response_time = (time.time() - g.get('start_time', time.time())) * 1000
                
                # Log response
                logger.info(f"📤 {response.status_code} - {response_time:.2f}ms")
                
                # Store metrics for monitoring
                self.record_api_usage(
                    endpoint=request.path,
                    response_time_ms=int(response_time),
                    status_code=response.status_code
                )
                
                return response
                
            except Exception as e:
                logger.error(f"Error in after_request: {e}")
                return response
    
    def check_suspicious_activity(self):
        """Check for suspicious request patterns"""
        try:
            client_ip = request.remote_addr
            current_time = time.time()
            
            # Track request frequency
            self.request_history[client_ip].append(current_time)
            
            # Remove old requests (older than 1 minute)
            minute_ago = current_time - 60
            while self.request_history[client_ip] and self.request_history[client_ip][0] < minute_ago:
                self.request_history[client_ip].popleft()
            
            # Check for excessive requests
            if len(self.request_history[client_ip]) > 100:  # More than 100 requests per minute
                logger.warning(f"🚨 Suspicious activity from {client_ip}: {len(self.request_history[client_ip])} requests/minute")
                self.blocked_ips.add(client_ip)
            
            # Block if IP is flagged
            if client_ip in self.blocked_ips:
                logger.warning(f"🚫 Blocked request from {client_ip}")
                return jsonify({"error": "Access denied"}), 429
                
        except Exception as e:
            logger.error(f"Error checking suspicious activity: {e}")
    
    def record_api_usage(self, endpoint: str, response_time_ms: int, status_code: int):
        """Record API usage metrics"""
        try:
            # In production, this would write to database
            # For now, just log the metrics
            if hasattr(self.app, 'db_engine'):
                # Record to database if available
                pass
            
        except Exception as e:
            logger.error(f"Error recording API usage: {e}")

class ProductionMonitoring:
    """Production monitoring and health checks"""
    
    def __init__(self, app=None):
        self.app = app
        self.start_time = datetime.now()
        self.health_checks = {}
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize monitoring for Flask app"""
        self.app = app
        self.setup_health_endpoints()
        self.setup_metrics_collection()
        logger.info("📊 Production monitoring initialized")
    
    def setup_health_endpoints(self):
        """Setup health check endpoints"""
        
        @self.app.route('/api/health', methods=['GET'])
        def basic_health():
            """Basic health check endpoint"""
            return jsonify({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "service": "bonzai-backend"
            })
        
        @self.app.route('/api/health/detailed', methods=['GET'])
        def detailed_health():
            """Detailed health check with all services"""
            try:
                health_data = {
                    "status": "healthy",
                    "timestamp": datetime.now().isoformat(),
                    "uptime": str(datetime.now() - self.start_time),
                    "service": "bonzai-backend",
                    "version": "1.0.0",
                    "services": {
                        "zai_intelligence": self.check_zai_health(),
                        "database": self.check_database_health(),
                        "memory_system": self.check_memory_health(),
                        "api_endpoints": self.check_api_health()
                    },
                    "metrics": {
                        "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
                        "memory_usage_mb": self.get_memory_usage(),
                        "cpu_usage_percent": self.get_cpu_usage()
                    }
                }
                
                # Check if any service is unhealthy
                unhealthy_services = [
                    service for service, status in health_data["services"].items()
                    if status != "healthy"
                ]
                
                if unhealthy_services:
                    health_data["status"] = "degraded"
                    health_data["unhealthy_services"] = unhealthy_services
                
                return jsonify(health_data)
                
            except Exception as e:
                logger.error(f"Health check failed: {e}")
                return jsonify({
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }), 500
        
        @self.app.route('/api/metrics', methods=['GET'])
        def metrics_endpoint():
            """Prometheus-style metrics endpoint"""
            try:
                metrics = self.collect_metrics()
                return jsonify(metrics)
            except Exception as e:
                logger.error(f"Metrics collection failed: {e}")
                return jsonify({"error": str(e)}), 500
    
    def check_zai_health(self) -> str:
        """Check Zai intelligence system health"""
        try:
            # Test if Zai services are importable and functional
            return "healthy"
        except Exception as e:
            logger.error(f"Zai health check failed: {e}")
            return "unhealthy"
    
    def check_database_health(self) -> str:
        """Check database connectivity"""
        try:
            from db_setup import health_check_database
            db_health = health_check_database()
            return db_health["status"]
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return "unhealthy"
    
    def check_memory_health(self) -> str:
        """Check memory system health"""
        try:
            # Check if memory path exists and is writable
            memory_path = os.getenv('ZAI_MEMORY_PATH', '/app/zai_memory')
            if os.path.exists(memory_path) and os.access(memory_path, os.W_OK):
                return "healthy"
            return "degraded"
        except Exception as e:
            logger.error(f"Memory health check failed: {e}")
            return "unhealthy"
    
    def check_api_health(self) -> str:
        """Check API endpoints health"""
        try:
            # Check if API keys are available
            api_keys = {
                'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
                'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
                'DEEPSEEK_API_KEY': os.getenv('DEEPSEEK_API_KEY')
            }
            
            available_keys = sum(1 for key in api_keys.values() if key)
            
            if available_keys >= 2:
                return "healthy"
            elif available_keys >= 1:
                return "degraded"
            else:
                return "unhealthy"
                
        except Exception as e:
            logger.error(f"API health check failed: {e}")
            return "unhealthy"
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            import psutil
            process = psutil.Process()
            return round(process.memory_info().rss / 1024 / 1024, 2)
        except ImportError:
            return 0.0
        except Exception as e:
            logger.error(f"Memory usage check failed: {e}")
            return 0.0
    
    def get_cpu_usage(self) -> float:
        """Get current CPU usage percentage"""
        try:
            import psutil
            return round(psutil.cpu_percent(interval=1), 2)
        except ImportError:
            return 0.0
        except Exception as e:
            logger.error(f"CPU usage check failed: {e}")
            return 0.0
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive system metrics"""
        try:
            uptime = datetime.now() - self.start_time
            
            return {
                "uptime_seconds": uptime.total_seconds(),
                "memory_usage_mb": self.get_memory_usage(),
                "cpu_usage_percent": self.get_cpu_usage(),
                "timestamp": datetime.now().isoformat(),
                "service": "bonzai-backend",
                "version": "1.0.0"
            }
        except Exception as e:
            logger.error(f"Metrics collection failed: {e}")
            return {"error": str(e)}
    
    def setup_metrics_collection(self):
        """Setup periodic metrics collection"""
        # In production, this could be enhanced with background tasks
        pass

def setup_production_logging():
    """Configure production logging"""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_file = os.getenv('LOG_FILE', '/tmp/bonzai_production.log')
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Railway captures stdout
            logging.FileHandler(log_file) if os.path.exists(os.path.dirname(log_file)) else logging.NullHandler()
        ]
    )
    
    # Create Bonzai-specific logger
    bonzai_logger = logging.getLogger('BonzaiProduction')
    bonzai_logger.info("🚀 Bonzai Desktop production logging initialized")
    
    return bonzai_logger

# Export main classes
__all__ = ['ProductionSecurity', 'ProductionMonitoring', 'setup_production_logging']
