import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')  # Use env var for security

DEBUG = True

ALLOWED_HOSTS = ['*']  # Restrict in prod

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'auditlog',
    'encrypted_model_fields',
    'checklist',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auditlog.middleware.AuditlogMiddleware',  # For governance logging
]

ROOT_URLCONF = 'hipaa_checklist.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hipaa_checklist',
        'USER': 'hipaa_user',
        'PASSWORD': 'securepass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Secure token expiry
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# HIPAA Security: Encrypt fields
FIELD_ENCRYPTION_KEYS = [
    os.getenv('ENCRYPTION_KEY', '32-byte-key-here')  # 32 bytes for AES256
]

# Governance: Align with NIST 800-53 (e.g., AC-2 access control)
SECURE_SSL_REDIRECT = False  # Enable in deployment
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True