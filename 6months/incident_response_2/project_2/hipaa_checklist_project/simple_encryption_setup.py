#!/usr/bin/env python3
"""
Simple database encryption setup
"""

import os
import sys
import shutil
from pathlib import Path
from cryptography.fernet import Fernet

def setup_simple_encryption():
    """Set up simple database encryption"""
    print("🔐 Setting up simple database encryption...")
    
    backend_dir = Path("backend")
    db_path = backend_dir / "db.sqlite3"
    encrypted_path = backend_dir / "db.sqlite3.encrypted"
    
    if not db_path.exists():
        print("❌ Database not found")
        return False
    
    try:
        # Generate or load encryption key
        key_file = backend_dir / "encryption.key"
        if key_file.exists():
            with open(key_file, 'rb') as f:
                key = f.read()
            print("✅ Using existing encryption key")
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            print("✅ Generated new encryption key")
        
        # Read database file
        with open(db_path, 'rb') as f:
            db_data = f.read()
        
        # Encrypt the data
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(db_data)
        
        # Write encrypted data
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)
        
        print(f"✅ Database encrypted: {encrypted_path}")
        
        # Verify encryption
        try:
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = fernet.decrypt(encrypted_data)
            print("✅ Encryption verification successful")
            
            # Create backup of original
            backup_path = backend_dir / "db.sqlite3.backup"
            shutil.copy2(db_path, backup_path)
            print(f"✅ Backup created: {backup_path}")
            
            # Remove original (optional - for security)
            # db_path.unlink()
            # print("✅ Original database removed")
            
            return True
            
        except Exception as e:
            print(f"❌ Encryption verification failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Encryption setup failed: {e}")
        return False

def restore_database():
    """Restore database from encrypted version"""
    print("🔄 Restoring database from encrypted version...")
    
    backend_dir = Path("backend")
    db_path = backend_dir / "db.sqlite3"
    encrypted_path = backend_dir / "db.sqlite3.encrypted"
    key_file = backend_dir / "encryption.key"
    
    if not encrypted_path.exists():
        print("❌ Encrypted database not found")
        return False
    
    if not key_file.exists():
        print("❌ Encryption key not found")
        return False
    
    try:
        # Load encryption key
        with open(key_file, 'rb') as f:
            key = f.read()
        
        # Read encrypted data
        with open(encrypted_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Decrypt the data
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Write decrypted data
        with open(db_path, 'wb') as f:
            f.write(decrypted_data)
        
        print(f"✅ Database restored: {db_path}")
        return True
        
    except Exception as e:
        print(f"❌ Database restoration failed: {e}")
        return False

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'restore':
        success = restore_database()
    else:
        success = setup_simple_encryption()
    
    if success:
        print("🎉 Operation completed successfully!")
    else:
        print("⚠️  Operation failed")
