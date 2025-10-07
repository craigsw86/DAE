#!/usr/bin/env python3
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
    print_status("\n1. Testing Server Availability", "INFO")
    success, status = test_endpoint(f"{base_url}/admin/", "Django Admin")
    results["Server"] = {"success": success, "status": status}
    
    # Test 2: Public Endpoints
    print_status("\n2. Testing Public Endpoints", "INFO")
    public_endpoints = [
        ("/api/health/", "Health Check"),
        ("/api/info/", "API Info"),
        ("/api/stats/", "Public Stats"),
    ]
    
    for endpoint, name in public_endpoints:
        success, status = test_endpoint(f"{base_url}{endpoint}", name)
        results[name] = {"success": success, "status": status}
    
    # Test 3: Authentication
    print_status("\n3. Testing Authentication", "INFO")
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
                print_status("\n4. Testing Protected Endpoints", "INFO")
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
                print_status("\n5. Testing Checklist Operations", "INFO")
                
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
                    headers,
                    expected_status=201  # 201 is correct for creation
                )
                results["Checklist Creation"] = {"success": success, "status": status}
                
                # Test 6: Export Functionality
                print_status("\n6. Testing Export Functionality", "INFO")
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
    print_status("\n7. Testing Performance", "INFO")
    start_time = time.time()
    success, status = test_endpoint(f"{base_url}/api/health/", "Performance Test")
    end_time = time.time()
    response_time = round((end_time - start_time) * 1000, 2)
    
    if response_time < 1000:  # Less than 1 second
        print_status(f"Performance:  {response_time}ms", "SUCCESS")
    else:
        print_status(f"Performance:  {response_time}ms (slow)", "WARNING")
    
    results["Performance"] = {"success": response_time < 2000, "response_time": response_time}  # More reasonable threshold
    
    # Summary
    print_status("\n" + "=" * 50)
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
    print_status("\nDetailed Results:", "INFO")
    for test_name, result in results.items():
        status_symbol = "" if result.get("success", False) else ""
        print_status(f"  {test_name}: {status_symbol} {result.get('status', 'Unknown')}")
    
    return results

if __name__ == "__main__":
    main()
