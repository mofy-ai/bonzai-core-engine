# This file makes the 'backend' directory a Python package.

# Ensure proper imports when run as module
import sys
import os

# Add current directory to path for config imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)