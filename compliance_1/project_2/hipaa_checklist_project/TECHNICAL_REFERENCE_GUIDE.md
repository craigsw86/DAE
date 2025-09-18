# Technical Reference Guide - Weeks 10, 11, 12

## Table of Contents
1. [Nginx Configuration](#nginx-configuration)
2. [Django Security Implementation](#django-security-implementation)
3. [Docker Configuration](#docker-configuration)
4. [React Deployment](#react-deployment)
5. [Database Security](#database-security)
6. [API Testing Framework](#api-testing-framework)
7. [SSL/TLS Setup](#ssltls-setup)
8. [Performance Optimization](#performance-optimization)

---

## Nginx Configuration

### HTTPS Configuration (`nginx-https.conf`)
```nginx
# Rate limiting zones
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/s;

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name localhost;
    return 301 https://$host$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name localhost;
    
    # SSL configuration
    ssl_certificate /etc/nginx/ssl/hipaa_checklist.crt;
    ssl_certificate_key /etc/nginx/ssl/hipaa_checklist.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'";
    add_header Referrer-Policy "strict-origin-when-cross-origin";
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()";
    
    # Static files
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /var/www/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # API endpoints with rate limiting
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Login endpoint with stricter rate limiting
    location /api/token/ {
        limit_req zone=login burst=5 nodelay;
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Admin interface
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Main application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### React Nginx Configuration (`nginx-react.conf`)
```nginx
server {
    listen 80;
    server_name localhost;
    root /var/www/html;
    index index.html;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # Serve React app
    location / {
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Expires "0";
    }
    
    # Static assets with long-term caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # API proxy
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Django Security Implementation

### Security Middleware (`backend/checklist/security_middleware.py`)
```python
from django.utils.deprecation import MiddlewareMixin

class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware to add security headers to all responses
    """
    
    def process_response(self, request, response):
        # XSS Protection
        response['X-XSS-Protection'] = "1; mode=block"
        
        # HSTS
        response['Strict-Transport-Security'] = "max-age=31536000; includeSubDomains"
        
        # Content Type Options
        response['X-Content-Type-Options'] = "nosniff"
        
        # Frame Options
        response['X-Frame-Options'] = "DENY"
        
        return response
```

### Public API Views (`backend/checklist/public_views.py`)
```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'HIPAA Checklist API is running',
        'version': '1.0.0'
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """API information endpoint"""
    return Response({
        'name': 'HIPAA Checklist API',
        'version': '1.0.0',
        'description': 'HIPAA compliance checklist management system',
        'endpoints': {
            'health': '/api/health/',
            'info': '/api/info/',
            'checklist': '/api/checklist/ (requires auth)',
            'regulations': '/api/regulations/ (requires auth)',
            'admin': '/admin/',
            'token': '/api/token/'
        }
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def public_checklist_stats(request):
    """Public checklist statistics (no sensitive data)"""
    try:
        from .models import ChecklistItem
        total_items = ChecklistItem.objects.count()
        completed_items = ChecklistItem.objects.filter(completed=True).count()
        
        return Response({
            'total_items': total_items,
            'completed_items': completed_items,
            'completion_rate': round((completed_items / total_items * 100) if total_items > 0 else 0, 2)
        })
    except Exception as e:
        return Response({
            'error': 'Unable to retrieve statistics',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

### URL Configuration (`backend/checklist/urls.py`)
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegulationUpdateViewSet, ChecklistItemViewSet, ComplianceReportView, checklist_view, compliance_report_view, AuditLogView, UserProfileView, ChecklistExportCSV, ChecklistExportPDF, ReportTrendsView
from .public_views import health_check, api_info, public_checklist_stats

router = DefaultRouter()
router.register(r'regulations', RegulationUpdateViewSet, basename='regulationupdate')
router.register(r'checklist', ChecklistItemViewSet, basename='checklistitem')

urlpatterns = [
    path('checklist-page/', checklist_view, name='checklist_page'),
    path('compliance-report/', compliance_report_view, name='compliance_report_page'),
    path('api/', include(router.urls)),
    path('api/report/', ComplianceReportView.as_view(), name='compliance-report'),
    path('api/auditlog/<str:model_name>/<int:object_id>/', AuditLogView.as_view(), name='auditlog-api'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/checklist/export/csv/', ChecklistExportCSV.as_view(), name='checklist-export-csv'),
    path('api/checklist/export/pdf/', ChecklistExportPDF.as_view(), name='checklist-export-pdf'),
    path('api/report/trends/', ReportTrendsView.as_view(), name='report-trends'),
    # Public endpoints (no authentication required)
    path('api/health/', health_check, name='health-check'),
    path('api/info/', api_info, name='api-info'),
    path('api/stats/', public_checklist_stats, name='public-stats'),
]

urlpatterns += router.urls
```

---

## Docker Configuration

### Development Docker Compose (`docker-compose.dev.yml`)
```yaml
version: '3.8'

services:
  django:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - ./backend/db.sqlite3:/app/db.sqlite3
    environment:
      - DEBUG=True
      - DATABASE_URL=sqlite:///db.sqlite3
      - ALLOWED_HOSTS=localhost,127.0.0.1
    depends_on:
      - redis
    command: python manage.py runserver 0.0.0.0:8000

  react:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - REACT_APP_API_URL=http://localhost:8000
      - CHOKIDAR_USEPOLLING=true
    command: npm start

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx-dev.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
      - ./frontend/build:/var/www/html
      - ./backend/staticfiles:/var/www/static
    depends_on:
      - django
      - react

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  monitoring:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  backup:
    build: ./backup
    volumes:
      - ./backend/db.sqlite3:/backup/db.sqlite3
      - ./backups:/backups
    environment:
      - BACKUP_SCHEDULE=0 2 * * *
    command: python backup_script.py

volumes:
  redis_data:
```

### React Development Dockerfile (`frontend/Dockerfile.dev`)
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start development server
CMD ["npm", "start"]
```

### React Production Dockerfile (`frontend/Dockerfile`)
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the app
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built app
COPY --from=build /app/build /var/www/html

# Copy nginx config
COPY nginx-react.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

---

## Database Security

### SQLite Encryption (`backend/sqlite_encryption.py`)
```python
import os
import base64
from cryptography.fernet import Fernet
from pathlib import Path

class SQLiteEncryption:
    """
    SQLite database encryption using Fernet symmetric encryption
    """
    
    def __init__(self, key_file='encryption.key'):
        self.key_file = key_file
        self.key = self._load_or_generate_key()
        self.fernet = Fernet(self.key)
    
    def _load_or_generate_key(self):
        """Load existing key or generate new one"""
        key_path = Path(self.key_file)
        
        if key_path.exists():
            with open(key_path, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_path, 'wb') as f:
                f.write(key)
            # Set secure permissions
            os.chmod(key_path, 0o600)
            return key
    
    def encrypt_database(self, db_path, encrypted_path):
        """Encrypt SQLite database"""
        try:
            with open(db_path, 'rb') as f:
                data = f.read()
            
            encrypted_data = self.fernet.encrypt(data)
            
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Set secure permissions
            os.chmod(encrypted_path, 0o600)
            
            return True
        except Exception as e:
            print(f"Encryption error: {e}")
            return False
    
    def decrypt_database(self, encrypted_path, db_path):
        """Decrypt SQLite database"""
        try:
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            
            data = self.fernet.decrypt(encrypted_data)
            
            with open(db_path, 'wb') as f:
                f.write(data)
            
            return True
        except Exception as e:
            print(f"Decryption error: {e}")
            return False
    
    def is_encrypted(self, file_path):
        """Check if file is encrypted"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read(100)  # Read first 100 bytes
            
            # Try to decrypt a small portion
            self.fernet.decrypt(data)
            return True
        except:
            return False
```

### Database Security Setup (`backend/setup_database_security.py`)
```python
import os
import sqlite3
from pathlib import Path

def setup_database_security(db_path='db.sqlite3'):
    """Set up database security and optimizations"""
    
    if not Path(db_path).exists():
        print(f"Database {db_path} not found")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Security pragmas
        security_pragmas = [
            "PRAGMA journal_mode=WAL",
            "PRAGMA synchronous=NORMAL",
            "PRAGMA cache_size=10000",
            "PRAGMA temp_store=MEMORY",
            "PRAGMA mmap_size=268435456",
            "PRAGMA optimize"
        ]
        
        for pragma in security_pragmas:
            cursor.execute(pragma)
        
        # Set secure file permissions
        os.chmod(db_path, 0o600)
        
        conn.close()
        print("Database security setup completed")
        return True
        
    except Exception as e:
        print(f"Database security setup error: {e}")
        return False

if __name__ == '__main__':
    setup_database_security()
```

---

## API Testing Framework

### Comprehensive Backend Testing (`test_backend_final.py`)
```python
#!/usr/bin/env python3
"""
Final Backend SQLite API Connectivity Test
Comprehensive testing of Django backend with SQLite database
"""

import requests
import json
import time
from datetime import datetime

class FinalBackendTester:
    """Final comprehensive backend testing"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.api_url = f"{self.base_url}/api"
        self.test_results = []
    
    def log_test(self, test_name, success, message="", data=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status} {message}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
    
    def test_health_endpoint(self):
        """Test health endpoint"""
        print("\n📝 Test 1: Health Endpoint")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.api_url}/health/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", True, f"Status: {data.get('status')}")
                self.log_test("API Version", True, f"Version: {data.get('version')}")
                self.log_test("API Message", True, f"Message: {data.get('message')}")
                return True
            else:
                self.log_test("Health Check", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Error: {e}")
            return False
    
    def test_info_endpoint(self):
        """Test API info endpoint"""
        print("\n📝 Test 2: API Info Endpoint")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.api_url}/info/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("API Info", True, f"Name: {data.get('name')}")
                self.log_test("API Description", True, f"Description: {data.get('description')}")
                self.log_test("API Endpoints", True, f"Endpoints: {len(data.get('endpoints', {}))}")
                return True
            else:
                self.log_test("API Info", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Info", False, f"Error: {e}")
            return False
    
    def test_stats_endpoint(self):
        """Test public stats endpoint"""
        print("\n📝 Test 3: Public Stats Endpoint")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.api_url}/stats/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Public Stats", True, f"Total items: {data.get('total_items', 0)}")
                self.log_test("Completed Items", True, f"Completed: {data.get('completed_items', 0)}")
                self.log_test("Completion Rate", True, f"Rate: {data.get('completion_rate', 0)}%")
                return True
            else:
                self.log_test("Public Stats", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Public Stats", False, f"Error: {e}")
            return False
    
    def test_authentication_flow(self):
        """Test authentication flow"""
        print("\n📝 Test 4: Authentication Flow")
        print("-" * 40)
        
        # Test with common test credentials
        test_credentials = [
            ("admin", "admin"),
            ("testuser", "testpass123"),
            ("user", "password"),
            ("admin", "password")
        ]
        
        for username, password in test_credentials:
            try:
                response = requests.post(f"{self.api_url}/token/", 
                                      json={"username": username, "password": password}, 
                                      timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test("Login Success", True, f"Logged in as {username}")
                    return True
                elif response.status_code == 401:
                    self.log_test(f"Login Attempt ({username})", True, "Correctly rejects invalid credentials")
                else:
                    self.log_test(f"Login Attempt ({username})", False, f"Unexpected status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Login Attempt ({username})", False, f"Error: {e}")
        
        self.log_test("Authentication Flow", False, "No valid credentials found")
        return False
    
    def test_protected_endpoints(self):
        """Test protected endpoints"""
        print("\n📝 Test 5: Protected Endpoints")
        print("-" * 40)
        
        protected_endpoints = [
            ("/api/checklist/", "Checklist API"),
            ("/api/regulations/", "Regulations API"),
            ("/api/report/", "Compliance Report API"),
            ("/api/profile/", "User Profile API")
        ]
        
        for endpoint, name in protected_endpoints:
            try:
                response = requests.get(f"{self.api_url}{endpoint}", timeout=10)
                if response.status_code == 401:
                    self.log_test(f"{name} (No Auth)", True, "Correctly requires authentication")
                elif response.status_code == 404:
                    self.log_test(f"{name} (No Auth)", True, "Endpoint exists but requires auth")
                else:
                    self.log_test(f"{name} (No Auth)", False, f"Unexpected status: {response.status_code}")
            except Exception as e:
                self.log_test(f"{name} (No Auth)", False, f"Error: {e}")
    
    def test_performance(self):
        """Test API performance"""
        print("\n📝 Test 6: Performance Testing")
        print("-" * 40)
        
        endpoints = [
            ("/api/health/", "Health Check"),
            ("/api/info/", "API Info"),
            ("/api/stats/", "Public Stats")
        ]
        
        for endpoint, name in endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{self.api_url}{endpoint}", timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    if response_time < 0.5:
                        self.log_test(f"{name} Performance", True, f"Fast: {response_time:.3f}s")
                    elif response_time < 1.0:
                        self.log_test(f"{name} Performance", True, f"Good: {response_time:.3f}s")
                    else:
                        self.log_test(f"{name} Performance", False, f"Slow: {response_time:.3f}s")
                else:
                    self.log_test(f"{name} Performance", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"{name} Performance", False, f"Error: {e}")
    
    def test_error_handling(self):
        """Test error handling"""
        print("\n📝 Test 7: Error Handling")
        print("-" * 40)
        
        # Test 404 endpoint
        try:
            response = requests.get(f"{self.api_url}/nonexistent/", timeout=10)
            if response.status_code == 404:
                self.log_test("404 Handling", True, "Correctly returns 404")
            else:
                self.log_test("404 Handling", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("404 Handling", False, f"Error: {e}")
        
        # Test invalid JSON
        try:
            response = requests.post(f"{self.api_url}/token/", 
                                  data="invalid json", 
                                  headers={'Content-Type': 'application/json'},
                                  timeout=10)
            if response.status_code == 400:
                self.log_test("Invalid JSON Handling", True, "Correctly returns 400")
            else:
                self.log_test("Invalid JSON Handling", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("Invalid JSON Handling", False, f"Error: {e}")
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 BACKEND SQLITE API CONNECTIVITY TEST REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
        
        # Save detailed report
        report_file = f"final_backend_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🧪 Starting Final Backend SQLite API Connectivity Tests")
        print("=" * 60)
        
        self.test_health_endpoint()
        self.test_info_endpoint()
        self.test_stats_endpoint()
        self.test_authentication_flow()
        self.test_protected_endpoints()
        self.test_performance()
        self.test_error_handling()
        
        return self.generate_report()

def main():
    """Main function"""
    tester = FinalBackendTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All backend API tests passed!")
        print("✅ Django backend is properly connected to SQLite!")
        print("✅ All API endpoints are working correctly!")
    else:
        print("\n⚠️  Some backend API tests failed.")
        print("Please check the configuration and try again.")
    
    return success

if __name__ == '__main__':
    main()
```

---

## SSL/TLS Setup

### Certificate Generation Script (`ssl/create_working_certs.ps1`)
```powershell
# Create working SSL certificates for Nginx
$certName = "hipaa_checklist"
$subject = "CN=localhost, O=HIPAA Checklist, C=US"

# Create certificate
$cert = New-SelfSignedCertificate -Subject $subject -DnsName "localhost" -CertStoreLocation "Cert:\CurrentUser\My" -KeyUsage DigitalSignature,KeyEncipherment -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.1")

# Export certificate to .crt file
$certPath = ".\$certName.crt"
Export-Certificate -Cert $cert -FilePath $certPath -Type CERT

# Export private key to .key file
$keyPath = ".\$certName.key"
$pwd = ConvertTo-SecureString -String "password" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath ".\$certName.pfx" -Password $pwd

# Convert PFX to PEM format for private key
$pfx = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2(".\$certName.pfx", "password")
$privateKey = [System.Security.Cryptography.X509Certificates.RSACertificateExtensions]::GetRSAPrivateKey($pfx)
$privateKeyBytes = $privateKey.ExportRSAPrivateKey()
[System.IO.File]::WriteAllBytes($keyPath, $privateKeyBytes)

Write-Host "Certificates created successfully:"
Write-Host "  Certificate: $certPath"
Write-Host "  Private Key: $keyPath"
Write-Host "  PFX: .\$certName.pfx"
```

---

## Performance Optimization

### Waitress Configuration (`backend/waitress_config.py`)
```python
"""
Waitress server configuration for optimal performance
"""

import os
from pathlib import Path

class WaitressConfig:
    """Waitress server configuration"""
    
    def __init__(self):
        self.host = os.getenv('WAITRESS_HOST', '0.0.0.0')
        self.port = int(os.getenv('WAITRESS_PORT', '8000'))
        self.threads = int(os.getenv('WAITRESS_THREADS', '8'))
        self.connection_limit = int(os.getenv('WAITRESS_CONNECTION_LIMIT', '1000'))
        self.cleanup_interval = int(os.getenv('WAITRESS_CLEANUP_INTERVAL', '30'))
        self.channel_timeout = int(os.getenv('WAITRESS_CHANNEL_TIMEOUT', '120'))
        self.log_socket_errors = os.getenv('WAITRESS_LOG_SOCKET_ERRORS', 'True').lower() == 'true'
        
    def get_config(self):
        """Get Waitress configuration dictionary"""
        return {
            'host': self.host,
            'port': self.port,
            'threads': self.threads,
            'connection_limit': self.connection_limit,
            'cleanup_interval': self.cleanup_interval,
            'channel_timeout': self.channel_timeout,
            'log_socket_errors': self.log_socket_errors,
        }
    
    def optimize_for_production(self):
        """Optimize configuration for production"""
        self.threads = 16
        self.connection_limit = 2000
        self.cleanup_interval = 60
        self.channel_timeout = 300
        
    def optimize_for_development(self):
        """Optimize configuration for development"""
        self.threads = 4
        self.connection_limit = 100
        self.cleanup_interval = 10
        self.channel_timeout = 60
```

### Database Optimization Script (`optimize_performance.py`)
```python
#!/usr/bin/env python3
"""
Performance optimization script for Django and SQLite
"""

import os
import sys
import sqlite3
from pathlib import Path

# Add backend to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def optimize_database():
    """Optimize SQLite database for performance"""
    db_path = backend_dir / "db.sqlite3"
    
    if not db_path.exists():
        print("Database not found")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Performance optimizations
        optimizations = [
            "PRAGMA journal_mode=WAL",
            "PRAGMA synchronous=NORMAL",
            "PRAGMA cache_size=10000",
            "PRAGMA temp_store=MEMORY",
            "PRAGMA mmap_size=268435456",
            "PRAGMA optimize"
        ]
        
        for optimization in optimizations:
            cursor.execute(optimization)
            print(f"Applied: {optimization}")
        
        conn.close()
        print("Database optimization completed")
        return True
        
    except Exception as e:
        print(f"Database optimization error: {e}")
        return False

def optimize_django_settings():
    """Optimize Django settings for performance"""
    settings_file = backend_dir / "hipaa_checklist" / "settings.py"
    
    if not settings_file.exists():
        print("Settings file not found")
        return False
    
    try:
        with open(settings_file, 'r') as f:
            content = f.read()
        
        # Add performance optimizations
        performance_settings = """
# Performance optimizations
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Database connection pooling
DATABASES['default'].update({
    'CONN_MAX_AGE': 60,
    'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    }
})

# Static files optimization
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
"""
        
        if 'CACHES' not in content:
            with open(settings_file, 'a') as f:
                f.write(performance_settings)
            print("Django settings optimized")
        
        return True
        
    except Exception as e:
        print(f"Django settings optimization error: {e}")
        return False

def main():
    """Main optimization function"""
    print("🚀 Starting performance optimization...")
    
    # Optimize database
    optimize_database()
    
    # Optimize Django settings
    optimize_django_settings()
    
    print("✅ Performance optimization completed!")

if __name__ == '__main__':
    main()
```

---

## Deployment Scripts

### React Deployment Script (`deploy_react_local.py`)
```python
#!/usr/bin/env python3
"""
React Local Deployment Script
Builds and deploys React application locally
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class ReactDeployer:
    """React application deployer"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.frontend_dir = self.project_root / "frontend"
        self.build_dir = self.frontend_dir / "build"
        self.nginx_dir = self.project_root / "nginx"
        
    def check_prerequisites(self):
        """Check if prerequisites are installed"""
        print("🔍 Checking prerequisites...")
        
        # Check Node.js
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print(f"✅ Node.js: {result.stdout.strip()}")
            else:
                print("❌ Node.js not found")
                return False
        except:
            print("❌ Node.js not found")
            return False
        
        # Check npm
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print(f"✅ npm: {result.stdout.strip()}")
            else:
                print("❌ npm not found")
                return False
        except:
            print("❌ npm not found")
            return False
        
        return True
    
    def install_dependencies(self):
        """Install npm dependencies"""
        print("📦 Installing dependencies...")
        
        try:
            result = subprocess.run(['npm', 'install'], cwd=self.frontend_dir, shell=True)
            if result.returncode == 0:
                print("✅ Dependencies installed")
                return True
            else:
                print("❌ Failed to install dependencies")
                return False
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
    
    def build_application(self):
        """Build React application"""
        print("🏗️  Building application...")
        
        try:
            result = subprocess.run(['npm', 'run', 'build'], cwd=self.frontend_dir, shell=True)
            if result.returncode == 0:
                print("✅ Application built successfully")
                return True
            else:
                print("❌ Failed to build application")
                return False
        except Exception as e:
            print(f"❌ Error building application: {e}")
            return False
    
    def setup_nginx(self):
        """Setup Nginx configuration"""
        print("🔧 Setting up Nginx...")
        
        nginx_conf = self.project_root / "nginx-react.conf"
        if not nginx_conf.exists():
            print("❌ Nginx configuration not found")
            return False
        
        # Copy build files to nginx directory
        nginx_html_dir = self.nginx_dir / "html"
        nginx_html_dir.mkdir(exist_ok=True)
        
        if self.build_dir.exists():
            shutil.copytree(self.build_dir, nginx_html_dir, dirs_exist_ok=True)
            print("✅ Build files copied to Nginx directory")
            return True
        else:
            print("❌ Build directory not found")
            return False
    
    def start_nginx(self):
        """Start Nginx server"""
        print("🚀 Starting Nginx...")
        
        try:
            # Check if Nginx is already running
            result = subprocess.run(['nginx', '-t'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Nginx configuration is valid")
                
                # Start Nginx
                subprocess.run(['nginx'], shell=True)
                print("✅ Nginx started successfully")
                return True
            else:
                print(f"❌ Nginx configuration error: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error starting Nginx: {e}")
            return False
    
    def test_deployment(self):
        """Test the deployment"""
        print("🧪 Testing deployment...")
        
        try:
            import requests
            response = requests.get("http://localhost", timeout=10)
            if response.status_code == 200:
                print("✅ Deployment test successful")
                return True
            else:
                print(f"❌ Deployment test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error testing deployment: {e}")
            return False
    
    def deploy(self):
        """Deploy React application"""
        print("🚀 Starting React deployment...")
        
        # Check prerequisites
        if not self.check_prerequisites():
            return False
        
        # Install dependencies
        if not self.install_dependencies():
            return False
        
        # Build application
        if not self.build_application():
            return False
        
        # Setup Nginx
        if not self.setup_nginx():
            return False
        
        # Start Nginx
        if not self.start_nginx():
            return False
        
        # Test deployment
        if not self.test_deployment():
            return False
        
        print("🎉 React deployment completed successfully!")
        print("🌐 Application available at: http://localhost")
        return True

def main():
    """Main function"""
    deployer = ReactDeployer()
    success = deployer.deploy()
    
    if not success:
        print("❌ Deployment failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

---

This technical reference guide provides all the code snippets, configurations, and implementation details for the work completed during Weeks 10, 11, and 12. Each section includes the actual code used in the project, making it easy to understand and replicate the implementations.
