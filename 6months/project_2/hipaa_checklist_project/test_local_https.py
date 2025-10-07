#!/usr/bin/env python3
"""
Local HTTPS testing server for HIPAA Checklist Project
This script creates a simple HTTPS server for testing the configuration
"""

import http.server
import ssl
import socketserver
import os
import sys
from pathlib import Path

def create_https_server():
    """Create a simple HTTPS server for testing"""
    
    # Set up paths
    frontend_build = Path("frontend/build")
    ssl_cert = Path("ssl/hipaa_checklist.crt")
    ssl_key = Path("ssl/hipaa_checklist.key")
    
    # Check if required files exist
    if not frontend_build.exists():
        print(" Frontend build directory not found!")
        print("   Please build the frontend first: cd frontend && npm run build")
        return False
    
    if not ssl_cert.exists() or not ssl_key.exists():
        print(" SSL certificate files not found!")
        print("   Please run: powershell -ExecutionPolicy Bypass -File ssl\\create_working_certs.ps1")
        return False
    
    # Change to frontend build directory
    os.chdir(frontend_build)
    
    # Create HTTPS server
    PORT = 8443
    
    class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # Add security headers
            self.send_header('X-Frame-Options', 'DENY')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-XSS-Protection', '1; mode=block')
            self.send_header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
            super().end_headers()
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            # Configure SSL
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(str(ssl_cert.absolute()), str(ssl_key.absolute()))
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            
            print(f" HTTPS Server started on https://localhost:{PORT}")
            print(" Serving files from frontend/build/")
            print(" Using self-signed SSL certificates")
            print("  Browser will show security warning - click 'Advanced' and 'Proceed'")
            print("\nPress Ctrl+C to stop the server")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n Server stopped by user")
        return True
    except Exception as e:
        print(f" Error starting server: {e}")
        return False

if __name__ == "__main__":
    print(" Starting Local HTTPS Test Server")
    print("=" * 50)
    
    success = create_https_server()
    sys.exit(0 if success else 1)
