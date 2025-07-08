#!/usr/bin/env python3
"""
FAMILY INTEGRATION TEST - IMPROVED VERSION
Tests all backend services for DXT extension readiness
Handles missing configurations gracefully
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("🎯 BONZAI FAMILY INTEGRATION TEST")
print("=" * 50)
print(f"Test Started: {datetime.now()}")
print("=" * 50)

# Check Python version
print(f"\n📌 Python Version: {sys.version}")

# Test results tracking
test_results = {
    "timestamp": str(datetime.now()),
    "environment": {},
    "services": {},
    "summary": {"passed": 0, "failed": 0, "warnings": 0}
}

def check_env_vars():
    """Check critical environment variables"""
    print("\n🔐 Checking Environment Variables...")
    
    required_vars = {
        "GEMINI_API_KEY": "Gemini/Vertex AI access",
        "MEM0_API_KEY": "Memory system",
        "PORT": "Backend service port"
    }
    
    optional_vars = {
        "DEEPSEEK_API_KEY": "Cost optimization",
        "OPENAI_API_KEY": "OpenAI compatibility",
        "SCRAPYBARA_API_KEY": "Web scraping",
        "E2B_API_KEY": "Code execution"
    }
    
    all_good = True
    
    # Check required vars
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value != f"your_{var.lower()}_here":
            print(f"   ✅ {var}: Set ({description})")
            test_results["environment"][var] = "✅ Set"
        else:
            print(f"   ❌ {var}: Missing! ({description})")
            test_results["environment"][var] = "❌ Missing"
            all_good = False
            test_results["summary"]["failed"] += 1
    
    # Check optional vars
    print("\n   Optional services:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value and value != f"your_{var.lower()}_here":
            print(f"   ✅ {var}: Set ({description})")
            test_results["environment"][var] = "✅ Set"
        else:
            print(f"   ⚠️  {var}: Not configured ({description})")
            test_results["environment"][var] = "⚠️ Optional"
            test_results["summary"]["warnings"] += 1
    
    return all_good

def test_python_imports():
    """Test if required Python packages are installed"""
    print("\n📦 Testing Python Dependencies...")
    
    required_packages = [
        ("flask", "Web framework"),
        ("flask_cors", "CORS support"),
        ("google.generativeai", "Gemini AI"),
        ("mem0", "Memory system"),
    ]
    
    optional_packages = [
        ("openai", "OpenAI compatibility"),
        ("deepseek", "Cost optimization"),
        ("websockets", "Real-time communication"),
    ]
    
    all_good = True
    
    # Test required packages
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}: Installed ({description})")
            test_results["services"][f"package_{package}"] = "✅ Installed"
            test_results["summary"]["passed"] += 1
        except ImportError:
            print(f"   ❌ {package}: Not installed! ({description})")
            test_results["services"][f"package_{package}"] = "❌ Missing"
            test_results["summary"]["failed"] += 1
            all_good = False
    
    # Test optional packages
    print("\n   Optional packages:")
    for package, description in optional_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}: Installed ({description})")
            test_results["services"][f"package_{package}"] = "✅ Installed"
        except ImportError:
            print(f"   ⚠️  {package}: Not installed ({description})")
            test_results["services"][f"package_{package}"] = "⚠️ Optional"
            test_results["summary"]["warnings"] += 1
    
    return all_good

def test_services():
    """Test individual services"""
    print("\n🧠 Testing Backend Services...")
    
    services_to_test = [
        {
            "name": "ZAI Orchestration",
            "module": "services.zai_orchestration",
            "class": "ZAIOrchestration",
            "critical": True
        },
        {
            "name": "Model Manager",
            "module": "services.zai_model_manager",
            "class": "ZAIModelManager",
            "critical": True
        },
        {
            "name": "Memory System",
            "module": "services.zai_memory_system",
            "class": "ZAIMemorySystem",
            "critical": True
        },
        {
            "name": "Specialized Variants",
            "module": "services.zai_specialized_variants",
            "class": "ZAISpecializedVariants",
            "critical": True
        },
        {
            "name": "Express Vertex",
            "module": "services.express_mode_vertex_integration",
            "class": "ExpressModeVertexIntegration",
            "critical": False
        },
        {
            "name": "WebSocket Coordinator",
            "module": "services.bonzai_websocket_coordinator",
            "class": "BonzaiWebSocketCoordinator",
            "critical": False
        }
    ]
    
    for service in services_to_test:
        print(f"\n   Testing {service['name']}...")
        try:
            # Try to import the module
            module = __import__(service['module'], fromlist=[service['class']])
            print(f"   ✅ {service['name']}: Module loaded")
            
            # Try to get the class
            if hasattr(module, service['class']):
                print(f"   ✅ {service['name']}: Class found")
                test_results["services"][service['name']] = "✅ Ready"
                test_results["summary"]["passed"] += 1
            else:
                print(f"   ⚠️  {service['name']}: Class not found")
                test_results["services"][service['name']] = "⚠️ Partial"
                if service['critical']:
                    test_results["summary"]["failed"] += 1
                else:
                    test_results["summary"]["warnings"] += 1
                    
        except Exception as e:
            error_msg = str(e)
            if "No module named" in error_msg:
                print(f"   ❌ {service['name']}: Module not found")
            else:
                print(f"   ❌ {service['name']}: {error_msg[:50]}...")
            
            test_results["services"][service['name']] = f"❌ Error"
            if service['critical']:
                test_results["summary"]["failed"] += 1
            else:
                test_results["summary"]["warnings"] += 1

def test_ports():
    """Check if required ports are available"""
    print("\n🔌 Testing Port Availability...")
    
    import socket
    
    ports_to_check = [
        (5000, "Main Backend API"),
        (5001, "Alternative Backend Port"),
        (8765, "WebSocket Bridge"),
        (8080, "OpenAI Proxy")
    ]
    
    for port, description in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            print(f"   ⚠️  Port {port}: In use ({description})")
            test_results["services"][f"port_{port}"] = "⚠️ In use"
        else:
            print(f"   ✅ Port {port}: Available ({description})")
            test_results["services"][f"port_{port}"] = "✅ Available"

def generate_fix_script():
    """Generate a script to fix common issues"""
    print("\n📝 Generating fix script...")
    
    fix_script = """#!/bin/bash
