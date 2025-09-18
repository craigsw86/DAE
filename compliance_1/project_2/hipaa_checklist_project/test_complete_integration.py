#!/usr/bin/env python3
"""
Complete integration test for the security scanning system
"""

import os
import sys
import json
import subprocess
import time
import requests
from pathlib import Path

def test_django_setup():
    """Test Django setup and configuration"""
    print("🔍 Testing Django setup...")
    
    try:
        # Change to backend directory
        backend_dir = Path(__file__).parent / 'backend'
        os.chdir(backend_dir)
        
        # Test Django check
        result = subprocess.run(['python', 'manage.py', 'check'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("   ✅ Django configuration is valid")
            return True
        else:
            print(f"   ❌ Django check failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Django setup test failed: {e}")
        return False

def test_security_scanning():
    """Test the real security scanning functionality"""
    print("\n🔍 Testing security scanning...")
    
    try:
        # Run the security scan
        result = subprocess.run(['python', 'manage.py', 'scan_detect'], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("   ✅ Security scan completed successfully")
            
            # Check if report was generated
            reports_dir = Path(__file__).parent / 'reports' / 'detect'
            report_files = list(reports_dir.glob('real_scan_*_report.json'))
            
            if report_files:
                latest_report = max(report_files, key=os.path.getmtime)
                print(f"   ✅ Report generated: {latest_report.name}")
                
                # Parse and display summary
                with open(latest_report, 'r') as f:
                    data = json.load(f)
                
                vulns = data.get('vulnerabilities', [])
                deps = data.get('dependencies', [])
                summary = data.get('summary', {})
                
                print(f"   📊 Vulnerabilities found: {len(vulns)}")
                print(f"   📊 Dependencies scanned: {len(deps)}")
                print(f"   📊 Critical: {summary.get('critical_vulnerabilities', 0)}")
                print(f"   📊 High: {summary.get('high_vulnerabilities', 0)}")
                print(f"   📊 Medium: {summary.get('medium_vulnerabilities', 0)}")
                print(f"   📊 Low: {summary.get('low_vulnerabilities', 0)}")
                
                return True
            else:
                print("   ❌ No report files generated")
                return False
        else:
            print(f"   ❌ Security scan failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Security scanning test failed: {e}")
        return False

def test_api_endpoints():
    """Test the API endpoints"""
    print("\n🔍 Testing API endpoints...")
    
    try:
        # Start Django server in background
        print("   🚀 Starting Django server...")
        server_process = subprocess.Popen(['python', 'manage.py', 'runserver', '8000'], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(10)
        
        # Test security report endpoint
        try:
            response = requests.get('http://localhost:8000/api/security/report/', timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("   ✅ Security report API working")
                print(f"   📊 Status: {data.get('status')}")
                print(f"   📊 Vulnerabilities: {len(data.get('vulnerabilities', []))}")
                print(f"   📊 Dependencies: {len(data.get('dependencies', []))}")
            else:
                print(f"   ❌ Security report API failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ API request failed: {e}")
            return False
        
        # Test security scan endpoint
        try:
            response = requests.post('http://localhost:8000/api/security/scan/', timeout=30)
            if response.status_code == 200:
                data = response.json()
                print("   ✅ Security scan API working")
                print(f"   📊 Scan ID: {data.get('scan_id')}")
                print(f"   📊 Vulnerabilities found: {data.get('vulnerabilities_found', 0)}")
            else:
                print(f"   ❌ Security scan API failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Scan API request failed: {e}")
            return False
        
        # Stop the server
        server_process.terminate()
        server_process.wait()
        
        return True
        
    except Exception as e:
        print(f"   ❌ API testing failed: {e}")
        return False

def test_react_setup():
    """Test React setup"""
    print("\n🔍 Testing React setup...")
    
    try:
        frontend_dir = Path(__file__).parent / 'frontend'
        
        if not (frontend_dir / 'package.json').exists():
            print("   ❌ package.json not found")
            return False
        
        if not (frontend_dir / 'node_modules').exists():
            print("   ⚠️ node_modules not found - run 'npm install' first")
            return False
        
        if not (frontend_dir / 'src' / 'components' / 'SecurityDashboard.js').exists():
            print("   ❌ SecurityDashboard.js not found")
            return False
        
        print("   ✅ React setup looks good")
        return True
        
    except Exception as e:
        print(f"   ❌ React setup test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Complete Integration Test")
    print("=" * 50)
    
    tests = [
        ("Django Setup", test_django_setup),
        ("Security Scanning", test_security_scanning),
        ("API Endpoints", test_api_endpoints),
        ("React Setup", test_react_setup)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Ready for demonstration!")
        print("\n📋 To start your demo:")
        print("1. Terminal 1: .\\start_django.bat")
        print("2. Terminal 2: .\\start_react.bat")
        print("3. Open http://localhost:3000")
    else:
        print("❌ Some tests failed. Please fix the issues before demonstrating.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
