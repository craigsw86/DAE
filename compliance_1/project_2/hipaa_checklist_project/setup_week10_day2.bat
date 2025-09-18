@echo off
echo 🚀 WEEK 10 DAY 2: Setting up Waitress Django Server with SQLite Security
echo ========================================================================

echo 📝 Step 1: Installing Waitress and dependencies...
cd backend
pip install waitress==2.1.2 psutil==5.9.8
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 📝 Step 2: Setting up database security...
python setup_database_security.py
if %errorlevel% neq 0 (
    echo ❌ Database security setup failed
    pause
    exit /b 1
)

echo.
echo 📝 Step 3: Testing Waitress server...
echo Starting Waitress server in test mode...
echo Press Ctrl+C to stop the server after testing
echo.
python waitress_server.py

echo.
echo ✅ Week 10 Day 2 setup completed!
echo.
echo 🚀 To start the production server:
echo    cd backend
echo    python waitress_server.py
echo.
echo 📊 Server will be available at:
echo    http://localhost:8000
echo.
echo 🔐 Security features enabled:
echo    ✅ Database file permissions secured
echo    ✅ SQLite PRAGMAs configured for security
echo    ✅ Waitress WSGI server with production settings
echo    ✅ Enhanced logging and monitoring
echo.
pause
