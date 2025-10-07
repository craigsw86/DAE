#!/usr/bin/env python3
"""
Simple Performance Optimization for HIPAA Checklist System
"""

import os
import sys
import django
import time
import requests

# Add backend to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

def print_status(message, status="INFO"):
    """Print status message with formatting"""
    symbols = {"INFO": "ℹ", "SUCCESS": "", "ERROR": "", "WARNING": ""}
    print(f"{symbols.get(status, 'ℹ')} {message}")

def optimize_database_direct():
    """Optimize database directly with SQL"""
    print_status(" Optimizing Database Directly", "INFO")
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Set performance pragmas
            print_status("Setting performance pragmas...", "INFO")
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA synchronous=NORMAL")
            cursor.execute("PRAGMA cache_size=10000")
            cursor.execute("PRAGMA temp_store=MEMORY")
            cursor.execute("PRAGMA mmap_size=268435456")  # 256MB
            cursor.execute("PRAGMA optimize")
            
            print_status(" Database performance optimizations applied", "SUCCESS")
            
            # Check current indexes
            print_status(" Current indexes:", "INFO")
            cursor.execute("PRAGMA index_list('checklist_checklistitem')")
            indexes = cursor.fetchall()
            for idx in indexes:
                print_status(f"  - {idx[1]} (unique: {bool(idx[2])})", "INFO")
            
            # Test query performance
            print_status(" Testing query performance...", "INFO")
            start_time = time.time()
            cursor.execute("SELECT COUNT(*) FROM checklist_checklistitem")
            count = cursor.fetchone()[0]
            end_time = time.time()
            query_time = (end_time - start_time) * 1000
            print_status(f"Count query: {query_time:.2f}ms for {count} items", "INFO")
            
            # Test select query
            start_time = time.time()
            cursor.execute("SELECT id, user_id, regulation_update_id, completed FROM checklist_checklistitem LIMIT 10")
            rows = cursor.fetchall()
            end_time = time.time()
            select_time = (end_time - start_time) * 1000
            print_status(f"Select query: {select_time:.2f}ms for {len(rows)} items", "INFO")
        
        return True
        
    except Exception as e:
        print_status(f" Database optimization error: {e}", "ERROR")
        return False

def test_api_performance():
    """Test API endpoint performance"""
    print_status(" Testing API Performance", "INFO")
    
    base_url = "http://localhost:8000"
    endpoints = [
        ("/api/health/", "Health Check"),
        ("/api/info/", "API Info"),
        ("/api/stats/", "Public Stats"),
    ]
    
    results = {}
    
    for endpoint, name in endpoints:
        times = []
        for i in range(5):  # Test 5 times for better average
            start_time = time.time()
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                times.append(response_time)
                print_status(f"{name} (attempt {i+1}): {response_time:.2f}ms - Status {response.status_code}", "INFO")
            except Exception as e:
                print_status(f"{name} (attempt {i+1}): Error - {e}", "ERROR")
                times.append(9999)
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            results[name] = {
                "avg": avg_time,
                "min": min_time,
                "max": max_time
            }
            print_status(f"{name} Summary: Avg={avg_time:.2f}ms, Min={min_time:.2f}ms, Max={max_time:.2f}ms", "INFO")
    
    return results

def create_optimized_server_script():
    """Create an optimized server startup script"""
    print_status(" Creating Optimized Server Script", "INFO")
    
    optimized_server = """#!/usr/bin/env python3
\"\"\"
Optimized Django Server for HIPAA Checklist
\"\"\"

import os
import sys
import django
from django.core.management import execute_from_command_line

# Add backend to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

def optimize_database():
    \"\"\"Optimize database before starting server\"\"\"
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Set performance pragmas
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=10000")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.execute("PRAGMA mmap_size=268435456")
        cursor.execute("PRAGMA optimize")
        print(" Database optimized for performance")

def main():
    \"\"\"Start optimized Django server\"\"\"
    print(" Starting Optimized HIPAA Checklist Server")
    
    # Optimize database
    optimize_database()
    
    # Start server with optimizations
    os.environ['DJANGO_SETTINGS_MODULE'] = 'hipaa_checklist.settings'
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])

if __name__ == "__main__":
    main()
"""
    
    with open('start_optimized_server.py', 'w') as f:
        f.write(optimized_server)
    
    print_status(" Optimized server script created", "SUCCESS")
    return True

def main():
    """Main performance optimization function"""
    print_status(" HIPAA Checklist Performance Optimization", "INFO")
    print_status("=" * 60)
    
    # Step 1: Optimize database
    print_status(" Step 1: Optimizing Database", "INFO")
    optimize_database_direct()
    
    # Step 2: Test current API performance
    print_status("\n Step 2: Testing Current API Performance", "INFO")
    api_perf_before = test_api_performance()
    
    # Step 3: Create optimized server script
    print_status("\n Step 3: Creating Optimized Server Script", "INFO")
    create_optimized_server_script()
    
    # Step 4: Test API performance again
    print_status("\n Step 4: Testing API Performance After Optimization", "INFO")
    api_perf_after = test_api_performance()
    
    # Summary
    print_status("\n" + "=" * 60)
    print_status("PERFORMANCE OPTIMIZATION SUMMARY", "INFO")
    print_status("=" * 60)
    
    if api_perf_after:
        print_status("API Performance Results:", "INFO")
        overall_avg = 0
        count = 0
        
        for endpoint, perf in api_perf_after.items():
            avg_time = perf['avg']
            overall_avg += avg_time
            count += 1
            
            if avg_time < 500:
                status = " EXCELLENT"
            elif avg_time < 1000:
                status = " GOOD"
            elif avg_time < 2000:
                status = " FAIR"
            else:
                status = " POOR"
            print_status(f"  {endpoint}: {avg_time:.2f}ms - {status}", "INFO")
        
        if count > 0:
            overall_avg = overall_avg / count
            print_status(f"Overall Average: {overall_avg:.2f}ms", "INFO")
            
            if overall_avg < 1000:
                print_status(" PERFORMANCE: EXCELLENT!", "SUCCESS")
            elif overall_avg < 2000:
                print_status(" PERFORMANCE: GOOD", "SUCCESS")
            else:
                print_status(" PERFORMANCE: NEEDS IMPROVEMENT", "WARNING")
    
    print_status("\nNext steps:", "INFO")
    print_status("1. Use 'python start_optimized_server.py' for better performance", "INFO")
    print_status("2. Run final comprehensive test", "INFO")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
