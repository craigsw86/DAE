#!/usr/bin/env python3
"""
Final Security Issues Fix Script for HIPAA Checklist Project
Addresses all critical security issues identified in the verification report
"""

import os
import sys
import stat
import shutil
import subprocess
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecurityFixer:
    """Fix all identified security issues"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.backend_path = self.project_root / 'backend'
        self.ssl_path = self.project_root / 'ssl'
        self.fixes_applied = []
        self.errors = []
    
    def fix_all_security_issues(self):
        """Apply all security fixes"""
        logger.info("🔧 Starting Security Issues Fix")
        logger.info("=" * 50)
        
        # 1. Fix file permissions
        self.fix_file_permissions()
        
        # 2. Fix database encryption
        self.fix_database_encryption()
        
        # 3. Fix SSL certificate issues
        self.fix_ssl_certificates()
        
        # 4. Create proper encryption key management
        self.setup_encryption_key_management()
        
        # 5. Generate final report
        self.generate_fix_report()
        
        return len(self.fixes_applied), len(self.errors)
    
    def fix_file_permissions(self):
        """Fix overly permissive file permissions"""
        logger.info("📁 Fixing File Permissions...")
        
        # Files that need secure permissions
        sensitive_files = [
            self.backend_path / 'db.sqlite3',
            self.backend_path / 'db.sqlite3.encrypted',
            self.backend_path / 'db.encrypted',
            self.ssl_path / 'hipaa_checklist.key',
            self.backend_path / 'encryption.key'
        ]
        
        for file_path in sensitive_files:
            if file_path.exists():
                try:
                    # Set secure permissions (owner read/write only)
                    file_path.chmod(stat.S_IRUSR | stat.S_IWUSR)
                    logger.info(f"✅ Fixed permissions for {file_path.name}")
                    self.fixes_applied.append(f"Fixed permissions: {file_path.name}")
                except Exception as e:
                    logger.error(f"❌ Failed to fix permissions for {file_path.name}: {e}")
                    self.errors.append(f"Permission fix failed: {file_path.name}")
        
        # Fix directory permissions
        sensitive_dirs = [self.backend_path, self.ssl_path, self.project_root / 'logs']
        for dir_path in sensitive_dirs:
            if dir_path.exists():
                try:
                    # Set secure directory permissions (owner read/write/execute only)
                    dir_path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
                    logger.info(f"✅ Fixed directory permissions for {dir_path.name}")
                    self.fixes_applied.append(f"Fixed directory permissions: {dir_path.name}")
                except Exception as e:
                    logger.error(f"❌ Failed to fix directory permissions for {dir_path.name}: {e}")
                    self.errors.append(f"Directory permission fix failed: {dir_path.name}")
    
    def fix_database_encryption(self):
        """Fix database encryption issues"""
        logger.info("🔐 Fixing Database Encryption...")
        
        try:
            # Import the encryption module
            sys.path.append(str(self.backend_path))
            from sqlite_encryption import DatabaseSecurityManager
            
            # Setup secure database
            db_path = self.backend_path / 'db.sqlite3'
            if db_path.exists():
                manager = DatabaseSecurityManager(db_path)
                
                # Ensure database is properly encrypted
                if manager.setup_secure_database():
                    logger.info("✅ Database encryption fixed")
                    self.fixes_applied.append("Database encryption properly configured")
                else:
                    logger.error("❌ Database encryption setup failed")
                    self.errors.append("Database encryption setup failed")
            else:
                logger.warning("⚠️ Database file not found, skipping encryption fix")
                
        except Exception as e:
            logger.error(f"❌ Database encryption fix failed: {e}")
            self.errors.append(f"Database encryption fix failed: {e}")
    
    def fix_ssl_certificates(self):
        """Fix SSL certificate issues"""
        logger.info("🔒 Fixing SSL Certificates...")
        
        try:
            # Check if certificate generation script exists
            cert_script = self.ssl_path / 'create_working_certs.ps1'
            if cert_script.exists():
                # Regenerate certificates
                result = subprocess.run([
                    'powershell', '-ExecutionPolicy', 'Bypass', 
                    '-File', str(cert_script)
                ], capture_output=True, text=True, cwd=str(self.ssl_path))
                
                if result.returncode == 0:
                    logger.info("✅ SSL certificates regenerated")
                    self.fixes_applied.append("SSL certificates regenerated")
                else:
                    logger.error(f"❌ SSL certificate generation failed: {result.stderr}")
                    self.errors.append("SSL certificate generation failed")
            else:
                logger.warning("⚠️ Certificate generation script not found")
                
        except Exception as e:
            logger.error(f"❌ SSL certificate fix failed: {e}")
            self.errors.append(f"SSL certificate fix failed: {e}")
    
    def setup_encryption_key_management(self):
        """Setup proper encryption key management"""
        logger.info("🔑 Setting up Encryption Key Management...")
        
        try:
            # Create secure encryption key file
            key_file = self.backend_path / 'encryption.key'
            
            if not key_file.exists():
                # Generate new encryption key
                from cryptography.fernet import Fernet
                key = Fernet.generate_key()
                
                with open(key_file, 'wb') as f:
                    f.write(key)
                
                # Set secure permissions
                key_file.chmod(stat.S_IRUSR | stat.S_IWUSR)
                
                logger.info("✅ Encryption key created with secure permissions")
                self.fixes_applied.append("Encryption key created with secure permissions")
            else:
                # Just fix permissions
                key_file.chmod(stat.S_IRUSR | stat.S_IWUSR)
                logger.info("✅ Encryption key permissions fixed")
                self.fixes_applied.append("Encryption key permissions fixed")
                
        except Exception as e:
            logger.error(f"❌ Encryption key management setup failed: {e}")
            self.errors.append(f"Encryption key management setup failed: {e}")
    
    def generate_fix_report(self):
        """Generate security fix report"""
        logger.info("📋 Generating Security Fix Report...")
        
        report = {
            'timestamp': str(Path().cwd()),
            'fixes_applied': self.fixes_applied,
            'errors': self.errors,
            'total_fixes': len(self.fixes_applied),
            'total_errors': len(self.errors),
            'success_rate': f"{(len(self.fixes_applied)/(len(self.fixes_applied)+len(self.errors)))*100:.1f}%" if (len(self.fixes_applied)+len(self.errors)) > 0 else "0%"
        }
        
        # Save report
        report_file = f"security_fix_report_{Path().cwd().name}.json"
        import json
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Security fix report saved: {report_file}")
        
        # Print summary
        print("\n" + "=" * 50)
        print("🔧 SECURITY FIX SUMMARY")
        print("=" * 50)
        print(f"✅ Fixes Applied: {len(self.fixes_applied)}")
        print(f"❌ Errors: {len(self.errors)}")
        print(f"📊 Success Rate: {report['success_rate']}")
        
        if self.fixes_applied:
            print(f"\n✅ Applied Fixes:")
            for fix in self.fixes_applied:
                print(f"  • {fix}")
        
        if self.errors:
            print(f"\n❌ Errors:")
            for error in self.errors:
                print(f"  • {error}")
        
        print("\n" + "=" * 50)

def main():
    """Main function to run security fixes"""
    print("🔧 HIPAA Checklist Project - Security Issues Fix")
    print("Final Week Security Verification - Fixing Critical Issues")
    print("=" * 60)
    
    fixer = SecurityFixer()
    fixes_count, errors_count = fixer.fix_all_security_issues()
    
    return fixes_count, errors_count

if __name__ == '__main__':
    main()
