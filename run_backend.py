#!/usr/bin/env python3
"""
Backend startup script with proper UTF-8 encoding configuration
Ensures clean output on Windows systems
"""

import os
import sys
import io

# Set UTF-8 encoding for Windows console (FIXED: removed buffer wrapping for MCP compatibility)
if sys.platform == 'win32':
    # Set console code page to UTF-8
    os.system('chcp 65001 > nul')
    
    # Set Python environment to use UTF-8 (safer approach)
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Note: Removed sys.stdout/stderr buffer wrapping to prevent MCP STDIO conflicts

# Import and run the app
if __name__ == '__main__':
    # Set Flask environment
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'development')
    
    # Import app after encoding is set
    from app import app, socketio
    
    # Get port from environment or default
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'true').lower() == 'true'
    
    print(f"\n[INFO] Starting backend on port {port}")
    print(f"[INFO] Debug mode: {debug}")
    print(f"[INFO] UTF-8 encoding enabled\n")
    
    # Run with socketio
    socketio.run(
        app,
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=debug
    )