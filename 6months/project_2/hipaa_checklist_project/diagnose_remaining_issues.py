#!/usr/bin/env python3
"""
Diagnose Remaining Issues in HIPAA Checklist System
"""

import requests
import json
import time
import sys

def print_status(message, status="INFO"):
    """Print status message with formatting"""
    symbols = {"INFO": "ℹ", "SUCCESS": "", "ERROR": "", "WARNING": ""}
    print(f"{symbols.get(status, 'ℹ')} {message}")

def test_performance_detailed():
    """Test performance with detailed timing"""
    print_status(" Detailed Performance Analysis", "INFO")
    
    base_url = "http://localhost:8000"
    endpoints = [
        ("/api/health/", "Health Check"),
        ("/api/info/", "API Info"),
        ("/api/stats/", "Public Stats"),
        ("/admin/", "Django Admin"),
    ]
    
    results = {}
    
    for endpoint, name in endpoints:
        times = []
        for i in range(3):  # Test 3 times
            start_time = time.time()
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                times.append(response_time)
                if response.status_code != 200:
                    print_status(f"{name} (attempt {i+1}):  Status {response.status_code}", "ERROR")
                else:
                    print_status(f"{name} (attempt {i+1}):  {response_time:.2f}ms", "SUCCESS")
            except Exception as e:
                print_status(f"{name} (attempt {i+1}):  Error - {e}", "ERROR")
                times.append(9999)  # Mark as very slow
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            results[name] = {
                "avg": avg_time,
                "min": min_time,
                "max": max_time,
                "times": times
            }
            print_status(f"{name} Summary: Avg={avg_time:.2f}ms, Min={min_time:.2f}ms, Max={max_time:.2f}ms", "INFO")
    
    return results

def test_database_operations():
    """Test database operations to identify constraint issues"""
    print_status(" Database Operations Test", "INFO")
    
    base_url = "http://localhost:8000"
    
    # Get authentication token
    try:
        auth_response = requests.post(f"{base_url}/api/token/", json={
            "username": "testuser", 
            "password": "testpass123"
        }, timeout=10)
        
        if auth_response.status_code == 200:
            token_data = auth_response.json()
            access_token = token_data.get('access')
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Test 1: Check regulations
            print_status(" Checking regulations...", "INFO")
            regs_response = requests.get(f"{base_url}/api/regulations/", headers=headers, timeout=10)
            print_status(f"Regulations API: Status {regs_response.status_code}", "INFO")
            if regs_response.status_code == 200:
                regulations = regs_response.json()
                print_status(f"Available regulations: {len(regulations)}", "INFO")
                for reg in regulations:
                    print_status(f"  - ID: {reg.get('id')}, Title: {reg.get('title')}", "INFO")
            
            # Test 2: Check existing checklist items
            print_status(" Checking existing checklist items...", "INFO")
            checklist_response = requests.get(f"{base_url}/api/checklist/", headers=headers, timeout=10)
            print_status(f"Checklist API: Status {checklist_response.status_code}", "INFO")
            if checklist_response.status_code == 200:
                items = checklist_response.json()
                print_status(f"Existing checklist items: {len(items)}", "INFO")
                for item in items[:3]:  # Show first 3
                    print_status(f"  - ID: {item.get('id')}, Regulation: {item.get('regulation_update_title')}", "INFO")
            
            # Test 3: Try to create a new item with existing regulation
            if regulations:
                print_status(" Testing checklist creation with existing regulation...", "INFO")
                test_data = {
                    "regulation_update": regulations[0]['id'],
                    "completed": False,
                    "notes": "Diagnostic test",
                    "likelihood": 2,
                    "impact": 3,
                    "mitigation_steps": "Test mitigation"
                }
                
                create_response = requests.post(
                    f"{base_url}/api/checklist/",
                    json=test_data,
                    headers=headers,
                    timeout=10
                )
                
                print_status(f"Create Response: Status {create_response.status_code}", "INFO")
                if create_response.status_code == 201:
                    print_status(" Checklist creation successful!", "SUCCESS")
                else:
                    print_status(f" Checklist creation failed: {create_response.text}", "ERROR")
            else:
                print_status(" No regulations available for testing", "WARNING")
                
        else:
            print_status(f" Authentication failed: {auth_response.status_code}", "ERROR")
            
    except Exception as e:
        print_status(f" Database test error: {e}", "ERROR")

def test_server_health():
    """Test overall server health"""
    print_status(" Server Health Check", "INFO")
    
    base_url = "http://localhost:8000"
    
    # Test basic connectivity
    try:
        response = requests.get(f"{base_url}/admin/", timeout=5)
        if response.status_code == 200:
            print_status(" Server is running and accessible", "SUCCESS")
        else:
            print_status(f" Server responded with status {response.status_code}", "WARNING")
    except Exception as e:
        print_status(f" Server not accessible: {e}", "ERROR")
        return False
    
    # Test API endpoints
    api_endpoints = [
        "/api/health/",
        "/api/info/",
        "/api/stats/"
    ]
    
    for endpoint in api_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print_status(f" {endpoint} - Working", "SUCCESS")
            else:
                print_status(f" {endpoint} - Status {response.status_code}", "ERROR")
        except Exception as e:
            print_status(f" {endpoint} - Error: {e}", "ERROR")
    
    return True

def main():
    """Main diagnostic function"""
    print_status(" HIPAA Checklist System - Detailed Diagnostics", "INFO")
    print_status("=" * 60)
    
    # Test 1: Server Health
    if not test_server_health():
        print_status(" Server health check failed. Cannot proceed.", "ERROR")
        return
    
    print_status("\n" + "=" * 60)
    
    # Test 2: Performance Analysis
    perf_results = test_performance_detailed()
    
    print_status("\n" + "=" * 60)
    
    # Test 3: Database Operations
    test_database_operations()
    
    print_status("\n" + "=" * 60)
    print_status("DIAGNOSTIC SUMMARY", "INFO")
    print_status("=" * 60)
    
    # Analyze performance
    if perf_results:
        avg_times = [result["avg"] for result in perf_results.values()]
        overall_avg = sum(avg_times) / len(avg_times)
        
        print_status(f"Overall Average Response Time: {overall_avg:.2f}ms", "INFO")
        
        if overall_avg < 1000:
            print_status("Performance:  EXCELLENT", "SUCCESS")
        elif overall_avg < 2000:
            print_status("Performance:  GOOD", "SUCCESS")
        elif overall_avg < 3000:
            print_status("Performance:  FAIR", "WARNING")
        else:
            print_status("Performance:  POOR", "ERROR")
    
    print_status("\nNext steps:", "INFO")
    print_status("1. Address any performance issues found", "INFO")
    print_status("2. Fix any database constraint errors", "INFO")
    print_status("3. Run final comprehensive test", "INFO")

if __name__ == "__main__":
    main()
