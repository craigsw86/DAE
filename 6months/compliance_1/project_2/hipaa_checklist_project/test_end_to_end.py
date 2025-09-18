#!/usr/bin/env python3
"""
End-to-End Local Network Tests
Tests complete user workflow: Login -> Checklist -> Updates -> Reports
"""

import requests
import json
import time
from datetime import datetime
import os
import sys

# Add backend to Python path
backend_dir = os.path.join(os.path.dirname(__file__), "backend")
sys.path.insert(0, backend_dir)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')

class EndToEndTester:
    """Comprehensive end-to-end testing"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.api_url = f"{self.base_url}/api"
        self.test_results = []
        self.auth_token = None
        self.refresh_token = None
        self.user_id = None
        self.test_data = {}
        
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
    
    def setup_test_user(self):
        """Create or get test user"""
        print("\n📝 Setting up Test User")
        print("-" * 40)
        
        try:
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
                    'last_name': 'User',
                    'is_active': True
                }
            )
            
            if created:
                user.set_password('testpass123')
                user.save()
                self.log_test("User Creation", True, "Test user created successfully")
            else:
                # Update password to ensure it's correct
                user.set_password('testpass123')
                user.save()
                self.log_test("User Creation", True, "Test user already exists, password updated")
            
            self.user_id = user.id
            self.test_data['user_id'] = self.user_id
            
            # Test authentication
            auth_user = authenticate(username='testuser', password='testpass123')
            if auth_user:
                self.log_test("User Authentication", True, "User authenticated successfully")
                return True
            else:
                self.log_test("User Authentication", False, "Authentication failed")
                return False
                
        except Exception as e:
            self.log_test("User Setup", False, f"Error: {e}")
            return False
    
    def test_login_flow(self):
        """Test user login and JWT token generation"""
        print("\n📝 Test 1: Login Flow")
        print("-" * 40)
        
        try:
            # Test login with correct credentials
            response = requests.post(f"{self.api_url}/token/", 
                                  json={"username": "testuser", "password": "testpass123"}, 
                                  timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('access')
                self.refresh_token = data.get('refresh')
                
                self.log_test("Login Success", True, "Successfully logged in")
                self.log_test("Access Token", True, f"Token received: {self.auth_token[:20]}...")
                self.log_test("Refresh Token", True, f"Refresh token received: {self.refresh_token[:20]}...")
                
                self.test_data['access_token'] = self.auth_token
                self.test_data['refresh_token'] = self.refresh_token
                
                return True
            else:
                self.log_test("Login Success", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Login Flow", False, f"Error: {e}")
            return False
    
    def test_token_refresh(self):
        """Test JWT token refresh"""
        print("\n📝 Test 2: Token Refresh")
        print("-" * 40)
        
        if not self.refresh_token:
            self.log_test("Token Refresh", False, "No refresh token available")
            return False
        
        try:
            response = requests.post(f"{self.api_url}/token/refresh/", 
                                  json={"refresh": self.refresh_token}, 
                                  timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                new_access_token = data.get('access')
                self.log_test("Token Refresh", True, "Successfully refreshed token")
                self.log_test("New Access Token", True, f"New token: {new_access_token[:20]}...")
                
                # Update the access token
                self.auth_token = new_access_token
                self.test_data['access_token'] = self.auth_token
                
                return True
            else:
                self.log_test("Token Refresh", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Token Refresh", False, f"Error: {e}")
            return False
    
    def test_protected_endpoints_access(self):
        """Test access to protected endpoints with authentication"""
        print("\n📝 Test 3: Protected Endpoints Access")
        print("-" * 40)
        
        if not self.auth_token:
            self.log_test("Protected Access", False, "No authentication token available")
            return False
        
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        
        protected_endpoints = [
            ("/api/profile/", "User Profile"),
            ("/api/checklist/", "Checklist API"),
            ("/api/regulations/", "Regulations API"),
            ("/api/report/", "Compliance Report API")
        ]
        
        for endpoint, name in protected_endpoints:
            try:
                response = requests.get(f"{self.api_url}{endpoint}", headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(f"{name} Access", True, f"Successfully accessed {name}")
                    self.log_test(f"{name} Data", True, f"Response: {str(data)[:100]}...")
                elif response.status_code == 401:
                    self.log_test(f"{name} Access", False, "Unauthorized - token may be invalid")
                else:
                    self.log_test(f"{name} Access", False, f"Unexpected status: {response.status_code}")
            except Exception as e:
                self.log_test(f"{name} Access", False, f"Error: {e}")
    
    def test_checklist_operations(self):
        """Test checklist CRUD operations"""
        print("\n📝 Test 4: Checklist Operations")
        print("-" * 40)
        
        if not self.auth_token:
            self.log_test("Checklist Operations", False, "No authentication token available")
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
                self.log_test("Get Checklist Items", False, f"Status: {response.status_code}")
                return False
            
            # Test creating a new checklist item
            new_item_data = {
                "title": "Test Checklist Item",
                "description": "End-to-end test item",
                "completed": False,
                "notes": "Created during E2E testing",
                "priority": "medium"
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
                self.log_test("Create Checklist Item", False, f"Status: {response.status_code}")
                return False
            
            # Test updating the checklist item
            if 'created_item_id' in self.test_data:
                item_id = self.test_data['created_item_id']
                update_data = {
                    "completed": True,
                    "notes": "Updated during E2E testing"
                }
                
                response = requests.patch(f"{self.api_url}/checklist/{item_id}/", 
                                       json=update_data, 
                                       headers=headers, 
                                       timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test("Update Checklist Item", True, f"Updated item {item_id}")
                else:
                    self.log_test("Update Checklist Item", False, f"Status: {response.status_code}")
            
            return True
            
        except Exception as e:
            self.log_test("Checklist Operations", False, f"Error: {e}")
            return False
    
    def test_regulation_updates(self):
        """Test regulation updates functionality"""
        print("\n📝 Test 5: Regulation Updates")
        print("-" * 40)
        
        if not self.auth_token:
            self.log_test("Regulation Updates", False, "No authentication token available")
            return False
        
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        
        try:
            # Test GET regulations
            response = requests.get(f"{self.api_url}/regulations/", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Get Regulations", True, f"Retrieved {len(data)} regulations")
                self.test_data['regulations'] = data
            else:
                self.log_test("Get Regulations", False, f"Status: {response.status_code}")
                return False
            
            # Test creating a new regulation update
            new_regulation_data = {
                "title": "Test Regulation Update",
                "description": "End-to-end test regulation",
                "effective_date": "2024-01-01",
                "status": "active",
                "category": "privacy"
            }
            
            response = requests.post(f"{self.api_url}/regulations/", 
                                  json=new_regulation_data, 
                                  headers=headers, 
                                  timeout=10)
            
            if response.status_code == 201:
                data = response.json()
                self.log_test("Create Regulation", True, f"Created regulation with ID: {data.get('id')}")
                self.test_data['created_regulation_id'] = data.get('id')
            else:
                self.log_test("Create Regulation", False, f"Status: {response.status_code}")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Regulation Updates", False, f"Error: {e}")
            return False
    
    def test_compliance_reports(self):
        """Test compliance report generation"""
        print("\n📝 Test 6: Compliance Reports")
        print("-" * 40)
        
        if not self.auth_token:
            self.log_test("Compliance Reports", False, "No authentication token available")
            return False
        
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        
        try:
            # Test GET compliance report
            response = requests.get(f"{self.api_url}/report/", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Get Compliance Report", True, f"Generated compliance report")
                self.log_test("Report Data", True, f"Report: {str(data)[:100]}...")
                self.test_data['compliance_report'] = data
            else:
                self.log_test("Get Compliance Report", False, f"Status: {response.status_code}")
                return False
            
            # Test report trends
            response = requests.get(f"{self.api_url}/report/trends/", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Get Report Trends", True, f"Retrieved report trends")
                self.test_data['report_trends'] = data
            else:
                self.log_test("Get Report Trends", False, f"Status: {response.status_code}")
            
            return True
            
        except Exception as e:
            self.log_test("Compliance Reports", False, f"Error: {e}")
            return False
    
    def test_user_profile(self):
        """Test user profile functionality"""
        print("\n📝 Test 7: User Profile")
        print("-" * 40)
        
        if not self.auth_token:
            self.log_test("User Profile", False, "No authentication token available")
            return False
        
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        
        try:
            # Test GET user profile
            response = requests.get(f"{self.api_url}/profile/", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Get User Profile", True, f"Retrieved user profile")
                self.log_test("Profile Data", True, f"Profile: {str(data)[:100]}...")
                self.test_data['user_profile'] = data
            else:
                self.log_test("Get User Profile", False, f"Status: {response.status_code}")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("User Profile", False, f"Error: {e}")
            return False
    
    def test_export_functionality(self):
        """Test export functionality (CSV/PDF)"""
        print("\n📝 Test 8: Export Functionality")
        print("-" * 40)
        
        if not self.auth_token:
            self.log_test("Export Functionality", False, "No authentication token available")
            return False
        
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        
        try:
            # Test CSV export
            response = requests.get(f"{self.api_url}/checklist/export/csv/", headers=headers, timeout=10)
            if response.status_code == 200:
                self.log_test("CSV Export", True, f"CSV export successful, size: {len(response.content)} bytes")
            else:
                self.log_test("CSV Export", False, f"Status: {response.status_code}")
            
            # Test PDF export
            response = requests.get(f"{self.api_url}/checklist/export/pdf/", headers=headers, timeout=10)
            if response.status_code == 200:
                self.log_test("PDF Export", True, f"PDF export successful, size: {len(response.content)} bytes")
            else:
                self.log_test("PDF Export", False, f"Status: {response.status_code}")
            
            return True
            
        except Exception as e:
            self.log_test("Export Functionality", False, f"Error: {e}")
            return False
    
    def test_audit_logging(self):
        """Test audit logging functionality"""
        print("\n📝 Test 9: Audit Logging")
        print("-" * 40)
        
        if not self.auth_token:
            self.log_test("Audit Logging", False, "No authentication token available")
            return False
        
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        
        try:
            # Test audit log for checklist items
            if 'created_item_id' in self.test_data:
                item_id = self.test_data['created_item_id']
                response = requests.get(f"{self.api_url}/auditlog/checklistitem/{item_id}/", 
                                      headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    self.log_test("Audit Log Retrieval", True, f"Retrieved audit log for item {item_id}")
                else:
                    self.log_test("Audit Log Retrieval", False, f"Status: {response.status_code}")
            
            return True
            
        except Exception as e:
            self.log_test("Audit Logging", False, f"Error: {e}")
            return False
    
    def test_complete_workflow(self):
        """Test complete user workflow"""
        print("\n📝 Test 10: Complete Workflow")
        print("-" * 40)
        
        workflow_steps = [
            ("User Login", self.test_login_flow),
            ("Token Refresh", self.test_token_refresh),
            ("Checklist Operations", self.test_checklist_operations),
            ("Regulation Updates", self.test_regulation_updates),
            ("Compliance Reports", self.test_compliance_reports),
            ("User Profile", self.test_user_profile),
            ("Export Functionality", self.test_export_functionality),
            ("Audit Logging", self.test_audit_logging)
        ]
        
        successful_steps = 0
        total_steps = len(workflow_steps)
        
        for step_name, step_function in workflow_steps:
            try:
                if step_function():
                    successful_steps += 1
                    self.log_test(f"Workflow Step: {step_name}", True, "Completed successfully")
                else:
                    self.log_test(f"Workflow Step: {step_name}", False, "Failed")
            except Exception as e:
                self.log_test(f"Workflow Step: {step_name}", False, f"Error: {e}")
        
        workflow_success_rate = (successful_steps / total_steps) * 100
        self.log_test("Complete Workflow", workflow_success_rate >= 80, 
                     f"Success rate: {workflow_success_rate:.1f}% ({successful_steps}/{total_steps})")
        
        return workflow_success_rate >= 80
    
    def cleanup_test_data(self):
        """Clean up test data"""
        print("\n📝 Cleaning up Test Data")
        print("-" * 40)
        
        if not self.auth_token:
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
                    self.log_test("Cleanup Checklist Item", False, f"Status: {response.status_code}")
            
            # Delete created regulation
            if 'created_regulation_id' in self.test_data:
                reg_id = self.test_data['created_regulation_id']
                response = requests.delete(f"{self.api_url}/regulations/{reg_id}/", 
                                        headers=headers, timeout=10)
                if response.status_code in [200, 204]:
                    self.log_test("Cleanup Regulation", True, f"Deleted regulation {reg_id}")
                else:
                    self.log_test("Cleanup Regulation", False, f"Status: {response.status_code}")
            
        except Exception as e:
            self.log_test("Cleanup", False, f"Error: {e}")
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 END-TO-END LOCAL NETWORK TEST REPORT")
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
        report_file = f"end_to_end_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'test_results': self.test_results,
                'test_data': self.test_data,
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'success_rate': (passed_tests/total_tests)*100
                }
            }, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """Run all end-to-end tests"""
        print("🧪 Starting End-to-End Local Network Tests")
        print("=" * 60)
        
        # Setup
        self.setup_test_user()
        
        # Core tests
        self.test_login_flow()
        self.test_token_refresh()
        self.test_protected_endpoints_access()
        self.test_checklist_operations()
        self.test_regulation_updates()
        self.test_compliance_reports()
        self.test_user_profile()
        self.test_export_functionality()
        self.test_audit_logging()
        
        # Complete workflow test
        self.test_complete_workflow()
        
        # Cleanup
        self.cleanup_test_data()
        
        return self.generate_report()

def main():
    """Main function"""
    tester = EndToEndTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All end-to-end tests passed!")
        print("✅ Complete user workflow is functioning!")
        print("✅ Login, checklist, updates, and reports all working!")
    else:
        print("\n⚠️  Some end-to-end tests failed.")
        print("Please check the configuration and try again.")
    
    return success

if __name__ == '__main__':
    main()
