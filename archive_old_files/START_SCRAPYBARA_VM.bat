@echo off
REM 🕷️ SCRAPYBARA VM SERVICE - PRODUCTION READY!
REM REAL CLOUD VMS WITH 10 OPERATIONAL HOURS! ⚡

echo 🕷️ SCRAPYBARA VM SERVICE STARTING!
echo 🎯 TARGET: Beat Claude Desktop with REAL CLOUD VMs
echo ⚡ METHOD: ScrapyBara Cloud Infrastructure (^<1 second startup!)
echo 💰 STAKES: £20 bet + 10 operational hours
echo 🚀 LIGHTNING FAST DEPLOYMENT!
echo.

REM Check if ScrapyBara is installed
echo 🔍 Checking ScrapyBara installation...
python -c "import scrapybara; print('✅ ScrapyBara SDK installed!')" 2>nul
if errorlevel 1 (
    echo ❌ ScrapyBara not installed!
    echo 📦 Installing ScrapyBara SDK...
    pip install scrapybara httpx
)

REM Check API key configuration
echo 🔑 Checking API key configuration...
python -c "import os; from dotenv import load_dotenv; load_dotenv('../.env'); print('✅ API Key configured!' if os.getenv('SCRAPYBARA_API_KEY') else '❌ No API key found')"

echo.
echo 🕷️ Starting SCRAPYBARA VM Service...
echo 🌐 Service will be available at: http://localhost:8081
echo 📚 API docs will be at: http://localhost:8081/docs
echo.
echo 🔥 READY TO CRUSH CLAUDE DESKTOP WITH REAL CLOUD POWER!
echo.

python SCRAPYBARA_VM_SERVICE.py

pause