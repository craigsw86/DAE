#!/usr/bin/env python3
"""
Final Performance Optimization for HIPAA Checklist System
"""

import os
import sys
import django
import time
import requests
from django.db import connection

# Add backend to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

def print_status(message, status="INFO"):
    """Print status message with formatting"""
    symbols = {"INFO": "ℹ", "SUCCESS": "", "ERROR": "", "WARNING": ""}
    print(f"{symbols.get(status, 'ℹ')} {message}")

def analyze_database_performance():
    """Analyze database performance issues"""
    print_status(" Analyzing Database Performance", "INFO")
    
    try:
        from checklist.models import ChecklistItem, RegulationUpdate
        from django.contrib.auth.models import User
        
        # Test 1: Basic query performance
        print_status(" Testing basic queries...", "INFO")
        
        start_time = time.time()
        items = list(ChecklistItem.objects.all())
        end_time = time.time()
        basic_query_time = (end_time - start_time) * 1000
        print_status(f"Basic query: {basic_query_time:.2f}ms for {len(items)} items", "INFO")
        
        # Test 2: Select related performance
        start_time = time.time()
        items_with_relations = list(ChecklistItem.objects.select_related('regulation_update', 'user').all())
        end_time = time.time()
        related_query_time = (end_time - start_time) * 1000
        print_status(f"Select related query: {related_query_time:.2f}ms for {len(items_with_relations)} items", "INFO")
        
        # Test 3: Filtered query performance
        start_time = time.time()
        user_items = list(ChecklistItem.objects.filter(user_id=2).select_related('regulation_update'))
        end_time = time.time()
        filtered_query_time = (end_time - start_time) * 1000
        print_status(f"Filtered query: {filtered_query_time:.2f}ms for {len(user_items)} items", "INFO")
        
        # Test 4: Count query performance
        start_time = time.time()
        total_count = ChecklistItem.objects.count()
        completed_count = ChecklistItem.objects.filter(completed=True).count()
        end_time = time.time()
        count_query_time = (end_time - start_time) * 1000
        print_status(f"Count queries: {count_query_time:.2f}ms (total: {total_count}, completed: {completed_count})", "INFO")
        
        return {
            'basic_query': basic_query_time,
            'related_query': related_query_time,
            'filtered_query': filtered_query_time,
            'count_query': count_query_time
        }
        
    except Exception as e:
        print_status(f" Database analysis error: {e}", "ERROR")
        return None

def optimize_database():
    """Optimize database for better performance"""
    print_status(" Optimizing Database", "INFO")
    
    try:
        with connection.cursor() as cursor:
            # Analyze current indexes
            print_status(" Current indexes:", "INFO")
            cursor.execute("PRAGMA index_list('checklist_checklistitem')")
            indexes = cursor.fetchall()
            for idx in indexes:
                print_status(f"  - {idx[1]} (unique: {bool(idx[2])})", "INFO")
            
            # Optimize database
            print_status(" Running VACUUM and ANALYZE...", "INFO")
            cursor.execute("VACUUM")
            cursor.execute("ANALYZE")
            print_status(" Database optimized", "SUCCESS")
            
            # Check query plan for common queries
            print_status(" Query execution plans:", "INFO")
            
            # Test query plan for user items
            cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM checklist_checklistitem WHERE user_id = ?", [2])
            plan = cursor.fetchall()
            print_status("User items query plan:", "INFO")
            for row in plan:
                print_status(f"  - {row[3]}", "INFO")
            
            # Test query plan for completed items
            cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM checklist_checklistitem WHERE completed = 1")
            plan = cursor.fetchall()
            print_status("Completed items query plan:", "INFO")
            for row in plan:
                print_status(f"  - {row[3]}", "INFO")
        
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

