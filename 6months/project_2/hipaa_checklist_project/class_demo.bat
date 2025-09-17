@echo off
echo ========================================
echo Black Duck Detect Integration Demo
echo ========================================
echo.

echo Step 1: Testing Java 11...
java -version
if %errorlevel% neq 0 (
    echo ERROR: Java 11 not found!
    pause
    exit /b 1
)
echo Java 11 is working!
echo.

echo Step 2: Testing Django...
cd backend
python manage.py check
if %errorlevel% neq 0 (
    echo ERROR: Django check failed!
    pause
    exit /b 1
)
echo Django is working!
echo.

echo Step 3: Testing Security Command...
python manage.py scan_detect --help
if %errorlevel% neq 0 (
    echo ERROR: Security command failed!
    pause
    exit /b 1
)
echo Security command is working!
echo.

echo Step 4: Starting Django Server...
echo Starting Django server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver
