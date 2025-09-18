# PowerShell script to start both Django and React servers for demo
# Run this script to start both servers

Write-Host "🚀 Starting HIPAA Self-Audit Tool Demo Servers" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green

# Function to start Django server
function Start-DjangoServer {
    Write-Host "`n🔧 Starting Django Backend Server..." -ForegroundColor Yellow
    Set-Location backend
    
    # Check if manage.py exists
    if (Test-Path "manage.py") {
        Write-Host "✅ Django project found" -ForegroundColor Green
        Write-Host "🌐 Starting server on http://localhost:8000" -ForegroundColor Cyan
        Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
        Write-Host ""
        
        # Start Django server
        python manage.py runserver
    } else {
        Write-Host "❌ manage.py not found in backend directory" -ForegroundColor Red
        Write-Host "Current directory: $(Get-Location)" -ForegroundColor Gray
        Write-Host "Files in current directory:" -ForegroundColor Gray
        Get-ChildItem | Select-Object Name
    }
}

# Function to start React server
function Start-ReactServer {
    Write-Host "`n🔧 Starting React Frontend Server..." -ForegroundColor Yellow
    Set-Location frontend
    
    # Check if package.json exists
    if (Test-Path "package.json") {
        Write-Host "✅ React project found" -ForegroundColor Green
        Write-Host "🌐 Starting server on http://localhost:3000" -ForegroundColor Cyan
        Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
        Write-Host ""
        
        # Start React server
        npm start
    } else {
        Write-Host "❌ package.json not found in frontend directory" -ForegroundColor Red
        Write-Host "Current directory: $(Get-Location)" -ForegroundColor Gray
        Write-Host "Files in current directory:" -ForegroundColor Gray
        Get-ChildItem | Select-Object Name
    }
}

# Main execution
Write-Host "Choose which server to start:" -ForegroundColor White
Write-Host "1. Django Backend (http://localhost:8000)" -ForegroundColor Cyan
Write-Host "2. React Frontend (http://localhost:3000)" -ForegroundColor Cyan
Write-Host "3. Both (requires two terminals)" -ForegroundColor Cyan
Write-Host ""

$choice = Read-Host "Enter your choice (1-3)"

switch ($choice) {
    "1" {
        Start-DjangoServer
    }
    "2" {
        Start-ReactServer
    }
    "3" {
        Write-Host "`n📋 To start both servers, run this script twice:" -ForegroundColor Yellow
        Write-Host "Terminal 1: Choose option 1 (Django)" -ForegroundColor Gray
        Write-Host "Terminal 2: Choose option 2 (React)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Or use the individual batch files:" -ForegroundColor Yellow
        Write-Host "Terminal 1: .\start_django.bat" -ForegroundColor Gray
        Write-Host "Terminal 2: .\start_react.bat" -ForegroundColor Gray
    }
    default {
        Write-Host "Invalid choice. Please run the script again." -ForegroundColor Red
    }
}
