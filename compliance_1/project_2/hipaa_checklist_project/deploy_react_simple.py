#!/usr/bin/env python3
"""
Simple React Local Deployment (without Docker)
Uses Python's built-in HTTP server to serve React build
"""

import os
import sys
import subprocess
import shutil
import time
import requests
import threading
import http.server
import socketserver
from pathlib import Path

class SimpleReactDeployer:
    """Simple React deployment without Docker"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.frontend_dir = self.project_root / "frontend"
        self.build_dir = self.frontend_dir / "build"
        self.serve_dir = self.project_root / "react_serve"
        self.server_thread = None
        self.server = None
        self.port = 8080
    
    def log(self, message, level="INFO"):
        """Log messages with timestamp"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        self.log("Checking prerequisites...")
        
        # Check if Node.js is installed
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=10, shell=True)
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
    
    def setup_serving_directory(self):
        """Set up directory for serving React build"""
        self.log("Setting up serving directory...")
        
        # Create serving directory
        self.serve_dir.mkdir(exist_ok=True)
        
        # Copy React build to serving directory
        if self.serve_dir.exists():
            shutil.rmtree(self.serve_dir)
        
        shutil.copytree(self.build_dir, self.serve_dir)
        self.log(f"React build copied to {self.serve_dir}")
        
        return True
    
    def start_server(self):
        """Start HTTP server for React build"""
        self.log(f"Starting HTTP server on port {self.port}...")
        
        try:
            os.chdir(self.serve_dir)
            
            # Create custom handler for SPA routing
            class SPAHandler(http.server.SimpleHTTPRequestHandler):
                def end_headers(self):
                    # Add CORS headers
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
                    self.send_header('Access-Control-Allow-Headers', 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization')
                    super().end_headers()
                
                def do_GET(self):
                    # Handle SPA routing - serve index.html for all routes
                    if not self.path.startswith('/static/') and not self.path.endswith(('.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.woff', '.woff2', '.ttf', '.eot')):
                        self.path = '/index.html'
                    super().do_GET()
            
            # Start server in a separate thread
            self.server = socketserver.TCPServer(("", self.port), SPAHandler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            self.log(f"HTTP server started successfully on http://localhost:{self.port}")
            return True
            
        except Exception as e:
            self.log(f"Failed to start server: {e}", "ERROR")
            return False
        finally:
            os.chdir(self.project_root)
    
    def test_deployment(self):
        """Test the React deployment"""
        self.log("Testing React deployment...")
        
        # Wait for server to start
        time.sleep(2)
        
        try:
            # Test main page
            response = requests.get(f"http://localhost:{self.port}/", timeout=10)
            if response.status_code == 200:
                content = response.text.lower()
                if 'react' in content or 'root' in content or 'app' in content:
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
        self.log("Starting simple React local deployment...")
        
        if not self.check_prerequisites():
            return False
        
        if not self.install_dependencies():
            return False
        
        if not self.build_react_app():
            return False
        
        if not self.setup_serving_directory():
            return False
        
        if not self.start_server():
            return False
        
        if not self.test_deployment():
            self.log("Deployment completed with warnings", "WARNING")
        else:
            self.log("Deployment completed successfully!")
        
        self.log(f"React app is now available at: http://localhost:{self.port}")
        self.log("Press Ctrl+C to stop the server")
        
        return True
    
    def stop_server(self):
        """Stop the HTTP server"""
        if self.server:
            self.log("Stopping HTTP server...")
            self.server.shutdown()
            self.server.server_close()
            self.log("Server stopped")

def main():
    """Main function"""
    deployer = SimpleReactDeployer()
    
    try:
        success = deployer.deploy()
        if success:
            # Keep server running
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        deployer.stop_server()
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        deployer.stop_server()

if __name__ == '__main__':
    main()
