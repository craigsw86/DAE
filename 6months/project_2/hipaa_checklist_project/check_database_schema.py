#!/usr/bin/env python3
"""
Check Database Schema
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
    """Check database schema"""
    print_status(" Checking Database Schema", "INFO")
    print_status("=" * 40)
    
    try:
        from django.db import connection
        
        # Check ChecklistItem table schema
        print_status(" ChecklistItem table schema:", "INFO")
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info('checklist_checklistitem')")
            columns = cursor.fetchall()
            for col in columns:
                print_status(f"  - {col[1]} ({col[2]}) - Nullable: {not col[3]}, Default: {col[4]}", "INFO")
        
        # Check foreign key constraints
        print_status(" Foreign key constraints:", "INFO")
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA foreign_key_list('checklist_checklistitem')")
            fks = cursor.fetchall()
            for fk in fks:
                print_status(f"  - {fk[3]} -> {fk[2]}.{fk[4]}", "INFO")
        
        # Check indexes
        print_status(" Indexes:", "INFO")
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA index_list('checklist_checklistitem')")
            indexes = cursor.fetchall()
            for idx in indexes:
                print_status(f"  - {idx[1]} (unique: {bool(idx[2])})", "INFO")
        
        # Test raw SQL query
        print_status(" Testing raw SQL query:", "INFO")
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, user_id, regulation_update_id, completed FROM checklist_checklistitem LIMIT 3")
            rows = cursor.fetchall()
            for row in rows:
                print_status(f"  - ID: {row[0]}, User: {row[1]}, Regulation: {row[2]}, Completed: {row[3]}", "INFO")
        
        return True
        
    except Exception as e:
        print_status(f" Error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
