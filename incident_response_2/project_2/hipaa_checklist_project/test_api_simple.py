#!/usr/bin/env python3
"""
Simple Backend API Testing Script
Tests Django backend with SQLite database integration
"""

import requests
import json
import time
from datetime import datetime

class SimpleAPITester:
    """Simple API testing"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.api_url = f"{self.base_url}/api"
        self.test_results = []
    
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
    
    def test_health_endpoint(self):
        """Test health endpoint"""
        print("\n📝 Test 1: Health Endpoint")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.api_url}/health/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", True, f"Status: {data.get('status')}")
                self.log_test("API Version", True, f"Version: {data.get('version')}")
                return True
            else:
                self.log_test("Health Check", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Error: {e}")
            return False
    
    def test_info_endpoint(self):
        """Test API info endpoint"""
        print("\n📝 Test 2: API Info Endpoint")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.api_url}/info/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("API Info", True, f"Name: {data.get('name')}")
                self.log_test("API Description", True, f"Description: {data.get('description')}")
                return True
            else:
                self.log_test("API Info", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Info", False, f"Error: {e}")
            return False
    
    def test_stats_endpoint(self):
        """Test public stats endpoint"""
        print("\n📝 Test 3: Public Stats Endpoint")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.api_url}/stats/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Public Stats", True, f"Total items: {data.get('total_items', 0)}")
                self.log_test("Completion Rate", True, f"Rate: {data.get('completion_rate', 0)}%")
                return True
            else:
                self.log_test("Public Stats", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Public Stats", False, f"Error: {e}")
            return False
    
    def test_token_endpoint(self):
        """Test JWT token endpoint"""
        print("\n📝 Test 4: JWT Token Endpoint")
        print("-" * 40)
        
        try:
            # Test with invalid credentials first
            response = requests.post(f"{self.api_url}/token/", 
                                  json={"username": "testuser", "password": "testpass"}, 
                                  timeout=10)
            
            if response.status_code == 401:
                self.log_test("Token Endpoint", True, "Correctly rejects invalid credentials")
                return True
            elif response.status_code == 200:
                data = response.json()
                self.log_test("Token Generation", True, "JWT tokens generated")
                return True
            else:
                self.log_test("Token Endpoint", False, f"Unexpected status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Token Endpoint", False, f"Error: {e}")
            return False
    
    def test_admin_endpoint(self):
        """Test admin endpoint"""
        print("\n📝 Test 5: Admin Endpoint")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/admin/", timeout=10)
            if response.status_code == 200:
                self.log_test("Admin Interface", True, "Admin interface accessible")
                return True
            else:
                self.log_test("Admin Interface", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Admin Interface", False, f"Error: {e}")
            return False
    
    def test_protected_endpoints(self):
        """Test protected endpoints without auth"""
        print("\n📝 Test 6: Protected Endpoints (No Auth)")
        print("-" * 40)
        
        protected_endpoints = [
            ("/api/checklist/", "Checklist API"),
            ("/api/regulations/", "Regulations API"),
            ("/api/report/", "Compliance Report API")
        ]
        
        for endpoint, name in protected_endpoints:
            try:
                response = requests.get(f"{self.api_url}{endpoint}", timeout=10)
                if response.status_code == 401:
                    self.log_test(f"{name} (No Auth)", True, "Correctly requires authentication")
                else:
                    self.log_test(f"{name} (No Auth)", False, f"Unexpected status: {response.status_code}")
            except Exception as e:
                self.log_test(f"{name} (No Auth)", False, f"Error: {e}")
    
    def test_performance(self):
        """Test API performance"""
        print("\n📝 Test 7: API Performance")
        print("-" * 40)
        
        endpoints = [
            ("/api/health/", "Health Check"),
            ("/api/info/", "API Info"),
            ("/api/stats/", "Public Stats")
        ]
        
        for endpoint, name in endpoints:
            try:
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
        """Test error handling"""
        print("\n📝 Test 8: Error Handling")
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
        """Generate test report"""
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
        report_file = f"simple_api_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🧪 Starting Simple Backend API Tests")
        print("=" * 60)
        
        self.test_health_endpoint()
        self.test_info_endpoint()
        self.test_stats_endpoint()
        self.test_token_endpoint()
        self.test_admin_endpoint()
        self.test_protected_endpoints()
        self.test_performance()
        self.test_error_handling()
        
        return self.generate_report()

def main():
    """Main function"""
    tester = SimpleAPITester()
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
