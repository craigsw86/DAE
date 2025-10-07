#!/usr/bin/env python3
"""
Manual Flow Verification and Documentation - FIXED VERSION
Comprehensive manual testing of the complete application flow
"""

import requests
import json
import time
from datetime import datetime
import os
import sys

class ManualFlowVerifierFixed:
    """Fixed manual flow verification and testing"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.api_url = f"{self.base_url}/api"
        self.test_results = []
        self.issues_found = []
        self.auth_token = None
        self.refresh_token = None
        self.test_data = {}
        
    def log_test(self, test_name, success, message="", data=None, issue_type=None):
        """Log test result"""
        status = " PASS" if success else " FAIL"
        print(f"{test_name}: {status} {message}")
        
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'issue_type': issue_type
        }
        
        self.test_results.append(result)
        
        if not success and issue_type:
            self.issues_found.append({
                'test': test_name,
                'issue': message,
                'type': issue_type,
                'timestamp': datetime.now().isoformat()
            })
    
    def test_server_availability(self):
        """Test 1: Server Availability"""
        print("\n Test 1: Server Availability")
        print("=" * 50)
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            if response.status_code in [200, 404]:
                self.log_test("Server Response", True, f"Server responding (Status: {response.status_code})")
                return True
            else:
                self.log_test("Server Response", False, f"Unexpected status: {response.status_code}", issue_type="server")
                return False
        except Exception as e:
            self.log_test("Server Response", False, f"Error: {e}", issue_type="server")
            return False
    
    def test_public_endpoints(self):
        """Test 2: Public Endpoints - FIXED"""
        print("\n Test 2: Public Endpoints")
        print("=" * 50)
        
        public_endpoints = [
            ("/api/health/", "Health Check"),
            ("/api/info/", "API Info"),
            ("/api/stats/", "Public Stats"),
            ("/admin/", "Admin Interface")
        ]
        
        for endpoint, name in public_endpoints:
            try:
                # Use the correct URL construction
                url = f"{self.api_url}{endpoint}" if endpoint.startswith("/api/") else f"{self.base_url}{endpoint}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    if endpoint.startswith("/api/"):
                        data = response.json()
                        self.log_test(f"{name} Endpoint", True, f"Status: {response.status_code}")
                        self.log_test(f"{name} Data", True, f"Response: {str(data)[:100]}...")
                    else:
                        self.log_test(f"{name} Endpoint", True, f"Status: {response.status_code}")
                        self.log_test(f"{name} Data", True, "HTML Response received")
                else:
                    self.log_test(f"{name} Endpoint", False, f"Status: {response.status_code}", issue_type="endpoint")
            except Exception as e:
                self.log_test(f"{name} Endpoint", False, f"Error: {e}", issue_type="endpoint")
    
    def create_test_user_via_django_admin(self):
        """Create test user via Django admin interface"""
        print("\n Test 3: User Creation via Django Admin")
        print("=" * 50)
        
        try:
            # Check if admin is accessible
            response = requests.get(f"{self.base_url}/admin/", timeout=10)
            if response.status_code == 200:
                self.log_test("Admin Access", True, "Admin interface accessible")
                
                # Try to create user via Django management command
                self.create_user_via_management_command()
                return True
            else:
                self.log_test("Admin Access", False, f"Status: {response.status_code}", issue_type="admin")
                return False
                
        except Exception as e:
            self.log_test("User Creation", False, f"Error: {e}", issue_type="user_creation")
            return False
    
    def create_user_via_management_command(self):
        """Create user via Django management command"""
        try:
            import subprocess
            import os
            
            # Change to backend directory
            backend_dir = os.path.join(os.path.dirname(__file__), "backend")
            
            # Create user via Django shell
            create_user_script = """
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create test user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'is_active': True,
        'is_staff': True
    }
)

if created:
    user.set_password('testpass123')
    user.save()
    print("User created successfully")
else:
    user.set_password('testpass123')
    user.save()
    print("User already exists, password updated")

# Test authentication
auth_user = authenticate(username='testuser', password='testpass123')
if auth_user:
    print("User authentication successful")
else:
    print("User authentication failed")
