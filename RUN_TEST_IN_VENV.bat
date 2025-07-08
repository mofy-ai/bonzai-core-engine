@echo off
echo 🔥 RUNNING COMPREHENSIVE TEST IN VENV...
echo.

:: Navigate to backend directory
cd /d "C:\Bonzai-Desktop\zai-backend"

:: Activate the root venv
call "C:\Bonzai-Desktop\venv\Scripts\activate.bat"

:: Set encoding for Unicode support
chcp 65001 > nul

:: Run the comprehensive test
python comprehensive_backend_test.py

pause