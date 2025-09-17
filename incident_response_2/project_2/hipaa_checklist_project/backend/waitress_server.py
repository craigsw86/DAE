#!/usr/bin/env python3
"""
Waitress WSGI Server Configuration for HIPAA Checklist Project
Production-ready server with security enhancements
"""

import os
import sys
import logging
from pathlib import Path
from waitress import serve
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('waitress.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def setup_database_permissions():
    """Set up proper database file permissions for SQLite"""
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
    """Verify encryption key is properly set"""
    encryption_key = os.environ.get('FIELD_ENCRYPTION_KEY')
    if not encryption_key:
        logger.warning("⚠️  FIELD_ENCRYPTION_KEY not set. Using default key.")
        os.environ['FIELD_ENCRYPTION_KEY'] = '1f2WjIy7cmJebkD-ywTrmct3Ms7-VuUjv7wleofoP54='
    else:
        logger.info("✅ Encryption key is set")

def run_migrations():
    """Run database migrations"""
    try:
        logger.info("🔄 Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        logger.info("✅ Migrations completed")
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        sys.exit(1)

def collect_static_files():
    """Collect static files for production"""
    try:
        logger.info("🔄 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        logger.info("✅ Static files collected")
    except Exception as e:
        logger.error(f"❌ Static file collection failed: {e}")
        sys.exit(1)

def start_waitress_server():
    """Start the Waitress WSGI server"""
    # Get WSGI application
    application = get_wsgi_application()
    
    # Server configuration
    host = os.environ.get('WAITRESS_HOST', '0.0.0.0')
    port = int(os.environ.get('WAITRESS_PORT', '8000'))
    threads = int(os.environ.get('WAITRESS_THREADS', '4'))
    
    logger.info(f"🚀 Starting Waitress server on {host}:{port}")
    logger.info(f"📊 Configuration: {threads} threads")
    
    # Security headers and settings
    serve(
        application,
        host=host,
        port=port,
        threads=threads,
        # Security settings
        connection_limit=1000,
        cleanup_interval=30,
        channel_timeout=120,
        # Logging
        ident='HIPAA-Checklist',
        # Performance tuning
        send_bytes=18000,
        outbuf_overflow=1048576,
        inbuf_overflow=1048576,
        max_request_header_size=262144,
        max_request_body_size=1048576,
        expose_tracebacks=False,  # Security: don't expose tracebacks
    )

def main():
    """Main entry point"""
    logger.info("🔐 HIPAA Checklist - Waitress Server Starting...")
    
    # Setup steps
    setup_encryption()
    run_migrations()
    collect_static_files()
    setup_database_permissions()
    
    # Start server
    start_waitress_server()

if __name__ == '__main__':
    main()
