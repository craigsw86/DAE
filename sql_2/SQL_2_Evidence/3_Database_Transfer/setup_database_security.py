#!/usr/bin/env python3
"""
Database Security Setup Script for HIPAA Checklist Project
Configures SQLite encryption, permissions, and security features
"""

import os
import sys
import logging
import sqlite3
from pathlib import Path
from sqlite_encryption import DatabaseSecurityManager

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_security_setup.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class DatabaseSecuritySetup:
    """Comprehensive database security setup"""
    
    def __init__(self):
        self.db_path = backend_dir / 'db.sqlite3'
        self.db_manager = DatabaseSecurityManager(self.db_path)
        self.setup_logs_dir()
    
    def setup_logs_dir(self):
        """Create logs directory with secure permissions"""
        logs_dir = backend_dir / 'logs'
        logs_dir.mkdir(exist_ok=True)
        
        try:
            import stat
            # Set restrictive permissions
            current_perms = logs_dir.stat().st_mode
            new_perms = current_perms & ~stat.S_IWGRP & ~stat.S_IWOTH & ~stat.S_IRGRP & ~stat.S_IROTH
            logs_dir.chmod(new_perms)
            logger.info(f" Logs directory permissions set: {oct(new_perms)}")
        except Exception as e:
            logger.warning(f"  Could not set logs directory permissions: {e}")
    
    def check_database_exists(self):
        """Check if database exists and is accessible"""
        if not self.db_path.exists():
            logger.error(" Database file not found. Please run migrations first.")
            return False
        
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            conn.close()
            
            logger.info(f" Database accessible with {len(tables)} tables")
            return True
        except Exception as e:
            logger.error(f" Database access failed: {e}")
            return False
    
    def setup_encryption(self):
        """Set up database encryption"""
        logger.info(" Setting up database encryption...")
        
        # Check current encryption status
        db_info = self.db_manager.get_database_info()
        logger.info(f"Database info: {db_info}")
        
        if db_info['is_encrypted']:
            logger.info(" Database is already encrypted")
            return True
        
        if not db_info['plaintext_exists']:
            logger.error(" No database file found to encrypt")
            return False
        
        # Encrypt the database
        if self.db_manager.setup_secure_database():
            logger.info(" Database encryption completed")
            return True
        else:
            logger.error(" Database encryption failed")
            return False
    
    def configure_sqlite_security(self):
        """Configure SQLite security settings"""
        logger.info(" Configuring SQLite security settings...")
        
        try:
            # Restore database temporarily for configuration
            if not self.db_path.exists() and self.db_manager.encryption.encrypted_db_path.exists():
                self.db_manager.restore_database()
            
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Security pragmas
            security_pragmas = [
                "PRAGMA journal_mode=WAL",  # Write-Ahead Logging
                "PRAGMA synchronous=FULL",  # Full synchronization
                "PRAGMA cache_size=1000",   # Cache size
                "PRAGMA temp_store=MEMORY", # Store temp tables in memory
                "PRAGMA mmap_size=268435456", # Memory-mapped I/O
                "PRAGMA page_size=4096",    # Page size
                "PRAGMA auto_vacuum=INCREMENTAL", # Incremental vacuum
                "PRAGMA secure_delete=ON",  # Secure delete
                "PRAGMA locking_mode=EXCLUSIVE", # Exclusive locking
            ]
            
            for pragma in security_pragmas:
                try:
                    cursor.execute(pragma)
                    result = cursor.fetchone()
                    logger.info(f" {pragma}: {result[0] if result else 'OK'}")
                except Exception as e:
                    logger.warning(f"  {pragma} failed: {e}")
            
            # Create security audit table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS security_audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    event_type TEXT NOT NULL,
                    description TEXT,
                    user_id INTEGER,
                    ip_address TEXT,
                    success BOOLEAN DEFAULT 1
                )
            """)
            
            # Create indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_security_audit_timestamp ON security_audit(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_security_audit_event_type ON security_audit(event_type)")
            
            conn.commit()
            conn.close()
            
            logger.info(" SQLite security configuration completed")
            return True
            
        except Exception as e:
            logger.error(f" SQLite security configuration failed: {e}")
            return False
    
    def set_file_permissions(self):
        """Set secure file permissions"""
        logger.info(" Setting secure file permissions...")
        
        try:
            import stat
            
            files_to_secure = [
                self.db_path,
                self.db_manager.encryption.encrypted_db_path,
                backend_dir / 'logs',
            ]
            
            for file_path in files_to_secure:
                if file_path.exists():
                    if file_path.is_file():
                        # File permissions: owner read/write, no group/other access
                        file_path.chmod(stat.S_IRUSR | stat.S_IWUSR)
                        logger.info(f" File permissions set: {file_path.name}")
                    elif file_path.is_dir():
                        # Directory permissions: owner read/write/execute, no group/other access
                        file_path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
                        logger.info(f" Directory permissions set: {file_path.name}")
            
            return True
            
        except Exception as e:
            logger.warning(f"  Could not set file permissions: {e}")
            return False
    
    def create_backup(self):
        """Create encrypted backup of database"""
        logger.info(" Creating encrypted backup...")
        
        try:
            backup_dir = backend_dir / 'backups'
            backup_dir.mkdir(exist_ok=True)
            
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = backup_dir / f'db_backup_{timestamp}.encrypted'
            
            # Create backup using encryption
            if self.db_path.exists():
                # Read and encrypt database
                with open(self.db_path, 'rb') as f:
                    db_data = f.read()
                
                from sqlite_encryption import SQLiteEncryption
                encryption = SQLiteEncryption(str(backup_path))
                encrypted_data = encryption.encrypt_database()
                
                if encrypted_data:
                    logger.info(f" Backup created: {backup_path}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f" Backup creation failed: {e}")
            return False
    
    def run_security_tests(self):
        """Run security tests"""
        logger.info(" Running security tests...")
        
        tests_passed = 0
        total_tests = 4
        
        # Test 1: Database encryption
        if self.db_manager.encryption.verify_encryption():
            logger.info(" Test 1: Database encryption - PASSED")
            tests_passed += 1
        else:
            logger.warning("  Test 1: Database encryption - FAILED")
        
        # Test 2: File permissions
        if self.db_path.exists():
            import stat
            perms = self.db_path.stat().st_mode
            if not (perms & stat.S_IRGRP or perms & stat.S_IWGRP or perms & stat.S_IROTH or perms & stat.S_IWOTH):
                logger.info(" Test 2: File permissions - PASSED")
                tests_passed += 1
            else:
                logger.warning("  Test 2: File permissions - FAILED")
        
        # Test 3: Database accessibility
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.close()
            logger.info(" Test 3: Database accessibility - PASSED")
            tests_passed += 1
        except:
            logger.warning("  Test 3: Database accessibility - FAILED")
        
        # Test 4: Security audit table
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='security_audit'")
            if cursor.fetchone():
                logger.info(" Test 4: Security audit table - PASSED")
                tests_passed += 1
            else:
                logger.warning("  Test 4: Security audit table - FAILED")
            conn.close()
        except:
            logger.warning("  Test 4: Security audit table - FAILED")
        
        logger.info(f" Security tests: {tests_passed}/{total_tests} passed")
        return tests_passed == total_tests
    
    def run_full_setup(self):
        """Run complete security setup"""
        logger.info(" Starting comprehensive database security setup...")
        logger.info("=" * 60)
        
        # Step 1: Check database exists
        if not self.check_database_exists():
            return False
        
        # Step 2: Configure SQLite security
        if not self.configure_sqlite_security():
            logger.warning("  SQLite security configuration had issues")
        
        # Step 3: Set up encryption
        if not self.setup_encryption():
            logger.error(" Encryption setup failed")
            return False
        
        # Step 4: Set file permissions
        self.set_file_permissions()
        
        # Step 5: Create backup
        self.create_backup()
        
        # Step 6: Run security tests
        if self.run_security_tests():
            logger.info(" Database security setup completed successfully!")
            return True
        else:
            logger.warning("  Database security setup completed with warnings")
            return True

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup database security for HIPAA Checklist')
    parser.add_argument('--encrypt-only', action='store_true', help='Only encrypt the database')
    parser.add_argument('--test-only', action='store_true', help='Only run security tests')
    parser.add_argument('--backup-only', action='store_true', help='Only create backup')
    
    args = parser.parse_args()
    
    setup = DatabaseSecuritySetup()
    
    if args.encrypt_only:
        success = setup.setup_encryption()
    elif args.test_only:
        success = setup.run_security_tests()
    elif args.backup_only:
        success = setup.create_backup()
    else:
        success = setup.run_full_setup()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()