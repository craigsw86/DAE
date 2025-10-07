#!/usr/bin/env python3
"""
Create test user and get authentication tokens for testing
"""

import os
import sys
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')

# Setup Django
django.setup()

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def create_test_user():
    """Create a test user for API testing"""
    username = 'testuser'
    email = 'test@hipaa-checklist.com'
    password = 'testpassword123'
    
    # Create or get user
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        user.set_password(password)
        user.save()
        print(f" Created test user: {username}")
    else:
        print(f" Test user already exists: {username}")
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    
    print(f" Access Token: {access_token}")
    print(f" Refresh Token: {refresh_token}")
    
    # Save tokens to file for testing
    with open('test_tokens.txt', 'w') as f:
        f.write(f"ACCESS_TOKEN={access_token}\n")
        f.write(f"REFRESH_TOKEN={refresh_token}\n")
        f.write(f"USERNAME={username}\n")
        f.write(f"PASSWORD={password}\n")
    
    print(" Tokens saved to test_tokens.txt")
    
    return {
        'username': username,
        'password': password,
        'access_token': access_token,
        'refresh_token': refresh_token
    }

if __name__ == '__main__':
    create_test_user()

