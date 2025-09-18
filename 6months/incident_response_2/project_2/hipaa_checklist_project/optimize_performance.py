#!/usr/bin/env python3
"""
Performance optimization for Waitress server
"""

import os
import sys
from pathlib import Path

def optimize_django_settings():
    """Optimize Django settings for performance"""
    print("⚡ Optimizing Django settings for performance...")
    
    settings_file = Path("backend/hipaa_checklist/settings.py")
    
    if not settings_file.exists():
        print("❌ Settings file not found")
        return False
    
    try:
        # Read current settings
        with open(settings_file, 'r') as f:
            content = f.read()
        
        # Add performance optimizations
        performance_settings = '''
# Performance optimizations
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CULL_FREQUENCY': 3,
        }
    }
}

# Database connection optimization
DATABASES['default'].update({
    'OPTIONS': {
        'timeout': 20,
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    }
})

# Static files optimization
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Session optimization
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'

# Logging optimization (reduce verbosity)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
'''
        
        # Check if performance settings already exist
        if 'CACHES = {' in content:
            print("✅ Performance settings already exist")
            return True
        
        # Add performance settings before the last line
        lines = content.split('\n')
        lines.insert(-1, performance_settings)
        
        # Write updated settings
        with open(settings_file, 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ Performance settings added")
        return True
        
    except Exception as e:
        print(f"❌ Performance optimization failed: {e}")
        return False

def optimize_waitress_config():
    """Optimize Waitress configuration"""
    print("⚡ Optimizing Waitress configuration...")
    
    config_file = Path("backend/waitress_config.py")
    
    if not config_file.exists():
        print("❌ Waitress config file not found")
        return False
    
    try:
        # Read current config
        with open(config_file, 'r') as f:
            content = f.read()
        
        # Update performance settings
        optimized_config = '''# Optimized performance settings
WAITRESS_CONFIG.update({
    'threads': 8,  # Increase threads
    'connection_limit': 2000,  # Increase connection limit
    'send_bytes': 32768,  # Increase send buffer
    'outbuf_overflow': 2097152,  # 2MB
    'inbuf_overflow': 2097152,   # 2MB
    'recv_bytes': 16384,  # Increase receive buffer
    'cleanup_interval': 10,  # More frequent cleanup
    'channel_timeout': 60,  # Reduce timeout
})
'''
        
        # Check if optimization already exists
        if 'threads\': 8' in content:
            print("✅ Waitress optimization already exists")
            return True
        
        # Add optimization
        with open(config_file, 'a') as f:
            f.write('\n' + optimized_config)
        
        print("✅ Waitress configuration optimized")
        return True
        
    except Exception as e:
        print(f"❌ Waitress optimization failed: {e}")
        return False

def create_performance_middleware():
    """Create performance middleware"""
    print("⚡ Creating performance middleware...")
    
    middleware_file = Path("backend/checklist/performance_middleware.py")
    
    if middleware_file.exists():
        print("✅ Performance middleware already exists")
        return True
    
    middleware_content = '''"""
Performance middleware for HIPAA Checklist Project
"""

import time
from django.utils.deprecation import MiddlewareMixin

class PerformanceMiddleware(MiddlewareMixin):
    """Middleware to optimize performance"""
    
    def process_request(self, request):
        """Process request - start timing"""
        request.start_time = time.time()
    
    def process_response(self, request, response):
        """Process response - add performance headers"""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            response['X-Response-Time'] = f"{duration:.3f}s"
            
            # Add caching headers for static content
            if request.path.startswith('/static/'):
                response['Cache-Control'] = 'public, max-age=31536000'  # 1 year
                response['Expires'] = 'Thu, 31 Dec 2025 23:59:59 GMT'
        
        return response
'''
    
    try:
        with open(middleware_file, 'w') as f:
            f.write(middleware_content)
        
        print("✅ Performance middleware created")
        return True
        
    except Exception as e:
        print(f"❌ Performance middleware creation failed: {e}")
        return False

def main():
    """Run all performance optimizations"""
    print("🚀 Starting performance optimization...")
    print("=" * 50)
    
    optimizations = [
        ("Django Settings", optimize_django_settings),
        ("Waitress Config", optimize_waitress_config),
        ("Performance Middleware", create_performance_middleware),
    ]
    
    success_count = 0
    total_count = len(optimizations)
    
    for name, func in optimizations:
        print(f"\n📋 {name}...")
        if func():
            success_count += 1
            print(f"✅ {name} optimization completed")
        else:
            print(f"❌ {name} optimization failed")
    
    print(f"\n📊 Performance Optimization Results:")
    print(f"Completed: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 All performance optimizations completed!")
        return True
    else:
        print("⚠️  Some optimizations failed")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
