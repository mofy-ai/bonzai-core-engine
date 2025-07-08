#!/bin/bash
# 🔥 BONZAI BACKEND COMPREHENSIVE FIX SCRIPT
# Generated: 2025-07-05 21:37:55.309642

echo "🔧 BONZAI BACKEND FIX SCRIPT"
echo "============================"

# Activate virtual environment if exists
if [ -d "venv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate || source venv/Scripts/activate
fi

# Install core dependencies
echo "📦 Installing core dependencies..."
pip install --upgrade pip
pip install flask flask-cors flask-socketio
pip install google-generativeai mem0 python-dotenv
pip install requests aiohttp asyncio
pip install beautifulsoup4 lxml

# Install AI SDKs
echo "🤖 Installing AI SDKs..."
pip install openai anthropic google-cloud-aiplatform

# Install optional dependencies
echo "📚 Installing optional packages..."
pip install websockets redis pymongo
pip install celery dramatiq
pip install pydantic sqlalchemy

# Create required directories
echo "📁 Creating required directories..."
mkdir -p logs
mkdir -p zai_memory
mkdir -p credentials
mkdir -p services/orchestration
mkdir -p services/supervisor

# Environment setup
if [ ! -f .env ]; then
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your API keys!"
    echo ""
fi

# Download missing service files if needed
echo "📥 Checking service files..."
# Add any specific file downloads here

echo ""
echo "✅ Fix script complete!"
echo ""
echo "📋 NEXT STEPS:"
echo "1. Edit .env file with your API keys"
echo "2. Run: python app.py"
echo "3. Check http://localhost:5001/api/health"
echo ""
echo "🚀 Ready for DXT packaging once backend starts!"
