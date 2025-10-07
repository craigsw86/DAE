# Nginx Reverse Proxy Configuration with Local HTTPS

## Overview
This document describes the complete setup for Nginx reverse proxy with local HTTPS using self-signed certificates for the HIPAA Checklist Project.

## Files Created/Configured

### 1. SSL Certificates
- **Location**: `ssl/` directory
- **Files**:
  - `hipaa_checklist.crt` - SSL certificate
  - `hipaa_checklist.key` - Private key
  - `hipaa_checklist.pfx` - PFX format certificate

### 2. Nginx Configuration
- **File**: `nginx-https.conf`
- **Features**:
  - HTTP to HTTPS redirect
  - SSL/TLS configuration with security headers
  - Rate limiting for API endpoints
  - Static file serving
  - Reverse proxy to Django backend

### 3. Docker Compose Configuration
- **File**: `docker-compose.nginx.yml`
- **Services**:
  - Nginx reverse proxy
  - Django backend
  - Volume mounts for SSL certificates and static files

## Setup Instructions

### Prerequisites
1. Docker Desktop installed and running
2. Frontend build available in `frontend/build/`
3. Django backend configured

### Step 1: Generate SSL Certificates
```bash
# Run the certificate generation script
powershell -ExecutionPolicy Bypass -File ssl\create_working_certs.ps1
```

### Step 2: Start Services
```bash
# Start all services with Docker Compose
docker-compose -f docker-compose.nginx.yml up --build -d
```

### Step 3: Verify Setup
```bash
# Run the HTTPS test script
python test_https_setup.py
```

## Configuration Details

### Nginx HTTPS Configuration
The `nginx-https.conf` includes:

1. **Security Headers**:
   - X-Frame-Options: DENY
   - X-Content-Type-Options: nosniff
   - X-XSS-Protection: 1; mode=block
   - Strict-Transport-Security: max-age=31536000

2. **SSL Configuration**:
   - TLS 1.2 and 1.3 protocols
   - Strong cipher suites
   - SSL session caching

3. **Rate Limiting**:
   - API endpoints: 10 requests/second
   - Login endpoints: 5 requests/minute
   - JWT token endpoint: 3 requests/minute

4. **Reverse Proxy**:
   - `/api/` → Django backend (port 8000)
   - `/admin/` → Django backend (port 8000)
   - `/static/` → Static files
   - `/` → React frontend

### SSL Certificate Details
- **Type**: Self-signed certificate
- **Subject**: CN=localhost, O=HIPAA Checklist
- **Key Length**: 2048 bits
- **Validity**: 1 year
- **Usage**: Development only

## Testing

### Manual Testing
1. Access `https://localhost` (accept security warning)
2. Verify HTTP redirects to HTTPS
3. Test API endpoints at `https://localhost/api/`
4. Check admin interface at `https://localhost/admin/`

### Automated Testing
Run the test script to verify:
- HTTP to HTTPS redirect
- HTTPS connection
- API endpoints accessibility
- Static files serving
- Security headers presence

## Security Considerations

### Development Setup
- Self-signed certificates are for development only
- Browsers will show security warnings
- Click "Advanced" and "Proceed" to continue

### Production Setup
For production, replace self-signed certificates with:
- Valid SSL certificates from a trusted CA
- Proper certificate management
- Regular certificate renewal

## Troubleshooting

### Common Issues
1. **Docker not running**: Start Docker Desktop
2. **Port conflicts**: Check if ports 80/443 are available
3. **Certificate errors**: Regenerate certificates
4. **Permission issues**: Check file permissions

### Logs
- Nginx logs: `docker logs hipaa_nginx`
- Django logs: `docker logs hipaa_django`

## File Structure
```
project/
 ssl/
    hipaa_checklist.crt
    hipaa_checklist.key
    hipaa_checklist.pfx
 nginx-https.conf
 docker-compose.nginx.yml
 test_https_setup.py
 frontend/build/
```

## Next Steps
1. Ensure Docker Desktop is running
2. Run the setup commands
3. Test the HTTPS configuration
4. Verify all endpoints are working
5. Document any issues or modifications needed
