DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hipaa_checklist',
        'USER': 'youruser',
        'PASSWORD': 'yourpass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

INSTALLED_APPS = [..., 'auditlog', 'encrypted_models_fields', 'rest_framework_simplejwt']
REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',)}
FIELD_ENCRYPTION_KEYS = ['secure-key-here'] # Generate via fernet
DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'hipaa_db', ...}}
AUDITLOG_INCLUDE_ALL_MODELS = True
