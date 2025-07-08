@echo off
REM Clean backend startup for Windows
REM Sets UTF-8 encoding and runs with clean output

echo ========================================
echo BONZAI BACKEND - CLEAN STARTUP
echo ========================================
echo.

REM Set UTF-8 code page
chcp 65001 > nul 2>&1

REM Set Python UTF-8 encoding
set PYTHONIOENCODING=utf-8

REM Set Flask environment variables
set FLASK_APP=app.py
set FLASK_ENV=development
set PORT=5001

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] No virtual environment found
)

echo.
echo [INFO] Starting Bonzai Backend on port %PORT%
echo [INFO] UTF-8 encoding enabled
echo [INFO] Clean logging enabled
echo.

REM Run the backend with clean startup script
python run_backend.py

REM If run_backend.py doesn't exist, fall back to flask run
if errorlevel 1 (
    echo.
    echo [INFO] Falling back to flask run...
    flask run --host=0.0.0.0 --port=%PORT%
)

pause