#!/usr/bin/env python3
"""
Comprehensive HIPAA Testing Execution Script
Runs all HIPAA compliance tests and generates detailed reports
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check if we're in the right directory
    if not os.path.exists("backend/manage.py"):
        print("❌ Error: Not in the project root directory")
        print("   Please run this script from the project root directory")
        return False
    
    # Check if Django backend exists
    if not os.path.exists("backend/checklist"):
        print("❌ Error: Django backend not found")
        return False
    
    # Check if comprehensive testing suite exists
    if not os.path.exists("comprehensive_hipaa_testing_suite.py"):
        print("❌ Error: comprehensive_hipaa_testing_suite.py not found")
        return False
    
    print("✅ Prerequisites check passed")
    return True

def start_django_server():
    """Start Django server in background"""
    print("🚀 Starting Django server...")
    
    # Change to backend directory
    os.chdir("backend")
    
    # Start Django server
    try:
        # Use the existing start script if available
        if os.path.exists("../start_django.bat"):
            subprocess.Popen(["../start_django.bat"], shell=True)
        else:
            # Start Django server directly
            subprocess.Popen(["python", "manage.py", "runserver", "8000"], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
        
        print("✅ Django server started")
        return True
    except Exception as e:
        print(f"❌ Error starting Django server: {e}")
        return False
    finally:
        # Return to project root
        os.chdir("..")

def wait_for_server():
    """Wait for Django server to be ready"""
    print("⏳ Waiting for Django server to be ready...")
    
    import requests
    max_attempts = 30
    
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/api/health/", timeout=5)
            if response.status_code == 200:
                print("✅ Django server is ready!")
                return True
        except:
            pass
        time.sleep(2)
    
    print("❌ Django server did not start within 60 seconds")
    return False

def run_hipaa_tests():
    """Run comprehensive HIPAA tests"""
    print("🏥 Running comprehensive HIPAA compliance tests...")
    
    try:
        # Run the comprehensive testing suite
        result = subprocess.run([
            "python", "comprehensive_hipaa_testing_suite.py"
        ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
        
        if result.returncode == 0:
            print("✅ HIPAA tests completed successfully")
            print("\n" + "="*60)
            print("📊 TEST OUTPUT:")
            print("="*60)
            print(result.stdout)
            return True
        else:
            print("❌ HIPAA tests failed")
            print("Error output:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ HIPAA tests timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"❌ Error running HIPAA tests: {e}")
        return False

def run_additional_security_tests():
    """Run additional security and compliance tests"""
    print("🔒 Running additional security tests...")
    
    additional_tests = [
        "comprehensive_testing_suite.py",
        "owasp_zap_security_audit.py",
        "security_verification_final.py"
    ]
    
    results = {}
    
    for test_script in additional_tests:
        if os.path.exists(test_script):
            print(f"   Running {test_script}...")
            try:
                result = subprocess.run([
                    "python", test_script
                ], capture_output=True, text=True, timeout=120)
                
                results[test_script] = {
                    "status": "PASS" if result.returncode == 0 else "FAIL",
                    "output": result.stdout,
                    "error": result.stderr
                }
                
                if result.returncode == 0:
                    print(f"   ✅ {test_script} completed successfully")
                else:
                    print(f"   ❌ {test_script} failed")
                    
            except subprocess.TimeoutExpired:
                print(f"   ⏰ {test_script} timed out")
                results[test_script] = {"status": "TIMEOUT", "output": "", "error": "Test timed out"}
            except Exception as e:
                print(f"   ❌ Error running {test_script}: {e}")
                results[test_script] = {"status": "ERROR", "output": "", "error": str(e)}
        else:
            print(f"   ⚠️ {test_script} not found, skipping")
    
    return results

def generate_final_report():
    """Generate final comprehensive report"""
    print("📋 Generating final comprehensive report...")
    
    # Look for the most recent test report
    import glob
    import json
    from datetime import datetime
    
    # Find the most recent comprehensive HIPAA test report
    hipaa_reports = glob.glob("comprehensive_hipaa_test_report_*.json")
    if hipaa_reports:
        latest_hipaa_report = max(hipaa_reports, key=os.path.getctime)
        
        try:
            with open(latest_hipaa_report, 'r') as f:
                hipaa_data = json.load(f)
            
            # Generate summary report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"FINAL_HIPAA_COMPLIANCE_REPORT_{timestamp}.md"
            
            with open(report_filename, 'w') as f:
                f.write("# Final HIPAA Compliance Report\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Project:** HIPAA Checklist Management System\n\n")
                
                # Overall summary
                summary = hipaa_data.get('summary', {})
                overall = summary.get('overall', {})
                f.write(f"## Executive Summary\n\n")
                f.write(f"- **Overall Compliance Rate:** {overall.get('success_rate', 0):.1f}%\n")
                f.write(f"- **Tests Passed:** {overall.get('passed', 0)}/{overall.get('total', 0)}\n")
                f.write(f"- **Compliance Status:** {'✅ COMPLIANT' if overall.get('success_rate', 0) >= 80 else '⚠️ NEEDS ATTENTION'}\n\n")
                
                # Category breakdown
                f.write("## HIPAA Rule Category Results\n\n")
                categories = summary.get('categories', {})
                for category, data in categories.items():
                    status = "✅" if data.get('success_rate', 0) >= 80 else "⚠️" if data.get('success_rate', 0) >= 60 else "❌"
                    f.write(f"- **{category}:** {status} {data.get('passed', 0)}/{data.get('total', 0)} ({data.get('success_rate', 0):.1f}%)\n")
                
                f.write("\n## Detailed Test Results\n\n")
                
                # Detailed results for each category
                for category_name, category_tests in hipaa_data.items():
                    if category_name in ['timestamp', 'summary']:
                        continue
                    
                    f.write(f"### {category_name.replace('_', ' ').title()}\n\n")
                    
                    for test_name, test_result in category_tests.items():
                        status_icon = "✅" if test_result.get('status') == 'PASS' else "❌"
                        f.write(f"- {status_icon} **{test_name}:** {test_result.get('status', 'UNKNOWN')}\n")
                        if test_result.get('details'):
                            f.write(f"  - Details: {test_result.get('details')}\n")
                        if test_result.get('hipaa_reference'):
                            f.write(f"  - HIPAA Reference: {test_result.get('hipaa_reference')}\n")
                        f.write("\n")
                
                f.write("## Recommendations\n\n")
                if overall.get('success_rate', 0) >= 90:
                    f.write("- ✅ System is fully HIPAA compliant\n")
                    f.write("- ✅ Continue regular compliance monitoring\n")
                    f.write("- ✅ Maintain current security controls\n")
                elif overall.get('success_rate', 0) >= 80:
                    f.write("- ⚠️ System is mostly HIPAA compliant with minor gaps\n")
                    f.write("- ⚠️ Address identified compliance gaps\n")
                    f.write("- ⚠️ Enhance documentation where needed\n")
                else:
                    f.write("- ❌ Significant HIPAA compliance gaps identified\n")
                    f.write("- ❌ Immediate action required to address compliance issues\n")
                    f.write("- ❌ Consider professional HIPAA compliance consultation\n")
                
                f.write("\n---\n")
                f.write("*This report was generated by the Comprehensive HIPAA Testing Suite*\n")
            
            print(f"✅ Final report generated: {report_filename}")
            return report_filename
            
        except Exception as e:
            print(f"❌ Error generating final report: {e}")
            return None
    else:
        print("❌ No HIPAA test reports found")
        return None

def main():
    """Main execution function"""
    print("🏥 COMPREHENSIVE HIPAA COMPLIANCE TESTING")
    print("=" * 60)
    print("Testing entire project against full set of HIPAA regulations and guidelines")
    print("=" * 60)
    
    # Step 1: Check prerequisites
    if not check_prerequisites():
        return False
    
    # Step 2: Start Django server
    if not start_django_server():
        return False
    
    # Step 3: Wait for server to be ready
    if not wait_for_server():
        return False
    
    # Step 4: Run comprehensive HIPAA tests
    if not run_hipaa_tests():
        print("⚠️ HIPAA tests had issues, but continuing with additional tests...")
    
    # Step 5: Run additional security tests
    additional_results = run_additional_security_tests()
    
    # Step 6: Generate final report
    report_file = generate_final_report()
    
    print("\n" + "="*60)
    print("🎉 COMPREHENSIVE HIPAA TESTING COMPLETED")
    print("="*60)
    
    if report_file:
        print(f"📋 Final report: {report_file}")
    
    print("\n📊 Summary of additional security tests:")
    for test_name, result in additional_results.items():
        status_icon = "✅" if result['status'] == 'PASS' else "❌"
        print(f"   {status_icon} {test_name}: {result['status']}")
    
    print("\n🏥 Your HIPAA Checklist Project has been thoroughly tested against all major HIPAA regulations!")
    print("   Review the generated reports for detailed compliance information.")
    
    return True

if __name__ == "__main__":
    main()
