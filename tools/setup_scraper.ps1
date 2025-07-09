# 🐻 MAMA BEAR'S WEB SCRAPER SETUP SCRIPT
# =====================================
# Easy setup for Nathan's web scraping tool

Write-Host "🐻 MAMA BEAR'S WEB SCRAPER SETUP" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Check if Python is available
Write-Host "`n🔍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.8+ first." -ForegroundColor Red
    exit 1
}

# Check if we're in the right directory
$currentDir = Get-Location
Write-Host "📁 Current directory: $currentDir" -ForegroundColor Yellow

# Install dependencies
Write-Host "`n📦 Installing scraper dependencies..." -ForegroundColor Yellow
try {
    python -m pip install -r tools/scraper_requirements.txt
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install dependencies. Make sure pip is working." -ForegroundColor Red
    exit 1
}

# Create output directory
Write-Host "`n📁 Creating output directory..." -ForegroundColor Yellow
if (!(Test-Path "scraped_websites")) {
    New-Item -ItemType Directory -Path "scraped_websites" | Out-Null
    Write-Host "✅ Created 'scraped_websites' directory" -ForegroundColor Green
} else {
    Write-Host "✅ Output directory already exists" -ForegroundColor Green
}

# Check for Mem0 API key
Write-Host "`n🔑 Checking Mem0 configuration..." -ForegroundColor Yellow
$mem0Key = $env:MEM0_API_KEY
if ($mem0Key) {
    Write-Host "✅ MEM0_API_KEY environment variable found" -ForegroundColor Green
} else {
    Write-Host "⚠️ MEM0_API_KEY not set - you can set it later for automatic memory uploads" -ForegroundColor Yellow
    Write-Host "💡 To set it: `$env:MEM0_API_KEY = 'your-api-key-here'" -ForegroundColor Cyan
}

# Test the scraper
Write-Host "`n🧪 Testing the scraper..." -ForegroundColor Yellow
try {
    Set-Location tools
    python -c "from mama_bear_web_scraper import MamaBearWebScraper; print('✅ Scraper imports successfully!')"
    Set-Location ..
    Write-Host "✅ Scraper is ready to use!" -ForegroundColor Green
} catch {
    Write-Host "❌ Scraper test failed. Check the error above." -ForegroundColor Red
    exit 1
}

# Show usage instructions
Write-Host "`n🎉 SETUP COMPLETE!" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green

Write-Host "`n📚 How to use:" -ForegroundColor Cyan
Write-Host "1. Single website:" -ForegroundColor White
Write-Host "   Set-Location tools" -ForegroundColor Gray
Write-Host "   python scraper_examples.py" -ForegroundColor Gray

Write-Host "`n2. Custom usage:" -ForegroundColor White
Write-Host "   python -c `"from scraper_examples import scrape_and_memorize; scrape_and_memorize('https://example.com')`"" -ForegroundColor Gray

Write-Host "`n3. Interactive mode:" -ForegroundColor White
Write-Host "   python mama_bear_web_scraper.py" -ForegroundColor Gray

Write-Host "`n📁 Output files will be saved in: scraped_websites/" -ForegroundColor Cyan
Write-Host "🧠 Mem0 chunks will be automatically uploaded if API key is set" -ForegroundColor Cyan

Write-Host "`n🐻 Mama Bear says: Happy scraping, Nathan! ❤️" -ForegroundColor Magenta
