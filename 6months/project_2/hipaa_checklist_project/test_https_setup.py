#!/usr/bin/env python3
"""
Test script for HTTPS setup verification
Tests nginx reverse proxy configuration with HTTPS
"""

import requests
import json
import sys
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings for self-signed certificates
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def test_https_setup():
    """Test the HTTPS setup and nginx configuration"""
    
    print("🔐 Testing HTTPS Setup for HIPAA Checklist Project")
    print("=" * 50)
    
    base_url = "https://localhost"
    api_url = f"{base_url}/api"
    
    tests = []
    
    # Test 1: HTTPS redirect
    print("\n📝 Test 1: HTTP to HTTPS redirect...")
    try:
        response = requests.get("http://localhost", allow_redirects=False, timeout=10)
        if response.status_code == 301:
            print("✅ HTTP redirects to HTTPS")
            tests.append(("HTTP Redirect", True))
        else:
            print(f"❌ HTTP redirect failed: {response.status_code}")
            tests.append(("HTTP Redirect", False))
    except Exception as e:
        print(f"❌ HTTP redirect test failed: {e}")
        tests.append(("HTTP Redirect", False))
    
    # Test 2: HTTPS connection
    print("\n📝 Test 2: HTTPS connection...")
    try:
        response = requests.get(base_url, verify=False, timeout=10)
        if response.status_code == 200:
            print("✅ HTTPS connection successful")
            tests.append(("HTTPS Connection", True))
        else:
            print(f"❌ HTTPS connection failed: {response.status_code}")
            tests.append(("HTTPS Connection", False))
    except Exception as e:
        print(f"❌ HTTPS connection test failed: {e}")
        tests.append(("HTTPS Connection", False))
    
    # Test 3: API endpoints
    print("\n📝 Test 3: API endpoints...")
    try:
        response = requests.get(f"{api_url}/checklist/", verify=False, timeout=10)
        if response.status_code in [200, 401, 403]:  # 401/403 are expected without auth
            print("✅ API endpoints accessible")
            tests.append(("API Endpoints", True))
        else:
            print(f"❌ API endpoints failed: {response.status_code}")
            tests.append(("API Endpoints", False))
    except Exception as e:
        print(f"❌ API endpoints test failed: {e}")
        tests.append(("API Endpoints", False))
    
    # Test 4: Static files
    print("\n📝 Test 4: Static files...")
    try:
        response = requests.get(f"{base_url}/static/admin/css/base.css", verify=False, timeout=10)
        if response.status_code == 200:
            print("✅ Static files accessible")
            tests.append(("Static Files", True))
        else:
            print(f"❌ Static files failed: {response.status_code}")
            tests.append(("Static Files", False))
    except Exception as e:
        print(f"❌ Static files test failed: {e}")
        tests.append(("Static Files", False))
    
    # Test 5: Security headers
    print("\n📝 Test 5: Security headers...")
    try:
        response = requests.get(base_url, verify=False, timeout=10)
        headers = response.headers
        
        security_headers = [
            'X-Frame-Options',
            'X-Content-Type-Options',
            'X-XSS-Protection',
            'Strict-Transport-Security'
        ]
        
        found_headers = 0
        for header in security_headers:
            if header in headers:
                found_headers += 1
                print(f"✅ {header}: {headers[header]}")
            else:
                print(f"❌ Missing: {header}")
        
        if found_headers >= 3:
            tests.append(("Security Headers", True))
        else:
            tests.append(("Security Headers", False))
            
    except Exception as e:
        print(f"❌ Security headers test failed: {e}")
        tests.append(("Security Headers", False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! HTTPS setup is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the configuration.")
        return False

if __name__ == "__main__":
    success = test_https_setup()
    sys.exit(0 if success else 1)
