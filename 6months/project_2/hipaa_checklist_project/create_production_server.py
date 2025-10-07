#!/usr/bin/env python3
"""
Create Production-Ready Server for HIPAA Checklist System
This will significantly improve performance by using a production WSGI server
"""

import os
import sys
import django

# Add backend to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

def print_status(message, status="INFO"):
    """Print status message with formatting"""
    symbols = {"INFO": "ℹ", "SUCCESS": "", "ERROR": "", "WARNING": ""}
    print(f"{symbols.get(status, 'ℹ')} {message}")

def create_production_server():
    """Create a production-ready server configuration"""
    print_status(" Creating Production Server Configuration", "INFO")
    
    # Create production server script
    production_server = """#!/usr/bin/env python3
\"\"\"
Production Server for HIPAA Checklist System
Uses Waitress WSGI server for better performance
\"\"\"

import os
import sys
import django
from waitress import serve

# Add backend to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

def optimize_database():
    \"\"\"Optimize database for production\"\"\"
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Set production performance pragmas
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=50000")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.execute("PRAGMA mmap_size=1073741824")  # 1GB
        cursor.execute("PRAGMA optimize")
        print(" Database optimized for production")

def main():
    \"\"\"Start production server\"\"\"
    print(" Starting HIPAA Checklist Production Server")
    print("Using Waitress WSGI server for optimal performance")
    
    # Optimize database
    optimize_database()
    
    # Import Django application
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    # Start Waitress server with production settings
    print(" Server starting on http://0.0.0.0:8000")
    print("Press Ctrl+C to stop the server")
    
    serve(
        application,
        host='0.0.0.0',
        port=8000,
        threads=4,  # Multi-threaded for better performance
        connection_limit=100,
        cleanup_interval=30,
        send_bytes=18000,
        channel_timeout=120,
        log_socket_errors=True
    )

if __name__ == "__main__":
    main()
"""
    
    with open('start_production_server.py', 'w') as f:
        f.write(production_server)
    
    print_status(" Production server script created", "SUCCESS")
    
    # Create performance test script
    performance_test = """#!/usr/bin/env python3
\"\"\"
Performance Test for HIPAA Checklist System
\"\"\"

import requests
import time

def test_performance():
    \"\"\"Test system performance\"\"\"
    base_url = "http://localhost:8000"
    
    endpoints = [
        ("/api/health/", "Health Check"),
        ("/api/info/", "API Info"),
        ("/api/stats/", "Public Stats"),
        ("/admin/", "Django Admin"),
    ]
    
    print(" Testing System Performance")
    print("=" * 50)
    
    total_time = 0
    test_count = 0
    passed_tests = 0
    
    for endpoint, name in endpoints:
        start_time = time.time()
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            total_time += response_time
            test_count += 1
            
            if response.status_code == 200:
                passed_tests += 1
                if response_time < 500:
                    status = " EXCELLENT"
                elif response_time < 1000:
                    status = " GOOD"
                elif response_time < 2000:
                    status = " FAIR"
                else:
                    status = " POOR"
                print(f"{name}: {response_time:.2f}ms - {status}")
            else:
                print(f"{name}: {response_time:.2f}ms -  Status {response.status_code}")
                
        except Exception as e:
            print(f"{name}: Error - {e}")
    
    if test_count > 0:
        avg_time = total_time / test_count
        success_rate = (passed_tests / test_count) * 100
        
        print("\\n" + "=" * 50)
        print(f"Average Response Time: {avg_time:.2f}ms")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if avg_time < 1000 and success_rate >= 90:
            print(" PERFORMANCE: EXCELLENT! System is optimized!")
            return True
        elif avg_time < 2000 and success_rate >= 80:
            print(" PERFORMANCE: GOOD! System is working well!")
            return True
        else:
            print(" PERFORMANCE: NEEDS IMPROVEMENT")
            return False
    
    return False

if __name__ == "__main__":
    test_performance()
"""
    
    with open('test_production_performance.py', 'w') as f:
        f.write(performance_test)
    
    print_status(" Performance test script created", "SUCCESS")
    
    return True

def main():
    """Main function"""
    print_status(" Creating Production Server for HIPAA Checklist", "INFO")
    print_status("=" * 60)
    
    # Create production server
    create_production_server()
    
    print_status("\n" + "=" * 60)
    print_status("PRODUCTION SERVER CREATED", "SUCCESS")
    print_status("=" * 60)
    
    print_status("To start the production server:", "INFO")
    print_status("1. Run: python start_production_server.py", "INFO")
    print_status("2. Test performance: python test_production_performance.py", "INFO")
    print_status("3. Run final test: python test_improved_flow.py", "INFO")
    
    print_status("\nExpected improvements:", "INFO")
    print_status("- Response times should drop to under 500ms", "INFO")
    print_status("- Multi-threaded processing for better concurrency", "INFO")
    print_status("- Production-grade WSGI server (Waitress)", "INFO")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
