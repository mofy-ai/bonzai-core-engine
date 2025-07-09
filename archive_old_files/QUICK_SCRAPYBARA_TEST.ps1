# 🕷️ QUICK SCRAPYBARA TEST - VERIFY IT'S WORKING!

Write-Host "🕷️ QUICK SCRAPYBARA VM SERVICE TEST!" -ForegroundColor Red

# Test 1: Service Status
Write-Host "📊 Testing service..." -ForegroundColor Cyan
try {
    $status = Invoke-RestMethod -Uri "http://localhost:8081/" -Method GET -TimeoutSec 5
    Write-Host "✅ SERVICE IS RUNNING!" -ForegroundColor Green
    Write-Host "Status: $($status.status)" -ForegroundColor White
    Write-Host "Operational Hours: $($status.operational_hours)" -ForegroundColor White
} catch {
    Write-Host "❌ Service not accessible: $_" -ForegroundColor Red
    exit
}

# Test 2: ScrapyBara Info
Write-Host "🔍 Checking ScrapyBara config..." -ForegroundColor Cyan
try {
    $info = Invoke-RestMethod -Uri "http://localhost:8081/scrapybara/info" -Method GET -TimeoutSec 5
    Write-Host "✅ SCRAPYBARA CONFIGURED!" -ForegroundColor Green
    Write-Host "API Key: $($info.api_key_configured)" -ForegroundColor White
    Write-Host "Capabilities: $($info.capabilities.Length) features" -ForegroundColor White
} catch {
    Write-Host "❌ Config check failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 SCRAPYBARA VM SERVICE IS LIVE!" -ForegroundColor Green
Write-Host "🌐 Access at: http://localhost:8081" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8081/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Ready to create REAL CLOUD VMs!" -ForegroundColor Yellow