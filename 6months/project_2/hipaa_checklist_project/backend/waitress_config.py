#!/usr/bin/env python3
"""
Waitress Configuration for HIPAA Checklist Project
Production-ready configuration with security and performance optimizations
"""

import os
from pathlib import Path

# Server Configuration
WAITRESS_CONFIG = {
    # Basic settings
    'host': os.environ.get('WAITRESS_HOST', '0.0.0.0'),
    'port': int(os.environ.get('WAITRESS_PORT', '8000')),
    'threads': int(os.environ.get('WAITRESS_THREADS', '4')),
    
    # Security settings
    'connection_limit': 1000,
    'cleanup_interval': 30,
    'channel_timeout': 120,
    'expose_tracebacks': False,  # Security: don't expose tracebacks
    
    # Performance settings
    'send_bytes': 18000,
    'outbuf_overflow': 1048576,  # 1MB
    'inbuf_overflow': 1048576,   # 1MB
    'recv_bytes': 8192,
    
    # Request limits
    'max_request_header_size': 262144,  # 256KB
    'max_request_body_size': 1048576,   # 1MB
    
    # Logging
    'ident': 'HIPAA-Checklist',
    
    # Advanced settings
    'asyncore_use_poll': True,
    'unix_socket': None,
    'unix_socket_perms': None,
    'url_scheme': 'https' if os.environ.get('HTTPS', 'false').lower() == 'true' else 'http',
}

# Security Headers Configuration
SECURITY_HEADERS = {
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
    'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
}

# Database Security Configuration
DATABASE_SECURITY = {
    'encryption_enabled': True,
    'backup_enabled': True,
    'backup_interval': 3600,  # 1 hour
    'max_backups': 7,  # Keep 7 days of backups
    'encryption_password': os.environ.get('DB_ENCRYPTION_PASSWORD', 'hipaa_secure_password_2024'),
}

# Logging Configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'security': {
            'format': '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
        },
        'performance': {
            'format': '%(asctime)s - PERFORMANCE - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/waitress.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'security_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/security.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10,
            'formatter': 'security',
        },
        'performance_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/performance.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'performance',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'waitress': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'security': {
            'handlers': ['security_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'performance': {
            'handlers': ['performance_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Performance Monitoring Configuration
PERFORMANCE_CONFIG = {
    'monitor_enabled': True,
    'monitor_interval': 30,  # seconds
    'memory_threshold': 80,  # percentage
    'cpu_threshold': 80,     # percentage
    'disk_threshold': 90,    # percentage
    'response_time_threshold': 5.0,  # seconds
}

# Health Check Configuration
HEALTH_CHECK_CONFIG = {
    'enabled': True,
    'endpoint': '/health/',
    'timeout': 5,  # seconds
    'checks': [
        'database',
        'disk_space',
        'memory',
        'encryption',
    ],
}

def get_config():
    """Get the complete Waitress configuration"""
    return {
        'waitress': WAITRESS_CONFIG,
        'security_headers': SECURITY_HEADERS,
        'database_security': DATABASE_SECURITY,
        'logging': LOGGING_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'health_check': HEALTH_CHECK_CONFIG,
    }

def validate_config():
    """Validate the configuration"""
    errors = []
    
    # Validate port
    if not (1 <= WAITRESS_CONFIG['port'] <= 65535):
        errors.append("Invalid port number")
    
    # Validate threads
    if WAITRESS_CONFIG['threads'] < 1:
        errors.append("Threads must be at least 1")
    
    # Validate file sizes
    if WAITRESS_CONFIG['max_request_header_size'] < 1024:
        errors.append("Max request header size too small")
    
    if WAITRESS_CONFIG['max_request_body_size'] < 1024:
        errors.append("Max request body size too small")
    
    # Validate security settings
    if not isinstance(WAITRESS_CONFIG['expose_tracebacks'], bool):
        errors.append("expose_tracebacks must be boolean")
    
    return errors

def print_config():
    """Print the current configuration"""
    print(" Waitress Configuration")
    print("=" * 40)
    
    for category, config in get_config().items():
        print(f"\n {category.upper()}:")
        for key, value in config.items():
            print(f"  {key}: {value}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'validate':
        errors = validate_config()
        if errors:
            print(" Configuration validation failed:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        else:
            print(" Configuration is valid")
    else:
        print_config()
