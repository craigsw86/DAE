#!/usr/bin/env python3
"""
Quick test script to verify Black Duck Detect integration
Run this before your class demonstration
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def test_java():
    """Test Java 11 installation"""
    print(" Testing Java 11...")
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stderr.split('\n')[0]
            if '11.' in version_line:
                print(f"    Java 11 found: {version_line}")
                return True
            else:
                print(f"    Wrong Java version: {version_line}")
                return False
        else:
            print("    Java not found")
            return False
    except Exception as e:
        print(f"    Java test failed: {e}")
        return False

def test_django():
    """Test Django setup"""
    print("\n Testing Django...")
    try:
        os.chdir('backend')
        result = subprocess.run(['python', 'manage.py', 'check'], capture_output=True, text=True)
        if result.returncode == 0:
            print("    Django setup is valid")
            return True
        else:
            print(f"    Django check failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"    Django test failed: {e}")
        return False
    finally:
        os.chdir('..')

def test_react():
    """Test React setup"""
    print("\n Testing React...")
    try:
        os.chdir('frontend')
        if Path('node_modules').exists():
            print("    Node modules installed")
            return True
        else:
            print("    Node modules not found - run 'npm install'")
            return False
    except Exception as e:
        print(f"    React test failed: {e}")
        return False
    finally:
        os.chdir('..')

def test_security_components():
    """Test security components exist"""
    print("\n Testing security components...")
    
    components = [
        'frontend/src/components/SecurityDashboard.js',
        'frontend/src/components/SecurityDashboard.css',
        'backend/checklist/security_views.py',
        'tools/detect/detect.ps1',
        'tools/detect/run-detect-jdk11.bat'
    ]
    
    all_exist = True
    for component in components:
        if Path(component).exists():
            print(f"    {component}")
        else:
            print(f"    {component} - MISSING")
            all_exist = False
    
    return all_exist

def test_django_command():
    """Test Django management command"""
    print("\n Testing Django management command...")
    try:
        os.chdir('backend')
        result = subprocess.run(['python', 'manage.py', 'scan_detect', '--help'], 
                              capture_output=True, text=True)
        if result.returncode == 0 and 'Run Black Duck Detect security scan' in result.stdout:
            print("    Django management command working")
            return True
        else:
            print("    Django management command failed")
            return False
    except Exception as e:
        print(f"    Django command test failed: {e}")
        return False
    finally:
        os.chdir('..')

def create_demo_data():
    """Create demonstration data"""
    print("\n Creating demonstration data...")
    try:
        # Create reports directory
        reports_dir = Path('reports/detect')
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Create mock scan result
        import json
        from datetime import datetime
        
        mock_data = {
            'vulnerabilities': [
                {
                    'id': 'CVE-2023-1234',
                    'severity': 'HIGH',
                    'component': 'react@18.2.0',
                    'description': 'Cross-site scripting vulnerability in React',
                    'cvss_score': 7.5,
                    'status': 'open'
                },
                {
                    'id': 'CVE-2023-5678',
                    'severity': 'MEDIUM',
                    'component': 'django@4.2.0',
                    'description': 'SQL injection vulnerability in Django ORM',
                    'cvss_score': 5.2,
                    'status': 'open'
                }
            ],
            'dependencies': [
                {
                    'name': 'react',
                    'version': '18.2.0',
                    'type': 'npm',
                    'vulnerabilities': 1,
                    'license': 'MIT'
                },
                {
                    'name': 'django',
                    'version': '4.2.0',
                    'type': 'pip',
                    'vulnerabilities': 1,
                    'license': 'BSD-3-Clause'
                }
            ],
            'summary': {
                'total_dependencies': 2,
                'vulnerable_dependencies': 2,
                'critical_vulnerabilities': 0,
                'high_vulnerabilities': 1,
                'medium_vulnerabilities': 1,
                'low_vulnerabilities': 0,
                'last_scan': datetime.now().isoformat()
            }
        }
        
        # Save mock data
        with open(reports_dir / 'demo_scan_report.json', 'w') as f:
            json.dump(mock_data, f, indent=2)
        
        print("    Demonstration data created")
        return True
        
    except Exception as e:
        print(f"    Demo data creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print(" Black Duck Detect Integration - Quick Test")
    print("=" * 50)
    
    tests = [
        test_java,
        test_django,
        test_react,
        test_security_components,
        test_django_command,
        create_demo_data
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f" Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print(" ALL TESTS PASSED! Ready for demonstration!")
        print("\n Next steps:")
        print("1. Start Django: cd backend && python manage.py runserver")
        print("2. Start React: cd frontend && npm start")
        print("3. Open http://localhost:3000 and test the Security Dashboard")
    else:
        print(" Some tests failed. Please fix the issues before demonstrating.")
        print("\n Common fixes:")
        print("- Install Java 11: choco install openjdk11 -y")
        print("- Install dependencies: npm install && pip install -r requirements.txt")
        print("- Check file paths and permissions")

if __name__ == '__main__':
    main()
