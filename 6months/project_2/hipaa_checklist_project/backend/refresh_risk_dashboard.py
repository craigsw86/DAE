#!/usr/bin/env python3
"""
Complete Risk Dashboard Refresh Script
Clears all data and starts fresh for presentation
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

from checklist.models import ChecklistItem, RegulationUpdate
from django.contrib.auth.models import User
from auditlog.models import LogEntry

def refresh_risk_dashboard():
    """Completely refresh the risk dashboard"""
    
    print("🔄 HIPAA Risk Dashboard - Complete Refresh")
    print("=" * 50)
    print()
    
    # 1. Show current state
    print("1️⃣ CURRENT STATE")
    print("-" * 30)
    regulations_count = RegulationUpdate.objects.count()
    checklist_count = ChecklistItem.objects.count()
    users_count = User.objects.count()
    audit_count = LogEntry.objects.count()
    
    print(f"📊 Regulations: {regulations_count}")
    print(f"📊 Checklist Items: {checklist_count}")
    print(f"📊 Users: {users_count}")
    print(f"📊 Audit Logs: {audit_count}")
    print()
    
    # 2. Clear all data
    print("2️⃣ CLEARING ALL DATA")
    print("-" * 30)
    
    # Clear checklist items
    checklist_deleted = ChecklistItem.objects.all().delete()
    print(f"🗑️  Deleted {checklist_deleted[0]} checklist items")
    
    # Clear audit logs
    audit_deleted = LogEntry.objects.all().delete()
    print(f"🗑️  Deleted {audit_deleted[0]} audit log entries")
    
    # Clear regulations
    regulations_deleted = RegulationUpdate.objects.all().delete()
    print(f"🗑️  Deleted {regulations_deleted[0]} regulations")
    
    # Keep users (don't delete them)
    print("👤 Users preserved (not deleted)")
    print()
    
    # 3. Reload regulations
    print("3️⃣ RELOADING HIPAA REGULATIONS")
    print("-" * 30)
    
    try:
        from create_comprehensive_hipaa_regulations import create_comprehensive_hipaa_regulations
        create_comprehensive_hipaa_regulations()
        print("✅ HIPAA regulations reloaded successfully")
    except Exception as e:
        print(f"❌ Error reloading regulations: {e}")
        return False
    
    # 4. Show final state
    print()
    print("4️⃣ FINAL STATE")
    print("-" * 30)
    final_regulations = RegulationUpdate.objects.count()
    final_checklist = ChecklistItem.objects.count()
    final_users = User.objects.count()
    
    print(f"📊 Regulations: {final_regulations}")
    print(f"📊 Checklist Items: {final_checklist}")
    print(f"📊 Users: {final_users}")
    print()
    
    # 5. Show available users
    print("5️⃣ AVAILABLE USERS")
    print("-" * 30)
    users = User.objects.all()
    for user in users:
        print(f"👤 {user.username} ({user.email})")
    print()
    
    # 6. Show regulations by category
    print("6️⃣ LOADED REGULATIONS")
    print("-" * 30)
    categories = {
        'Privacy Rule': RegulationUpdate.objects.filter(title__icontains='Privacy Rule'),
        'Security Rule': RegulationUpdate.objects.filter(title__icontains='Security Rule'),
        'Breach Notification': RegulationUpdate.objects.filter(title__icontains='Breach Notification'),
        'Enforcement': RegulationUpdate.objects.filter(title__icontains='Enforcement'),
        'Administrative': RegulationUpdate.objects.filter(title__icontains='Business Associate') | 
                         RegulationUpdate.objects.filter(title__icontains='Minimum Necessary') |
                         RegulationUpdate.objects.filter(title__icontains='Audit Controls') |
                         RegulationUpdate.objects.filter(title__icontains='Workforce Training') |
                         RegulationUpdate.objects.filter(title__icontains='Incident Response') |
                         RegulationUpdate.objects.filter(title__icontains='Data Backup')
    }
    
    for category, regulations in categories.items():
        count = regulations.count()
        if count > 0:
            print(f"📋 {category}: {count} regulations")
            for reg in regulations:
                print(f"   • {reg.title}")
    print()
    
    print("🎉 Risk dashboard refresh completed!")
    print()
    print("🚀 NEXT STEPS:")
    print("   1. Start your server: python manage.py runserver")
    print("   2. Go to: http://127.0.0.1:8000/checklist-page/")
    print("   3. Log in with any of the available users")
    print("   4. Start creating fresh checklist items")
    print()
    print("💡 TIP: Use the 'demo' user (password: demo123) for testing")

if __name__ == '__main__':
    refresh_risk_dashboard()
