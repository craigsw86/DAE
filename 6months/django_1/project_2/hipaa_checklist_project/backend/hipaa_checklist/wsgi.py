
"""
WSGI config for hipaa_checklist project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
application = get_wsgi_application()
