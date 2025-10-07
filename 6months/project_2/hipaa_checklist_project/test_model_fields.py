#!/usr/bin/env python3
"""
Test Model Fields to Identify the Issue
"""

import os
import sys
import django

# Add backend to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

def print_status(message, status="INFO"):
    """Print status message with formatting"""
    symbols = {"INFO": "ℹ", "SUCCESS": "", "ERROR": "", "WARNING": ""}
    print(f"{symbols.get(status, 'ℹ')} {message}")

def main():
    """Test model fields"""
    print_status(" Testing Model Fields", "INFO")
    print_status("=" * 40)
    
    try:
        from checklist.models import ChecklistItem
        
        # Get model fields
        fields = ChecklistItem._meta.get_fields()
        print_status(" ChecklistItem model fields:", "INFO")
        for field in fields:
            print_status(f"  - {field.name} ({field.__class__.__name__})", "INFO")
        
        # Test basic query
        print_status(" Testing basic query...", "INFO")
        items = ChecklistItem.objects.all()
        print_status(f" Found {items.count()} items", "SUCCESS")
        
        # Test with select_related
        print_status(" Testing select_related...", "INFO")
        items_with_regs = ChecklistItem.objects.select_related('regulation').all()
        print_status(f" Found {items_with_regs.count()} items with regulations", "SUCCESS")
        
        # Test filtering by regulation
        print_status(" Testing regulation filter...", "INFO")
        try:
            items_with_regs = ChecklistItem.objects.filter(regulation__isnull=False)
            print_status(f" Found {items_with_regs.count()} items with non-null regulation", "SUCCESS")
        except Exception as e:
            print_status(f" Error filtering by regulation: {e}", "ERROR")
        
        # Test filtering by regulation_id
        print_status(" Testing regulation_id filter...", "INFO")
        try:
            items_with_regs = ChecklistItem.objects.filter(regulation_id__isnull=False)
            print_status(f" Found {items_with_regs.count()} items with non-null regulation_id", "SUCCESS")
        except Exception as e:
            print_status(f" Error filtering by regulation_id: {e}", "ERROR")
        
        # Test performance
        print_status("⏱ Testing performance...", "INFO")
        import time
        
        start_time = time.time()
        items = list(ChecklistItem.objects.select_related('regulation', 'user').all())
        end_time = time.time()
        query_time = (end_time - start_time) * 1000
        
        print_status(f" Query time: {query_time:.2f}ms for {len(items)} items", "INFO")
        
        if query_time < 100:
            print_status(" Performance: EXCELLENT", "SUCCESS")
        elif query_time < 500:
            print_status(" Performance: GOOD", "SUCCESS")
        elif query_time < 1000:
            print_status(" Performance: FAIR", "WARNING")
        else:
            print_status(" Performance: POOR", "ERROR")
        
        return True
        
    except Exception as e:
        print_status(f" Error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
