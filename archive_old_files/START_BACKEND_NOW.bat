@echo off
echo BONZAI BACKEND QUICK START (Windows)
echo =====================================
echo.

REM Install missing python-dotenv if needed
echo Installing python-dotenv...
pip install python-dotenv

echo.
echo Starting backend with ROOT environment...
cd C:\Bonzai-Desktop\zai-backend
python start_backend_with_root_env.py

pause
