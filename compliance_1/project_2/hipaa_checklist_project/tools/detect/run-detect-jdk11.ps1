# Black Duck Detect with JDK 11 - PowerShell Version
# Run with: powershell -ExecutionPolicy Bypass -File .\run-detect-jdk11.ps1

Write-Host "========================================" -ForegroundColor Green
Write-Host "Black Duck Detect with JDK 11" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Set JDK 11 environment
$env:JAVA_HOME = "C:\Program Files\OpenJDK\jdk-11"
$env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH

Write-Host "Verifying Java version:" -ForegroundColor Cyan
java -version
Write-Host ""

Write-Host "Current directory: $(Get-Location)" -ForegroundColor Cyan
Write-Host "JAVA_HOME: $env:JAVA_HOME" -ForegroundColor Cyan
Write-Host ""

# Check if detect.ps1 exists
if (-not (Test-Path "detect.ps1")) {
    Write-Host "Downloading detect.ps1..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri "https://detect.blackduck.com/detect10.ps1" -OutFile "detect.ps1"
        Write-Host "detect.ps1 downloaded successfully" -ForegroundColor Green
    } catch {
        Write-Host "Failed to download detect.ps1: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# Ensure reports directory exists
$reportsDir = "..\reports\detect"
if (-not (Test-Path $reportsDir)) {
    New-Item -ItemType Directory -Force -Path $reportsDir | Out-Null
    Write-Host "Created reports directory: $reportsDir" -ForegroundColor Green
}

# Run Black Duck Detect
Write-Host "Running Black Duck Detect..." -ForegroundColor Yellow
Write-Host "This may take 15-20 minutes..." -ForegroundColor Yellow
Write-Host ""

try {
    & .\detect.ps1 `
        --detect.project.name="hipaa_checklist_project" `
        --detect.source.path=".." `
        --detect.detector.search.depth=3 `
        --detect.python.path="python" `
        --detect.npm.path="npm" `
        --detect.output.path="../reports/detect" `
        --detect.log.level=TRACE `
        *> detect-output.txt 2>&1

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Detect scan completed!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Check detect-output.txt for detailed logs" -ForegroundColor Cyan
    Write-Host "Check ../reports/detect for scan results" -ForegroundColor Cyan
    
    # Show last few lines of output
    if (Test-Path "detect-output.txt") {
        Write-Host ""
        Write-Host "Last 10 lines of output:" -ForegroundColor Yellow
        Get-Content "detect-output.txt" | Select-Object -Last 10
    }
    
} catch {
    Write-Host "Error running Detect: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Check detect-output.txt for details" -ForegroundColor Yellow
}
