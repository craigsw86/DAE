#!/usr/bin/env python3
"""
Simple Fix Script for HIPAA Checklist Project
Fixes URL routing and creates improved test script
"""

import os
import requests
import json
import time

def print_status(message, status="INFO"):
    """Print status message with formatting"""
    symbols = {"INFO": "ℹ", "SUCCESS": "", "ERROR": "", "WARNING": ""}
    print(f"{symbols.get(status, 'ℹ')} {message}")

def check_server_running():
    """Check if Django server is running"""
    try:
        response = requests.get("http://localhost:8000/admin/", timeout=5)
        return response.status_code == 200
    except:
        return False

def fix_url_routing():
    """Fix URL routing issues"""
    print_status("Fixing URL routing configuration...")
    
    # Check if public_views.py exists
    public_views_path = "backend/checklist/public_views.py"
    if not os.path.exists(public_views_path):
        print_status("Creating public_views.py...")
        with open(public_views_path, 'w') as f:
            f.write('''"""
Public API views that don't require authentication
For testing and public access
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'HIPAA Checklist API is running',
        'version': '1.0.0'
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """API information endpoint"""
    return Response({
        'name': 'HIPAA Checklist API',
        'version': '1.0.0',
        'description': 'HIPAA compliance checklist management system',
        'endpoints': {
            'health': '/api/health/',
            'info': '/api/info/',
            'checklist': '/api/checklist/ (requires auth)',
            'regulations': '/api/regulations/ (requires auth)',
            'admin': '/admin/',
            'token': '/api/token/'
        }
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def public_checklist_stats(request):
    """Public checklist statistics (no sensitive data)"""
    try:
        from .models import ChecklistItem
        total_items = ChecklistItem.objects.count()
        completed_items = ChecklistItem.objects.filter(completed=True).count()
        
        return Response({
            'total_items': total_items,
            'completed_items': completed_items,
            'completion_rate': round((completed_items / total_items * 100) if total_items > 0 else 0, 2)
        })
    except Exception as e:
        return Response({
            'error': 'Unable to retrieve statistics',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
''')
    
    # Check if URLs are properly configured
    urls_path = "backend/checklist/urls.py"
    if os.path.exists(urls_path):
        with open(urls_path, 'r') as f:
            content = f.read()
        
        # Ensure public endpoints are included
        if "path('api/health/', health_check" not in content:
            print_status("Adding public endpoints to URLs...")
            # Add public endpoints if missing
            new_content = content.replace(
                "urlpatterns += router.urls",
                '''# Public endpoints (no authentication required)
    path('api/health/', health_check, name='health-check'),
    path('api/info/', api_info, name='api-info'),
    path('api/stats/', public_checklist_stats, name='public-stats'),
]

urlpatterns += router.urls'''
            )
            
            with open(urls_path, 'w') as f:
                f.write(new_content)
    
    print_status("URL routing configuration updated", "SUCCESS")

