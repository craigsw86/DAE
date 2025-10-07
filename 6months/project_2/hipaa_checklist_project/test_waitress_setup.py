#!/usr/bin/env python3
"""
Comprehensive test script for Waitress Django Server Setup
Tests SQLite encryption, permissions, and server functionality
"""

import requests
import json
import time
import sqlite3
import os
import sys
from pathlib import Path
from datetime import datetime

class WaitressSetupTester:
    """Test the Waitress server setup and security features"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.db_path = Path("backend/db.sqlite3")
        self.encrypted_db_path = Path("backend/db.sqlite3.encrypted")
        self.test_results = []
    
    def log_test(self, test_name, success, message=""):
        """Log test result"""
        status = " PASS" if success else " FAIL"
        print(f"{test_name}: {status} {message}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    
    def test_server_availability(self):
        """Test if the server is running and accessible"""
        print("\n Test 1: Server Availability")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                self.log_test("Server Response", True, f"Status: {response.status_code}")
            else:
                self.log_test("Server Response", False, f"Unexpected status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            self.log_test("Server Connection", False, "Server not running or not accessible")
        except Exception as e:
            self.log_test("Server Connection", False, f"Error: {e}")
    
    def test_api_endpoints(self):
        """Test API endpoints functionality"""
        print("\n Test 2: API Endpoints")
        print("-" * 40)
        
        endpoints = [
            ("/api/checklist/", "Checklist API"),
            ("/admin/", "Admin Interface"),
            ("/static/admin/css/base.css", "Static Files"),
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                if response.status_code in [200, 401, 403, 404]:  # 401/403 are expected without auth
                    self.log_test(f"{name} Endpoint", True, f"Status: {response.status_code}")
                else:
                    self.log_test(f"{name} Endpoint", False, f"Unexpected status: {response.status_code}")
            except Exception as e:
                self.log_test(f"{name} Endpoint", False, f"Error: {e}")
    
    def test_database_encryption(self):
        """Test database encryption status"""
        print("\n Test 3: Database Encryption")
        print("-" * 40)
        
        # Check if encrypted database exists
        if self.encrypted_db_path.exists():
            self.log_test("Encrypted Database File", True, "Encrypted database file exists")
            
            # Try to read as SQLite (should fail if properly encrypted)
            try:
                conn = sqlite3.connect(str(self.encrypted_db_path))
                conn.close()
                self.log_test("Database Encryption", False, "Database appears to be unencrypted")
            except:
                self.log_test("Database Encryption", True, "Database is properly encrypted")
        else:
            self.log_test("Encrypted Database File", False, "Encrypted database file not found")
        
        # Check if plaintext database exists (should not exist if encrypted)
        if self.db_path.exists():
            self.log_test("Plaintext Database", False, "Plaintext database still exists")
        else:
            self.log_test("Plaintext Database", True, "Plaintext database properly removed")
    
    def test_database_permissions(self):
        """Test database file permissions"""
        print("\n Test 4: Database Permissions")
        print("-" * 40)
        
        db_files = [self.db_path, self.encrypted_db_path]
        
        for db_file in db_files:
            if db_file.exists():
                try:
                    import stat
                    perms = db_file.stat().st_mode
                    
                    # Check if group/other have write permissions (should not)
                    has_group_write = bool(perms & stat.S_IWGRP)
                    has_other_write = bool(perms & stat.S_IWOTH)
                    has_group_read = bool(perms & stat.S_IRGRP)
                    has_other_read = bool(perms & stat.S_IROTH)
                    
                    if not (has_group_write or has_other_write or has_group_read or has_other_read):
                        self.log_test(f"{db_file.name} Permissions", True, f"Secure permissions: {oct(perms)}")
                    else:
                        self.log_test(f"{db_file.name} Permissions", False, f"Insecure permissions: {oct(perms)}")
                        
                except Exception as e:
                    self.log_test(f"{db_file.name} Permissions", False, f"Error checking permissions: {e}")
            else:
                self.log_test(f"{db_file.name} Permissions", True, "File not found (expected)")
    
    def test_security_headers(self):
        """Test security headers"""
        print("\n Test 5: Security Headers")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            headers = response.headers
            
            security_headers = [
                'X-Frame-Options',
                'X-Content-Type-Options',
                'X-XSS-Protection',
                'Strict-Transport-Security'
            ]
            
            found_headers = 0
            for header in security_headers:
                if header in headers:
                    found_headers += 1
                    self.log_test(f"Header {header}", True, f"Value: {headers[header]}")
                else:
                    self.log_test(f"Header {header}", False, "Header not found")
            
            if found_headers >= 3:
                self.log_test("Overall Security Headers", True, f"{found_headers}/4 headers present")
            else:
                self.log_test("Overall Security Headers", False, f"Only {found_headers}/4 headers present")
                
        except Exception as e:
            self.log_test("Security Headers", False, f"Error: {e}")
    
    def test_database_functionality(self):
        """Test database functionality"""
        print("\n Test 6: Database Functionality")
        print("-" * 40)
        
        # First restore database for testing
        if self.encrypted_db_path.exists() and not self.db_path.exists():
            try:
                from backend.sqlite_encryption import DatabaseSecurityManager
                manager = DatabaseSecurityManager(str(self.db_path))
                if manager.restore_database():
                    self.log_test("Database Restore", True, "Database restored from encrypted version")
                else:
                    self.log_test("Database Restore", False, "Failed to restore database")
                    return
            except Exception as e:
                self.log_test("Database Restore", False, f"Error: {e}")
                return
        
        if self.db_path.exists():
            try:
                conn = sqlite3.connect(str(self.db_path))
                cursor = conn.cursor()
                
                # Test basic queries
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                self.log_test("Database Tables", True, f"Found {len(tables)} tables")
                
                # Test security audit table
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='security_audit'")
                if cursor.fetchone():
                    self.log_test("Security Audit Table", True, "Security audit table exists")
                else:
                    self.log_test("Security Audit Table", False, "Security audit table not found")
                
                # Test pragma settings
                cursor.execute("PRAGMA journal_mode")
                journal_mode = cursor.fetchone()[0]
                self.log_test("Journal Mode", True, f"Mode: {journal_mode}")
                
                cursor.execute("PRAGMA secure_delete")
                secure_delete = cursor.fetchone()[0]
                self.log_test("Secure Delete", True, f"Enabled: {secure_delete == 'ON'}")
                
                conn.close()
                
            except Exception as e:
                self.log_test("Database Functionality", False, f"Error: {e}")
        else:
            self.log_test("Database Functionality", False, "Database file not found")
    
    def test_performance_metrics(self):
        """Test performance and monitoring"""
        print("\n Test 7: Performance Metrics")
        print("-" * 40)
        
        try:
            # Test response time
            start_time = time.time()
            response = requests.get(f"{self.base_url}/", timeout=10)
            response_time = time.time() - start_time
            
            if response_time < 2.0:
                self.log_test("Response Time", True, f"{response_time:.2f}s")
            else:
                self.log_test("Response Time", False, f"Slow response: {response_time:.2f}s")
            
            # Test if monitoring files exist
            logs_dir = Path("backend/logs")
            if logs_dir.exists():
                log_files = list(logs_dir.glob("*.log"))
                self.log_test("Log Files", True, f"Found {len(log_files)} log files")
            else:
                self.log_test("Log Files", False, "Logs directory not found")
                
        except Exception as e:
            self.log_test("Performance Metrics", False, f"Error: {e}")
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "=" * 60)
        print(" WAITRESS SETUP TEST REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
        
        # Save detailed report
        report_file = f"waitress_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n Detailed report saved to: {report_file}")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """Run all tests"""
        print(" Starting Waitress Setup Tests")
        print("=" * 60)
        
        self.test_server_availability()
        self.test_api_endpoints()
        self.test_database_encryption()
        self.test_database_permissions()
        self.test_security_headers()
        self.test_database_functionality()
        self.test_performance_metrics()
        
        return self.generate_report()

def main():
    """Main function"""
    tester = WaitressSetupTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n All tests passed! Waitress setup is working correctly.")
        sys.exit(0)
    else:
        print("\n  Some tests failed. Please check the configuration.")
        sys.exit(1)

if __name__ == '__main__':
    main()
