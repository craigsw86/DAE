#!/usr/bin/env python3
"""
Secure Waitress WSGI Server Configuration for HIPAA Checklist Project
Enhanced with SQLite encryption and comprehensive security features
"""

import os
import sys
import logging
import signal
import time
from pathlib import Path
from waitress import serve
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line
from sqlite_encryption import DatabaseSecurityManager

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')

# Configure comprehensive logging
log_dir = backend_dir / 'logs'
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'waitress_secure.log'),
        logging.FileHandler(log_dir / 'security.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
security_logger = logging.getLogger('security')

class SecureWaitressServer:
    """Secure Waitress server with encryption and monitoring"""
    
    def __init__(self):
        self.db_path = backend_dir / 'db.sqlite3'
        self.db_manager = DatabaseSecurityManager(self.db_path)
        self.server_process = None
        self.running = False
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"🛑 Received signal {signum}, shutting down gracefully...")
        self.running = False
        sys.exit(0)
    
    def setup_environment(self):
        """Set up secure environment variables"""
        # Encryption key for field encryption
        if not os.environ.get('FIELD_ENCRYPTION_KEY'):
            os.environ['FIELD_ENCRYPTION_KEY'] = '1f2WjIy7cmJebkD-ywTrmct3Ms7-VuUjv7wleofoP54='
            logger.info("✅ Field encryption key set")
        
        # Database encryption password
        if not os.environ.get('DB_ENCRYPTION_PASSWORD'):
            os.environ['DB_ENCRYPTION_PASSWORD'] = 'hipaa_secure_password_2024'
            logger.info("✅ Database encryption password set")
        
        # Security settings
        os.environ['DJANGO_SETTINGS_MODULE'] = 'hipaa_checklist.settings'
        
        # Disable debug in production
        if os.environ.get('ENVIRONMENT') == 'production':
            os.environ['DEBUG'] = 'False'
            logger.info("🔒 Production mode enabled")
    
    def setup_database_security(self):
        """Set up database encryption and security"""
        logger.info("🔐 Setting up database security...")
        
        # Check if we need to restore from encrypted version
        if not self.db_path.exists() and self.db_manager.encryption.encrypted_db_path.exists():
            logger.info("🔄 Restoring database from encrypted version...")
            if not self.db_manager.restore_database():
                logger.error("❌ Failed to restore database")
                return False
        
        # Set up encryption if not already encrypted
        if self.db_path.exists() and not self.db_manager.encryption.verify_encryption():
            logger.info("🔐 Encrypting database...")
            if not self.db_manager.setup_secure_database():
                logger.error("❌ Failed to encrypt database")
                return False
        
        # Set secure file permissions
        self._set_secure_permissions()
        
        logger.info("✅ Database security configured")
        return True
    
    def _set_secure_permissions(self):
        """Set secure file permissions for database and logs"""
        try:
            import stat
            
            # Database permissions
            if self.db_path.exists():
                current_perms = self.db_path.stat().st_mode
                new_perms = current_perms & ~stat.S_IWGRP & ~stat.S_IWOTH & ~stat.S_IRGRP & ~stat.S_IROTH
                self.db_path.chmod(new_perms)
                logger.info(f"✅ Database permissions: {oct(new_perms)}")
            
            # Log directory permissions
            if log_dir.exists():
                current_perms = log_dir.stat().st_mode
                new_perms = current_perms & ~stat.S_IWGRP & ~stat.S_IWOTH & ~stat.S_IRGRP & ~stat.S_IROTH
                log_dir.chmod(new_perms)
                logger.info(f"✅ Log directory permissions: {oct(new_perms)}")
                
        except Exception as e:
            logger.warning(f"⚠️  Could not set permissions: {e}")
    
    def run_migrations(self):
        """Run database migrations"""
        try:
            logger.info("🔄 Running database migrations...")
            execute_from_command_line(['manage.py', 'migrate'])
            logger.info("✅ Migrations completed")
            return True
        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            return False
    
    def collect_static_files(self):
        """Collect static files for production"""
        try:
            logger.info("🔄 Collecting static files...")
            execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
            logger.info("✅ Static files collected")
            return True
        except Exception as e:
            logger.error(f"❌ Static file collection failed: {e}")
            return False
    
    def setup_security_headers(self):
        """Configure security headers and settings"""
        # Add security middleware
        security_settings = {
            'SECURE_BROWSER_XSS_FILTER': True,
            'SECURE_CONTENT_TYPE_NOSNIFF': True,
            'X_FRAME_OPTIONS': 'DENY',
            'SECURE_HSTS_SECONDS': 31536000,
            'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
            'SECURE_HSTS_PRELOAD': True,
        }
        
        for setting, value in security_settings.items():
            os.environ[f'DJANGO_{setting}'] = str(value)
        
        logger.info("✅ Security headers configured")
    
    def start_server(self):
        """Start the Waitress server with security enhancements"""
        # Get WSGI application
        application = get_wsgi_application()
        
        # Server configuration
        host = os.environ.get('WAITRESS_HOST', '0.0.0.0')
        port = int(os.environ.get('WAITRESS_PORT', '8000'))
        threads = int(os.environ.get('WAITRESS_THREADS', '4'))
        
        logger.info(f"🚀 Starting Secure Waitress server on {host}:{port}")
        logger.info(f"📊 Configuration: {threads} threads")
        logger.info(f"🔐 Database: {'Encrypted' if self.db_manager.encryption.verify_encryption() else 'Plaintext'}")
        
        # Security and performance settings
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
            ident='HIPAA-Checklist-Secure',
            # Performance tuning
            send_bytes=18000,
            outbuf_overflow=1048576,
            inbuf_overflow=1048576,
            max_request_header_size=262144,
            max_request_body_size=1048576,
            expose_tracebacks=False,  # Security: don't expose tracebacks
            # Additional security
            asyncore_use_poll=True,
            recv_bytes=8192,
        )
    
    def run(self):
        """Main run method"""
        logger.info("🔐 HIPAA Checklist - Secure Waitress Server Starting...")
        
        try:
            # Setup steps
            self.setup_environment()
            self.setup_security_headers()
            
            if not self.setup_database_security():
                logger.error("❌ Database security setup failed")
                sys.exit(1)
            
            if not self.run_migrations():
                logger.error("❌ Database migrations failed")
                sys.exit(1)
            
            if not self.collect_static_files():
                logger.error("❌ Static file collection failed")
                sys.exit(1)
            
            # Log security information
            db_info = self.db_manager.get_database_info()
            security_logger.info(f"Database Security Info: {db_info}")
            
            # Start server
            self.running = True
            self.start_server()
            
        except KeyboardInterrupt:
            logger.info("🛑 Server stopped by user")
        except Exception as e:
            logger.error(f"❌ Server error: {e}")
            sys.exit(1)

def main():
    """Main entry point"""
    server = SecureWaitressServer()
    server.run()

if __name__ == '__main__':
    main()
