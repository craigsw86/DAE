@echo off
echo  WEEK 10 DAY 1: Setting up Nginx Reverse Proxy with HTTPS
echo ================================================================

REM Check if OpenSSL is available
where openssl >nul 2>nul
if %errorlevel% neq 0 (
    echo  OpenSSL not found. Please install OpenSSL first.
    echo    Download from: https://slproweb.com/products/Win32OpenSSL.html
    echo    Or use Git Bash which includes OpenSSL
    pause
    exit /b 1
)

echo  Step 1: Generating SSL certificates...
call generate_ssl_cert.bat

echo.
echo  Step 2: Building React frontend...
cd frontend
call npm run build
if %errorlevel% neq 0 (
    echo  Failed to build React frontend
    pause
    exit /b 1
)
cd ..

echo.
echo  Step 3: Collecting Django static files...
cd backend
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo  Failed to collect static files
    pause
    exit /b 1
)
cd ..

echo.
echo  Step 4: Starting services with Docker Compose...
docker-compose -f docker-compose.nginx.yml up -d

echo.
echo  Setup complete! 
echo.
echo  Access your application:
echo    HTTP:  http://localhost (redirects to HTTPS)
echo    HTTPS: https://localhost
echo.
echo   Note: You'll see a security warning for the self-signed certificate.
echo    Click "Advanced" and "Proceed to localhost" to continue.
echo.
echo  To view logs:
echo    docker-compose -f docker-compose.nginx.yml logs -f
echo.
echo  To stop services:
echo    docker-compose -f docker-compose.nginx.yml down
echo.
pause
