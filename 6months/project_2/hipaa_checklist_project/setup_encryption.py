#!/usr/bin/env python3
"""
Set up database encryption properly
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')

def setup_encryption():
    """Set up database encryption"""
    print(" Setting up database encryption...")
    
    try:
        from sqlite_encryption import DatabaseSecurityManager
        
        db_path = backend_dir / "db.sqlite3"
        manager = DatabaseSecurityManager(str(db_path))
        
        # Check if database exists
        if not db_path.exists():
            print(" Database not found")
            return False
        
        # Get current info
        info = manager.get_database_info()
        print(f"Database info: {info}")
        
        # Set up encryption
        if manager.setup_secure_database():
            print(" Database encryption setup completed")
            
            # Verify encryption
            if manager.encryption.verify_encryption():
                print(" Encryption verified")
                return True
            else:
                print(" Encryption verification failed")
                return False
        else:
            print(" Encryption setup failed")
            return False
            
    except Exception as e:
        print(f" Error: {e}")
        return False

if __name__ == '__main__':
    success = setup_encryption()
    if success:
        print(" Database encryption setup completed successfully!")
    else:
        print("  Database encryption setup failed")

