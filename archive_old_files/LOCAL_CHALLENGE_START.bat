@echo off
REM 🚨 45-MINUTE LOCAL VM CHALLENGE - DOCKER DESKTOP EDITION
REM NO GCLOUD BULLSHIT - PURE LOCAL POWER! ⚡

echo 🚨 45-MINUTE LOCAL VM CHALLENGE STARTING!
echo 🎯 TARGET: Beat Claude Desktop's 4-week prediction LOCALLY
echo 🐳 METHOD: Docker Desktop containers as VMs  
echo 💰 STAKES: £20 bet
echo ⚡ NO GCLOUD NEEDED - LOCAL DOCKER POWER!
echo.

REM Check if Docker Desktop is running
echo 🔍 Checking Docker Desktop status...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Desktop not running!
    echo 🔧 Please start Docker Desktop and try again
    echo.
    pause
    exit /b 1
)

echo ✅ Docker Desktop is running!
echo.

REM Install Python dependencies
echo 📦 Installing dependencies...
pip install fastapi uvicorn docker

REM Start the local VM service
echo 🚀 Starting LOCAL VM Challenge Service...
echo 🌐 Service will be available at: http://localhost:8080
echo.
echo 🔥 READY TO CRUSH CLAUDE DESKTOP'S 4-WEEK PREDICTION!
echo.

python LOCAL_VM_CHALLENGE.py

pause