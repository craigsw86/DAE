"""
Health check endpoints for HIPAA Checklist Project
Provides system health monitoring and status information
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.core.cache import cache
import psutil
import sqlite3
from pathlib import Path
import json
from datetime import datetime

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Basic health check endpoint
    Returns 200 if service is healthy, 503 if not
    """
    try:
        # Check database connectivity
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        return JsonResponse({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'hipaa-checklist-backend'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }, status=503)

@csrf_exempt
@require_http_methods(["GET"])
def detailed_health(request):
    """
    Detailed health check with system metrics
    """
    health_data = {
        'timestamp': datetime.now().isoformat(),
        'service': 'hipaa-checklist-backend',
        'status': 'healthy',
        'checks': {}
    }
    
    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        health_data['checks']['database'] = {'status': 'healthy', 'message': 'Database connection successful'}
    except Exception as e:
        health_data['checks']['database'] = {'status': 'unhealthy', 'message': str(e)}
        health_data['status'] = 'unhealthy'
    
    # Cache check
    try:
        cache.set('health_check', 'ok', 30)
        cache_result = cache.get('health_check')
        if cache_result == 'ok':
            health_data['checks']['cache'] = {'status': 'healthy', 'message': 'Cache is working'}
        else:
            health_data['checks']['cache'] = {'status': 'unhealthy', 'message': 'Cache test failed'}
            health_data['status'] = 'unhealthy'
    except Exception as e:
        health_data['checks']['cache'] = {'status': 'unhealthy', 'message': str(e)}
        health_data['status'] = 'unhealthy'
    
    # System resources check
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_data['checks']['system'] = {
            'status': 'healthy',
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'disk_percent': disk.percent
        }
        
        # Check if resources are too high
        if cpu_percent > 90 or memory.percent > 90 or disk.percent > 90:
            health_data['checks']['system']['status'] = 'warning'
            health_data['status'] = 'degraded'
            
    except Exception as e:
        health_data['checks']['system'] = {'status': 'unhealthy', 'message': str(e)}
        health_data['status'] = 'unhealthy'
    
    # Database file check
    try:
        db_path = Path('db.sqlite3')
        if db_path.exists():
            db_size = db_path.stat().st_size
            health_data['checks']['database_file'] = {
                'status': 'healthy',
                'size_bytes': db_size,
                'size_mb': round(db_size / (1024 * 1024), 2)
            }
        else:
            health_data['checks']['database_file'] = {'status': 'unhealthy', 'message': 'Database file not found'}
            health_data['status'] = 'unhealthy'
    except Exception as e:
        health_data['checks']['database_file'] = {'status': 'unhealthy', 'message': str(e)}
        health_data['status'] = 'unhealthy'
    
    # Security check
    try:
        db_path = Path('db.sqlite3')
        if db_path.exists():
            perms = oct(db_path.stat().st_mode)
            health_data['checks']['security'] = {
                'status': 'healthy',
                'db_permissions': perms,
                'encrypted': False  # Would need to check encryption status
            }
        else:
            health_data['checks']['security'] = {'status': 'unhealthy', 'message': 'Database file not found'}
    except Exception as e:
        health_data['checks']['security'] = {'status': 'unhealthy', 'message': str(e)}
    
    status_code = 200 if health_data['status'] == 'healthy' else 503
    return JsonResponse(health_data, status=status_code)

@csrf_exempt
@require_http_methods(["GET"])
def metrics(request):
    """
    Prometheus-style metrics endpoint
    """
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Database metrics
        db_path = Path('db.sqlite3')
        db_size = db_path.stat().st_size if db_path.exists() else 0
        
        # Table counts
        table_counts = {}
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                for table in tables:
                    table_name = table[0]
                    if not table_name.startswith('sqlite_'):
                        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                        count = cursor.fetchone()[0]
                        table_counts[table_name] = count
        except:
            pass
        
        metrics_data = {
            'timestamp': datetime.now().isoformat(),
            'system': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_bytes': memory.available,
                'disk_percent': disk.percent,
                'disk_free_bytes': disk.free
            },
            'database': {
                'size_bytes': db_size,
                'size_mb': round(db_size / (1024 * 1024), 2),
                'table_counts': table_counts
            }
        }
        
        return JsonResponse(metrics_data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