# Auto-generated fix script for Bonzai Backend

echo "🔧 BONZAI BACKEND FIX SCRIPT"
echo "============================"

# Install missing Python packages
echo "📦 Installing required packages..."
pip install flask flask-cors google-generativeai mem0 python-dotenv

# Install optional packages
echo "📦 Installing optional packages..."
pip install openai websockets requests

# Create required directories
echo "📁 Creating required directories..."
mkdir -p logs
mkdir -p zai_memory
mkdir -p credentials

# Set up environment file if missing
if [ ! -f .env ]; then
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys!"
fi

echo "✅ Fix script complete!"
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: python app.py"
"""
    
    with open('fix_backend.sh', 'w') as f:
        f.write(fix_script)
    
    if os.name != 'nt':  # Unix-like systems
        os.chmod('fix_backend.sh', 0o755)
    
    print("   ✅ Created fix_backend.sh")

def main():
    """Run all tests"""
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    print(f"\n📂 Working directory: {os.getcwd()}")
    
    # Run tests
    env_ok = check_env_vars()
    imports_ok = test_python_imports()
    test_services()
    test_ports()
    
    # Generate fix script
    generate_fix_script()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"✅ Passed: {test_results['summary']['passed']}")
    print(f"❌ Failed: {test_results['summary']['failed']}")
    print(f"⚠️  Warnings: {test_results['summary']['warnings']}")
    
    # Save results
    with open('family_integration_test_results.json', 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n💾 Results saved to: family_integration_test_results.json")
    
    # Recommendations
    print("\n🎯 RECOMMENDATIONS:")
    if test_results['summary']['failed'] > 0:
        print("❌ Critical issues found! Run: bash fix_backend.sh")
        print("   Then edit .env file with your API keys")
    elif test_results['summary']['warnings'] > 0:
        print("⚠️  Optional features missing but core is ready!")
        print("   You can start the backend with: python app.py")
    else:
        print("🎉 ALL SYSTEMS GO! Start backend with: python app.py")
    
    # DXT readiness
    print("\n📦 DXT EXTENSION READINESS:")
    if env_ok and imports_ok:
        print("✅ Backend is ready for DXT packaging!")
        print("   Next: Start backend, then update DXT extension")
    else:
        print("❌ Fix backend issues before DXT packaging")
    
    return test_results['summary']['failed'] == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
