# Comprehensive setup script for HIPAA Self-Audit Tool with Chocolatey
# Run as Administrator: powershell -ExecutionPolicy Bypass -File .\setup-hipaa-project-with-chocolatey.ps1

Write-Host "========================================" -ForegroundColor Green
Write-Host "HIPAA Self-Audit Tool - Complete Setup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script requires Administrator privileges. Please run as Administrator." -ForegroundColor Red
    exit 1
}

# Step 1: Verify Chocolatey
Write-Host "Step 1: Verifying Chocolatey installation..." -ForegroundColor Yellow
try {
    $chocoVersion = choco --version
    Write-Host "✓ Chocolatey version: $chocoVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Chocolatey not found. Installing..." -ForegroundColor Red
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Step 2: Install JDK 11
Write-Host "`nStep 2: Installing JDK 11..." -ForegroundColor Yellow
choco install openjdk11 -y
Write-Host "✓ JDK 11 installed" -ForegroundColor Green

# Step 3: Install supporting tools
Write-Host "`nStep 3: Installing supporting tools..." -ForegroundColor Yellow
$tools = @('docker-desktop', 'nodejs', 'python', 'git', 'curl', '7zip')
foreach ($tool in $tools) {
    Write-Host "Installing $tool..." -ForegroundColor Cyan
    choco install $tool -y
}
Write-Host "✓ Supporting tools installed" -ForegroundColor Green

# Step 4: Set up project environment
Write-Host "`nStep 4: Setting up project environment..." -ForegroundColor Yellow

# Create reports directory
New-Item -ItemType Directory -Force -Path "reports\detect" | Out-Null
Write-Host "✓ Reports directory created" -ForegroundColor Green

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
if (Test-Path "backend\requirements.txt") {
    pip install -r backend\requirements.txt
    Write-Host "✓ Python dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠ requirements.txt not found" -ForegroundColor Yellow
}

# Install Node.js dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Cyan
if (Test-Path "frontend\package.json") {
    Set-Location frontend
    npm install
    Set-Location ..
    Write-Host "✓ Node.js dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠ package.json not found" -ForegroundColor Yellow
}

# Step 5: Verify installations
Write-Host "`nStep 5: Verifying installations..." -ForegroundColor Yellow

# Set JDK 11 environment for verification
$env:JAVA_HOME = "C:\Program Files\OpenJDK\jdk-11"
$env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH

Write-Host "Java version: $(java -version 2>&1 | Select-Object -First 1)" -ForegroundColor Cyan
Write-Host "Node.js version: $(node --version 2>$null)" -ForegroundColor Cyan
Write-Host "npm version: $(npm --version 2>$null)" -ForegroundColor Cyan
Write-Host "Python version: $(python --version 2>$null)" -ForegroundColor Cyan
Write-Host "pip version: $(pip --version 2>$null)" -ForegroundColor Cyan
Write-Host "Git version: $(git --version 2>$null)" -ForegroundColor Cyan

# Step 6: Test Black Duck Detect
Write-Host "`nStep 6: Testing Black Duck Detect..." -ForegroundColor Yellow
Set-Location tools\detect

# Download detect.ps1 if not exists
if (-not (Test-Path "detect.ps1")) {
    Write-Host "Downloading detect.ps1..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri "https://detect.blackduck.com/detect10.ps1" -OutFile "detect.ps1"
}

# Run a quick test scan
Write-Host "Running test scan (this may take a few minutes)..." -ForegroundColor Cyan
try {
    & .\detect.ps1 --detect.project.name="hipaa_checklist_project" --detect.source.path=".." --detect.output.path="../reports/detect" --detect.log.level=INFO *> test-scan-output.txt 2>&1
    
    if (Test-Path "../reports/detect") {
        $outputFiles = Get-ChildItem "../reports/detect"
        if ($outputFiles.Count -gt 0) {
            Write-Host "✓ Black Duck Detect test scan successful" -ForegroundColor Green
            Write-Host "Output files created: $($outputFiles.Count)" -ForegroundColor Cyan
        } else {
            Write-Host "⚠ No output files created, check test-scan-output.txt" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠ No reports directory created" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠ Test scan failed, check test-scan-output.txt for details" -ForegroundColor Yellow
}

Set-Location ..\..

# Step 7: Create convenience scripts
Write-Host "`nStep 7: Creating convenience scripts..." -ForegroundColor Yellow

# Create main project runner
$mainRunner = @"
@echo off
echo ========================================
echo HIPAA Self-Audit Tool
echo ========================================
echo.
echo Choose an option:
echo 1. Start Backend Server
echo 2. Start Frontend Development Server
echo 3. Run Black Duck Detect Scan
echo 4. Run Security Tests
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Starting Backend Server...
    cd backend
    python manage.py runserver
) else if "%choice%"=="2" (
    echo Starting Frontend Server...
    cd frontend
    npm start
) else if "%choice%"=="3" (
    echo Running Black Duck Detect...
    cd tools\detect
    .\run-detect-jdk11.bat
) else if "%choice%"=="4" (
    echo Running Security Tests...
    cd backend
    python manage.py scan_detect
) else if "%choice%"=="5" (
    echo Goodbye!
    exit
) else (
    echo Invalid choice. Please run the script again.
)
pause
"@

$mainRunner | Out-File -FilePath "run-hipaa-project.bat" -Encoding ASCII

Write-Host "✓ Convenience scripts created" -ForegroundColor Green

# Final summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Restart your machine (required for Docker Desktop)" -ForegroundColor Cyan
Write-Host "2. Run '.\run-hipaa-project.bat' to start the application" -ForegroundColor Cyan
Write-Host "3. Or run individual components:" -ForegroundColor Cyan
Write-Host "   - Backend: cd backend && python manage.py runserver" -ForegroundColor Cyan
Write-Host "   - Frontend: cd frontend && npm start" -ForegroundColor Cyan
Write-Host "   - Security Scan: cd tools\detect && .\run-detect-jdk11.bat" -ForegroundColor Cyan
Write-Host ""
Write-Host "Project structure:" -ForegroundColor Yellow
Write-Host "- Backend: Django REST API" -ForegroundColor Cyan
Write-Host "- Frontend: React application" -ForegroundColor Cyan
Write-Host "- Security: Black Duck Detect integration" -ForegroundColor Cyan
Write-Host "- Reports: Generated in reports\detect\" -ForegroundColor Cyan
Write-Host ""
Write-Host "For detailed documentation, see:" -ForegroundColor Yellow
Write-Host "- README.md" -ForegroundColor Cyan
Write-Host "- FINAL_PROJECT_DOCUMENTATION.md" -ForegroundColor Cyan
Write-Host "- TECHNICAL_REFERENCE_GUIDE.md" -ForegroundColor Cyan
