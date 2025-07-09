#!/usr/bin/env python3
"""
Quick Backend Starter - Uses ROOT .env file
"""
import os
import sys
from pathlib import Path

# FORCE loading from ROOT .env file
root_dir = Path(__file__).parent.parent  # Go up to C:\Bonzai-Desktop
root_env = root_dir / '.env'

print(f" Loading environment from: {root_env}")

# Load the ROOT .env file
if root_env.exists():
    from dotenv import load_dotenv
    load_dotenv(root_env, override=True)
    print(" Loaded ROOT .env file!")
    
    # Show what we loaded
    mem0_key = os.getenv('MEM0_API_KEY')
    if mem0_key and not mem0_key.startswith('your_'):
        print(f" MEM0_API_KEY: Loaded (starts with {mem0_key[:10]}...)")
    else:
        print(" MEM0_API_KEY: Not found or invalid")
else:
    print(f" ROOT .env not found at {root_env}")
    sys.exit(1)

# Now start the backend
print("\n Starting Bonzai Backend with ROOT environment...")
os.chdir(Path(__file__).parent)

# Import and run app
try:
    from app import app, socketio
    print(" Backend modules loaded!")
    
    # Start the server
    print(f"\n Starting server on http://localhost:5001")
    print("Press Ctrl+C to stop\n")
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=5001,
        debug=False,
        allow_unsafe_werkzeug=True
    )
except Exception as e:
    print(f" Error starting backend: {e}")
