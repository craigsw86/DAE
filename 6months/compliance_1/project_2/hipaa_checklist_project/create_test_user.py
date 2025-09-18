#!/usr/bin/env python3
"""
Create test user for end-to-end testing
"""

import os
import sys
import django

# Add backend to Python path
backend_dir = os.path.join(os.path.dirname(__file__), "backend")
sys.path.insert(0, backend_dir)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')

def create_test_user():
    """Create a test user for end-to-end testing"""
    try:
        django.setup()
        
        from django.contrib.auth.models import User
        from django.contrib.auth import authenticate
        
        # Create test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User',
                'is_active': True,
                'is_staff': True
            }
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            print("✅ Test user created successfully")
        else:
            # Update password to ensure it's correct
            user.set_password('testpass123')
            user.save()
            print("✅ Test user already exists, password updated")
        
        # Test authentication
        auth_user = authenticate(username='testuser', password='testpass123')
        if auth_user:
            print("✅ User authentication successful")
            return True
        else:
            print("❌ User authentication failed")
            return False
            
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return False

if __name__ == '__main__':
    create_test_user()
