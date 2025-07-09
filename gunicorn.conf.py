# Gunicorn configuration for Railway deployment
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
backlog = 2048

# Worker processes
workers = 1  # Start with 1 worker for Railway
worker_class = "sync"
worker_connections = 1000
timeout = 60
keepalive = 2

# Restart workers
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Process naming
proc_name = "bonzai-railway"

# Application
module = "app_railway:app"