#!/usr/bin/env python
import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append('backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

from django.contrib.auth.models import User
from checklist.models import ChecklistItem, RegulationUpdate

def check_and_add_data():
    print("=== Checking Compliance Data ===")
    
    # Check users
    users = User.objects.all()
    print(f"Total users: {users.count()}")
    for user in users:
        items = ChecklistItem.objects.filter(user=user)
        print(f"- {user.username}: {items.count()} items")
    
    # Check if TestUsername has items
    try:
        test_user = User.objects.get(username='TestUsername')
        items = ChecklistItem.objects.filter(user=test_user)
        print(f"\nTestUsername has {items.count()} items")
        
        if items.count() == 0:
            print("Adding test data for TestUsername...")
            
            # Get or create a regulation update
            regulation, created = RegulationUpdate.objects.get_or_create(
                title="Test HIPAA Regulation",
                defaults={
                    'description': 'Test regulation for compliance testing',
                    'effective_date': '2024-01-01',
                    'category': 'Privacy'
                }
            )
            
            # Create test checklist items
            test_items = [
                {
                    'regulation_update': regulation,
                    'user': test_user,
                    'completed': True,
                    'likelihood': 2,
                    'impact': 3,
                    'notes': 'Test completed item',
                    'admin_notes': 'Admin approved'
                },
                {
                    'regulation_update': regulation,
                    'user': test_user,
                    'completed': False,
                    'likelihood': 4,
                    'impact': 5,
                    'notes': 'Test incomplete item',
                    'admin_notes': 'Needs attention'
                },
                {
                    'regulation_update': regulation,
                    'user': test_user,
                    'completed': True,
                    'likelihood': 1,
                    'impact': 2,
                    'notes': 'Another completed item',
                    'admin_notes': 'Good progress'
                }
            ]
            
            for item_data in test_items:
                ChecklistItem.objects.create(**item_data)
            
            print(f"Created {len(test_items)} test items for TestUsername")
            
            # Verify the data
            items = ChecklistItem.objects.filter(user=test_user)
            print(f"TestUsername now has {items.count()} items")
            for item in items:
                print(f"- ID: {item.id}, Completed: {item.completed}, Likelihood: {item.likelihood}, Impact: {item.impact}")
        else:
            print("TestUsername already has items:")
            for item in items:
                print(f"- ID: {item.id}, Completed: {item.completed}, Likelihood: {item.likelihood}, Impact: {item.impact}")
                
    except User.DoesNotExist:
        print("TestUsername user not found!")

if __name__ == "__main__":
    check_and_add_data()
