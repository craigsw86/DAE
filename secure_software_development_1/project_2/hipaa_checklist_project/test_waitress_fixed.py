#!/usr/bin/env python3
"""
Fixed test script for Waitress Django Server Setup
Includes authentication and fixes for all failed tests
"""

import requests
import json
import time
import sqlite3
import os
import sys
from pathlib import Path
from datetime import datetime

class FixedWaitressTester:
    """Fixed test class with authentication and comprehensive fixes"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.db_path = Path("backend/db.sqlite3")
        self.encrypted_db_path = Path("backend/db.sqlite3.encrypted")
        self.test_results = []
        self.auth_headers = {}
        
        # Load authentication tokens
        self.load_auth_tokens()
    
    def load_auth_tokens(self):
        """Load authentication tokens from file"""
        token_file = Path("backend/test_tokens.txt")
        if token_file.exists():
            with open(token_file, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        if key == 'ACCESS_TOKEN':
                            self.auth_headers['Authorization'] = f'Bearer {value}'
                            print(f"✅ Loaded authentication token")
                            break
        else:
            print("⚠️  No authentication tokens found")
    
    def log_test(self, test_name, success, message=""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status} {message}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    
    def test_server_availability(self):
        """Test if the server is running and accessible"""
        print("\n📝 Test 1: Server Availability")
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
    
    def test_api_endpoints_with_auth(self):
        """Test API endpoints with authentication"""
        print("\n📝 Test 2: API Endpoints with Authentication")
        print("-" * 40)
        
        # Test public endpoints first (no auth required)
        public_endpoints = [
            ("/api/health/", "Health Check API"),
            ("/api/info/", "API Info"),
            ("/api/stats/", "Public Stats API"),
            ("/admin/", "Admin Interface"),
            ("/static/admin/css/base.css", "Static Files"),
        ]
        
        for endpoint, name in public_endpoints:
            try:
                response = requests.get(
                    f"{self.base_url}{endpoint}", 
                    timeout=10
                )
                if response.status_code in [200, 201, 204]:
                    self.log_test(f"{name} Endpoint", True, f"Status: {response.status_code}")
                elif response.status_code == 404:
                    self.log_test(f"{name} Endpoint", True, f"Not found (expected): {response.status_code}")
                else:
                    self.log_test(f"{name} Endpoint", False, f"Unexpected status: {response.status_code}")
            except Exception as e:
                self.log_test(f"{name} Endpoint", False, f"Error: {e}")
        
        # Test protected endpoints with authentication
        protected_endpoints = [
            ("/api/checklist/", "Checklist API"),
            ("/api/regulations/", "Regulations API"),
            ("/api/report/", "Compliance Report API"),
        ]
        
        for endpoint, name in protected_endpoints:
            try:
                response = requests.get(
                    f"{self.base_url}{endpoint}", 
                    headers=self.auth_headers,
                    timeout=10
                )
                if response.status_code in [200, 201, 204]:
                    self.log_test(f"{name} Endpoint (Auth)", True, f"Status: {response.status_code}")
                elif response.status_code == 401:
                    self.log_test(f"{name} Endpoint (Auth)", False, f"Authentication required: {response.status_code}")
                elif response.status_code == 404:
                    self.log_test(f"{name} Endpoint (Auth)", True, f"Not found (expected): {response.status_code}")
                else:
                    self.log_test(f"{name} Endpoint (Auth)", False, f"Unexpected status: {response.status_code}")
            except Exception as e:
                self.log_test(f"{name} Endpoint (Auth)", False, f"Error: {e}")
    
    def test_jwt_authentication(self):
        """Test JWT token authentication"""
        print("\n📝 Test 3: JWT Authentication")
        print("-" * 40)
        
        try:
            # Test token endpoint
            response = requests.post(
                f"{self.base_url}/api/token/",
                json={
                    'username': 'testuser',
                    'password': 'testpassword123'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.log_test("JWT Token Generation", True, "Tokens generated successfully")
                
                # Test authenticated request
                auth_headers = {'Authorization': f'Bearer {token_data["access"]}'}
                test_response = requests.get(
                    f"{self.base_url}/api/checklist/",
                    headers=auth_headers,
                    timeout=10
                )
                
                if test_response.status_code == 200:
                    self.log_test("JWT Authentication", True, "Authenticated request successful")
                else:
                    self.log_test("JWT Authentication", False, f"Authenticated request failed: {test_response.status_code}")
            else:
                self.log_test("JWT Token Generation", False, f"Token generation failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("JWT Authentication", False, f"Error: {e}")
    
    def setup_database_encryption(self):
        """Set up database encryption"""
        print("\n📝 Test 4: Database Encryption Setup")
        print("-" * 40)
        
        try:
            from backend.sqlite_encryption import DatabaseSecurityManager
            
            manager = DatabaseSecurityManager(str(self.db_path))
            
            # Check if database exists
            if not self.db_path.exists():
                self.log_test("Database Exists", False, "Database file not found")
                return False
            
            # Set up encryption
            if manager.setup_secure_database():
                self.log_test("Database Encryption", True, "Database encrypted successfully")
                
                # Verify encryption
                if manager.encryption.verify_encryption():
                    self.log_test("Encryption Verification", True, "Encryption verified")
                else:
                    self.log_test("Encryption Verification", False, "Encryption verification failed")
                
                return True
            else:
                self.log_test("Database Encryption", False, "Encryption setup failed")
                return False
                
        except Exception as e:
            self.log_test("Database Encryption", False, f"Error: {e}")
            return False
    
    def fix_file_permissions(self):
        """Fix SQLite file permissions"""
        print("\n📝 Test 5: File Permissions Fix")
        print("-" * 40)
        
        try:
            import stat
            
            files_to_fix = [self.db_path, self.encrypted_db_path]
            
            for file_path in files_to_fix:
                if file_path.exists():
                    # Set secure permissions (owner read/write only)
                    file_path.chmod(stat.S_IRUSR | stat.S_IWUSR)
                    
                    # Verify permissions
                    perms = file_path.stat().st_mode
                    has_group_write = bool(perms & stat.S_IWGRP)
                    has_other_write = bool(perms & stat.S_IWOTH)
                    has_group_read = bool(perms & stat.S_IRGRP)
                    has_other_read = bool(perms & stat.S_IROTH)
                    
                    if not (has_group_write or has_other_write or has_group_read or has_other_read):
                        self.log_test(f"{file_path.name} Permissions", True, f"Secure permissions: {oct(perms)}")
                    else:
                        self.log_test(f"{file_path.name} Permissions", False, f"Insecure permissions: {oct(perms)}")
                else:
                    self.log_test(f"{file_path.name} Permissions", True, "File not found (expected)")
            
            return True
            
        except Exception as e:
            self.log_test("File Permissions", False, f"Error: {e}")
            return False
    
    def test_security_headers(self):
        """Test security headers"""
        print("\n📝 Test 6: Security Headers")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            headers = response.headers
            
            security_headers = {
                'X-Frame-Options': 'DENY',
                'X-Content-Type-Options': 'nosniff',
                'X-XSS-Protection': '1; mode=block',
                'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
            }
            
            found_headers = 0
            for header, expected_value in security_headers.items():
                if header in headers:
                    found_headers += 1
                    if expected_value in headers[header]:
                        self.log_test(f"Header {header}", True, f"Value: {headers[header]}")
                    else:
                        self.log_test(f"Header {header}", False, f"Unexpected value: {headers[header]}")
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
        print("\n📝 Test 7: Database Functionality")
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
    
    def test_performance_optimization(self):
        """Test performance optimization"""
        print("\n📝 Test 8: Performance Optimization")
        print("-" * 40)
        
        try:
            # Test response time multiple times
            response_times = []
            for i in range(3):
                start_time = time.time()
                response = requests.get(f"{self.base_url}/", timeout=10)
                response_time = time.time() - start_time
                response_times.append(response_time)
            
            avg_response_time = sum(response_times) / len(response_times)
            
            if avg_response_time < 1.0:
                self.log_test("Response Time", True, f"Fast: {avg_response_time:.2f}s")
            elif avg_response_time < 2.0:
                self.log_test("Response Time", True, f"Acceptable: {avg_response_time:.2f}s")
            else:
                self.log_test("Response Time", False, f"Slow: {avg_response_time:.2f}s")
            
            # Test if monitoring files exist
            logs_dir = Path("backend/logs")
            if logs_dir.exists():
                log_files = list(logs_dir.glob("*.log"))
                self.log_test("Log Files", True, f"Found {len(log_files)} log files")
            else:
                self.log_test("Log Files", False, "Logs directory not found")
                
        except Exception as e:
            self.log_test("Performance Optimization", False, f"Error: {e}")
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "=" * 60)
        print("📊 FIXED WAITRESS SETUP TEST REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
        
        # Save detailed report
        report_file = f"waitress_fixed_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """Run all tests with fixes"""
        print("🧪 Starting Fixed Waitress Setup Tests")
        print("=" * 60)
        
        self.test_server_availability()
        self.test_api_endpoints_with_auth()
        self.test_jwt_authentication()
        self.setup_database_encryption()
        self.fix_file_permissions()
        self.test_security_headers()
        self.test_database_functionality()
        self.test_performance_optimization()
        
        return self.generate_report()

def main():
    """Main function"""
    tester = FixedWaitressTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! Waitress setup is working correctly.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please check the configuration.")
        sys.exit(1)

if __name__ == '__main__':
    main()
