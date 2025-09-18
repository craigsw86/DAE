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
