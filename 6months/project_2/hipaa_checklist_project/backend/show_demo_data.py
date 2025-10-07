#!/usr/bin/env python3
"""
Show Demo Data
Displays the demo checklist problems for presentation
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

from checklist.models import ChecklistItem
from django.contrib.auth.models import User

def show_demo_data():
    """Show the demo checklist data"""
    
    print(" DEMO CHECKLIST DATA OVERVIEW")
    print("=" * 50)
    print()
    
    # Get demo user
    try:
        demo_user = User.objects.get(username='demo')
    except User.DoesNotExist:
        print(" Demo user not found! Run create_demo_checklist_problems.py first")
        return
    
    # Get all checklist items for demo user
    items = ChecklistItem.objects.filter(user=demo_user).order_by('-likelihood', '-impact')
    
    print(f" Demo User: {demo_user.username}")
    print(f" Total Problems: {items.count()}")
    print()
    
    # Show critical issues first
    critical_items = [item for item in items if item.likelihood * item.impact >= 20]
    high_items = [item for item in items if 15 <= item.likelihood * item.impact < 20]
    medium_items = [item for item in items if 10 <= item.likelihood * item.impact < 15]
    low_items = [item for item in items if item.likelihood * item.impact < 10]
    
    print(" CRITICAL ISSUES (Risk Score 20+)")
    print("-" * 40)
    for item in critical_items:
        risk_score = item.likelihood * item.impact
        print(f"• {item.regulation_update.title}")
        print(f"  Risk: L{item.likelihood} × I{item.impact} = {risk_score}")
        print(f"  Notes: {item.notes[:80]}...")
        print()
    
    print("🟠 HIGH RISK ISSUES (Risk Score 15-19)")
    print("-" * 40)
    for item in high_items:
        risk_score = item.likelihood * item.impact
        print(f"• {item.regulation_update.title}")
        print(f"  Risk: L{item.likelihood} × I{item.impact} = {risk_score}")
        print(f"  Notes: {item.notes[:80]}...")
        print()
    
    print("🟡 MEDIUM RISK ISSUES (Risk Score 10-14)")
    print("-" * 40)
    for item in medium_items:
        risk_score = item.likelihood * item.impact
        print(f"• {item.regulation_update.title}")
        print(f"  Risk: L{item.likelihood} × I{item.impact} = {risk_score}")
        print(f"  Notes: {item.notes[:80]}...")
        print()
    
    print("🟢 LOW RISK ISSUES (Risk Score < 10)")
    print("-" * 40)
    for item in low_items:
        risk_score = item.likelihood * item.impact
        print(f"• {item.regulation_update.title}")
        print(f"  Risk: L{item.likelihood} × I{item.impact} = {risk_score}")
        print(f"  Notes: {item.notes[:80]}...")
        print()
    
    print(" SUMMARY STATISTICS")
    print("-" * 40)
    print(f" Critical: {len(critical_items)}")
    print(f"🟠 High: {len(high_items)}")
    print(f"🟡 Medium: {len(medium_items)}")
    print(f"🟢 Low: {len(low_items)}")
    print()
    
    print(" DEMONSTRATION TIPS")
    print("-" * 40)
    print("1. Show risk prioritization (Critical → High → Medium → Low)")
    print("2. Demonstrate mitigation steps and admin notes")
    print("3. Show regulation-based organization")
    print("4. Highlight compliance tracking features")
    print("5. Show how long issues have been open")
    print()
    print(" Ready for your presentation!")

if __name__ == '__main__':
    show_demo_data()
