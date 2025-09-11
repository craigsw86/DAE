#!/usr/bin/env python3
"""
Comprehensive fix for all issues
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path
from cryptography.fernet import Fernet
import shutil

def fix_all_issues():
    """Fix all identified issues"""
    print("🔧 Starting comprehensive fix...")
    
    # 1. Fix file permissions
    print("\n1. Fixing file permissions...")
    files_to_secure = [
        "backend/db.sqlite3",
        "backend/db.sqlite3.encrypted",
        "backend/encryption.key"
    ]
    
    dirs_to_secure = [
        "backend/logs",
        "backend/backups"
    ]
    
    for file_path in files_to_secure:
        if os.path.exists(file_path):
            os.chmod(file_path, 0o600)
            print(f"   ✅ Secured: {file_path}")
    
    for dir_path in dirs_to_secure:
        if os.path.exists(dir_path):
            os.chmod(dir_path, 0o700)
            print(f"   ✅ Secured: {dir_path}")
        else:
            os.makedirs(dir_path, mode=0o700, exist_ok=True)
            print(f"   ✅ Created: {dir_path}")
    
    # 2. Fix database encryption
    print("\n2. Fixing database encryption...")
    db_path = Path("backend/db.sqlite3")
    if db_path.exists():
        # Create backup
        backup_path = Path("backend/db.sqlite3.backup")
        if not backup_path.exists():
            shutil.copy2(db_path, backup_path)
            print(f"   ✅ Created backup: {backup_path}")
        
        # Generate encryption key
        key = Fernet.generate_key()
        key_file = Path("backend/encryption.key")
        with open(key_file, 'wb') as f:
            f.write(key)
        os.chmod(key_file, 0o600)
        print(f"   ✅ Generated encryption key: {key_file}")
        
        # Encrypt database
        fernet = Fernet(key)
        encrypted_path = Path("backend/db.sqlite3.encrypted")
        
        with open(db_path, 'rb') as f:
            data = f.read()
        
        encrypted_data = fernet.encrypt(data)
        
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)
        
        os.chmod(encrypted_path, 0o600)
        print(f"   ✅ Encrypted database: {encrypted_path}")
    
    # 3. Fix database security pragmas
    print("\n3. Fixing database security...")
    if db_path.exists():
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
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
            print("   ✅ Applied security pragmas")
        except Exception as e:
            print(f"   ❌ Database security failed: {e}")
    
    # 4. Install missing dependencies
    print("\n4. Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "cryptography"], check=True)
        print("   ✅ Installed cryptography")
    except:
        print("   ⚠️  Cryptography already installed")
    
    # 5. Run Django migrations
    print("\n5. Running Django migrations...")
    try:
        os.chdir("backend")
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        print("   ✅ Migrations completed")
        os.chdir("..")
    except Exception as e:
        print(f"   ❌ Migrations failed: {e}")
        os.chdir("..")
    
    # 6. Collect static files
    print("\n6. Collecting static files...")
    try:
        os.chdir("backend")
        subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
        print("   ✅ Static files collected")
        os.chdir("..")
    except Exception as e:
        print(f"   ❌ Static collection failed: {e}")
        os.chdir("..")
    
    print("\n🎉 Comprehensive fix completed!")
    return True

if __name__ == '__main__':
    fix_all_issues()
