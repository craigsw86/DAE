@echo off
echo ========================================
echo Starting Django Backend Server
echo ========================================
echo.

cd backend
if not exist manage.py (
    echo ERROR: manage.py not found in backend directory
    echo Current directory: %CD%
    echo Files in current directory:
    dir
    pause
    exit /b 1
)

echo Starting Django server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver
