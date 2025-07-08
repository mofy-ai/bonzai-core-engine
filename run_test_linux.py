#!/usr/bin/env python3
"""
Run comprehensive test using Linux Python with Windows venv packages
"""
import os
import sys

# Add Windows venv packages to Python path
venv_packages = "/mnt/c/Bonzai-Desktop/venv/lib/python3.12/site-packages"
if venv_packages not in sys.path:
    sys.path.insert(0, venv_packages)

print(f"🔥 Added venv packages to path: {venv_packages}")

# Now run the comprehensive test
if __name__ == "__main__":
    import asyncio
    import comprehensive_backend_test
    success = asyncio.run(comprehensive_backend_test.main())
    sys.exit(0 if success else 1)