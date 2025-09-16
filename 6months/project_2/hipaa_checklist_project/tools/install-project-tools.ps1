# Install supporting tools for HIPAA Self-Audit Tool project
# Run as Administrator: powershell -ExecutionPolicy Bypass -File .\install-project-tools.ps1

Write-Host "========================================" -ForegroundColor Green
Write-Host "Installing Project Tools with Chocolatey" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script requires Administrator privileges. Please run as Administrator." -ForegroundColor Red
    exit 1
}

# Verify Chocolatey is installed
try {
    $chocoVersion = choco --version
    Write-Host "Chocolatey version: $chocoVersion" -ForegroundColor Green
} catch {
    Write-Host "Chocolatey not found. Please install it first from https://chocolatey.org/install" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Installing supporting tools..." -ForegroundColor Yellow

# Install Docker Desktop
Write-Host "Installing Docker Desktop..." -ForegroundColor Cyan
choco install docker-desktop -y

# Install Node.js (if not already installed)
Write-Host "Installing Node.js..." -ForegroundColor Cyan
choco install nodejs -y

# Install Python (if not already installed)
Write-Host "Installing Python..." -ForegroundColor Cyan
choco install python -y

# Install Git (if not already installed)
Write-Host "Installing Git..." -ForegroundColor Cyan
choco install git -y

# Install additional useful tools
Write-Host "Installing additional tools..." -ForegroundColor Cyan
choco install curl -y
choco install 7zip -y

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Installation completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Verify installations
Write-Host "Verifying installations:" -ForegroundColor Yellow
Write-Host "Docker: $(docker --version 2>$null)" -ForegroundColor Cyan
Write-Host "Node.js: $(node --version 2>$null)" -ForegroundColor Cyan
Write-Host "npm: $(npm --version 2>$null)" -ForegroundColor Cyan
Write-Host "Python: $(python --version 2>$null)" -ForegroundColor Cyan
Write-Host "pip: $(pip --version 2>$null)" -ForegroundColor Cyan
Write-Host "Git: $(git --version 2>$null)" -ForegroundColor Cyan

Write-Host ""
Write-Host "Please restart your machine after Docker Desktop installation." -ForegroundColor Yellow
Write-Host "Then you can run the project tools and Black Duck Detect." -ForegroundColor Green
