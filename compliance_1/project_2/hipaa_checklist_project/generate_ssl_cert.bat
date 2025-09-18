@echo off
echo 🔐 Generating SSL certificates for HIPAA Checklist Project...

REM Create SSL directory
if not exist ssl mkdir ssl

REM Check if OpenSSL is available
where openssl >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ OpenSSL not found. Please install OpenSSL or use Git Bash.
    echo    Download from: https://slproweb.com/products/Win32OpenSSL.html
    pause
    exit /b 1
)

REM Generate private key
echo 📝 Generating private key...
openssl genrsa -out ssl\hipaa_checklist.key 2048

REM Generate certificate signing request
echo 📝 Generating certificate signing request...
openssl req -new -key ssl\hipaa_checklist.key -out ssl\hipaa_checklist.csr -subj "/C=US/ST=CA/L=San Francisco/O=HIPAA Checklist/OU=IT Department/CN=localhost"

REM Generate self-signed certificate
echo 📝 Generating self-signed certificate...
openssl x509 -req -days 365 -in ssl\hipaa_checklist.csr -signkey ssl\hipaa_checklist.key -out ssl\hipaa_checklist.crt

REM Set proper permissions (Windows)
icacls ssl\hipaa_checklist.key /inheritance:r /grant:r "%USERNAME%:F" >nul 2>nul
icacls ssl\hipaa_checklist.crt /inheritance:r /grant:r "%USERNAME%:F" >nul 2>nul

REM Clean up CSR file
del ssl\hipaa_checklist.csr

echo ✅ SSL certificates generated successfully!
echo 📁 Certificate files created in ssl\ directory:
echo    - hipaa_checklist.crt (certificate)
echo    - hipaa_checklist.key (private key)
echo.
echo ⚠️  Note: These are self-signed certificates for development only.
echo    Browsers will show a security warning - click 'Advanced' and 'Proceed' to continue.
echo.
echo 🚀 Next steps:
echo    1. Copy ssl\ directory to your nginx container or server
echo    2. Update nginx configuration to use these certificates
echo    3. Restart nginx service
echo.
pause
