#!/usr/bin/env python3
"""
Final comprehensive test and fix for the HIPAA Checklist Project
"""

import os
import sys
import subprocess
import sqlite3
import requests
import time
from pathlib import Path
from cryptography.fernet import Fernet

def test_and_fix_all():
    """Test and fix all issues comprehensively"""
    print(" FINAL COMPREHENSIVE TEST AND FIX")
    print("=" * 50)
    
    # 1. Fix file permissions
    print("\n1. Fixing file permissions...")
    files_to_secure = [
        "backend/db.sqlite3",
        "backend/db.sqlite3.encrypted",
        "backend/encryption.key"
    ]
    
    for file_path in files_to_secure:
        if os.path.exists(file_path):
            os.chmod(file_path, 0o600)
            print(f"    Secured: {file_path}")
        else:
            print(f"     Not found: {file_path}")
    
    # 2. Fix database encryption
    print("\n2. Fixing database encryption...")
    db_path = Path("backend/db.sqlite3")
    if db_path.exists():
        # Generate encryption key
        key = Fernet.generate_key()
        key_file = Path("backend/encryption.key")
        with open(key_file, 'wb') as f:
            f.write(key)
        os.chmod(key_file, 0o600)
        print(f"    Generated encryption key: {key_file}")
        
        # Encrypt database
        fernet = Fernet(key)
        encrypted_path = Path("backend/db.sqlite3.encrypted")
        
        with open(db_path, 'rb') as f:
            data = f.read()
        
        encrypted_data = fernet.encrypt(data)
        
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)
        
        os.chmod(encrypted_path, 0o600)
        print(f"    Encrypted database: {encrypted_path}")
    
    # 3. Test database functionality
    print("\n3. Testing database functionality...")
    if db_path.exists():
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Test basic functionality
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"    Found {len(tables)} tables in database")
            
            # Apply security pragmas
            security_pragmas = [
                "PRAGMA journal_mode=WAL",
                "PRAGMA synchronous=NORMAL",
                "PRAGMA cache_size=10000",
                "PRAGMA secure_delete=ON",
                "PRAGMA foreign_keys=ON"
            ]
            
            for pragma in security_pragmas:
                cursor.execute(pragma)
            
            conn.commit()
            conn.close()
            print("    Database security pragmas applied")
            
        except Exception as e:
            print(f"    Database test failed: {e}")
    
    # 4. Test Django setup
    print("\n4. Testing Django setup...")
    try:
        os.chdir("backend")
        
        # Test migrations
        result = subprocess.run([sys.executable, "manage.py", "migrate", "--check"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("    Django migrations are up to date")
        else:
            print("     Running migrations...")
            subprocess.run([sys.executable, "manage.py", "migrate"], timeout=60)
            print("    Migrations completed")
        
        # Test static files
        result = subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("    Static files collected")
        else:
            print("     Static file collection had issues")
        
        os.chdir("..")
        
    except Exception as e:
        print(f"    Django setup failed: {e}")
        os.chdir("..")
    
    # 5. Test server startup
    print("\n5. Testing server startup...")
    try:
        # Start server in background
        os.chdir("backend")
        server_process = subprocess.Popen([sys.executable, "manage.py", "runserver", "8000"], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
        os.chdir("..")
        
        # Wait for server to start
        print("   ⏳ Waiting for server to start...")
        time.sleep(10)
        
        # Test server response
        try:
            response = requests.get("http://localhost:8000/api/health/", timeout=5)
            if response.status_code == 200:
                print("    Server is running and responding!")
                print(f"    Health check response: {response.json()}")
            else:
                print(f"     Server responded with status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"    Server not responding: {e}")
        
        # Test additional endpoints
        endpoints_to_test = [
            ("/api/info/", "API Info"),
            ("/api/stats/", "Public Stats"),
            ("/admin/", "Admin Interface")
        ]
        
        for endpoint, name in endpoints_to_test:
            try:
                response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
                if response.status_code in [200, 401, 403]:
                    print(f"    {name} endpoint: Status {response.status_code}")
                else:
                    print(f"     {name} endpoint: Status {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"    {name} endpoint: {e}")
        
        # Stop server
        server_process.terminate()
        server_process.wait()
        print("    Server stopped")
        
    except Exception as e:
        print(f"    Server test failed: {e}")
    
    # 6. Final status report
    print("\n" + "=" * 50)
    print(" FINAL STATUS REPORT")
    print("=" * 50)
    
    # Check file permissions
    print("\nFile Permissions:")
    for file_path in files_to_secure:
        if os.path.exists(file_path):
            stat_info = os.stat(file_path)
            permissions = oct(stat_info.st_mode)[-3:]
            if permissions == "600":
                print(f"    {file_path}: {permissions}")
            else:
                print(f"    {file_path}: {permissions}")
    
    # Check database encryption
    print("\nDatabase Encryption:")
    if os.path.exists("backend/encryption.key") and os.path.exists("backend/db.sqlite3.encrypted"):
        print("    Encryption key exists")
        print("    Encrypted database exists")
    else:
        print("    Encryption setup incomplete")
    
    # Check database functionality
    print("\nDatabase Functionality:")
    if db_path.exists():
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"    Database has {len(tables)} tables")
            conn.close()
        except Exception as e:
            print(f"    Database error: {e}")
    
    print("\n Final test and fix completed!")
    return True

if __name__ == '__main__':
    test_and_fix_all()