def create_improved_test_script():
    """Create an improved test script with proper data validation"""
    print_status("Creating improved test script...")
    
    test_script_content = '''#!/usr/bin/env python3
"""
Improved Manual Flow Verification Script
Fixes all identified issues and provides comprehensive testing
"""

import requests
import json
import time
import sys
from datetime import datetime

def print_status(message, status="INFO"):
    """Print status message with formatting"""
    symbols = {"INFO": "ℹ", "SUCCESS": "", "ERROR": "", "WARNING": ""}
    print(f"{symbols.get(status, 'ℹ')} {message}")

def test_endpoint(url, name, method="GET", data=None, headers=None, expected_status=200):
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            return False, f"Unsupported method: {method}"
        
        success = response.status_code == expected_status
        status_symbol = "" if success else ""
        print_status(f"{name}: {status_symbol} Status {response.status_code}")
        
        if success and response.status_code == 200:
            try:
                data = response.json()
                print_status(f"  Response: {json.dumps(data, indent=2)[:200]}...")
            except:
                print_status(f"  Response: {response.text[:200]}...")
        
        return success, response.status_code
    except Exception as e:
        print_status(f"{name}:  Error - {e}", "ERROR")
        return False, str(e)

def main():
    """Main test function"""
    print_status("Starting Improved Manual Flow Verification", "INFO")
    print_status("=" * 50)
    
    base_url = "http://localhost:8000"
    results = {}
    
    # Test 1: Server Availability
    print_status("\\n1. Testing Server Availability", "INFO")
    success, status = test_endpoint(f"{base_url}/admin/", "Django Admin")
    results["Server"] = {"success": success, "status": status}
    
    # Test 2: Public Endpoints
    print_status("\\n2. Testing Public Endpoints", "INFO")
    public_endpoints = [
        ("/api/health/", "Health Check"),
        ("/api/info/", "API Info"),
        ("/api/stats/", "Public Stats"),
    ]
    
    for endpoint, name in public_endpoints:
        success, status = test_endpoint(f"{base_url}{endpoint}", name)
        results[name] = {"success": success, "status": status}
    
    # Test 3: Authentication
    print_status("\\n3. Testing Authentication", "INFO")
    auth_data = {"username": "testuser", "password": "testpass123"}
    success, status = test_endpoint(f"{base_url}/api/token/", "Login", "POST", auth_data)
    
    if success:
        try:
            response = requests.post(f"{base_url}/api/token/", json=auth_data, timeout=10)
            token_data = response.json()
            access_token = token_data.get('access')
            
            if access_token:
                print_status("Authentication:  Token received", "SUCCESS")
                headers = {"Authorization": f"Bearer {access_token}"}
                
                # Test 4: Protected Endpoints
                print_status("\\n4. Testing Protected Endpoints", "INFO")
                protected_endpoints = [
                    ("/api/checklist/", "Checklist API"),
                    ("/api/regulations/", "Regulations API"),
                    ("/api/report/", "Compliance Report API"),
                    ("/api/profile/", "User Profile API"),
                ]
                
                for endpoint, name in protected_endpoints:
                    success, status = test_endpoint(f"{base_url}{endpoint}", name, headers=headers)
                    results[name] = {"success": success, "status": status}
                
                # Test 5: Checklist Operations
                print_status("\\n5. Testing Checklist Operations", "INFO")
                
                # Test checklist creation with proper data
                checklist_data = {
                    "regulation_update": 1,  # Assuming regulation exists
                    "completed": False,
                    "notes": "Test notes from improved script",
                    "likelihood": 3,
                    "impact": 4,
                    "mitigation_steps": "Test mitigation steps from improved script"
                }
                
                success, status = test_endpoint(
                    f"{base_url}/api/checklist/",
                    "Create Checklist Item",
                    "POST",
                    checklist_data,
                    headers
                )
                results["Checklist Creation"] = {"success": success, "status": status}
                
                # Test 6: Export Functionality
                print_status("\\n6. Testing Export Functionality", "INFO")
                export_endpoints = [
                    ("/api/checklist/export/csv/", "CSV Export"),
                    ("/api/checklist/export/pdf/", "PDF Export"),
                ]
                
                for endpoint, name in export_endpoints:
                    success, status = test_endpoint(f"{base_url}{endpoint}", name, headers=headers)
                    results[name] = {"success": success, "status": status}
                
            else:
                print_status("Authentication:  No access token", "ERROR")
                results["Authentication"] = {"success": False, "status": "No token"}
        except Exception as e:
            print_status(f"Authentication:  Error - {e}", "ERROR")
            results["Authentication"] = {"success": False, "status": str(e)}
    else:
        print_status("Authentication:  Failed", "ERROR")
        results["Authentication"] = {"success": False, "status": status}
    
    # Test 7: Performance Test
    print_status("\\n7. Testing Performance", "INFO")
    start_time = time.time()
    success, status = test_endpoint(f"{base_url}/api/health/", "Performance Test")
    end_time = time.time()
    response_time = round((end_time - start_time) * 1000, 2)
    
    if response_time < 1000:  # Less than 1 second
        print_status(f"Performance:  {response_time}ms", "SUCCESS")
    else:
        print_status(f"Performance:  {response_time}ms (slow)", "WARNING")
    
    results["Performance"] = {"success": response_time < 1000, "response_time": response_time}
    
    # Summary
    print_status("\\n" + "=" * 50)
    print_status("TEST SUMMARY", "INFO")
    print_status("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result.get("success", False))
    success_rate = round((passed_tests / total_tests) * 100, 1)
    
    print_status(f"Total Tests: {total_tests}")
    print_status(f"Passed: {passed_tests}")
    print_status(f"Failed: {total_tests - passed_tests}")
    print_status(f"Success Rate: {success_rate}%")
    
    if success_rate >= 90:
        print_status("Overall System:  EXCELLENT", "SUCCESS")
    elif success_rate >= 80:
        print_status("Overall System:  GOOD", "SUCCESS")
    elif success_rate >= 70:
        print_status("Overall System:  FAIR", "WARNING")
    else:
        print_status("Overall System:  NEEDS IMPROVEMENT", "ERROR")
    
    # Detailed results
    print_status("\\nDetailed Results:", "INFO")
    for test_name, result in results.items():
        status_symbol = "" if result.get("success", False) else ""
        print_status(f"  {test_name}: {status_symbol} {result.get('status', 'Unknown')}")
    
    return results

if __name__ == "__main__":
    main()
'''
    
    with open("test_improved_flow.py", "w") as f:
        f.write(test_script_content)
    
    print_status("Improved test script created: test_improved_flow.py", "SUCCESS")

def main():
    """Main fix function"""
    print_status("Starting Simple Fix for HIPAA Checklist Project", "INFO")
    print_status("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("backend/manage.py"):
        print_status("Error: Please run this script from the project root directory", "ERROR")
        return False
    
    # Step 1: Fix URL routing
    fix_url_routing()
    
    # Step 2: Check if server is running
    if not check_server_running():
        print_status("Django server is not running. Please start it first:", "WARNING")
        print_status("cd backend && python manage.py runserver 8000", "INFO")
        return False
    else:
        print_status("Django server is running", "SUCCESS")
    
    # Step 3: Create improved test script
    create_improved_test_script()
    
    print_status("\\n" + "=" * 60)
    print_status("FIX COMPLETE", "SUCCESS")
    print_status("=" * 60)
    
    print_status("Next steps:", "INFO")
    print_status("1. Run: python test_improved_flow.py")
    print_status("2. Check the detailed results")
    print_status("3. Address any remaining issues")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
