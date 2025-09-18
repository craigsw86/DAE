#!/usr/bin/env python3
"""
Fixed Waitress WSGI Server for HIPAA Checklist Project
Enhanced with security features, database encryption, and monitoring
"""

import os
import sys
import logging
import sqlite3
import subprocess
from pathlib import Path
from waitress import serve
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')

# Configure logging without emojis for Windows compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/waitress.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SecureWaitressServer:
    """Enhanced Waitress server with security features"""
    
    def __init__(self, host='0.0.0.0', port=8000, threads=4):
        self.host = host
        self.port = port
        self.threads = threads
        self.app = None
        
    def setup_environment(self):
        """Set up the environment and security features"""
        logger.info("Setting up secure environment...")
        
        # Create necessary directories
        os.makedirs('logs', exist_ok=True)
        os.makedirs('backups', exist_ok=True)
        
        # Set field encryption key
        if not os.environ.get('FIELD_ENCRYPTION_KEY'):
            os.environ['FIELD_ENCRYPTION_KEY'] = '1f2WjIy7cmJebkD-ywTrmct3Ms7-VuUjv7wleofoP54='
            logger.info("Field encryption key set")
        
        # Set secret key
        if not os.environ.get('SECRET_KEY'):
            os.environ['SECRET_KEY'] = 'tj3y6j#0l#6%*f=6fn%l=-^49=v_1_gbn-yb7)%%baff%_l@a4'
            logger.info("Secret key set")
        
        # Set up database security
        self.setup_database_security()
        
        # Run Django migrations
        self.run_migrations()
        
        # Collect static files
        self.collect_static_files()
        
        logger.info("Environment setup completed")
    
    def setup_database_security(self):
        """Set up database security features"""
        try:
            db_path = 'db.sqlite3'
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Set security pragmas
                security_pragmas = [
                    "PRAGMA journal_mode=WAL",
                    "PRAGMA synchronous=NORMAL",
                    "PRAGMA cache_size=10000",
                    "PRAGMA temp_store=MEMORY",
                    "PRAGMA mmap_size=268435456",
                    "PRAGMA secure_delete=ON",
                    "PRAGMA foreign_keys=ON"
                ]
                
                for pragma in security_pragmas:
                    cursor.execute(pragma)
                
                conn.commit()
                conn.close()
                logger.info("Database security pragmas applied")
            else:
                logger.warning("Database file not found, will be created by migrations")
                
        except Exception as e:
            logger.error(f"Database security setup failed: {e}")
    
    def run_migrations(self):
        """Run Django migrations"""
        try:
            logger.info("Running database migrations...")
            execute_from_command_line(['manage.py', 'migrate'])
            logger.info("Migrations completed")
        except Exception as e:
            logger.error(f"Migration failed: {e}")
    
    def collect_static_files(self):
        """Collect static files"""
        try:
            logger.info("Collecting static files...")
            execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
            logger.info("Static files collected")
        except Exception as e:
            logger.error(f"Static file collection failed: {e}")
    
    def setup_file_permissions(self):
        """Set up secure file permissions"""
        try:
            # Set secure permissions for database
            db_files = ['db.sqlite3', 'db.sqlite3.encrypted']
            for db_file in db_files:
                if os.path.exists(db_file):
                    os.chmod(db_file, 0o600)  # Owner read/write only
                    logger.info(f"Set secure permissions for {db_file}")
            
            # Set secure permissions for logs directory
            if os.path.exists('logs'):
                os.chmod('logs', 0o700)  # Owner read/write/execute only
                logger.info("Set secure permissions for logs directory")
                
        except Exception as e:
            logger.error(f"Permission setup failed: {e}")
    
    def start_server(self):
        """Start the Waitress server"""
        try:
            # Get Django WSGI application
            self.app = get_wsgi_application()
            
            logger.info(f"Starting Waitress server on {self.host}:{self.port}")
            logger.info(f"Threads: {self.threads}")
            logger.info("Server is ready to accept connections")
            
            # Start the server
            serve(
                self.app,
                host=self.host,
                port=self.port,
                threads=self.threads,
                url_scheme='http',
                ident='HIPAA-Checklist-Server'
            )
            
        except Exception as e:
            logger.error(f"Server startup failed: {e}")
            sys.exit(1)
    
    def run(self):
        """Run the complete server setup and start"""
        try:
            self.setup_environment()
            self.setup_file_permissions()
            self.start_server()
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}")
            sys.exit(1)

def main():
    """Main function"""
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Start the server
    server = SecureWaitressServer()
    server.run()

if __name__ == '__main__':
    main()
