#!/usr/bin/env python3
"""
Run comprehensive test using the new backend venv
"""
import subprocess
import sys
import os

backend_dir = "/mnt/c/Bonzai-Desktop/zai-backend"
venv_python = os.path.join(backend_dir, "backend_venv", "bin", "python")
test_script = os.path.join(backend_dir, "comprehensive_backend_test.py")

print(" RUNNING COMPREHENSIVE TEST WITH BACKEND VENV...")
print(f"Using Python: {venv_python}")
print(f"Test script: {test_script}")
print()

# Run the test
try:
    result = subprocess.run([venv_python, test_script], 
                          capture_output=False, 
                          text=True,
                          cwd=backend_dir)
    sys.exit(result.returncode)
except Exception as e:
    print(f"Error running test: {e}")
    sys.exit(1)