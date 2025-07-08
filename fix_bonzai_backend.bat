@echo off
REM 🔥 BONZAI BACKEND COMPREHENSIVE FIX SCRIPT (Windows)
REM Generated: 2025-07-05 21:37:55.312304

echo 🔧 BONZAI BACKEND FIX SCRIPT (Windows)
echo ====================================

REM Activate virtual environment if exists
if exist venv\Scripts\activate.bat (
    echo 🐍 Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Install dependencies
echo 📦 Installing all dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Create directories
echo 📁 Creating required directories...
if not exist logs mkdir logs
if not exist zai_memory mkdir zai_memory
if not exist credentials mkdir credentials

REM Check environment
if not exist .env (
    echo 📝 Creating .env from template...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Edit .env file and add your API keys!
    echo.
)

echo.
echo ✅ Fix script complete!
echo.
echo 📋 NEXT STEPS:
echo 1. Edit .env file with your API keys
echo 2. Run: python app.py
echo 3. Check http://localhost:5001/api/health
echo.
pause
