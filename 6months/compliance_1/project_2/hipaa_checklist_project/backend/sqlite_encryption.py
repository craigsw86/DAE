#!/usr/bin/env python3
"""
SQLite Database Encryption Module for HIPAA Checklist Project
Provides encryption at rest for SQLite database files
"""

import os
import sqlite3
import hashlib
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

logger = logging.getLogger(__name__)

class SQLiteEncryption:
    """SQLite database encryption handler"""
    
    def __init__(self, db_path, password=None):
        self.db_path = Path(db_path)
        self.password = password or os.environ.get('DB_ENCRYPTION_PASSWORD', 'default_hipaa_password_2024')
        self.encrypted_db_path = self.db_path.with_suffix('.encrypted')
        self.key = self._derive_key()
    
    def _derive_key(self):
        """Derive encryption key from password using PBKDF2"""
        password_bytes = self.password.encode('utf-8')
        salt = b'hipaa_checklist_salt_2024'  # In production, use random salt
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key
    
    def encrypt_database(self):
        """Encrypt the SQLite database file"""
        if not self.db_path.exists():
            logger.error(f"Database file not found: {self.db_path}")
            return False
        
        try:
            # Read the database file
            with open(self.db_path, 'rb') as f:
                db_data = f.read()
            
            # Encrypt the data
            fernet = Fernet(self.key)
            encrypted_data = fernet.encrypt(db_data)
            
            # Write encrypted data
            with open(self.encrypted_db_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Set secure permissions
            self._set_secure_permissions(self.encrypted_db_path)
            
            logger.info(f"✅ Database encrypted: {self.encrypted_db_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Encryption failed: {e}")
            return False
    
    def decrypt_database(self):
        """Decrypt the SQLite database file"""
        if not self.encrypted_db_path.exists():
            logger.warning("Encrypted database not found, using original")
            return True
        
        try:
            # Read encrypted data
            with open(self.encrypted_db_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt the data
            fernet = Fernet(self.key)
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Write decrypted data
            with open(self.db_path, 'wb') as f:
                f.write(decrypted_data)
            
            # Set secure permissions
            self._set_secure_permissions(self.db_path)
            
            logger.info(f"✅ Database decrypted: {self.db_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Decryption failed: {e}")
            return False
    
    def _set_secure_permissions(self, file_path):
        """Set secure file permissions"""
        try:
            import stat
            # Remove write permissions for group and others
            current_perms = file_path.stat().st_mode
            new_perms = current_perms & ~stat.S_IWGRP & ~stat.S_IWOTH & ~stat.S_IRGRP & ~stat.S_IROTH
            file_path.chmod(new_perms)
            logger.info(f"✅ Secure permissions set: {oct(new_perms)}")
        except Exception as e:
            logger.warning(f"⚠️  Could not set permissions: {e}")
    
    def verify_encryption(self):
        """Verify that the database is properly encrypted"""
        if not self.encrypted_db_path.exists():
            return False
        
        try:
            # Try to read as SQLite (should fail if encrypted)
            conn = sqlite3.connect(str(self.encrypted_db_path))
            conn.close()
            return False  # If we can connect, it's not encrypted
        except:
            return True  # If we can't connect, it's likely encrypted
    
    def cleanup_plaintext(self):
        """Remove the plaintext database file after encryption"""
        if self.encrypted_db_path.exists() and self.db_path.exists():
            try:
                self.db_path.unlink()
                logger.info("✅ Plaintext database removed")
                return True
            except Exception as e:
                logger.warning(f"⚠️  Could not remove plaintext database: {e}")
                return False
        return True

class DatabaseSecurityManager:
    """Manages database security and encryption"""
    
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.encryption = SQLiteEncryption(db_path)
    
    def setup_secure_database(self):
        """Set up secure database with encryption"""
        logger.info("🔐 Setting up secure database...")
        
        # Ensure database exists
        if not self.db_path.exists():
            logger.warning("Database not found, creating new one...")
            return False
        
        # Encrypt the database
        if self.encryption.encrypt_database():
            # Verify encryption
            if self.encryption.verify_encryption():
                logger.info("✅ Database encryption verified")
                # Clean up plaintext
                self.encryption.cleanup_plaintext()
                return True
            else:
                logger.error("❌ Database encryption verification failed")
                return False
        else:
            logger.error("❌ Database encryption failed")
            return False
    
    def restore_database(self):
        """Restore database from encrypted version"""
        logger.info("🔄 Restoring database from encrypted version...")
        
        if self.encryption.decrypt_database():
            logger.info("✅ Database restored successfully")
            return True
        else:
            logger.error("❌ Database restoration failed")
            return False
    
    def get_database_info(self):
        """Get database security information"""
        info = {
            'db_path': str(self.db_path),
            'encrypted_path': str(self.encryption.encrypted_db_path),
            'is_encrypted': self.encryption.verify_encryption(),
            'plaintext_exists': self.db_path.exists(),
            'encrypted_exists': self.encryption.encrypted_db_path.exists(),
        }
        
        if self.db_path.exists():
            info['db_size'] = self.db_path.stat().st_size
            info['db_permissions'] = oct(self.db_path.stat().st_mode)
        
        return info

def setup_database_security(db_path):
    """Convenience function to set up database security"""
    manager = DatabaseSecurityManager(db_path)
    return manager.setup_secure_database()

def restore_database(db_path):
    """Convenience function to restore database"""
    manager = DatabaseSecurityManager(db_path)
    return manager.restore_database()

if __name__ == '__main__':
    # Test the encryption
    import sys
    
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        db_path = 'db.sqlite3'
    
    manager = DatabaseSecurityManager(db_path)
    info = manager.get_database_info()
    
    print("🔐 Database Security Information")
    print("=" * 40)
    for key, value in info.items():
        print(f"{key}: {value}")
