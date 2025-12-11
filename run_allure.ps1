# run_allure.ps1
Write-Host "=== ParaBank Test Suite with Allure Reporting ===" -ForegroundColor Cyan

# Clean previous results
if (Test-Path "allure-results") {
    Remove-Item "allure-results\*" -Force -Recurse -ErrorAction SilentlyContinue
    Write-Host "Cleaned previous allure-results" -ForegroundColor Gray
} else {
    New-Item -ItemType Directory -Force -Path "allure-results" | Out-Null
    Write-Host "Created allure-results directory" -ForegroundColor Gray
}

if (Test-Path "allure-report") {
    Remove-Item "allure-report\*" -Force -Recurse -ErrorAction SilentlyContinue
    Write-Host "Cleaned previous allure-report" -ForegroundColor Gray
} else {
    New-Item -ItemType Directory -Force -Path "allure-report" | Out-Null
    Write-Host "Created allure-report directory" -ForegroundColor Gray
}

# Create screenshots directory
if (-not (Test-Path "screenshots")) {
    New-Item -ItemType Directory -Force -Path "screenshots" | Out-Null
    Write-Host "Created screenshots directory" -ForegroundColor Gray
}

# Run Registration Tests with Allure
Write-Host "`n[1/2] Running Registration Tests..." -ForegroundColor Green
pytest tests/test_registration.py `
    -v `
    --tb=short `
    --alluredir=allure-results

# Run Bill Pay Tests with Allure
Write-Host "`n[2/2] Running Bill Pay Tests..." -ForegroundColor Green
pytest tests/test_bill_pay.py `
    -v `
    --tb=short `
    --alluredir=allure-results

# Generate Allure Report
Write-Host "`nGenerating Allure Report..." -ForegroundColor Yellow
allure generate allure-results -o allure-report --clean

Write-Host "`n=== Report Generated Successfully ===" -ForegroundColor Cyan
Write-Host "Allure report available at: $pwd\allure-report\index.html" -ForegroundColor Yellow

# Ask to open report
$openReport = Read-Host "`nOpen report in browser? (y/n)"
if ($openReport -eq 'y') {
    Write-Host "Opening report in browser..." -ForegroundColor Green
    Start-Process "$pwd\allure-report\index.html"
}

Write-Host "`n=== Additional Commands ===" -ForegroundColor Gray
Write-Host "To serve report dynamically:" -ForegroundColor White
Write-Host "  allure serve allure-results" -ForegroundColor Yellow
Write-Host "`nTo view report from command line:" -ForegroundColor White
Write-Host "  allure open allure-report" -ForegroundColor Yellow
