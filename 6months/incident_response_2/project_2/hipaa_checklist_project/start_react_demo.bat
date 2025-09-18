@echo off
echo ========================================
echo Starting React Security Dashboard
echo ========================================
echo.

echo Step 1: Checking Node.js...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found!
    pause
    exit /b 1
)
echo Node.js is working!
echo.

echo Step 2: Checking npm...
npm --version
if %errorlevel% neq 0 (
    echo ERROR: npm not found!
    pause
    exit /b 1
)
echo npm is working!
echo.

echo Step 3: Starting React App...
echo Starting React app on http://localhost:3000
echo Press Ctrl+C to stop the app
echo.
cd frontend
npm start
