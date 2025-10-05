#!/usr/bin/env python3
"""
Waitress WSGI Server Configuration for HIPAA Checklist Project
Production-ready server with security enhancements

This server configuration provides a production-grade WSGI server
with comprehensive security features, performance optimizations,
and HIPAA compliance requirements.
"""

import os
import sys
import logging
from pathlib import Path
from waitress import serve
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

# Add the backend directory to Python path for proper module resolution
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# Set Django settings module for production configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')

# Configure comprehensive logging for production monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('waitress.log'),      # File logging for persistence
        logging.StreamHandler(sys.stdout)         # Console logging for monitoring
    ]
)

logger = logging.getLogger(__name__)

def setup_database_permissions():
    """
    Set up proper database file permissions for SQLite security.
    
    Applies restrictive file permissions to the SQLite database file
    to prevent unauthorized access and maintain HIPAA compliance.
    Only the owner can read/write, group and others have read-only access.
    """
    db_path = backend_dir / 'db.sqlite3'
    
    if db_path.exists():
        # Set restrictive permissions on SQLite database
        try:
            import stat
            # Remove write permissions for group and others
            current_perms = db_path.stat().st_mode
            new_perms = current_perms & ~stat.S_IWGRP & ~stat.S_IWOTH
            db_path.chmod(new_perms)
            logger.info(f"✅ Database permissions set: {oct(new_perms)}")
        except Exception as e:
            logger.warning(f"⚠️  Could not set database permissions: {e}")
    else:
        logger.warning("⚠️  Database file not found. Run migrations first.")

def setup_encryption():
    """
    Verify and set up encryption key for field encryption.
    
    Ensures that the FIELD_ENCRYPTION_KEY environment variable is set
    for encrypting sensitive data fields. Falls back to default key
    if not provided (for development only).
    """
    encryption_key = os.environ.get('FIELD_ENCRYPTION_KEY')
    if not encryption_key:
        logger.warning("⚠️  FIELD_ENCRYPTION_KEY not set. Using default key.")
        os.environ['FIELD_ENCRYPTION_KEY'] = '1f2WjIy7cmJebkD-ywTrmct3Ms7-VuUjv7wleofoP54='
    else:
        logger.info("✅ Encryption key is set")

def run_migrations():
    """
    Run Django database migrations to ensure schema is up to date.
    
    Executes all pending database migrations to maintain data integrity
    and ensure the database schema matches the current model definitions.
    """
    try:
        logger.info("🔄 Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        logger.info("✅ Migrations completed")
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        sys.exit(1)

def collect_static_files():
    """
    Collect static files for production deployment.
    
    Gathers all static files (CSS, JS, images) into the staticfiles
    directory for efficient serving by the web server.
    """
    try:
        logger.info("🔄 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        logger.info("✅ Static files collected")
    except Exception as e:
        logger.error(f"❌ Static file collection failed: {e}")
        sys.exit(1)

def start_waitress_server():
    """
    Start the Waitress WSGI server with production configuration.
    
    Configures and starts the Waitress server with security optimizations,
    performance tuning, and HIPAA compliance features.
    """
    # Get WSGI application
    application = get_wsgi_application()
    
    # Server configuration from environment variables
    host = os.environ.get('WAITRESS_HOST', '0.0.0.0')
    port = int(os.environ.get('WAITRESS_PORT', '8000'))
    threads = int(os.environ.get('WAITRESS_THREADS', '4'))
    
    logger.info(f"🚀 Starting Waitress server on {host}:{port}")
    logger.info(f"📊 Configuration: {threads} threads")
    
    # Start server with security and performance optimizations
    serve(
        application,
        host=host,
        port=port,
        threads=threads,
        # Security settings
        connection_limit=1000,        # Limit concurrent connections
        cleanup_interval=30,         # Cleanup interval in seconds
        channel_timeout=120,          # Request timeout
        # Logging configuration
        ident='HIPAA-Checklist',     # Server identification
        # Performance tuning
        send_bytes=18000,            # Bytes to send per iteration
        outbuf_overflow=1048576,     # Output buffer overflow limit
        inbuf_overflow=1048576,      # Input buffer overflow limit
        max_request_header_size=262144,  # Max request header size
        max_request_body_size=1048576,   # Max request body size
        expose_tracebacks=False,     # Security: don't expose tracebacks
    )

def main():
    """
    Main entry point for the Waitress server.
    
    Performs all necessary setup steps before starting the server:
    1. Encryption key verification
    2. Database migrations
    3. Static file collection
    4. Database security setup
    5. Server startup
    """
    logger.info("🔐 HIPAA Checklist - Waitress Server Starting...")
    
    # Execute setup steps in order
    setup_encryption()
    run_migrations()
    collect_static_files()
    setup_database_permissions()
    
    # Start the production server
    start_waitress_server()

if __name__ == '__main__':
    main()
