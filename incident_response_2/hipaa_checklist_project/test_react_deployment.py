#!/usr/bin/env python3
"""
Test React deployment via Nginx
"""

import requests
import time
import json
from datetime import datetime

class ReactDeploymentTester:
    """Test React deployment functionality"""
    
    def __init__(self):
        self.base_url = "http://localhost"
        self.test_results = []
    
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
    
    def test_nginx_health(self):
        """Test Nginx health endpoint"""
        print("\n📝 Test 1: Nginx Health Check")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                self.log_test("Nginx Health", True, f"Status: {response.status_code}")
            else:
                self.log_test("Nginx Health", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("Nginx Health", False, f"Error: {e}")
    
    def test_react_app_serving(self):
        """Test React app serving"""
        print("\n📝 Test 2: React App Serving")
        print("-" * 40)
        
        try:
            response = requests.get(self.base_url, timeout=10)
            if response.status_code == 200:
                # Check if it's serving React content
                content = response.text.lower()
                if 'react' in content or 'root' in content or 'app' in content:
                    self.log_test("React App Content", True, "React content detected")
                else:
                    self.log_test("React App Content", False, "No React content detected")
                
                # Check for HTML structure
                if '<html' in content and '<body' in content:
                    self.log_test("HTML Structure", True, "Valid HTML structure")
                else:
                    self.log_test("HTML Structure", False, "Invalid HTML structure")
                
                # Check for React build files
                if 'static/js' in content or 'static/css' in content:
                    self.log_test("React Build Files", True, "Build files referenced")
                else:
                    self.log_test("React Build Files", False, "No build files referenced")
                
            else:
                self.log_test("React App Response", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("React App Serving", False, f"Error: {e}")
    
    def test_static_files(self):
        """Test static file serving"""
        print("\n📝 Test 3: Static Files")
        print("-" * 40)
        
        # Test common static file types
        static_tests = [
            ("/static/js/", "JavaScript files"),
            ("/static/css/", "CSS files"),
            ("/favicon.ico", "Favicon"),
            ("/manifest.json", "Manifest file")
        ]
        
        for path, description in static_tests:
            try:
                response = requests.get(f"{self.base_url}{path}", timeout=5)
                if response.status_code == 200:
                    self.log_test(f"Static {description}", True, f"Status: {response.status_code}")
                elif response.status_code == 404:
                    self.log_test(f"Static {description}", False, "File not found")
                else:
                    self.log_test(f"Static {description}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Static {description}", False, f"Error: {e}")
    
    def test_spa_routing(self):
        """Test Single Page Application routing"""
        print("\n📝 Test 4: SPA Routing")
        print("-" * 40)
        
        # Test various routes that should serve index.html
        spa_routes = [
            "/dashboard",
            "/checklist",
            "/reports",
            "/admin",
            "/api/test"
        ]
        
        for route in spa_routes:
            try:
                response = requests.get(f"{self.base_url}{route}", timeout=5)
                if response.status_code == 200:
                    # Should serve index.html for SPA routes
                    if '<html' in response.text.lower():
                        self.log_test(f"SPA Route {route}", True, "Serves index.html")
                    else:
                        self.log_test(f"SPA Route {route}", False, "Doesn't serve index.html")
                else:
                    self.log_test(f"SPA Route {route}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"SPA Route {route}", False, f"Error: {e}")
    
    def test_caching_headers(self):
        """Test caching headers"""
        print("\n📝 Test 5: Caching Headers")
        print("-" * 40)
        
        try:
            response = requests.get(self.base_url, timeout=10)
            headers = response.headers
            
            # Check for caching headers
            cache_headers = [
                'Cache-Control',
                'Expires',
                'ETag',
                'Last-Modified'
            ]
            
            found_headers = 0
            for header in cache_headers:
                if header in headers:
                    found_headers += 1
                    self.log_test(f"Cache Header {header}", True, f"Value: {headers[header]}")
                else:
                    self.log_test(f"Cache Header {header}", False, "Header not found")
            
            if found_headers >= 2:
                self.log_test("Caching Configuration", True, f"{found_headers}/4 headers present")
            else:
                self.log_test("Caching Configuration", False, f"Only {found_headers}/4 headers present")
                
        except Exception as e:
            self.log_test("Caching Headers", False, f"Error: {e}")
    
    def test_security_headers(self):
        """Test security headers"""
        print("\n📝 Test 6: Security Headers")
        print("-" * 40)
        
        try:
            response = requests.get(self.base_url, timeout=10)
            headers = response.headers
            
            security_headers = [
                'X-Frame-Options',
                'X-Content-Type-Options',
                'X-XSS-Protection',
                'Referrer-Policy'
            ]
            
            found_headers = 0
            for header in security_headers:
                if header in headers:
                    found_headers += 1
                    self.log_test(f"Security Header {header}", True, f"Value: {headers[header]}")
                else:
                    self.log_test(f"Security Header {header}", False, "Header not found")
            
            if found_headers >= 3:
                self.log_test("Security Configuration", True, f"{found_headers}/4 headers present")
            else:
                self.log_test("Security Configuration", False, f"Only {found_headers}/4 headers present")
                
        except Exception as e:
            self.log_test("Security Headers", False, f"Error: {e}")
    
    def test_performance(self):
        """Test performance metrics"""
        print("\n📝 Test 7: Performance")
        print("-" * 40)
        
        try:
            # Test response time
            start_time = time.time()
            response = requests.get(self.base_url, timeout=10)
            response_time = time.time() - start_time
            
            if response_time < 0.5:
                self.log_test("Response Time", True, f"Fast: {response_time:.3f}s")
            elif response_time < 1.0:
                self.log_test("Response Time", True, f"Good: {response_time:.3f}s")
            elif response_time < 2.0:
                self.log_test("Response Time", True, f"Acceptable: {response_time:.3f}s")
            else:
                self.log_test("Response Time", False, f"Slow: {response_time:.3f}s")
            
            # Test content size
            content_length = len(response.content)
            if content_length < 100000:  # 100KB
                self.log_test("Content Size", True, f"Small: {content_length} bytes")
            elif content_length < 500000:  # 500KB
                self.log_test("Content Size", True, f"Medium: {content_length} bytes")
            else:
                self.log_test("Content Size", True, f"Large: {content_length} bytes")
                
        except Exception as e:
            self.log_test("Performance", False, f"Error: {e}")
    
    def test_api_proxy(self):
        """Test API proxy to Django backend"""
        print("\n📝 Test 8: API Proxy")
        print("-" * 40)
        
        # Test API endpoints through Nginx proxy
        api_endpoints = [
            "/api/health/",
            "/api/info/",
            "/api/stats/"
        ]
        
        for endpoint in api_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                if response.status_code in [200, 401, 403]:
                    self.log_test(f"API Proxy {endpoint}", True, f"Status: {response.status_code}")
                else:
                    self.log_test(f"API Proxy {endpoint}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"API Proxy {endpoint}", False, f"Error: {e}")
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "=" * 60)
        print("📊 REACT DEPLOYMENT TEST REPORT")
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
        report_file = f"react_deployment_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """Run all React deployment tests"""
        print("🧪 Starting React Deployment Tests")
        print("=" * 60)
        
        self.test_nginx_health()
        self.test_react_app_serving()
        self.test_static_files()
        self.test_spa_routing()
        self.test_caching_headers()
        self.test_security_headers()
        self.test_performance()
        self.test_api_proxy()
        
        return self.generate_report()

def main():
    """Main function"""
    tester = ReactDeploymentTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All React deployment tests passed!")
        print("✅ React app is properly deployed via Nginx!")
    else:
        print("\n⚠️  Some React deployment tests failed.")
        print("Please check the configuration and try again.")
    
    return success

if __name__ == '__main__':
    main()