def optimize_django_settings():
    """Optimize Django settings for better performance"""
    print_status(" Optimizing Django Settings", "INFO")
    
    try:
        from django.conf import settings
        
        # Check current settings
        print_status(" Current Django settings:", "INFO")
        print_status(f"  - DEBUG: {settings.DEBUG}", "INFO")
        print_status(f"  - Database: {settings.DATABASES['default']['ENGINE']}", "INFO")
        print_status(f"  - Middleware count: {len(settings.MIDDLEWARE)}", "INFO")
        print_status(f"  - Installed apps count: {len(settings.INSTALLED_APPS)}", "INFO")
        
        # Check for performance-related settings
        if hasattr(settings, 'CACHES'):
            print_status(f"  - Cache backend: {settings.CACHES.get('default', {}).get('BACKEND', 'None')}", "INFO")
        else:
            print_status("  - No cache configured", "WARNING")
        
        # Check database connection settings
        db_options = settings.DATABASES['default'].get('OPTIONS', {})
        print_status(f"  - Database options: {db_options}", "INFO")
        
        return True
        
    except Exception as e:
        print_status(f" Settings analysis error: {e}", "ERROR")
        return False

def create_performance_optimizations():
    """Create performance optimization files"""
    print_status(" Creating Performance Optimizations", "INFO")
    
    # Create optimized settings
    optimized_settings = """
# Performance optimizations for production
import os

# Database optimizations
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 30,
            'init_command': "PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL; PRAGMA cache_size=10000; PRAGMA temp_store=MEMORY;",
        }
    }
}

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# Session optimization
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'

# Static files optimization
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Logging optimization
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
"""
    
    with open('backend/hipaa_checklist/performance_settings.py', 'w') as f:
        f.write(optimized_settings)
    
    print_status(" Performance settings created", "SUCCESS")
    
    # Create database optimization script
    db_optimization = """
#!/usr/bin/env python3
\"\"\"
Database Performance Optimization Script
\"\"\"

import os
import sys
import django

# Add backend to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

def optimize_database():
    \"\"\"Optimize database for better performance\"\"\"
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Set performance pragmas
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=10000")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.execute("PRAGMA mmap_size=268435456")  # 256MB
        cursor.execute("PRAGMA optimize")
        
        print(" Database performance optimizations applied")

if __name__ == "__main__":
    optimize_database()
"""
    
    with open('optimize_database.py', 'w') as f:
        f.write(db_optimization)
    
    print_status(" Database optimization script created", "SUCCESS")
    
    return True

def main():
    """Main performance optimization function"""
    print_status(" HIPAA Checklist Performance Optimization", "INFO")
    print_status("=" * 60)
    
    # Step 1: Analyze current performance
    print_status(" Step 1: Analyzing Current Performance", "INFO")
    db_perf = analyze_database_performance()
    api_perf = test_api_performance()
    
    # Step 2: Optimize database
    print_status("\n Step 2: Optimizing Database", "INFO")
    optimize_database()
    
    # Step 3: Check Django settings
    print_status("\n Step 3: Checking Django Settings", "INFO")
    optimize_django_settings()
    
    # Step 4: Create optimization files
    print_status("\n Step 4: Creating Optimization Files", "INFO")
    create_performance_optimizations()
    
    # Step 5: Test performance after optimizations
    print_status("\n Step 5: Testing Performance After Optimizations", "INFO")
    print_status("Running database optimization script...", "INFO")
    os.system("python optimize_database.py")
    
    # Test API performance again
    print_status("Testing API performance after optimizations...", "INFO")
    api_perf_after = test_api_performance()
    
    # Summary
    print_status("\n" + "=" * 60)
    print_status("PERFORMANCE OPTIMIZATION SUMMARY", "INFO")
    print_status("=" * 60)
    
    if db_perf:
        print_status("Database Performance:", "INFO")
        for query_type, time_ms in db_perf.items():
            if time_ms < 100:
                status = " EXCELLENT"
            elif time_ms < 500:
                status = " GOOD"
            elif time_ms < 1000:
                status = " FAIR"
            else:
                status = " POOR"
            print_status(f"  {query_type}: {time_ms:.2f}ms - {status}", "INFO")
    
    if api_perf_after:
        print_status("API Performance After Optimization:", "INFO")
        for endpoint, perf in api_perf_after.items():
            avg_time = perf['avg']
            if avg_time < 500:
                status = " EXCELLENT"
            elif avg_time < 1000:
                status = " GOOD"
            elif avg_time < 2000:
                status = " FAIR"
            else:
                status = " POOR"
            print_status(f"  {endpoint}: {avg_time:.2f}ms - {status}", "INFO")
    
    print_status("\nNext steps:", "INFO")
    print_status("1. Run final comprehensive test", "INFO")
    print_status("2. Verify 100% functionality", "INFO")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
