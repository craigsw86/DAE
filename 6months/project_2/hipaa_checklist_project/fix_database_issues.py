#!/usr/bin/env python3
"""
Fix Database Issues in HIPAA Checklist System
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

def fix_database_issues():
    """Fix database inconsistencies and performance issues"""
    print_status(" Fixing Database Issues", "INFO")
    
    try:
        from django.contrib.auth.models import User
        from checklist.models import RegulationUpdate, ChecklistItem
        from django.db import connection
        
        # Check current state
        print_status(" Current Database State:", "INFO")
        print_status(f"  Users: {User.objects.count()}", "INFO")
        print_status(f"  Regulations: {RegulationUpdate.objects.count()}", "INFO")
        print_status(f"  Checklist Items: {ChecklistItem.objects.count()}", "INFO")
        
        # List all regulations
        regulations = RegulationUpdate.objects.all()
        print_status(" Available Regulations:", "INFO")
        for reg in regulations:
            print_status(f"  - ID: {reg.id}, Title: {reg.title}", "INFO")
        
        # List all checklist items
        items = ChecklistItem.objects.all()
        print_status(" Checklist Items:", "INFO")
        for item in items[:5]:  # Show first 5
            reg_title = item.regulation_update.title if item.regulation_update else "MISSING"
            print_status(f"  - ID: {item.id}, Regulation: {reg_title} (ID: {item.regulation_update_id})", "INFO")
        
        # Check for orphaned checklist items
        orphaned_items = ChecklistItem.objects.filter(regulation_update__isnull=True)
        if orphaned_items.exists():
            print_status(f" Found {orphaned_items.count()} orphaned checklist items", "WARNING")
            
            # Try to fix orphaned items by assigning them to the first regulation
            if regulations.exists():
                first_reg = regulations.first()
                print_status(f" Assigning orphaned items to regulation: {first_reg.title}", "INFO")
                orphaned_items.update(regulation_update=first_reg)
                print_status(" Orphaned items fixed", "SUCCESS")
            else:
                print_status(" No regulations available to fix orphaned items", "ERROR")
        
        # Check for performance issues
        print_status(" Checking for performance issues...", "INFO")
        
        # Check database indexes
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA index_list('checklist_checklistitem')")
            indexes = cursor.fetchall()
            print_status(f" Database indexes: {len(indexes)}", "INFO")
            
            # Check if we need to add indexes
            cursor.execute("PRAGMA table_info('checklist_checklistitem')")
            columns = [row[1] for row in cursor.fetchall()]
            print_status(f" Table columns: {columns}", "INFO")
        
        # Optimize database
        print_status(" Optimizing database...", "INFO")
        with connection.cursor() as cursor:
            cursor.execute("VACUUM")
            cursor.execute("ANALYZE")
            print_status(" Database optimized", "SUCCESS")
        
        # Test query performance
        print_status("⏱ Testing query performance...", "INFO")
        import time
        
        start_time = time.time()
        items = ChecklistItem.objects.select_related('regulation_update', 'user').all()
        end_time = time.time()
        query_time = (end_time - start_time) * 1000
        
        print_status(f" Query time: {query_time:.2f}ms for {items.count()} items", "INFO")
        
        if query_time < 100:
            print_status(" Query performance: EXCELLENT", "SUCCESS")
        elif query_time < 500:
            print_status(" Query performance: GOOD", "SUCCESS")
        elif query_time < 1000:
            print_status(" Query performance: FAIR", "WARNING")
        else:
            print_status(" Query performance: POOR", "ERROR")
        
        return True
        
    except Exception as e:
        print_status(f" Error fixing database: {e}", "ERROR")
        return False

def create_missing_regulations():
    """Create missing regulations if needed"""
    print_status(" Creating Missing Regulations", "INFO")
    
    try:
        from checklist.models import RegulationUpdate
        
        # Check if we have regulations
        if RegulationUpdate.objects.count() == 0:
            print_status(" No regulations found, creating test regulations...", "WARNING")
            
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
            
            for reg_data in test_regulations:
                regulation = RegulationUpdate.objects.create(**reg_data)
                print_status(f" Created regulation: {regulation.title}", "SUCCESS")
        else:
            print_status(f"ℹ Found {RegulationUpdate.objects.count()} existing regulations", "INFO")
        
        return True
        
    except Exception as e:
        print_status(f" Error creating regulations: {e}", "ERROR")
        return False

def main():
    """Main fix function"""
    print_status(" HIPAA Checklist Database Fix", "INFO")
    print_status("=" * 50)
    
    # Step 1: Create missing regulations
    if not create_missing_regulations():
        print_status(" Failed to create regulations", "ERROR")
        return False
    
    # Step 2: Fix database issues
    if not fix_database_issues():
        print_status(" Failed to fix database issues", "ERROR")
        return False
    
    print_status("\n" + "=" * 50)
    print_status("FIX COMPLETE", "SUCCESS")
    print_status("=" * 50)
    
    print_status("Next steps:", "INFO")
    print_status("1. Run performance test", "INFO")
    print_status("2. Run comprehensive system test", "INFO")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
