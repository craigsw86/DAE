@echo off
echo  Starting HIPAA Checklist Secure Server
echo ================================================

REM Set environment variables
set FIELD_ENCRYPTION_KEY=%FIELD_ENCRYPTION_KEY%
set DB_ENCRYPTION_PASSWORD=%DB_ENCRYPTION_PASSWORD%
set DJANGO_SETTINGS_MODULE=hipaa_checklist.settings
set WAITRESS_HOST=0.0.0.0
set WAITRESS_PORT=8000
set WAITRESS_THREADS=4

echo  Environment configured
echo   - Field Encryption: 
echo   - Database Encryption: 
echo   - Server Host: %WAITRESS_HOST%
echo   - Server Port: %WAITRESS_PORT%
echo   - Threads: %WAITRESS_THREADS%

echo.
echo  Setting up database security...
cd backend
python setup_database_security.py

if %errorlevel% neq 0 (
    echo  Database security setup failed
    pause
    exit /b 1
)

echo.
echo  Starting secure Waitress server...
python waitress_secure.py

echo.
echo  Server stopped
pause
