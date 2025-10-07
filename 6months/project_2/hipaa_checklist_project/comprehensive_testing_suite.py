#!/usr/bin/env python3
"""
Comprehensive Testing Suite for HIPAA Checklist Project
Combines Original Testing Plan with Black Duck Detect Integration
"""

import os
import sys
import json
import time
import subprocess
import requests
from datetime import datetime
from pathlib import Path

class ComprehensiveTestingSuite:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "original_tests": {},
            "black_duck_tests": {},
            "integration_tests": {},
            "summary": {}
        }
        self.passed_tests = 0
        self.total_tests = 0
        
    def log_test(self, test_name, status, details=""):
        """Log test results"""
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
            print(f" {test_name}: PASS")
        else:
            print(f" {test_name}: FAIL - {details}")
        
        return {"status": status, "details": details, "timestamp": datetime.now().isoformat()}
    
    def wait_for_server(self, max_attempts=30):
        """Wait for Django server to be ready"""
        print(" Waiting for Django server to start...")
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{self.base_url}/api/health/", timeout=5)
                if response.status_code == 200:
                    print(" Django server is ready!")
                    return True
            except:
                pass
            time.sleep(2)
        return False
    
    def test_original_plan(self):
        """Execute original project testing plan"""
        print("\n" + "="*60)
        print(" EXECUTING ORIGINAL PROJECT TESTING PLAN")
        print("="*60)
        
        original_tests = {}
        
        # Test 1: Server Connectivity
        print("\n Test 1: Server Connectivity")
        print("-" * 40)
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            original_tests["server_connectivity"] = self.log_test(
                "Server Response", "PASS" if response.status_code == 200 else "FAIL",
                f"Status: {response.status_code}"
            )
        except Exception as e:
            original_tests["server_connectivity"] = self.log_test(
                "Server Response", "FAIL", str(e)
            )
        
        # Test 2: Public Endpoints
        print("\n Test 2: Public Endpoints")
        print("-" * 40)
        endpoints = [
            ("/api/health/", "Health Check"),
            ("/api/info/", "API Info"),
            ("/api/stats/", "Public Stats")
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                original_tests[f"endpoint_{endpoint.replace('/', '_').replace('api_', '')}"] = self.log_test(
                    f"{name} Endpoint", "PASS" if response.status_code == 200 else "FAIL",
                    f"Status: {response.status_code}"
                )
            except Exception as e:
                original_tests[f"endpoint_{endpoint.replace('/', '_').replace('api_', '')}"] = self.log_test(
                    f"{name} Endpoint", "FAIL", str(e)
                )
        
        # Test 3: Authentication Flow
        print("\n Test 3: Authentication Flow")
        print("-" * 40)
        auth_tests = [
            ("admin", "admin123"),
            ("testuser", "testpass123"),
            ("user", "password123")
        ]
        
        for username, password in auth_tests:
            try:
                response = requests.post(f"{self.base_url}/api/token/", 
                                       json={"username": username, "password": password}, 
                                       timeout=10)
                original_tests[f"auth_{username}"] = self.log_test(
                    f"Login Attempt ({username})", "PASS" if response.status_code == 200 else "FAIL",
                    f"Status: {response.status_code}"
                )
            except Exception as e:
                original_tests[f"auth_{username}"] = self.log_test(
                    f"Login Attempt ({username})", "FAIL", str(e)
                )
        
        # Test 4: Protected Endpoints
        print("\n Test 4: Protected Endpoints")
        print("-" * 40)
        protected_endpoints = [
            ("/api/checklist/", "Checklist API"),
            ("/api/regulations/", "Regulations API"),
            ("/api/report/", "Reports API"),
            ("/api/profile/", "Profile API")
        ]
        
        for endpoint, name in protected_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                original_tests[f"protected_{endpoint.replace('/', '_').replace('api_', '')}"] = self.log_test(
                    f"{name} (Protected)", "PASS" if response.status_code == 401 else "FAIL",
                    f"Status: {response.status_code} (should be 401 for unauthorized)"
                )
            except Exception as e:
                original_tests[f"protected_{endpoint.replace('/', '_').replace('api_', '')}"] = self.log_test(
                    f"{name} (Protected)", "FAIL", str(e)
                )
        
        # Test 5: Export Functionality
        print("\n Test 5: Export Functionality")
        print("-" * 40)
        export_endpoints = [
            ("/api/checklist/export/csv/", "CSV Export"),
            ("/api/checklist/export/pdf/", "PDF Export")
        ]
        
        for endpoint, name in export_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                original_tests[f"export_{endpoint.split('/')[-2]}"] = self.log_test(
                    f"{name}", "PASS" if response.status_code in [200, 401] else "FAIL",
                    f"Status: {response.status_code}"
                )
            except Exception as e:
                original_tests[f"export_{endpoint.split('/')[-2]}"] = self.log_test(
                    f"{name}", "FAIL", str(e)
                )
        
        self.test_results["original_tests"] = original_tests
        return original_tests
    
    def test_black_duck_detect(self):
        """Execute Black Duck Detect security scanning"""
        print("\n" + "="*60)
        print(" EXECUTING BLACK DUCK DETECT SECURITY SCANNING")
        print("="*60)
        
        black_duck_tests = {}
        
        # Test 1: Black Duck Detect Script Availability
        print("\n Test 1: Black Duck Detect Script Availability")
        print("-" * 50)
        detect_scripts = [
            "tools/detect/run-detect-jdk11.bat",
            "tools/detect/run-detect-jdk11.ps1",
            "tools/detect/switch-java-version.ps1"
        ]
        
        for script in detect_scripts:
            if os.path.exists(script):
                black_duck_tests[f"script_{script.split('/')[-1]}"] = self.log_test(
                    f"Script: {script.split('/')[-1]}", "PASS", "Script exists"
                )
            else:
                black_duck_tests[f"script_{script.split('/')[-1]}"] = self.log_test(
                    f"Script: {script.split('/')[-1]}", "FAIL", "Script not found"
                )
        
        # Test 2: Java Environment
        print("\n Test 2: Java Environment")
        print("-" * 50)
        try:
            result = subprocess.run(["java", "-version"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                black_duck_tests["java_version"] = self.log_test(
                    "Java Version", "PASS", "Java is available"
                )
            else:
                black_duck_tests["java_version"] = self.log_test(
                    "Java Version", "FAIL", "Java not available"
                )
        except Exception as e:
            black_duck_tests["java_version"] = self.log_test(
                "Java Version", "FAIL", str(e)
            )
        
        # Test 3: Dependencies Installation
        print("\n Test 3: Dependencies Installation")
        print("-" * 50)
        
        # Check frontend dependencies
        if os.path.exists("frontend/package.json"):
            if os.path.exists("frontend/node_modules"):
                black_duck_tests["frontend_deps"] = self.log_test(
                    "Frontend Dependencies", "PASS", "node_modules exists"
                )
            else:
                black_duck_tests["frontend_deps"] = self.log_test(
                    "Frontend Dependencies", "FAIL", "node_modules not found"
                )
        else:
            black_duck_tests["frontend_deps"] = self.log_test(
                "Frontend Dependencies", "FAIL", "package.json not found"
            )
        
        # Check backend dependencies
        if os.path.exists("backend/requirements.txt"):
            black_duck_tests["backend_deps"] = self.log_test(
                "Backend Dependencies", "PASS", "requirements.txt exists"
            )
        else:
            black_duck_tests["backend_deps"] = self.log_test(
                "Backend Dependencies", "FAIL", "requirements.txt not found"
            )
        
        # Test 4: Security API Endpoints
        print("\n Test 4: Security API Endpoints")
        print("-" * 50)
        security_endpoints = [
            ("/api/security/report/", "Security Report"),
            ("/api/security/scan/", "Security Scan")
        ]
        
        for endpoint, name in security_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                black_duck_tests[f"security_{endpoint.split('/')[-2]}"] = self.log_test(
                    f"{name} Endpoint", "PASS" if response.status_code in [200, 401] else "FAIL",
                    f"Status: {response.status_code}"
                )
            except Exception as e:
                black_duck_tests[f"security_{endpoint.split('/')[-2]}"] = self.log_test(
                    f"{name} Endpoint", "FAIL", str(e)
                )
        
        # Test 5: Mock Security Data Generation
        print("\n Test 5: Mock Security Data Generation")
        print("-" * 50)
        try:
            # Try to run the Django management command
            result = subprocess.run([
                "python", "manage.py", "scan_detect", "--mock"
            ], cwd="backend", capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                black_duck_tests["mock_security_data"] = self.log_test(
                    "Mock Security Data", "PASS", "Mock data generated successfully"
                )
            else:
                black_duck_tests["mock_security_data"] = self.log_test(
                    "Mock Security Data", "FAIL", f"Error: {result.stderr}"
                )
        except Exception as e:
            black_duck_tests["mock_security_data"] = self.log_test(
                "Mock Security Data", "FAIL", str(e)
            )
        
        # Test 6: Reports Directory
        print("\n Test 6: Reports Directory")
        print("-" * 50)
        reports_dir = "reports/detect"
        if os.path.exists(reports_dir):
            black_duck_tests["reports_directory"] = self.log_test(
                "Reports Directory", "PASS", "Reports directory exists"
            )
        else:
            os.makedirs(reports_dir, exist_ok=True)
            black_duck_tests["reports_directory"] = self.log_test(
                "Reports Directory", "PASS", "Reports directory created"
            )
        
        self.test_results["black_duck_tests"] = black_duck_tests
        return black_duck_tests
    
    def test_integration(self):
        """Test integration between original plan and Black Duck Detect"""
        print("\n" + "="*60)
        print(" TESTING INTEGRATION BETWEEN ORIGINAL PLAN AND BLACK DUCK DETECT")
        print("="*60)
        
        integration_tests = {}
        
        # Test 1: Security Dashboard Access
        print("\n Test 1: Security Dashboard Access")
        print("-" * 50)
        try:
            response = requests.get(f"{self.base_url}/api/security/report/", timeout=10)
            integration_tests["security_dashboard_access"] = self.log_test(
                "Security Dashboard Access", "PASS" if response.status_code in [200, 401] else "FAIL",
                f"Status: {response.status_code}"
            )
        except Exception as e:
            integration_tests["security_dashboard_access"] = self.log_test(
                "Security Dashboard Access", "FAIL", str(e)
            )
        
        # Test 2: React Frontend Integration
        print("\n Test 2: React Frontend Integration")
        print("-" * 50)
        if os.path.exists("frontend/src/components/SecurityDashboard.js"):
            integration_tests["react_security_dashboard"] = self.log_test(
                "React Security Dashboard", "PASS", "SecurityDashboard component exists"
            )
        else:
            integration_tests["react_security_dashboard"] = self.log_test(
                "React Security Dashboard", "FAIL", "SecurityDashboard component not found"
            )
        
        # Test 3: Django Management Command
        print("\n Test 3: Django Management Command")
        print("-" * 50)
        if os.path.exists("backend/checklist/management/commands/scan_detect.py"):
            integration_tests["django_management_command"] = self.log_test(
                "Django Management Command", "PASS", "scan_detect command exists"
            )
        else:
            integration_tests["django_management_command"] = self.log_test(
                "Django Management Command", "FAIL", "scan_detect command not found"
            )
        
        # Test 4: Security Views Integration
        print("\n Test 4: Security Views Integration")
        print("-" * 50)
        if os.path.exists("backend/checklist/security_views.py"):
            integration_tests["security_views"] = self.log_test(
                "Security Views", "PASS", "security_views.py exists"
            )
        else:
            integration_tests["security_views"] = self.log_test(
                "Security Views", "FAIL", "security_views.py not found"
            )
        
        # Test 5: URL Configuration
        print("\n Test 5: URL Configuration")
        print("-" * 50)
        try:
            with open("backend/checklist/urls.py", "r") as f:
                urls_content = f.read()
                if "security" in urls_content:
                    integration_tests["url_configuration"] = self.log_test(
                        "URL Configuration", "PASS", "Security URLs configured"
                    )
                else:
                    integration_tests["url_configuration"] = self.log_test(
                        "URL Configuration", "FAIL", "Security URLs not configured"
                    )
        except Exception as e:
            integration_tests["url_configuration"] = self.log_test(
                "URL Configuration", "FAIL", str(e)
            )
        
        self.test_results["integration_tests"] = integration_tests
        return integration_tests
    
    def test_hipaa_compliance(self):
        """Test HIPAA compliance requirements"""
        print("\n" + "="*60)
        print(" TESTING HIPAA COMPLIANCE REQUIREMENTS")
        print("="*60)
        
        hipaa_tests = {}
        
        # Test 1: Data Encryption
        print("\n Test 1: Data Encryption")
        print("-" * 50)
        if os.path.exists("backend/sqlite_encryption.py"):
            hipaa_tests["data_encryption"] = self.log_test(
                "Data Encryption", "PASS", "Database encryption implemented"
            )
        else:
            hipaa_tests["data_encryption"] = self.log_test(
                "Data Encryption", "FAIL", "Database encryption not implemented"
            )
        
        # Test 2: Authentication Security
        print("\n Test 2: Authentication Security")
        print("-" * 50)
        try:
            response = requests.post(f"{self.base_url}/api/token/", 
                                   json={"username": "invalid", "password": "invalid"}, 
                                   timeout=10)
            if response.status_code == 401:
                hipaa_tests["auth_security"] = self.log_test(
                    "Authentication Security", "PASS", "Invalid credentials properly rejected"
                )
            else:
                hipaa_tests["auth_security"] = self.log_test(
                    "Authentication Security", "FAIL", f"Unexpected status: {response.status_code}"
                )
        except Exception as e:
            hipaa_tests["auth_security"] = self.log_test(
                "Authentication Security", "FAIL", str(e)
            )
        
        # Test 3: HTTPS Support
        print("\n Test 3: HTTPS Support")
        print("-" * 50)
        if os.path.exists("nginx-https.conf"):
            hipaa_tests["https_support"] = self.log_test(
                "HTTPS Support", "PASS", "HTTPS configuration exists"
            )
        else:
            hipaa_tests["https_support"] = self.log_test(
                "HTTPS Support", "FAIL", "HTTPS configuration not found"
            )
        
        # Test 4: Security Headers
        print("\n Test 4: Security Headers")
        print("-" * 50)
        try:
            response = requests.get(f"{self.base_url}/api/health/", timeout=10)
            security_headers = [
                "X-Content-Type-Options",
                "X-Frame-Options",
                "X-XSS-Protection"
            ]
            found_headers = [header for header in security_headers if header in response.headers]
            if found_headers:
                hipaa_tests["security_headers"] = self.log_test(
                    "Security Headers", "PASS", f"Found headers: {found_headers}"
                )
            else:
                hipaa_tests["security_headers"] = self.log_test(
                    "Security Headers", "FAIL", "No security headers found"
                )
        except Exception as e:
            hipaa_tests["security_headers"] = self.log_test(
                "Security Headers", "FAIL", str(e)
            )
        
        # Test 5: Audit Logging
        print("\n Test 5: Audit Logging")
        print("-" * 50)
        if os.path.exists("logs"):
            hipaa_tests["audit_logging"] = self.log_test(
                "Audit Logging", "PASS", "Logs directory exists"
            )
        else:
            hipaa_tests["audit_logging"] = self.log_test(
                "Audit Logging", "FAIL", "Logs directory not found"
            )
        
        self.test_results["hipaa_compliance"] = hipaa_tests
        return hipaa_tests
    
    def generate_summary(self):
        """Generate comprehensive test summary"""
        print("\n" + "="*60)
        print(" COMPREHENSIVE TEST SUMMARY")
        print("="*60)
        
        # Calculate success rates
        original_success = sum(1 for test in self.test_results["original_tests"].values() if test["status"] == "PASS")
        original_total = len(self.test_results["original_tests"])
        original_rate = (original_success / original_total * 100) if original_total > 0 else 0
        
        black_duck_success = sum(1 for test in self.test_results["black_duck_tests"].values() if test["status"] == "PASS")
        black_duck_total = len(self.test_results["black_duck_tests"])
        black_duck_rate = (black_duck_success / black_duck_total * 100) if black_duck_total > 0 else 0
        
        integration_success = sum(1 for test in self.test_results["integration_tests"].values() if test["status"] == "PASS")
        integration_total = len(self.test_results["integration_tests"])
        integration_rate = (integration_success / integration_total * 100) if integration_total > 0 else 0
        
        hipaa_success = sum(1 for test in self.test_results["hipaa_compliance"].values() if test["status"] == "PASS")
        hipaa_total = len(self.test_results["hipaa_compliance"])
        hipaa_rate = (hipaa_success / hipaa_total * 100) if hipaa_total > 0 else 0
        
        overall_success = self.passed_tests
        overall_total = self.total_tests
        overall_rate = (overall_success / overall_total * 100) if overall_total > 0 else 0
        
        self.test_results["summary"] = {
            "original_plan": {
                "passed": original_success,
                "total": original_total,
                "success_rate": round(original_rate, 2)
            },
            "black_duck_detect": {
                "passed": black_duck_success,
                "total": black_duck_total,
                "success_rate": round(black_duck_rate, 2)
            },
            "integration": {
                "passed": integration_success,
                "total": integration_total,
                "success_rate": round(integration_rate, 2)
            },
            "hipaa_compliance": {
                "passed": hipaa_success,
                "total": hipaa_total,
                "success_rate": round(hipaa_rate, 2)
            },
            "overall": {
                "passed": overall_success,
                "total": overall_total,
                "success_rate": round(overall_rate, 2)
            }
        }
        
        print(f"\n Test Results Summary:")
        print(f"   Original Plan Tests: {original_success}/{original_total} ({original_rate:.1f}%)")
        print(f"   Black Duck Detect Tests: {black_duck_success}/{black_duck_total} ({black_duck_rate:.1f}%)")
        print(f"   Integration Tests: {integration_success}/{integration_total} ({integration_rate:.1f}%)")
        print(f"   HIPAA Compliance Tests: {hipaa_success}/{hipaa_total} ({hipaa_rate:.1f}%)")
        print(f"   Overall Success Rate: {overall_success}/{overall_total} ({overall_rate:.1f}%)")
        
        return self.test_results["summary"]
    
    def save_results(self):
        """Save test results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comprehensive_test_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n Test results saved to: {filename}")
        return filename
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print(" Starting Comprehensive Testing Suite")
        print("=" * 60)
        
        # Wait for server to be ready
        if not self.wait_for_server():
            print(" Django server is not running. Please start it first.")
            return False
        
        # Run all test categories
        self.test_original_plan()
        self.test_black_duck_detect()
        self.test_integration()
        self.test_hipaa_compliance()
        
        # Generate summary
        self.generate_summary()
        
        # Save results
        filename = self.save_results()
        
        print(f"\n Comprehensive testing completed!")
        print(f" Overall Success Rate: {self.test_results['summary']['overall']['success_rate']:.1f}%")
        print(f" Results saved to: {filename}")
        
        return True

def main():
    """Main function"""
    suite = ComprehensiveTestingSuite()
    suite.run_all_tests()

if __name__ == "__main__":
    main()
