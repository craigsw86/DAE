# HIPAA Checklist Project - Setup and Installation Guide
## Complete Installation and Configuration Manual

**Version**: 1.0  
**Date**: September 7, 2025  
**Project**: HIPAA Checklist Management System  

---

##  Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Database Setup](#database-setup)
5. [Security Configuration](#security-configuration)
6. [Server Setup](#server-setup)
7. [Frontend Setup](#frontend-setup)
8. [SSL/HTTPS Setup](#sslhttps-setup)
9. [Docker Setup](#docker-setup)
10. [Verification](#verification)
11. [Troubleshooting](#troubleshooting)

---

##  System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **Docker**: 20.10+ (optional)

### Recommended Requirements
- **OS**: Windows 11, macOS 12+, or Linux (Ubuntu 22.04+)
- **RAM**: 16GB
- **Storage**: 10GB free space
- **Python**: 3.11
- **Node.js**: 18.0+
- **Docker**: 24.0+

---

##  Installation Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/your-org/hipaa-checklist-project.git
cd hipaa-checklist-project
```

### Step 2: Backend Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

### Step 3: Frontend Setup
```bash
# Install Node.js dependencies
cd frontend
npm install
```

### Step 4: Database Setup
```bash
# Run migrations
cd backend
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

##  Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Security
FIELD_ENCRYPTION_KEY=your-encryption-key-here
DB_ENCRYPTION_PASSWORD=your-db-password-here

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-here
JWT_ACCESS_TOKEN_LIFETIME=3600
JWT_REFRESH_TOKEN_LIFETIME=86400

# Email Settings (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Django Settings
Key settings in `backend/hipaa_checklist/settings.py`:

```python
# Security Settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Database Encryption
FIELD_ENCRYPTION_KEY = os.environ.get('FIELD_ENCRYPTION_KEY')

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}
```

---

##  Database Setup

### SQLite Configuration (Default)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### PostgreSQL Configuration (Production)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hipaa_checklist',
        'USER': 'your-username',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Database Encryption Setup
```bash
# Run encryption setup
python backend/sqlite_encryption.py

# Verify encryption
python backend/check_database_schema.py
```

---

##  Security Configuration

### SSL/TLS Setup
```bash
# Generate SSL certificates
cd ssl
powershell -ExecutionPolicy Bypass -File create_working_certs.ps1

# Verify certificates
openssl x509 -in hipaa_checklist.crt -text -noout
```

### File Permissions
```bash
# Set secure permissions
python fix_permissions.py

# Verify permissions
ls -la backend/db.sqlite3*
ls -la ssl/hipaa_checklist.key
```

### Security Headers
Verify security headers in `backend/checklist/security_middleware.py`:

```python
security_headers = {
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'",
    'Referrer-Policy': 'strict-origin-when-cross-origin',
}
```

---

##  Server Setup

### Development Server
```bash
# Start Django development server
cd backend
python manage.py runserver 8000

# Start React development server
cd frontend
npm start
```

### Production Server (Waitress)
```bash
# Install Waitress
pip install waitress

# Start production server
cd backend
python waitress_secure.py
```

### Nginx Configuration
```bash
# Copy Nginx configuration
cp nginx-https.conf /etc/nginx/sites-available/hipaa-checklist
ln -s /etc/nginx/sites-available/hipaa-checklist /etc/nginx/sites-enabled/

# Test configuration
nginx -t

# Restart Nginx
systemctl restart nginx
```

---

##  Frontend Setup

### Development Build
```bash
cd frontend
npm install
npm start
```

### Production Build
```bash
cd frontend
npm run build
```

### Environment Configuration
Create `.env` file in frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_VERSION=1.0.0
REACT_APP_ENVIRONMENT=development
```

---

##  SSL/HTTPS Setup

### Self-Signed Certificates (Development)
```bash
# Generate certificates
cd ssl
openssl req -x509 -newkey rsa:2048 -keyout hipaa_checklist.key -out hipaa_checklist.crt -days 365 -nodes

# Convert to PFX (Windows)
openssl pkcs12 -export -out hipaa_checklist.pfx -inkey hipaa_checklist.key -in hipaa_checklist.crt
```

### Production Certificates
```bash
# Using Let's Encrypt
certbot --nginx -d your-domain.com

# Using commercial CA
# Follow your CA's instructions for certificate installation
```

### Nginx HTTPS Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/hipaa_checklist.crt;
    ssl_certificate_key /path/to/hipaa_checklist.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

##  Docker Setup

### Development Environment
```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up --build

# Access services
# Django: http://localhost:8000
# React: http://localhost:3000
# Nginx: http://localhost:80
```

### Production Environment
```bash
# Start production environment
docker-compose -f docker-compose.yml up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Docker Commands
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Stop services
docker-compose down

# Update services
docker-compose pull
docker-compose up -d
```

---

##  Verification

### System Health Check
```bash
# Run comprehensive health check
python security_verification_final.py

# Run sample data testing
python sample_data_testing.py

# Run OWASP security audit
python owasp_zap_security_audit.py
```

### Manual Verification
1. **Access Application**: Navigate to `https://localhost` or `http://localhost:8000`
2. **Test Authentication**: Try logging in with admin credentials
3. **Test API Endpoints**: Use API testing tools or browser
4. **Verify SSL**: Check certificate validity in browser
5. **Test Export**: Try exporting data in CSV/PDF format

### Performance Testing
```bash
# Run performance tests
python test_performance.py

# Check database performance
python check_database_schema.py
```

---

##  Troubleshooting

### Common Issues

#### 1. Django Server Won't Start
```bash
# Check for port conflicts
netstat -an | findstr :8000

# Kill existing processes
taskkill /F /PID <process_id>

# Check Django settings
python manage.py check
```

#### 2. Database Connection Issues
```bash
# Check database file permissions
ls -la backend/db.sqlite3

# Reset database
rm backend/db.sqlite3
python manage.py migrate
```

#### 3. SSL Certificate Issues
```bash
# Regenerate certificates
cd ssl
rm *.crt *.key *.pfx
powershell -ExecutionPolicy Bypass -File create_working_certs.ps1
```

#### 4. Frontend Build Issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 5. Permission Issues
```bash
# Fix file permissions
python fix_permissions.py

# Check directory permissions
ls -la backend/
ls -la ssl/
```

### Log Files
- **Django Logs**: `backend/logs/django.log`
- **Nginx Logs**: `/var/log/nginx/access.log`, `/var/log/nginx/error.log`
- **System Logs**: Check system event logs

### Support Resources
- **Documentation**: `docs/` directory
- **Issue Tracking**: GitHub Issues
- **Security Reports**: `security_verification_report_*.json`
- **Test Reports**: `*_test_report_*.json`

---

##  Support and Maintenance

### Getting Help
1. **Check Documentation**: Review all documentation in `docs/` directory
2. **Run Diagnostics**: Use provided testing scripts
3. **Check Logs**: Review application and system logs
4. **Contact Support**: Use GitHub Issues for bug reports

### Regular Maintenance
- **Daily**: Check application logs and system health
- **Weekly**: Review security logs and update dependencies
- **Monthly**: Run security audits and performance tests
- **Quarterly**: Update SSL certificates and review configurations

---

*Setup Guide Version: 1.0*  
*Last Updated: September 7, 2025*  
*Project: HIPAA Checklist Management System*
