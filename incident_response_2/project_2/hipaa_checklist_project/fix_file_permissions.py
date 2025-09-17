#!/usr/bin/env python3
"""
Fix file permissions for security
"""

import os
import stat
from pathlib import Path

def fix_file_permissions():
    """Fix file permissions for security"""
    print("Fixing file permissions...")
    
    # Files to secure
    files_to_secure = [
        "backend/db.sqlite3",
        "backend/db.sqlite3.encrypted",
        "backend/encryption.key"
    ]
    
    # Directories to secure
    dirs_to_secure = [
        "backend/logs",
        "backend/backups"
    ]
    
    # Secure files
    for file_path in files_to_secure:
        if os.path.exists(file_path):
            os.chmod(file_path, 0o600)  # Owner read/write only
            print(f"Secured file: {file_path}")
        else:
            print(f"File not found: {file_path}")
    
    # Secure directories
    for dir_path in dirs_to_secure:
        if os.path.exists(dir_path):
            os.chmod(dir_path, 0o700)  # Owner read/write/execute only
            print(f"Secured directory: {dir_path}")
        else:
            # Create directory with secure permissions
            os.makedirs(dir_path, mode=0o700, exist_ok=True)
            print(f"Created secure directory: {dir_path}")
    
    print("File permissions fixed successfully!")
    return True

if __name__ == '__main__':
    fix_file_permissions()
