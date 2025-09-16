#!/usr/bin/env python3
"""
Fix database encryption setup
"""

import os
import sqlite3
from pathlib import Path
from cryptography.fernet import Fernet
import shutil

def fix_database_encryption():
    """Fix database encryption setup"""
    print("Fixing database encryption...")
    
    # Check if database exists
    db_path = Path("backend/db.sqlite3")
    if not db_path.exists():
        print("Database not found, creating new one...")
        return True
    
    # Create backup
    backup_path = Path("backend/db.sqlite3.backup")
    if not backup_path.exists():
        shutil.copy2(db_path, backup_path)
        print(f"Created backup: {backup_path}")
    
    # Generate encryption key
    key = Fernet.generate_key()
    key_file = Path("backend/encryption.key")
    with open(key_file, 'wb') as f:
        f.write(key)
    print(f"Generated encryption key: {key_file}")
    
    # Encrypt database
    fernet = Fernet(key)
    encrypted_path = Path("backend/db.sqlite3.encrypted")
    
    with open(db_path, 'rb') as f:
        data = f.read()
    
    encrypted_data = fernet.encrypt(data)
    
    with open(encrypted_path, 'wb') as f:
        f.write(encrypted_data)
    
    print(f"Database encrypted: {encrypted_path}")
    
    # Set secure permissions
    os.chmod(db_path, 0o600)
    os.chmod(encrypted_path, 0o600)
    os.chmod(key_file, 0o600)
    
    print("Database encryption fixed successfully!")
    return True

if __name__ == '__main__':
    fix_database_encryption()
