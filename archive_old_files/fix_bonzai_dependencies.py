#!/usr/bin/env python3
"""
🔧 BONZAI DEPENDENCY FIXER
Fix all import and dependency issues in Nathan's sophisticated backend
"""
import subprocess
import sys
import os

def run_command(cmd):
    """Run command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def install_missing_packages():
    """Install all missing packages"""
    packages = [
        "python-dotenv",
        "flask",
        "flask-cors", 
        "flask-socketio",
        "google-generativeai",
        "anthropic",
        "openai",
        "requests",
        "asyncio",
        "mem0",
        "python-socketio",
        "websockets"
    ]
    
    print("🔧 Installing missing packages...")
    for package in packages:
        print(f"Installing {package}...")
        success, stdout, stderr = run_command(f"pip install {package}")
        if success:
            print(f"✅ {package} installed")
        else:
            print(f"❌ {package} failed: {stderr}")

def fix_import_paths():
    """Fix Python import paths in services"""
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create __init__.py files in all directories
    dirs_to_init = [
        "services",
        "api", 
        "routes",
        "config",
        "services/orchestration",
        "services/supervisor"
    ]
    
    for dir_name in dirs_to_init:
        dir_path = os.path.join(current_dir, dir_name)
        if os.path.exists(dir_path):
            init_file = os.path.join(dir_path, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write("# Bonzai service initialization\n")
                print(f"✅ Created __init__.py in {dir_name}")

def create_env_file():
    """Create proper .env file"""
    env_content = """# 🔧 BONZAI ENVIRONMENT CONFIGURATION
# Core Flask Settings
FLASK_SECRET_KEY=your-super-secret-flask-key-here
BACKEND_PORT=5001
DEBUG=True
LOG_LEVEL=INFO
LOG_FILE=bonzai.log

# AI Model API Keys (UPDATE THESE!)
ANTHROPIC_API_KEY=your-anthropic-key-here
OPENAI_API_KEY=your-openai-key-here
GOOGLE_API_KEY=your-google-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here
DEEPSEEK_API_KEY=your-deepseek-key-here

# Memory & Storage
MEM0_API_KEY=your-mem0-key-here

# Specialized Services
SCRAPYBARA_API_KEY=your-scrapybara-key-here
E2B_API_KEY=your-e2b-key-here
PIPEDREAM_API_TOKEN=your-pipedream-token-here
GITHUB_PAT=your-github-token-here

# Vertex AI Configuration (for Gemini)
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account.json
VERTEX_PROJECT_ID=your-project-id
VERTEX_LOCATION=us-central1

# Railway/Production Settings
RAILWAY_STATIC_URL=https://your-app.railway.app
"""
    
    env_file = ".env"
    if not os.path.exists(env_file):
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file template")
        print("🚨 IMPORTANT: Update your API keys in .env file!")
    else:
        print("⚠️ .env file already exists")

def main():
    """Run all fixes"""
    print("🔧 BONZAI DEPENDENCY FIXER STARTING...")
    print("=" * 50)
    
    install_missing_packages()
    print()
    
    fix_import_paths()
    print()
    
    create_env_file()
    print()
    
    print("🎯 NEXT STEPS:")
    print("1. Update API keys in .env file")
    print("2. Run: python app.py")
    print("3. Test endpoints at http://localhost:5001")
    print("4. Your sophisticated system should now work!")

if __name__ == "__main__":
    main()
