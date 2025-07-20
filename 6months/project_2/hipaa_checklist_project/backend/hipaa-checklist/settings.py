# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'hipaa_checklist',
#         'USER': 'youruser',
#         'PASSWORD': 'yourpass',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# INSTALLED_APPS = [..., 'auditlog', 'encrypted_models_fields', 'rest_framework_simplejwt']
# REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',)}
# FIELD_ENCRYPTION_KEYS = ['secure-key-here'] # Generate via fernet
# DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'hipaa_db', ...}}
# AUDITLOG_INCLUDE_ALL_MODELS = True

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('DJANGO_SEDCRET_KEY', 'your-secure-key-here') # Generate: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
DEBUG = False # For prod-like security
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'encrypted_model_fields',
    'auditlog',
    'checklist',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

FIELD_ENCRYPTION_KEYS = ['your-fernet-key-here'] # Generate later

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hipaa_db',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}