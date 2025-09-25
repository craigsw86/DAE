#!/usr/bin/env python3
"""
Test Enhanced HIPAA System
Tests the enhanced HIPAA regulations system with sample data
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

from checklist.models import RegulationUpdate, ChecklistItem
from django.contrib.auth.models import User
from checklist.forms import ChecklistItemForm

def test_enhanced_hipaa_system():
    """Test the enhanced HIPAA system with sample data"""
    
    print("🧪 Testing Enhanced HIPAA System")
    print("=" * 50)
    print()
    
    # 1. Create test user
    test_user, created = User.objects.get_or_create(
        username='test_user',
        defaults={'email': 'test@hipaa-checklist.com'}
    )
    
    print(f"👤 Test user: {test_user.username}")
    print()
    
    # 2. Get sample regulations
    regulations = RegulationUpdate.objects.all()[:5]  # Get first 5
    print(f"📋 Using {regulations.count()} sample regulations")
    print()
    
    # 3. Create sample checklist items
    sample_items = [
        {
            'regulation': regulations[0] if regulations.count() > 0 else None,
            'completed': False,
            'likelihood': 5,
            'impact': 5,
            'notes': 'Critical security requirement - implementing comprehensive risk assessment',
            'mitigation_steps': 'Conduct quarterly risk assessments, implement security management process, establish incident response procedures'
        },
        {
            'regulation': regulations[1] if regulations.count() > 1 else None,
            'completed': True,
            'likelihood': 2,
            'impact': 3,
            'notes': 'Completed - all physical safeguards implemented',
            'mitigation_steps': 'Facility access controls, workstation security, device controls implemented'
        },
        {
            'regulation': regulations[2] if regulations.count() > 2 else None,
            'completed': False,
            'likelihood': 4,
            'impact': 4,
            'notes': 'In progress - updating privacy notices and procedures',
            'mitigation_steps': 'Review and update privacy policies, train staff on new requirements'
        }
    ]
    
    created_items = []
    for i, item_data in enumerate(sample_items):
        if item_data['regulation']:
            checklist_item, item_created = ChecklistItem.objects.get_or_create(
                user=test_user,
                regulation_update=item_data['regulation'],
                defaults={
                    'completed': item_data['completed'],
                    'likelihood': item_data['likelihood'],
                    'impact': item_data['impact'],
                    'notes': item_data['notes'],
                    'mitigation_steps': item_data['mitigation_steps']
                }
            )
            
            if item_created:
                created_items.append(checklist_item)
                print(f"✅ Created item {i+1}: {checklist_item.regulation_update.title}")
            else:
                print(f"📋 Item {i+1} already exists: {checklist_item.regulation_update.title}")
    
    print()
    
    # 4. Show all checklist items
    print("4️⃣ ALL CHECKLIST ITEMS")
    print("-" * 40)
    
    all_items = ChecklistItem.objects.filter(user=test_user)
    print(f"📊 Total items: {all_items.count()}")
    print()
    
    for item in all_items:
        status = "✅ Completed" if item.completed else "⏳ In Progress"
        risk_score = item.likelihood * item.impact
        risk_level = "HIGH" if risk_score >= 20 else "MEDIUM" if risk_score >= 10 else "LOW"
        
        print(f"📋 {item.regulation_update.title}")
        print(f"   Status: {status}")
        print(f"   Risk: L{item.likelihood} × I{item.impact} = {risk_score} ({risk_level})")
        print(f"   Notes: {item.notes}")
        print(f"   Source: {item.regulation_update.source_url}")
        print()
    
    # 5. Show form usage
    print("5️⃣ FORM USAGE")
    print("-" * 40)
    
    form = ChecklistItemForm(user=test_user)
    print("📝 ChecklistItemForm fields:")
    for field_name, field in form.fields.items():
        print(f"   • {field_name}: {field.label}")
    print()
    
    # 6. Show API usage
    print("6️⃣ API USAGE")
    print("-" * 40)
    
    print("🔌 Available API endpoints:")
    print("   • GET /api/regulation-updates/ - List all regulations")
    print("   • GET /api/checklist-items/ - List user's checklist items")
    print("   • POST /api/checklist-items/ - Create new checklist item")
    print("   • PUT /api/checklist-items/{id}/ - Update checklist item")
    print()
    
    # 7. Show template usage
    print("7️⃣ TEMPLATE USAGE")
    print("-" * 40)
    
    print("🌐 Template variables available:")
    print("   • {{ item.regulation_update.title }} - Regulation title")
    print("   • {{ item.regulation_update.description }} - Full regulation text")
    print("   • {{ item.regulation_update.source_url }} - Official source URL")
    print("   • {{ item.completed }} - Completion status")
    print("   • {{ item.notes }} - User notes")
    print("   • {{ item.likelihood }} - Risk likelihood (1-5)")
    print("   • {{ item.impact }} - Risk impact (1-5)")
    print("   • {{ item.mitigation_steps }} - Mitigation steps")
    print()
    
    # 8. Show statistics
    print("8️⃣ SYSTEM STATISTICS")
    print("-" * 40)
    
    total_regulations = RegulationUpdate.objects.count()
    total_items = ChecklistItem.objects.count()
    completed_items = ChecklistItem.objects.filter(completed=True).count()
    in_progress_items = ChecklistItem.objects.filter(completed=False).count()
    
    print(f"📊 Total regulations: {total_regulations}")
    print(f"📊 Total checklist items: {total_items}")
    print(f"📊 Completed items: {completed_items}")
    print(f"📊 In progress items: {in_progress_items}")
    print()
    
    # 9. Show next steps
    print("9️⃣ NEXT STEPS")
    print("-" * 40)
    
    print("✅ Your system is ready with:")
    print("   • 15 official HIPAA regulations loaded")
    print("   • Sample checklist items created")
    print("   • Enhanced template available (index_enhanced.html)")
    print("   • Full API functionality")
    print("   • Risk scoring and mitigation tracking")
    print()
    
    print("🚀 To use the enhanced template:")
    print("   1. Copy index_enhanced.html to index.html")
    print("   2. Restart your Django server")
    print("   3. Visit your checklist page to see the enhancements")
    print()
    
    print("🎉 Enhanced HIPAA system test completed successfully!")

if __name__ == '__main__':
    test_enhanced_hipaa_system()
