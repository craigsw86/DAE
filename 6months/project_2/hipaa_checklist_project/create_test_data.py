#!/usr/bin/env python3
"""
Create Test Data for HIPAA Checklist Project
Creates regulations and test users for proper testing
"""

import os
import sys
import django

# Add backend to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

def create_test_data():
    """Create test regulations and users"""
    print(" Creating test data...")
    
    try:
        from django.contrib.auth.models import User
        from checklist.models import RegulationUpdate, ChecklistItem
        
        # Create test user if it doesn't exist
        username = "testuser"
        password = "testpass123"
        
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                password=password,
                email="test@example.com",
                first_name="Test",
                last_name="User"
            )
            print(f" Created test user: {username}")
        else:
            user = User.objects.get(username=username)
            print(f"ℹ Test user {username} already exists")
        
        # Create test regulations if they don't exist
        test_regulations = [
            {
                "title": "HIPAA Privacy Rule Amendment 2024",
                "description": "Updated privacy requirements for healthcare organizations",
                "source_url": "https://example.com/privacy-rule-2024"
            },
            {
                "title": "HIPAA Security Rule Update 2025",
                "description": "Enhanced security requirements for electronic health records",
                "source_url": "https://example.com/security-rule-2025"
            },
            {
                "title": "HIPAA Breach Notification Rule",
                "description": "Requirements for reporting data breaches",
                "source_url": "https://example.com/breach-notification"
            }
        ]
        
        created_regulations = []
        for reg_data in test_regulations:
            if not RegulationUpdate.objects.filter(title=reg_data["title"]).exists():
                regulation = RegulationUpdate.objects.create(**reg_data)
                created_regulations.append(regulation)
                print(f" Created regulation: {regulation.title}")
            else:
                regulation = RegulationUpdate.objects.get(title=reg_data["title"])
                created_regulations.append(regulation)
                print(f"ℹ Regulation already exists: {regulation.title}")
        
        # Create some test checklist items
        if created_regulations:
            test_checklist_items = [
                {
                    "user": user,
                    "regulation_update": created_regulations[0],
                    "completed": True,
                    "notes": "Implemented privacy controls",
                    "likelihood": 2,
                    "impact": 3,
                    "mitigation_steps": "Regular audits and training"
                },
                {
                    "user": user,
                    "regulation_update": created_regulations[1],
                    "completed": False,
                    "notes": "Need to implement encryption",
                    "likelihood": 4,
                    "impact": 5,
                    "mitigation_steps": "Deploy AES-256 encryption"
                }
            ]
            
            for item_data in test_checklist_items:
                if not ChecklistItem.objects.filter(
                    user=item_data["user"],
                    regulation_update=item_data["regulation_update"]
                ).exists():
                    item = ChecklistItem.objects.create(**item_data)
                    print(f" Created checklist item: {item.regulation_update.title}")
                else:
                    print(f"ℹ Checklist item already exists for: {item_data['regulation_update'].title}")
        
        print(f"\n Database Summary:")
        print(f"  Users: {User.objects.count()}")
        print(f"  Regulations: {RegulationUpdate.objects.count()}")
        print(f"  Checklist Items: {ChecklistItem.objects.count()}")
        
        print("\n Test data creation complete!")
        return True
        
    except Exception as e:
        print(f" Error creating test data: {e}")
        return False

if __name__ == "__main__":
    success = create_test_data()
    sys.exit(0 if success else 1)
