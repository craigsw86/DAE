#!/usr/bin/env python3
"""
Simple Database Fix for HIPAA Checklist System
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
    """Main fix function"""
    print_status(" Simple Database Fix", "INFO")
    print_status("=" * 40)
    
    try:
        from django.contrib.auth.models import User
        from checklist.models import RegulationUpdate, ChecklistItem
        from django.db import connection
        
        # Check current state
        print_status(" Current Database State:", "INFO")
        print_status(f"  Users: {User.objects.count()}", "INFO")
        print_status(f"  Regulations: {RegulationUpdate.objects.count()}", "INFO")
        print_status(f"  Checklist Items: {ChecklistItem.objects.count()}", "INFO")
        
        # Check database schema
        print_status(" Checking database schema...", "INFO")
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info('checklist_checklistitem')")
            columns = cursor.fetchall()
            print_status(" ChecklistItem table columns:", "INFO")
            for col in columns:
                print_status(f"  - {col[1]} ({col[2]})", "INFO")
        
        # Test basic queries
        print_status(" Testing basic queries...", "INFO")
        
        # Test regulations query
        regulations = RegulationUpdate.objects.all()
        print_status(f" Regulations query: {regulations.count()} items", "SUCCESS")
        
        # Test checklist items query
        items = ChecklistItem.objects.all()
        print_status(f" Checklist items query: {items.count()} items", "SUCCESS")
        
        # Test related queries
        items_with_regs = ChecklistItem.objects.select_related('regulation_update').all()
        print_status(f" Related query: {items_with_regs.count()} items", "SUCCESS")
        
        # Check for any issues
        print_status(" Checking for data issues...", "INFO")
        
        # Check if any items have null regulation_update
        null_regs = ChecklistItem.objects.filter(regulation_update__isnull=True)
        if null_regs.exists():
            print_status(f" Found {null_regs.count()} items with null regulation_update", "WARNING")
        else:
            print_status(" All items have valid regulation_update", "SUCCESS")
        
        # Test performance
        print_status("⏱ Testing query performance...", "INFO")
        import time
        
        start_time = time.time()
        items = ChecklistItem.objects.select_related('regulation_update', 'user').all()
        list(items)  # Force evaluation
        end_time = time.time()
        query_time = (end_time - start_time) * 1000
        
        print_status(f" Query time: {query_time:.2f}ms", "INFO")
        
        if query_time < 100:
            print_status(" Performance: EXCELLENT", "SUCCESS")
        elif query_time < 500:
            print_status(" Performance: GOOD", "SUCCESS")
        elif query_time < 1000:
            print_status(" Performance: FAIR", "WARNING")
        else:
            print_status(" Performance: POOR", "ERROR")
        
        # Optimize database
        print_status(" Optimizing database...", "INFO")
        with connection.cursor() as cursor:
            cursor.execute("VACUUM")
            cursor.execute("ANALYZE")
            print_status(" Database optimized", "SUCCESS")
        
        print_status("\n" + "=" * 40)
        print_status("FIX COMPLETE", "SUCCESS")
        print_status("=" * 40)
        
        return True
        
    except Exception as e:
        print_status(f" Error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
