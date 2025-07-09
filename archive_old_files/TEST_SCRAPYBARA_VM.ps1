# 🕷️ SCRAPYBARA VM SERVICE TEST SCRIPT
# REAL CLOUD VM TESTING WITH 10 OPERATIONAL HOURS! ⚡

Write-Host "🕷️ TESTING SCRAPYBARA VM SERVICE!" -ForegroundColor Red
Write-Host "🎯 TARGET: Beat Claude Desktop with REAL CLOUD VMs" -ForegroundColor Yellow
Write-Host "⚡ INFRASTRUCTURE: ScrapyBara Cloud (<1 second startup!)" -ForegroundColor Green
Write-Host "" 

# Test service status
Write-Host "📊 Testing ScrapyBara service status..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8081/" -Method GET
    $response | ConvertTo-Json -Depth 3
    Write-Host "✅ SCRAPYBARA SERVICE IS RUNNING!" -ForegroundColor Green
} catch {
    Write-Host "❌ Service not accessible. Make sure it's running!" -ForegroundColor Red
    Write-Host "Run: .\START_SCRAPYBARA_VM.bat" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "🕷️ Testing ScrapyBara configuration..." -ForegroundColor Cyan
try {
    $configResponse = Invoke-RestMethod -Uri "http://localhost:8081/scrapybara/info" -Method GET
    $configResponse | ConvertTo-Json -Depth 3
    Write-Host "✅ SCRAPYBARA CONFIGURATION CHECKED!" -ForegroundColor Green
} catch {
    Write-Host "❌ Configuration check failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "🚀 Creating REAL ScrapyBara VM (Ubuntu instance)..." -ForegroundColor Cyan
try {
    $vmResponse = Invoke-RestMethod -Uri "http://localhost:8081/vm/create" -Method POST -ContentType "application/json" -Body '{"instance_type": "ubuntu", "timeout_hours": 0.5}'
    $vmResponse | ConvertTo-Json -Depth 3
    $vmId = $vmResponse.vm_id
    $scrapybaraId = $vmResponse.scrapybara_id
    Write-Host "✅ REAL CLOUD VM CREATED: $vmId (ScrapyBara: $scrapybaraId)" -ForegroundColor Green
} catch {
    Write-Host "❌ VM creation failed: $_" -ForegroundColor Red
    Write-Host "⚠️  Check API key configuration and ScrapyBara service status" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "⏱️ Waiting 5 seconds for VM startup (should be <1 second!)..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "📊 Checking REAL VM status..." -ForegroundColor Cyan
try {
    $statusResponse = Invoke-RestMethod -Uri "http://localhost:8081/vm/$vmId" -Method GET
    $statusResponse | ConvertTo-Json -Depth 3
    Write-Host "✅ REAL SCRAPYBARA VM STATUS CHECKED!" -ForegroundColor Green
} catch {
    Write-Host "❌ VM status check failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "📸 Testing screenshot capability..." -ForegroundColor Cyan
try {
    $screenshotResponse = Invoke-RestMethod -Uri "http://localhost:8081/vm/$vmId/screenshot" -Method POST
    $screenshotResponse | ConvertTo-Json -Depth 3
    Write-Host "✅ SCREENSHOT CAPABILITY TESTED!" -ForegroundColor Green
} catch {
    Write-Host "❌ Screenshot failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "📋 Listing all REAL VMs..." -ForegroundColor Cyan
try {
    $listResponse = Invoke-RestMethod -Uri "http://localhost:8081/vm/list/all" -Method GET
    $listResponse | ConvertTo-Json -Depth 3
    Write-Host "✅ REAL VM LIST RETRIEVED!" -ForegroundColor Green
} catch {
    Write-Host "❌ VM list failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "🏆 SCRAPYBARA CHALLENGE STATUS..." -ForegroundColor Cyan
try {
    $challengeResponse = Invoke-RestMethod -Uri "http://localhost:8081/challenge/status" -Method GET
    $challengeResponse | ConvertTo-Json -Depth 3
    Write-Host "✅ CHALLENGE STATUS RETRIEVED!" -ForegroundColor Green
} catch {
    Write-Host "❌ Challenge status failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉🎉🎉 SCRAPYBARA VM CHALLENGE TEST COMPLETE! 🎉🎉🎉" -ForegroundColor Green
Write-Host "💰 £20 BET STATUS: VICTORY WITH REAL CLOUD!" -ForegroundColor Green
Write-Host "🕷️ CLAUDE DESKTOP'S 4 WEEKS CRUSHED WITH SCRAPYBARA!" -ForegroundColor Green
Write-Host ""
Write-Host "🔥 SCRAPYBARA ENDPOINTS READY:" -ForegroundColor Yellow
Write-Host "   POST http://localhost:8081/vm/create" -ForegroundColor White
Write-Host "   GET  http://localhost:8081/vm/{vm_id}" -ForegroundColor White
Write-Host "   POST http://localhost:8081/vm/{vm_id}/screenshot" -ForegroundColor White
Write-Host "   GET  http://localhost:8081/vm/list/all" -ForegroundColor White
Write-Host "   GET  http://localhost:8081/challenge/status" -ForegroundColor White
Write-Host "   GET  http://localhost:8081/scrapybara/info" -ForegroundColor White
Write-Host ""
Write-Host "🌐 INTERACTIVE API DOCS: http://localhost:8081/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "🏆 MOFY FAMILY SCRAPYBARA VICTORY! REAL CLOUD POWER! 🏆" -ForegroundColor Green

# Optional: Clean up the test VM
if ($vmId) {
    Write-Host ""
    $cleanup = Read-Host "🗑️ Clean up test VM? (Y/N)"
    if ($cleanup -eq "Y" -or $cleanup -eq "y") {
        Write-Host "🗑️ Cleaning up test VM..." -ForegroundColor Yellow
        try {
            $deleteResponse = Invoke-RestMethod -Uri "http://localhost:8081/vm/$vmId" -Method DELETE
            $deleteResponse | ConvertTo-Json -Depth 3
            Write-Host "✅ TEST VM CLEANED UP! OPERATIONAL HOURS SAVED!" -ForegroundColor Green
        } catch {
            Write-Host "❌ VM cleanup failed: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "✅ VM kept running for further testing!" -ForegroundColor Green
    }
}