@echo off
echo ========================================
echo Starting React Frontend Server
echo ========================================
echo.

cd frontend
if not exist package.json (
    echo ERROR: package.json not found in frontend directory
    echo Current directory: %CD%
    echo Files in current directory:
    dir
    pause
    exit /b 1
)

echo Starting React server on http://localhost:3000
echo Press Ctrl+C to stop the server
echo.
npm start
