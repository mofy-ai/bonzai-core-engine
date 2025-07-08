"""
🎯 ZAI Backend - Main Entry Point
Entry point for running the ZAI Backend service
"""

from app import app, socketio
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    host = '0.0.0.0'
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🧠 Starting ZAI Backend on port {port}")
    print(f"🌸 ZAI Intelligence System Online!")
    
    socketio.run(
        app,
        host=host,
        port=port,
        debug=debug,
        allow_unsafe_werkzeug=True
    )
