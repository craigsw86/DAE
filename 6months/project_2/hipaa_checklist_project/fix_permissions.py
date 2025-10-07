#!/usr/bin/env python3
"""
Fix file permissions for SQLite database and related files
"""

import os
import stat
from pathlib import Path

def fix_file_permissions():
    """Fix file permissions for security"""
    print(" Fixing file permissions...")
    
    # Files to secure
    files_to_secure = [
        Path("backend/db.sqlite3"),
        Path("backend/db.sqlite3.encrypted"),
        Path("backend/logs"),
    ]
    
    for file_path in files_to_secure:
        if file_path.exists():
            try:
                if file_path.is_file():
                    # File permissions: owner read/write only
                    file_path.chmod(stat.S_IRUSR | stat.S_IWUSR)
                    perms = file_path.stat().st_mode
                    print(f" {file_path.name}: {oct(perms)}")
                elif file_path.is_dir():
                    # Directory permissions: owner read/write/execute only
                    file_path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
                    perms = file_path.stat().st_mode
                    print(f" {file_path.name}/: {oct(perms)}")
            except Exception as e:
                print(f" {file_path.name}: {e}")
        else:
            print(f"  {file_path.name}: Not found")

if __name__ == '__main__':
    fix_file_permissions()