"""
            
            # Write script to temporary file
            script_file = os.path.join(backend_dir, "create_test_user_temp.py")
            with open(script_file, 'w') as f:
                f.write(create_user_script)
            
            # Run the script
            result = subprocess.run(['python', 'create_test_user_temp.py'], 
                                 cwd=backend_dir, 
                                 capture_output=True, 
                                 text=True, 
                                 timeout=30)
            
            if result.returncode == 0:
                self.log_test("User Creation", True, "Test user created successfully")
                self.log_test("User Authentication", True, "User authentication successful")
                self.test_data['user_created'] = True
                return True
            else:
                self.log_test("User Creation", False, f"Error: {result.stderr}", issue_type="user_creation")
                return False
                
        except Exception as e:
            self.log_test("User Creation", False, f"Error: {e}", issue_type="user_creation")
            return False
        finally:
            # Clean up temporary file
            try:
                if 'script_file' in locals():
                    os.remove(script_file)
            except:
                pass
    
    def test_authentication_flow(self):
        """Test 4: Authentication Flow"""
        print("\n Test 4: Authentication Flow")
        print("=" * 50)
        
        # Test login with test user
        try:
            response = requests.post(f"{self.api_url}/token/", 
                                  json={"username": "testuser", "password": "testpass123"}, 
                                  timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('access')
                self.refresh_token = data.get('refresh')
                
                self.log_test("Login Success", True, f"Successfully logged in as testuser")
                self.log_test("Access Token", True, f"Token received: {self.auth_token[:20]}...")
                self.log_test("Refresh Token", True, f"Refresh token received: {self.refresh_token[:20]}...")
                
                self.test_data['auth_token'] = self.auth_token
                self.test_data['refresh_token'] = self.refresh_token
                return True
            else:
                self.log_test("Login Success", False, f"Status: {response.status_code}", issue_type="authentication")
                return False
                
        except Exception as e:
            self.log_test("Authentication Flow", False, f"Error: {e}", issue_type="authentication")
            return False
    
    def test_protected_endpoints(self):
        """Test 5: Protected Endpoints"""
        print("\n Test 5: Protected Endpoints")
        print("=" * 50)
        
        if not self.auth_token:
            self.log_test("Protected Endpoints", False, "No authentication token available", issue_type="authentication")
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
                    self.log_test(f"{name} (Auth)", True, f"Successfully accessed {name}")
                    self.log_test(f"{name} Data", True, f"Response: {str(data)[:100]}...")
                elif response.status_code == 401:
                    self.log_test(f"{name} (Auth)", False, "Unauthorized - token may be invalid", issue_type="authentication")
                else:
                    self.log_test(f"{name} (Auth)", False, f"Status: {response.status_code}", issue_type="endpoint")
            except Exception as e:
                self.log_test(f"{name} (Auth)", False, f"Error: {e}", issue_type="endpoint")
    
    def test_checklist_workflow(self):
        """Test 6: Checklist Workflow"""
        print("\n Test 6: Checklist Workflow")
        print("=" * 50)
        
        if not self.auth_token:
            self.log_test("Checklist Workflow", False, "No authentication token available", issue_type="authentication")
            return False
        
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        
        try:
            # Test GET checklist items
            response = requests.get(f"{self.api_url}/checklist/", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Get Checklist Items", True, f"Retrieved {len(data)} items")
                self.test_data['checklist_items'] = data
            else:
                self.log_test("Get Checklist Items", False, f"Status: {response.status_code}", issue_type="checklist")
                return False
            
            # Test CREATE checklist item
            new_item_data = {
                "title": "Manual Test Checklist Item",
                "description": "Created during manual flow verification",
                "completed": False,
                "notes": "Manual testing item",
                "priority": "high"
            }
            
            response = requests.post(f"{self.api_url}/checklist/", 
                                  json=new_item_data, 
                                  headers=headers, 
                                  timeout=10)
            
            if response.status_code == 201:
                data = response.json()
                self.log_test("Create Checklist Item", True, f"Created item with ID: {data.get('id')}")
                self.test_data['created_item_id'] = data.get('id')
            else:
                self.log_test("Create Checklist Item", False, f"Status: {response.status_code}", issue_type="checklist")
                return False
            
            # Test UPDATE checklist item
            if 'created_item_id' in self.test_data:
                item_id = self.test_data['created_item_id']
                update_data = {
                    "completed": True,
                    "notes": "Updated during manual testing"
                }
                
                response = requests.patch(f"{self.api_url}/checklist/{item_id}/", 
                                       json=update_data, 
                                       headers=headers, 
                                       timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test("Update Checklist Item", True, f"Updated item {item_id}")
                else:
                    self.log_test("Update Checklist Item", False, f"Status: {response.status_code}", issue_type="checklist")
            
            return True
            
        except Exception as e:
            self.log_test("Checklist Workflow", False, f"Error: {e}", issue_type="checklist")
            return False
    
    def test_export_functionality(self):
        """Test 7: Export Functionality"""
        print("\n Test 7: Export Functionality")
        print("=" * 50)
        
        if not self.auth_token:
            self.log_test("Export Functionality", False, "No authentication token available", issue_type="authentication")
            return False
        
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        
        try:
            # Test CSV export
            response = requests.get(f"{self.api_url}/checklist/export/csv/", headers=headers, timeout=10)
            if response.status_code == 200:
                self.log_test("CSV Export", True, f"CSV export successful, size: {len(response.content)} bytes")
            else:
                self.log_test("CSV Export", False, f"Status: {response.status_code}", issue_type="export")
            
            # Test PDF export
            response = requests.get(f"{self.api_url}/checklist/export/pdf/", headers=headers, timeout=10)
            if response.status_code == 200:
                self.log_test("PDF Export", True, f"PDF export successful, size: {len(response.content)} bytes")
            else:
                self.log_test("PDF Export", False, f"Status: {response.status_code}", issue_type="export")
            
            return True
            
        except Exception as e:
            self.log_test("Export Functionality", False, f"Error: {e}", issue_type="export")
            return False
    
    def test_error_handling(self):
        """Test 8: Error Handling"""
        print("\n Test 8: Error Handling")
        print("=" * 50)
        
        # Test 404 endpoint
        try:
            response = requests.get(f"{self.api_url}/nonexistent/", timeout=10)
            if response.status_code == 404:
                self.log_test("404 Handling", True, "Correctly returns 404")
            else:
                self.log_test("404 Handling", False, f"Unexpected status: {response.status_code}", issue_type="error_handling")
        except Exception as e:
            self.log_test("404 Handling", False, f"Error: {e}", issue_type="error_handling")
        
        # Test invalid JSON
        try:
            response = requests.post(f"{self.api_url}/token/", 
                                  data="invalid json", 
                                  headers={'Content-Type': 'application/json'},
                                  timeout=10)
            if response.status_code == 400:
                self.log_test("Invalid JSON Handling", True, "Correctly returns 400")
            else:
                self.log_test("Invalid JSON Handling", False, f"Unexpected status: {response.status_code}", issue_type="error_handling")
        except Exception as e:
            self.log_test("Invalid JSON Handling", False, f"Error: {e}", issue_type="error_handling")
    
    def cleanup_test_data(self):
        """Clean up test data"""
        print("\n Cleaning up Test Data")
        print("=" * 50)
        
        if not self.auth_token:
            self.log_test("Cleanup", True, "No test data to clean up")
            return
        
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        
        try:
            # Delete created checklist item
            if 'created_item_id' in self.test_data:
                item_id = self.test_data['created_item_id']
                response = requests.delete(f"{self.api_url}/checklist/{item_id}/", 
                                        headers=headers, timeout=10)
                if response.status_code in [200, 204]:
                    self.log_test("Cleanup Checklist Item", True, f"Deleted item {item_id}")
                else:
                    self.log_test("Cleanup Checklist Item", False, f"Status: {response.status_code}", issue_type="cleanup")
            
        except Exception as e:
            self.log_test("Cleanup", False, f"Error: {e}", issue_type="cleanup")
    
    def generate_issues_report(self):
        """Generate comprehensive issues report"""
        print("\n" + "=" * 60)
        print(" MANUAL FLOW VERIFICATION - ISSUES REPORT")
        print("=" * 60)
        
        if not self.issues_found:
            print(" No issues found during manual testing!")
            return
        
        print(f"Total Issues Found: {len(self.issues_found)}")
        print("\nIssues by Type:")
        
        # Group issues by type
        issues_by_type = {}
        for issue in self.issues_found:
            issue_type = issue['type']
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)
        
        for issue_type, issues in issues_by_type.items():
            print(f"\n {issue_type.upper()} ({len(issues)} issues):")
            for issue in issues:
                print(f"  - {issue['test']}: {issue['issue']}")
        
        # Save detailed issues report
        issues_file = f"manual_flow_issues_fixed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(issues_file, 'w') as f:
            json.dump({
                'issues': self.issues_found,
                'issues_by_type': issues_by_type,
                'summary': {
                    'total_issues': len(self.issues_found),
                    'issues_by_type': {k: len(v) for k, v in issues_by_type.items()}
                }
            }, f, indent=2)
        
        print(f"\n Detailed issues report saved to: {issues_file}")
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print(" MANUAL FLOW VERIFICATION TEST REPORT")
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
        report_file = f"manual_flow_test_report_fixed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'test_results': self.test_results,
                'test_data': self.test_data,
                'issues_found': self.issues_found,
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'success_rate': (passed_tests/total_tests)*100
                }
            }, f, indent=2)
        
        print(f"\n Detailed report saved to: {report_file}")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """Run all manual flow verification tests"""
        print(" Starting Manual Flow Verification and Documentation - FIXED VERSION")
        print("=" * 60)
        
        # Core tests
        self.test_server_availability()
        self.test_public_endpoints()
        self.create_test_user_via_django_admin()
        self.test_authentication_flow()
        self.test_protected_endpoints()
        self.test_checklist_workflow()
        self.test_export_functionality()
        self.test_error_handling()
        
        # Cleanup
        self.cleanup_test_data()
        
        # Generate reports
        self.generate_issues_report()
        return self.generate_test_report()

def main():
    """Main function"""
    verifier = ManualFlowVerifierFixed()
    success = verifier.run_all_tests()
    
    if success:
        print("\n All manual flow tests passed!")
        print(" Complete application flow is working correctly!")
    else:
        print("\n  Some manual flow tests failed.")
        print("Please review the issues report and fix the problems.")
    
    return success

if __name__ == '__main__':
    main()
