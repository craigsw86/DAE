#!/usr/bin/env python3
"""
React Local Deployment Script
Builds React app and serves via Nginx
"""

import os
import sys
import subprocess
import shutil
import time
import requests
from pathlib import Path

class ReactLocalDeployer:
    """React local deployment manager"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.frontend_dir = self.project_root / "frontend"
        self.build_dir = self.frontend_dir / "build"
        self.nginx_dir = self.project_root / "nginx_serve"
        
    def log(self, message, level="INFO"):
        """Log messages with timestamp"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        self.log("Checking prerequisites...")
        
        # Check if Node.js is installed
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log(f"Node.js version: {result.stdout.strip()}")
            else:
                self.log("Node.js not found", "ERROR")
                return False
        except Exception as e:
            self.log(f"Node.js check failed: {e}", "ERROR")
            return False
        
        # Check if npm is installed
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=10, shell=True)
            if result.returncode == 0:
                self.log(f"npm version: {result.stdout.strip()}")
            else:
                self.log("npm not found", "ERROR")
                return False
        except Exception as e:
            self.log(f"npm check failed: {e}", "ERROR")
            return False
        
        # Check if frontend directory exists
        if not self.frontend_dir.exists():
            self.log("Frontend directory not found", "ERROR")
            return False
        
        # Check if package.json exists
        package_json = self.frontend_dir / "package.json"
        if not package_json.exists():
            self.log("package.json not found", "ERROR")
            return False
        
        self.log("All prerequisites met")
        return True
    
    def install_dependencies(self):
        """Install npm dependencies"""
        self.log("Installing npm dependencies...")
        
        try:
            os.chdir(self.frontend_dir)
            result = subprocess.run(['npm', 'install'], capture_output=True, text=True, timeout=300, shell=True)
            
            if result.returncode == 0:
                self.log("Dependencies installed successfully")
                return True
            else:
                self.log(f"Dependency installation failed: {result.stderr}", "ERROR")
                return False
        except Exception as e:
            self.log(f"Dependency installation error: {e}", "ERROR")
            return False
        finally:
            os.chdir(self.project_root)
    
    def build_react_app(self):
        """Build React application"""
        self.log("Building React application...")
        
        try:
            os.chdir(self.frontend_dir)
            
            # Clean previous build
            if self.build_dir.exists():
                shutil.rmtree(self.build_dir)
                self.log("Cleaned previous build")
            
            # Build the app
            result = subprocess.run(['npm', 'run', 'build'], capture_output=True, text=True, timeout=300, shell=True)
            
            if result.returncode == 0:
                self.log("React app built successfully")
                
                # Check build output
                if self.build_dir.exists():
                    build_files = list(self.build_dir.rglob('*'))
                    self.log(f"Build created with {len(build_files)} files")
                    return True
                else:
                    self.log("Build directory not created", "ERROR")
                    return False
            else:
                self.log(f"Build failed: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Build error: {e}", "ERROR")
            return False
        finally:
            os.chdir(self.project_root)
    
    def setup_nginx_serving(self):
        """Set up Nginx for serving React build"""
        self.log("Setting up Nginx serving...")
        
        # Create nginx serving directory
        self.nginx_dir.mkdir(exist_ok=True)
        
        # Copy React build to nginx directory
        nginx_html_dir = self.nginx_dir / "html"
        if nginx_html_dir.exists():
            shutil.rmtree(nginx_html_dir)
        
        shutil.copytree(self.build_dir, nginx_html_dir)
        self.log(f"React build copied to {nginx_html_dir}")
        
        # Create nginx configuration for local serving
        nginx_conf = self.nginx_dir / "nginx.conf"
        nginx_config = f"""
worker_processes 1;

events {{
    worker_connections 1024;
}}

http {{
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    
    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # Upstream for Django backend
    upstream django_backend {{
        server host.docker.internal:8000;
    }}

    server {{
        listen 80;
        server_name localhost;
        
        # Root directory for React build
        root /usr/share/nginx/html;
        index index.html;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        
        # API routes to Django backend
        location /api/ {{
            proxy_pass http://django_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
            
            # CORS headers
            add_header Access-Control-Allow-Origin "*" always;
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
            add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization" always;
        }}
        
        # Admin routes to Django backend
        location /admin/ {{
            proxy_pass http://django_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
        }}
        
        # Static files with caching
        location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {{
            expires 1y;
            add_header Cache-Control "public, immutable";
        }}
        
        # React app - serve index.html for all routes
        location / {{
            try_files $uri $uri/ /index.html;
        }}
        
        # Health check
        location /health {{
            access_log off;
            return 200 "healthy\\n";
            add_header Content-Type text/plain;
        }}
    }}
}}
"""
        
        with open(nginx_conf, 'w') as f:
            f.write(nginx_config)
        
        self.log(f"Nginx configuration created: {nginx_conf}")
        return True
    
    def start_nginx_container(self):
        """Start Nginx container for serving React"""
        self.log("Starting Nginx container...")
        
        try:
            # Stop any existing container
            subprocess.run(['docker', 'stop', 'hipaa-react-nginx'], 
                         capture_output=True, timeout=10)
            subprocess.run(['docker', 'rm', 'hipaa-react-nginx'], 
                         capture_output=True, timeout=10)
            
            # Start new container
            cmd = [
                'docker', 'run', '-d',
                '--name', 'hipaa-react-nginx',
                '-p', '80:80',
                '-v', f'{self.nginx_dir}/html:/usr/share/nginx/html:ro',
                '-v', f'{self.nginx_dir}/nginx.conf:/etc/nginx/nginx.conf:ro',
                'nginx:alpine'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log("Nginx container started successfully")
                return True
            else:
                self.log(f"Failed to start Nginx container: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Nginx container error: {e}", "ERROR")
            return False
    
    def test_deployment(self):
        """Test the React deployment"""
        self.log("Testing React deployment...")
        
        # Wait for container to start
        time.sleep(5)
        
        try:
            # Test health endpoint
            response = requests.get("http://localhost/health", timeout=10)
            if response.status_code == 200:
                self.log("Health check passed")
            else:
                self.log(f"Health check failed: {response.status_code}", "WARNING")
            
            # Test React app
            response = requests.get("http://localhost/", timeout=10)
            if response.status_code == 200:
                if "react" in response.text.lower() or "root" in response.text.lower():
                    self.log("React app is serving correctly")
                    return True
                else:
                    self.log("React app not detected in response", "WARNING")
                    return False
            else:
                self.log(f"React app test failed: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Deployment test failed: {e}", "ERROR")
            return False
    
    def deploy(self):
        """Deploy React app locally"""
        self.log("Starting React local deployment...")
        
        if not self.check_prerequisites():
            return False
        
        if not self.install_dependencies():
            return False
        
        if not self.build_react_app():
            return False
        
        if not self.setup_nginx_serving():
            return False
        
        if not self.start_nginx_container():
            return False
        
        if not self.test_deployment():
            self.log("Deployment completed with warnings", "WARNING")
        else:
            self.log("Deployment completed successfully!")
        
        self.log("React app is now available at: http://localhost")
        self.log("Health check available at: http://localhost/health")
        
        return True
    
    def stop_deployment(self):
        """Stop the React deployment"""
        self.log("Stopping React deployment...")
        
        try:
            subprocess.run(['docker', 'stop', 'hipaa-react-nginx'], 
                         capture_output=True, timeout=10)
            subprocess.run(['docker', 'rm', 'hipaa-react-nginx'], 
                         capture_output=True, timeout=10)
            self.log("React deployment stopped")
        except Exception as e:
            self.log(f"Error stopping deployment: {e}", "ERROR")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "stop":
        deployer = ReactLocalDeployer()
        deployer.stop_deployment()
    else:
        deployer = ReactLocalDeployer()
        success = deployer.deploy()
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
