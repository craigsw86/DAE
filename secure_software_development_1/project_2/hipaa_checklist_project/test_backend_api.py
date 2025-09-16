#!/usr/bin/env python3
"""
Comprehensive Backend SQLite API Connectivity Testing
Tests Django backend with SQLite database integration
"""

import os
import sys
import requests
import json
import time
import sqlite3
from datetime import datetime
from pathlib import Path

# Add backend to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')

class BackendAPITester:
    """Comprehensive backend API testing"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.api_url = f"{self.base_url}/api"
        self.test_results = []
        self.auth_token = None
        self.refresh_token = None
        
    def log_test(self, test_name, success, message="", data=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status} {message}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
    
    def test_database_connection(self):
        """Test SQLite database connection"""
        print("\n📝 Test 1: Database Connection")
        print("-" * 40)
        
        try:
            db_path = backend_dir / "db.sqlite3"
            if not db_path.exists():
                self.log_test("Database File", False, "Database file not found")
                return False
            
            # Test database connection
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Test basic query
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            self.log_test("Database Connection", True, f"Connected successfully")
            self.log_test("Database Tables", True, f"Found {len(tables)} tables")
            
            # List tables
            table_names = [table[0] for table in tables]
            self.log_test("Table List", True, f"Tables: {', '.join(table_names[:5])}{'...' if len(table_names) > 5 else ''}")
            
            conn.close()
            return True
            
        except Exception as e:
            self.log_test("Database Connection", False, f"Error: {e}")
            return False
    
    def test_django_setup(self):
        """Test Django setup and configuration"""
        print("\n📝 Test 2: Django Setup")
        print("-" * 40)
        
        try:
            import django
            from django.conf import settings
            from django.core.management import execute_from_command_line
            
            # Test Django configuration
            self.log_test("Django Import", True, f"Version: {django.get_version()}")
            self.log_test("Settings Load", True, f"Debug: {settings.DEBUG}")
            self.log_test("Database Config", True, f"Engine: {settings.DATABASES['default']['ENGINE']}")
            
            # Test migrations
            try:
                result = execute_from_command_line(['manage.py', 'migrate', '--check'])
                self.log_test("Migrations Check", True, "Migrations are up to date")
            except:
                self.log_test("Migrations Check", False, "Migration issues detected")
            
            return True
            
        except Exception as e:
            self.log_test("Django Setup", False, f"Error: {e}")
            return False
    
    def test_server_availability(self):
        """Test if Django server is running"""
        print("\n📝 Test 3: Server Availability")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/api/health/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Server Health", True, f"Status: {data.get('status', 'unknown')}")
                return True
            else:
                self.log_test("Server Health", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Server Health", False, f"Error: {e}")
            return False
    
    def test_public_endpoints(self):
        """Test public API endpoints"""
        print("\n📝 Test 4: Public Endpoints")
        print("-" * 40)
        
        public_endpoints = [
            ("/api/health/", "Health Check"),
            ("/api/info/", "API Info"),
            ("/api/stats/", "Public Stats")
        ]
        
        for endpoint, name in public_endpoints:
            try:
                response = requests.get(f"{self.api_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(f"{name} Endpoint", True, f"Status: {response.status_code}")
                    self.log_test(f"{name} Data", True, f"Response: {str(data)[:100]}...")
                else:
                    self.log_test(f"{name} Endpoint", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"{name} Endpoint", False, f"Error: {e}")
    
    def test_authentication(self):
        """Test JWT authentication"""
        print("\n📝 Test 5: Authentication")
        print("-" * 40)
        
        try:
            # Test token endpoint
            response = requests.post(f"{self.api_url}/token/", 
                                  json={"username": "testuser", "password": "testpass"}, 
                                  timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('access')
                self.refresh_token = data.get('refresh')
                self.log_test("Token Generation", True, "JWT tokens generated")
                return True
            else:
                self.log_test("Token Generation", False, f"Status: {response.status_code}")
                
                # Try to create a test user
                self.create_test_user()
                return False
                
        except Exception as e:
            self.log_test("Authentication", False, f"Error: {e}")
            return False
    
    def create_test_user(self):
        """Create a test user for authentication"""
        print("\n📝 Creating Test User")
        print("-" * 40)
        
        try:
            # Import Django modules
            import django
            django.setup()
            
            from django.contrib.auth.models import User
            from django.contrib.auth import authenticate
            
            # Create test user
            user, created = User.objects.get_or_create(
                username='testuser',
                defaults={
                    'email': 'test@example.com',
                    'first_name': 'Test',
                    'last_name': 'User'
                }
            )
            
            if created:
                user.set_password('testpass')
                user.save()
                self.log_test("Test User Creation", True, "User created successfully")
            else:
                self.log_test("Test User Creation", True, "User already exists")
            
            # Test authentication
            user = authenticate(username='testuser', password='testpass')
            if user:
                self.log_test("User Authentication", True, "User authenticated successfully")
            else:
                self.log_test("User Authentication", False, "Authentication failed")
            
            return True
            
        except Exception as e:
            self.log_test("Test User Creation", False, f"Error: {e}")
            return False
    
    def test_protected_endpoints(self):
        """Test protected API endpoints"""
        print("\n📝 Test 6: Protected Endpoints")
        print("-" * 40)
        
        if not self.auth_token:
            self.log_test("Protected Endpoints", False, "No authentication token available")
            return False
        
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        
        protected_endpoints = [
            ("/api/checklist/", "Checklist API"),
            ("/api/regulations/", "Regulations API"),
            ("/api/report/", "Compliance Report API"),
            ("/api/profile/", "User Profile API")
        ]
        
        for endpoint, name in protected_endpoints:
            try:
                response = requests.get(f"{self.api_url}{endpoint}", headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(f"{name} (Auth)", True, f"Status: {response.status_code}")
                    self.log_test(f"{name} Data", True, f"Response: {str(data)[:100]}...")
                elif response.status_code == 401:
                    self.log_test(f"{name} (Auth)", False, "Unauthorized - token may be invalid")
                else:
                    self.log_test(f"{name} (Auth)", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"{name} (Auth)", False, f"Error: {e}")
    
    def test_database_operations(self):
        """Test database CRUD operations"""
        print("\n📝 Test 7: Database Operations")
        print("-" * 40)
        
        try:
            import django
            django.setup()
            
            from checklist.models import ChecklistItem, RegulationUpdate
            from django.contrib.auth.models import User
            
            # Test model imports
            self.log_test("Model Imports", True, "All models imported successfully")
            
            # Test database queries
            total_items = ChecklistItem.objects.count()
            total_regulations = RegulationUpdate.objects.count()
            total_users = User.objects.count()
            
            self.log_test("Checklist Items Count", True, f"Count: {total_items}")
            self.log_test("Regulations Count", True, f"Count: {total_regulations}")
            self.log_test("Users Count", True, f"Count: {total_users}")
            
            # Test creating a test record
            try:
                user = User.objects.first()
                if user:
                    regulation = RegulationUpdate.objects.first()
                    if regulation:
                        item, created = ChecklistItem.objects.get_or_create(
                            user=user,
                            regulation_update=regulation,
                            defaults={'completed': False, 'notes': 'Test item'}
                        )
                        if created:
                            self.log_test("Database Create", True, "Test item created")
                        else:
                            self.log_test("Database Create", True, "Test item already exists")
                    else:
                        self.log_test("Database Create", False, "No regulations available")
                else:
                    self.log_test("Database Create", False, "No users available")
            except Exception as e:
                self.log_test("Database Create", False, f"Error: {e}")
            
            return True
            
        except Exception as e:
            self.log_test("Database Operations", False, f"Error: {e}")
            return False
    
    def test_api_performance(self):
        """Test API performance"""
        print("\n📝 Test 8: API Performance")
        print("-" * 40)
        
        endpoints_to_test = [
            ("/api/health/", "Health Check"),
            ("/api/info/", "API Info"),
            ("/api/stats/", "Public Stats")
        ]
        
        for endpoint, name in endpoints_to_test:
            try:
                # Test response time
                start_time = time.time()
                response = requests.get(f"{self.api_url}{endpoint}", timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    if response_time < 0.5:
                        self.log_test(f"{name} Performance", True, f"Fast: {response_time:.3f}s")
                    elif response_time < 1.0:
                        self.log_test(f"{name} Performance", True, f"Good: {response_time:.3f}s")
                    else:
                        self.log_test(f"{name} Performance", False, f"Slow: {response_time:.3f}s")
                else:
                    self.log_test(f"{name} Performance", False, f"Status: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"{name} Performance", False, f"Error: {e}")
    
    def test_error_handling(self):
        """Test API error handling"""
        print("\n📝 Test 9: Error Handling")
        print("-" * 40)
        
        # Test 404 endpoint
        try:
            response = requests.get(f"{self.api_url}/nonexistent/", timeout=10)
            if response.status_code == 404:
                self.log_test("404 Handling", True, "Correctly returns 404")
            else:
                self.log_test("404 Handling", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("404 Handling", False, f"Error: {e}")
        
        # Test invalid JSON
        try:
            response = requests.post(f"{self.api_url}/token/", 
                                  data="invalid json", 
                                  headers={'Content-Type': 'application/json'},
                                  timeout=10)
            if response.status_code == 400:
                self.log_test("Invalid JSON Handling", True, "Correctly returns 400")
            else:
                self.log_test("Invalid JSON Handling", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("Invalid JSON Handling", False, f"Error: {e}")
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 BACKEND SQLITE API CONNECTIVITY TEST REPORT")
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
        report_file = f"backend_api_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """Run all backend API tests"""
        print("🧪 Starting Backend SQLite API Connectivity Tests")
        print("=" * 60)
        
        self.test_database_connection()
        self.test_django_setup()
        self.test_server_availability()
        self.test_public_endpoints()
        self.test_authentication()
        self.test_protected_endpoints()
        self.test_database_operations()
        self.test_api_performance()
        self.test_error_handling()
        
        return self.generate_report()

def main():
    """Main function"""
    tester = BackendAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All backend API tests passed!")
        print("✅ Django backend is properly connected to SQLite!")
        print("✅ All API endpoints are working correctly!")
    else:
        print("\n⚠️  Some backend API tests failed.")
        print("Please check the configuration and try again.")
    
    return success

if __name__ == '__main__':
    main()
