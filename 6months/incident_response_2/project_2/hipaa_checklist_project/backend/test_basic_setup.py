#!/usr/bin/env python3
"""
Basic test for Waitress and database setup
"""

import os
import sys
import sqlite3
from pathlib import Path

def test_database():
    """Test database functionality"""
    print("Testing database...")
    
    db_path = Path("db.sqlite3")
    if not db_path.exists():
        print("ERROR: Database not found")
        return False
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"SUCCESS: Found {len(tables)} tables")
        
        # Test security audit table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='security_audit'")
        if cursor.fetchone():
            print("SUCCESS: Security audit table exists")
        else:
            print("WARNING: Security audit table not found")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERROR: Database test failed - {e}")
        return False

def test_encryption():
    """Test encryption setup"""
    print("Testing encryption...")
    
    try:
        from sqlite_encryption import DatabaseSecurityManager
        
        db_path = Path("db.sqlite3")
        manager = DatabaseSecurityManager(str(db_path))
        
        # Get database info
        info = manager.get_database_info()
        print(f"Database info: {info}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Encryption test failed - {e}")
        return False

def test_waitress_config():
    """Test Waitress configuration"""
    print("Testing Waitress configuration...")
    
    try:
        from waitress_config import get_config, validate_config
        
        config = get_config()
        print(f"Configuration loaded: {len(config)} sections")
        
        errors = validate_config()
        if errors:
            print(f"WARNING: Configuration issues - {errors}")
        else:
            print("SUCCESS: Configuration is valid")
        
        return len(errors) == 0
        
    except Exception as e:
        print(f"ERROR: Waitress config test failed - {e}")
        return False

def main():
    """Run all tests"""
    print("=== Basic Setup Tests ===")
    
    tests = [
        ("Database", test_database),
        ("Encryption", test_encryption),
        ("Waitress Config", test_waitress_config),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\n--- {name} Test ---")
        if test_func():
            passed += 1
            print(f"PASS: {name}")
        else:
            print(f"FAIL: {name}")
    
    print(f"\n=== Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("SUCCESS: All tests passed!")
        return True
    else:
        print("WARNING: Some tests failed")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
