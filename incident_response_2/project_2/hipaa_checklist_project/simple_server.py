#!/usr/bin/env python3
"""
Simple working server for testing
"""

import os
import sys
import logging
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Start a simple Django development server"""
    try:
        # Change to backend directory
        os.chdir(backend_dir)
        
        # Import Django
        import django
        from django.core.management import execute_from_command_line
        
        # Setup Django
        django.setup()
        
        logger.info("Starting Django development server...")
        logger.info("Server will be available at: http://localhost:8000")
        logger.info("Press Ctrl+C to stop the server")
        
        # Start the server
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
