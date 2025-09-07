#!/usr/bin/env python3
"""
Production Server for HIPAA Checklist System
Uses Waitress WSGI server for better performance
"""

import os
import sys
import django
from waitress import serve

# Add backend to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

def optimize_database():
    """Optimize database for production"""
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Set production performance pragmas
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=50000")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.execute("PRAGMA mmap_size=1073741824")  # 1GB
        cursor.execute("PRAGMA optimize")
        print("Database optimized for production")

def main():
    """Start production server"""
    print("Starting HIPAA Checklist Production Server")
    print("Using Waitress WSGI server for optimal performance")
    
    # Optimize database
    optimize_database()
    
    # Import Django application
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    # Start Waitress server with production settings
    print("Server starting on http://0.0.0.0:8000")
    print("Press Ctrl+C to stop the server")
    
    serve(
        application,
        host='0.0.0.0',
        port=8000,
        threads=4,  # Multi-threaded for better performance
        connection_limit=100,
        cleanup_interval=30,
        send_bytes=18000,
        channel_timeout=120,
        log_socket_errors=True
    )

if __name__ == "__main__":
    main()
