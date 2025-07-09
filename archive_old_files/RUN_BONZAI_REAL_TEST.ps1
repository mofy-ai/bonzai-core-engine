# 🔧 BONZAI REAL SYSTEM FIXER - PowerShell Version
# Fix Nathan's sophisticated backend - NO MORE FAKE RESPONSES!

Write-Host ""
Write-Host "🔧 BONZAI REAL SYSTEM FIXER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "This will fix Nathan's sophisticated backend" -ForegroundColor White
Write-Host "NO MORE FAKE RESPONSES - REAL AI ONLY!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 1: Fixing dependencies..." -ForegroundColor Yellow
python fix_bonzai_dependencies.py
Write-Host ""

Write-Host "Step 2: Starting Bonzai backend..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server when testing is done" -ForegroundColor White
Start-Sleep -Seconds 5

# Start the backend in a separate process
$backendProcess = Start-Process -FilePath "python" -ArgumentList "app.py" -PassThru -NoNewWindow
Write-Host "Backend started with PID: $($backendProcess.Id)" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "Step 4: Testing REAL system functionality..." -ForegroundColor Yellow
python test_real_bonzai_system.py

Write-Host ""
Write-Host "🎯 BONZAI SYSTEM VERIFICATION COMPLETE!" -ForegroundColor Green
Write-Host "Check the test results above ^^^" -ForegroundColor White
Write-Host ""
Write-Host "If tests show 'REAL AI responses' - YOUR SYSTEM WORKS!" -ForegroundColor Green
Write-Host "If tests show 'Mock detected' - More fixes needed" -ForegroundColor Red
Write-Host ""

# Stop the backend process
Write-Host "Stopping backend process..." -ForegroundColor Yellow
Stop-Process -Id $backendProcess.Id -Force
Write-Host "Backend stopped." -ForegroundColor Green

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor White
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
