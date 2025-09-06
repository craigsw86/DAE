#!/usr/bin/env python3
"""
Quick performance fixes
"""

import os
from pathlib import Path

def quick_fixes():
    """Apply quick performance fixes"""
    print("⚡ Applying quick performance fixes...")
    
    # Create logs directory
    logs_dir = Path("backend/logs")
    logs_dir.mkdir(exist_ok=True)
    print("✅ Logs directory created")
    
    # Set file permissions
    try:
        import stat
        db_path = Path("backend/db.sqlite3")
        if db_path.exists():
            db_path.chmod(stat.S_IRUSR | stat.S_IWUSR)
            print("✅ Database permissions fixed")
    except Exception as e:
        print(f"⚠️  Permission fix: {e}")
    
    print("✅ Quick performance fixes completed")

if __name__ == '__main__':
    quick_fixes()
