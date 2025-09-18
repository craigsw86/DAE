#!/usr/bin/env python3
"""
Comprehensive Docker setup testing script
Tests Docker containers, services, and integration
"""

import requests
import time
import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime

class DockerSetupTester:
    """Test Docker containerization setup"""
    
    def __init__(self):
        self.test_results = []
        self.base_url = "http://localhost"
        self.api_url = f"{self.base_url}/api"
        self.frontend_url = f"{self.base_url}"
        
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
    
    def test_docker_installation(self):
        """Test if Docker is installed and running"""
        print("\n📝 Test 1: Docker Installation")
        print("-" * 40)
        
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log_test("Docker Installation", True, f"Version: {result.stdout.strip()}")
            else:
                self.log_test("Docker Installation", False, "Docker not found")
                return False
        except Exception as e:
            self.log_test("Docker Installation", False, f"Error: {e}")
            return False
        
        try:
            result = subprocess.run(['docker-compose', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log_test("Docker Compose", True, f"Version: {result.stdout.strip()}")
            else:
                self.log_test("Docker Compose", False, "Docker Compose not found")
                return False
        except Exception as e:
            self.log_test("Docker Compose", False, f"Error: {e}")
            return False
        
        return True
    
    def test_docker_containers(self):
        """Test Docker containers status"""
        print("\n📝 Test 2: Docker Containers")
        print("-" * 40)
        
        try:
            result = subprocess.run(['docker', 'ps', '--format', 'json'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                containers = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        try:
                            container = json.loads(line)
                            containers.append(container)
                        except:
                            continue
                
                expected_containers = ['hipaa_backend', 'hipaa_frontend', 'hipaa_nginx']
                running_containers = [c['Names'] for c in containers]
                
                for expected in expected_containers:
                    if any(expected in name for name in running_containers):
                        self.log_test(f"Container {expected}", True, "Running")
                    else:
                        self.log_test(f"Container {expected}", False, "Not running")
                
                self.log_test("Total Containers", True, f"Found {len(containers)} containers")
                return True
            else:
                self.log_test("Container Status", False, "Failed to get container status")
                return False
        except Exception as e:
            self.log_test("Container Status", False, f"Error: {e}")
            return False
    
    def test_nginx_proxy(self):
        """Test Nginx reverse proxy"""
        print("\n📝 Test 3: Nginx Reverse Proxy")
        print("-" * 40)
        
        try:
            response = requests.get(self.base_url, timeout=10)
            if response.status_code == 200:
                self.log_test("Nginx Proxy", True, f"Status: {response.status_code}")
            else:
                self.log_test("Nginx Proxy", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("Nginx Proxy", False, f"Error: {e}")
    
    def test_django_backend(self):
        """Test Django backend through proxy"""
        print("\n📝 Test 4: Django Backend")
        print("-" * 40)
        
        endpoints = [
            ("/api/health/", "Health Check"),
            ("/api/info/", "API Info"),
            ("/admin/", "Admin Interface"),
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.api_url}{endpoint}", timeout=10)
                if response.status_code in [200, 401, 403]:
                    self.log_test(f"{name} Endpoint", True, f"Status: {response.status_code}")
                else:
                    self.log_test(f"{name} Endpoint", False, f"Unexpected status: {response.status_code}")
            except Exception as e:
                self.log_test(f"{name} Endpoint", False, f"Error: {e}")
    
    def test_react_frontend(self):
        """Test React frontend"""
        print("\n📝 Test 5: React Frontend")
        print("-" * 40)
        
        try:
            response = requests.get(self.frontend_url, timeout=10)
            if response.status_code == 200:
                # Check if it's serving React content
                if 'react' in response.text.lower() or 'root' in response.text.lower():
                    self.log_test("React Frontend", True, "React content served")
                else:
                    self.log_test("React Frontend", False, "No React content detected")
            else:
                self.log_test("React Frontend", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("React Frontend", False, f"Error: {e}")
    
    def test_database_connectivity(self):
        """Test database connectivity"""
        print("\n📝 Test 6: Database Connectivity")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.api_url}/stats/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'total_items' in data:
                    self.log_test("Database Connection", True, f"Items: {data['total_items']}")
                else:
                    self.log_test("Database Connection", False, "No database data")
            else:
                self.log_test("Database Connection", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Database Connection", False, f"Error: {e}")
    
    def test_static_files(self):
        """Test static file serving"""
        print("\n📝 Test 7: Static Files")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/static/admin/css/base.css", timeout=10)
            if response.status_code == 200:
                self.log_test("Static Files", True, "CSS files served")
            else:
                self.log_test("Static Files", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Static Files", False, f"Error: {e}")
    
    def test_cors_headers(self):
        """Test CORS headers"""
        print("\n📝 Test 8: CORS Headers")
        print("-" * 40)
        
        try:
            response = requests.options(f"{self.api_url}/health/", timeout=10)
            headers = response.headers
            
            cors_headers = [
                'Access-Control-Allow-Origin',
                'Access-Control-Allow-Methods',
                'Access-Control-Allow-Headers'
            ]
            
            found_headers = 0
            for header in cors_headers:
                if header in headers:
                    found_headers += 1
                    self.log_test(f"CORS {header}", True, f"Value: {headers[header]}")
                else:
                    self.log_test(f"CORS {header}", False, "Header not found")
            
            if found_headers >= 2:
                self.log_test("CORS Configuration", True, f"{found_headers}/3 headers present")
            else:
                self.log_test("CORS Configuration", False, f"Only {found_headers}/3 headers present")
                
        except Exception as e:
            self.log_test("CORS Headers", False, f"Error: {e}")
    
    def test_performance(self):
        """Test performance metrics"""
        print("\n📝 Test 9: Performance")
        print("-" * 40)
        
        try:
            # Test response time
            start_time = time.time()
            response = requests.get(self.base_url, timeout=10)
            response_time = time.time() - start_time
            
            if response_time < 1.0:
                self.log_test("Response Time", True, f"Fast: {response_time:.2f}s")
            elif response_time < 3.0:
                self.log_test("Response Time", True, f"Acceptable: {response_time:.2f}s")
            else:
                self.log_test("Response Time", False, f"Slow: {response_time:.2f}s")
            
            # Test concurrent requests
            import threading
            results = []
            
            def make_request():
                try:
                    resp = requests.get(f"{self.api_url}/health/", timeout=5)
                    results.append(resp.status_code == 200)
                except:
                    results.append(False)
            
            threads = []
            for _ in range(5):
                thread = threading.Thread(target=make_request)
                threads.append(thread)
                thread.start()
            
            for thread in threads:
                thread.join()
            
            success_rate = sum(results) / len(results) * 100
            if success_rate >= 80:
                self.log_test("Concurrent Requests", True, f"Success rate: {success_rate:.1f}%")
            else:
                self.log_test("Concurrent Requests", False, f"Success rate: {success_rate:.1f}%")
                
        except Exception as e:
            self.log_test("Performance", False, f"Error: {e}")
    
    def test_docker_volumes(self):
        """Test Docker volumes"""
        print("\n📝 Test 10: Docker Volumes")
        print("-" * 40)
        
        try:
            result = subprocess.run(['docker', 'volume', 'ls', '--format', 'json'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                volumes = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        try:
                            volume = json.loads(line)
                            volumes.append(volume)
                        except:
                            continue
                
                expected_volumes = ['database_data', 'logs_data', 'backups_data']
                volume_names = [v['Name'] for v in volumes]
                
                for expected in expected_volumes:
                    if any(expected in name for name in volume_names):
                        self.log_test(f"Volume {expected}", True, "Exists")
                    else:
                        self.log_test(f"Volume {expected}", False, "Not found")
                
                self.log_test("Total Volumes", True, f"Found {len(volumes)} volumes")
                return True
            else:
                self.log_test("Volume Status", False, "Failed to get volume status")
                return False
        except Exception as e:
            self.log_test("Volume Status", False, f"Error: {e}")
            return False
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "=" * 60)
        print("📊 DOCKER SETUP TEST REPORT")
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
        report_file = f"docker_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """Run all Docker tests"""
        print("🐳 Starting Docker Setup Tests")
        print("=" * 60)
        
        if not self.test_docker_installation():
            print("❌ Docker not available. Please install Docker and Docker Compose.")
            return False
        
        self.test_docker_containers()
        self.test_nginx_proxy()
        self.test_django_backend()
        self.test_react_frontend()
        self.test_database_connectivity()
        self.test_static_files()
        self.test_cors_headers()
        self.test_performance()
        self.test_docker_volumes()
        
        return self.generate_report()

def main():
    """Main function"""
    tester = DockerSetupTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All Docker tests passed! Setup is working correctly.")
        sys.exit(0)
    else:
        print("\n⚠️  Some Docker tests failed. Please check the configuration.")
        sys.exit(1)

if __name__ == '__main__':
    main()
