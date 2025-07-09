#!/usr/bin/env python3
"""
Run the comprehensive test using the correct venv Python
"""
import subprocess
import sys
import os

# Path to the venv Python
venv_python = r"C:\Bonzai-Desktop\venv\Scripts\python.exe"
test_script = r"C:\Bonzai-Desktop\zai-backend\comprehensive_backend_test.py"

# Set environment for UTF-8
env = os.environ.copy()
env['PYTHONIOENCODING'] = 'utf-8'

print(" RUNNING COMPREHENSIVE TEST WITH VENV PYTHON...")
print(f"Using Python: {venv_python}")
print(f"Test script: {test_script}")
print()

# Run the test
try:
    result = subprocess.run([venv_python, test_script], 
                          env=env, 
                          capture_output=False, 
                          text=True,
                          cwd=r"C:\Bonzai-Desktop\zai-backend")
    sys.exit(result.returncode)
except Exception as e:
    print(f"Error running test: {e}")
    sys.exit(1)