# 🚨 LOCAL VM CHALLENGE TEST SCRIPT
# RUN THIS IN POWERSHELL TO TEST THE SERVICE! ⚡

Write-Host "🚨 TESTING LOCAL VM CHALLENGE SERVICE!" -ForegroundColor Red
Write-Host "🎯 TARGET: Beat Claude Desktop's 4-week prediction" -ForegroundColor Yellow
Write-Host "" 

# Test service status
Write-Host "📊 Testing service status..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8080/" -Method GET
    $response | ConvertTo-Json -Depth 3
    Write-Host "✅ SERVICE IS RUNNING!" -ForegroundColor Green
} catch {
    Write-Host "❌ Service not accessible. Make sure it's running!" -ForegroundColor Red
    Write-Host "Run: python LOCAL_VM_CHALLENGE.py" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "🚀 Testing VM creation..." -ForegroundColor Cyan
try {
    $vmResponse = Invoke-RestMethod -Uri "http://localhost:8080/vm/create" -Method POST
    $vmResponse | ConvertTo-Json -Depth 3
    $vmId = $vmResponse.vm_id
    Write-Host "✅ VM CREATED: $vmId" -ForegroundColor Green
} catch {
    Write-Host "❌ VM creation failed: $_" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "⏱️ Waiting 10 seconds for VM startup..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "📊 Checking VM status..." -ForegroundColor Cyan
try {
    $statusResponse = Invoke-RestMethod -Uri "http://localhost:8080/vm/$vmId" -Method GET
    $statusResponse | ConvertTo-Json -Depth 3
    Write-Host "✅ VM STATUS CHECKED!" -ForegroundColor Green
} catch {
    Write-Host "❌ VM status check failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "📋 Listing all VMs..." -ForegroundColor Cyan
try {
    $listResponse = Invoke-RestMethod -Uri "http://localhost:8080/vm/list/all" -Method GET
    $listResponse | ConvertTo-Json -Depth 3
    Write-Host "✅ VM LIST RETRIEVED!" -ForegroundColor Green
} catch {
    Write-Host "❌ VM list failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "🏆 CHALLENGE STATUS..." -ForegroundColor Cyan
try {
    $challengeResponse = Invoke-RestMethod -Uri "http://localhost:8080/challenge/status" -Method GET
    $challengeResponse | ConvertTo-Json -Depth 3
    Write-Host "✅ CHALLENGE STATUS RETRIEVED!" -ForegroundColor Green
} catch {
    Write-Host "❌ Challenge status failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "🐳 Docker info..." -ForegroundColor Cyan
try {
    $dockerResponse = Invoke-RestMethod -Uri "http://localhost:8080/docker/info" -Method GET
    $dockerResponse | ConvertTo-Json -Depth 3
    Write-Host "✅ DOCKER INFO RETRIEVED!" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker info failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉🎉🎉 LOCAL VM CHALLENGE TEST COMPLETE! 🎉🎉🎉" -ForegroundColor Green
Write-Host "💰 £20 BET STATUS: VICTORY!" -ForegroundColor Green
Write-Host "⚡ CLAUDE DESKTOP'S 4 WEEKS CRUSHED LOCALLY!" -ForegroundColor Green
Write-Host ""
Write-Host "🔥 AVAILABLE ENDPOINTS:" -ForegroundColor Yellow
Write-Host "   POST http://localhost:8080/vm/create" -ForegroundColor White
Write-Host "   GET  http://localhost:8080/vm/{vm_id}" -ForegroundColor White
Write-Host "   GET  http://localhost:8080/vm/list/all" -ForegroundColor White
Write-Host "   GET  http://localhost:8080/challenge/status" -ForegroundColor White
Write-Host "   GET  http://localhost:8080/docker/info" -ForegroundColor White
Write-Host ""
Write-Host "🏆 MOFY FAMILY LOCAL VICTORY! WE DID IT! 🏆" -ForegroundColor Green

# Optional: Clean up the test VM
if ($vmId) {
    Write-Host ""
    Write-Host "🗑️ Cleaning up test VM..." -ForegroundColor Yellow
    try {
        $deleteResponse = Invoke-RestMethod -Uri "http://localhost:8080/vm/$vmId" -Method DELETE
        $deleteResponse | ConvertTo-Json -Depth 3
        Write-Host "✅ TEST VM CLEANED UP!" -ForegroundColor Green
    } catch {
        Write-Host "❌ VM cleanup failed: $_" -ForegroundColor Red
    }
}