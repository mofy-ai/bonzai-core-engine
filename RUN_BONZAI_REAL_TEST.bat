@echo off
echo.
echo 🔧 BONZAI REAL SYSTEM FIXER
echo ========================================
echo This will fix Nathan's sophisticated backend
echo NO MORE FAKE RESPONSES - REAL AI ONLY!
echo.

echo Step 1: Fixing dependencies...
python fix_bonzai_dependencies.py
echo.

echo Step 2: Starting Bonzai backend...
echo Press Ctrl+C to stop the server when testing is done
timeout /t 5 /nobreak
python app.py &

echo.
echo Step 3: Waiting for server to start...
timeout /t 10 /nobreak

echo.
echo Step 4: Testing REAL system functionality...
python test_real_bonzai_system.py

echo.
echo 🎯 BONZAI SYSTEM VERIFICATION COMPLETE!
echo Check the test results above ^^^
echo.
echo If tests show "REAL AI responses" - YOUR SYSTEM WORKS!
echo If tests show "Mock detected" - More fixes needed
echo.
pause
