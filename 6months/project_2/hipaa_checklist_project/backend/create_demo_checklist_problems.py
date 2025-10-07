#!/usr/bin/env python3
"""
Create Demo Checklist with Problems
Populates the system with realistic HIPAA compliance issues for demonstration
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

from checklist.models import RegulationUpdate, ChecklistItem
from django.contrib.auth.models import User

def create_demo_checklist_problems():
    """Create a comprehensive demo checklist with various problems"""
    
    print("Creating Demo Checklist with HIPAA Compliance Problems")
    print("=" * 60)
    print()
    
    # Get or create demo user
    demo_user, created = User.objects.get_or_create(
        username='demo',
        defaults={'email': 'demo@hipaa-checklist.com'}
    )
    
    if created:
        demo_user.set_password('demo123')
        demo_user.save()
        print(f"Created demo user: {demo_user.username}")
    else:
        print(f"Using existing demo user: {demo_user.username}")
    
    print()
    
    # Clear existing checklist items for demo user
    ChecklistItem.objects.filter(user=demo_user).delete()
    print("Cleared existing checklist items for demo")
    print()
    
    # Get regulations
    regulations = list(RegulationUpdate.objects.all())
    if not regulations:
        print("No regulations found! Run: python manage.py load_hipaa_regulations")
        return
    
    print(f"Found {len(regulations)} regulations to work with")
    print()
    
    # Create comprehensive demo problems
    demo_problems = [
        {
            'regulation': 'Administrative Safeguards',
            'title': 'Missing Security Officer Designation',
            'completed': False,
            'likelihood': 5,
            'impact': 5,
            'notes': 'CRITICAL: No designated security officer assigned. This is a major HIPAA violation that could result in significant penalties.',
            'mitigation_steps': '1. Appoint a qualified security officer immediately\n2. Document the appointment in writing\n3. Ensure officer has proper training and authority\n4. Establish reporting structure to senior management',
            'admin_notes': 'This is our highest priority issue. Legal team has been notified.',
            'days_old': 45
        },
        {
            'regulation': 'Technical Safeguards',
            'title': 'Unencrypted Database Storage',
            'completed': False,
            'likelihood': 4,
            'impact': 5,
            'notes': 'HIGH RISK: Patient data stored in unencrypted database. Recent audit revealed PHI is accessible in plain text.',
            'mitigation_steps': '1. Implement database encryption at rest\n2. Encrypt all existing data\n3. Update data handling procedures\n4. Train staff on new encryption protocols\n5. Schedule regular encryption audits',
            'admin_notes': 'IT team estimates 2-3 weeks for full implementation.',
            'days_old': 30
        },
        {
            'regulation': 'Physical Safeguards',
            'title': 'Inadequate Workstation Security',
            'completed': False,
            'likelihood': 3,
            'impact': 4,
            'notes': 'MEDIUM-HIGH: Workstations in public areas lack proper physical security. Staff computers left unlocked and unattended.',
            'mitigation_steps': '1. Install privacy screens on all workstations\n2. Implement automatic screen lock policies\n3. Relocate workstations away from public areas\n4. Install security cameras in sensitive areas\n5. Conduct regular security walkthroughs',
            'admin_notes': 'Facilities team working on workstation relocation plan.',
            'days_old': 20
        },
        {
            'regulation': 'Breach Notification',
            'title': 'Outdated Breach Response Procedures',
            'completed': False,
            'likelihood': 4,
            'impact': 4,
            'notes': 'HIGH: Current breach notification procedures are outdated and do not meet 2024 requirements. Risk of delayed reporting.',
            'mitigation_steps': '1. Review and update breach notification policies\n2. Create incident response team\n3. Establish 24/7 breach hotline\n4. Train all staff on new procedures\n5. Test breach response plan quarterly',
            'admin_notes': 'Legal team reviewing new procedures for compliance.',
            'days_old': 15
        },
        {
            'regulation': 'Privacy Rule',
            'title': 'Missing Patient Authorization Forms',
            'completed': False,
            'likelihood': 3,
            'impact': 3,
            'notes': 'MEDIUM: Some patient authorization forms are missing required elements. Could lead to unauthorized disclosures.',
            'mitigation_steps': '1. Audit all existing authorization forms\n2. Update forms to include all required elements\n3. Retrain staff on proper form completion\n4. Implement form validation system\n5. Regular compliance audits',
            'admin_notes': 'Forms department updating templates this week.',
            'days_old': 10
        },
        {
            'regulation': 'Audit Controls',
            'title': 'Insufficient Audit Logging',
            'completed': False,
            'likelihood': 4,
            'impact': 3,
            'notes': 'MEDIUM-HIGH: Current audit logging is incomplete. Not tracking all required system access and modifications.',
            'mitigation_steps': '1. Implement comprehensive audit logging system\n2. Enable logging for all PHI access\n3. Establish log review procedures\n4. Train IT staff on log analysis\n5. Regular log integrity checks',
            'admin_notes': 'IT security team implementing new logging system.',
            'days_old': 25
        },
        {
            'regulation': 'Workforce Training',
            'title': 'Incomplete Staff Training Records',
            'completed': False,
            'likelihood': 3,
            'impact': 3,
            'notes': 'MEDIUM: 40% of staff missing required HIPAA training. Training records are incomplete and outdated.',
            'mitigation_steps': '1. Conduct comprehensive training audit\n2. Schedule mandatory training for all staff\n3. Implement training tracking system\n4. Establish annual training requirements\n5. Create training completion reports',
            'admin_notes': 'HR department coordinating with compliance team.',
            'days_old': 35
        },
        {
            'regulation': 'Data Backup',
            'title': 'Inadequate Backup Procedures',
            'completed': False,
            'likelihood': 2,
            'impact': 5,
            'notes': 'HIGH IMPACT: Current backup procedures do not meet HIPAA requirements. Risk of data loss and non-compliance.',
            'mitigation_steps': '1. Implement automated daily backups\n2. Test backup restoration procedures\n3. Store backups in secure off-site location\n4. Encrypt all backup data\n5. Document backup and recovery procedures',
            'admin_notes': 'IT team working with cloud provider for secure backups.',
            'days_old': 40
        },
        {
            'regulation': 'Business Associate',
            'title': 'Missing Business Associate Agreements',
            'completed': False,
            'likelihood': 4,
            'impact': 4,
            'notes': 'HIGH: Several vendors handling PHI do not have current Business Associate Agreements. Major compliance risk.',
            'mitigation_steps': '1. Identify all vendors handling PHI\n2. Review existing agreements\n3. Execute new BAAs where needed\n4. Implement vendor management system\n5. Regular BAA renewal process',
            'admin_notes': 'Legal team prioritizing vendor agreements this month.',
            'days_old': 50
        },
        {
            'regulation': 'Minimum Necessary',
            'title': 'Excessive PHI Access Permissions',
            'completed': False,
            'likelihood': 3,
            'impact': 3,
            'notes': 'MEDIUM: Many staff members have access to more PHI than necessary for their job functions. Violates minimum necessary standard.',
            'mitigation_steps': '1. Conduct access rights audit\n2. Implement role-based access controls\n3. Review and update user permissions\n4. Train staff on minimum necessary principle\n5. Regular access reviews',
            'admin_notes': 'IT security implementing new access control system.',
            'days_old': 18
        },
        {
            'regulation': 'Incident Response',
            'title': 'No Incident Response Plan',
            'completed': False,
            'likelihood': 4,
            'impact': 4,
            'notes': 'HIGH: No formal incident response plan exists. Could lead to delayed response and increased breach impact.',
            'mitigation_steps': '1. Develop comprehensive incident response plan\n2. Create incident response team\n3. Establish communication procedures\n4. Train staff on incident response\n5. Regular plan testing and updates',
            'admin_notes': 'Emergency response team being formed.',
            'days_old': 60
        },
        {
            'regulation': 'Administrative Safeguards',
            'title': 'Incomplete Risk Assessment',
            'completed': False,
            'likelihood': 4,
            'impact': 4,
            'notes': 'HIGH: Last risk assessment was incomplete and outdated. Missing critical security vulnerabilities.',
            'mitigation_steps': '1. Conduct comprehensive risk assessment\n2. Engage external security consultant\n3. Document all identified risks\n4. Develop risk mitigation strategies\n5. Schedule regular risk assessments',
            'admin_notes': 'External consultant hired for comprehensive assessment.',
            'days_old': 90
        },
        {
            'regulation': 'Technical Safeguards',
            'title': 'Weak Password Policies',
            'completed': False,
            'likelihood': 3,
            'impact': 3,
            'notes': 'MEDIUM: Current password policies are weak. Many staff using simple passwords that could be easily compromised.',
            'mitigation_steps': '1. Implement strong password requirements\n2. Enable multi-factor authentication\n3. Conduct password security training\n4. Regular password audits\n5. Implement password management tools',
            'admin_notes': 'IT team rolling out MFA next week.',
            'days_old': 12
        },
        {
            'regulation': 'Physical Safeguards',
            'title': 'Unsecured Server Room',
            'completed': False,
            'likelihood': 2,
            'impact': 4,
            'notes': 'MEDIUM-HIGH: Server room lacks proper physical security. No access controls or monitoring.',
            'mitigation_steps': '1. Install keycard access system\n2. Add security cameras\n3. Implement visitor logging\n4. Install environmental monitoring\n5. Regular security inspections',
            'admin_notes': 'Facilities team installing access controls this month.',
            'days_old': 22
        },
        {
            'regulation': 'Privacy Rule',
            'title': 'Inadequate Notice of Privacy Practices',
            'completed': False,
            'likelihood': 3,
            'impact': 3,
            'notes': 'MEDIUM: Current Notice of Privacy Practices is outdated and missing required elements. Patients not properly informed.',
            'mitigation_steps': '1. Review and update privacy notice\n2. Ensure all required elements included\n3. Distribute updated notice to patients\n4. Update website and forms\n5. Staff training on privacy notice',
            'admin_notes': 'Legal team finalizing updated privacy notice.',
            'days_old': 28
        }
    ]
    
    created_items = []
    
    print("CREATING DEMO PROBLEMS")
    print("-" * 40)
    
    for i, problem in enumerate(demo_problems, 1):
        # Find matching regulation
        regulation = None
        for reg in regulations:
            if problem['regulation'] in reg.title:
                regulation = reg
                break
        
        if not regulation:
            # Use first regulation as fallback
            regulation = regulations[0]
        
        # Calculate creation date
        created_date = datetime.now() - timedelta(days=problem['days_old'])
        
        # Create checklist item
        item = ChecklistItem.objects.create(
            user=demo_user,
            regulation_update=regulation,
            completed=problem['completed'],
            likelihood=problem['likelihood'],
            impact=problem['impact'],
            notes=problem['notes'],
            mitigation_steps=problem['mitigation_steps'],
            admin_notes=problem['admin_notes']
        )
        
        # Update creation date
        item.last_updated = created_date
        item.save()
        
        created_items.append(item)
        
        risk_score = problem['likelihood'] * problem['impact']
        risk_level = "CRITICAL" if risk_score >= 20 else "HIGH" if risk_score >= 15 else "MEDIUM" if risk_score >= 10 else "LOW"
        
        print(f"{i:2d}. {problem['title']}")
        print(f"    Risk: L{problem['likelihood']} × I{problem['impact']} = {risk_score} ({risk_level})")
        print(f"    Age: {problem['days_old']} days old")
        print(f"    Regulation: {regulation.title}")
        print()
    
    print("=" * 60)
    print(f"Created {len(created_items)} demo problems!")
    print()
    
    # Show summary statistics
    print("DEMO PROBLEM SUMMARY")
    print("-" * 40)
    
    total_items = len(created_items)
    critical_items = len([item for item in created_items if item.likelihood * item.impact >= 20])
    high_items = len([item for item in created_items if 15 <= item.likelihood * item.impact < 20])
    medium_items = len([item for item in created_items if 10 <= item.likelihood * item.impact < 15])
    low_items = len([item for item in created_items if item.likelihood * item.impact < 10])
    
    print(f"Total Problems: {total_items}")
    print(f"Critical Risk: {critical_items}")
    print(f"High Risk: {high_items}")
    print(f"Medium Risk: {medium_items}")
    print(f"Low Risk: {low_items}")
    print()
    
    # Show by regulation category
    print("PROBLEMS BY REGULATION")
    print("-" * 40)
    
    regulation_counts = {}
    for item in created_items:
        reg_title = item.regulation_update.title
        if 'Administrative' in reg_title:
            category = 'Administrative Safeguards'
        elif 'Security Rule' in reg_title:
            category = 'Security Rule'
        elif 'Privacy Rule' in reg_title:
            category = 'Privacy Rule'
        elif 'Breach Notification' in reg_title:
            category = 'Breach Notification'
        else:
            category = 'Other'
        
        regulation_counts[category] = regulation_counts.get(category, 0) + 1
    
    for category, count in regulation_counts.items():
        print(f"   • {category}: {count} problems")
    
    print()
    print("DEMO READY!")
    print("-" * 40)
    print("Login with: demo / demo123")
    print("Go to: http://127.0.0.1:8000/checklist-page/")
    print("Show various risk levels and compliance issues")
    print("Demonstrate mitigation tracking and admin notes")
    print()
    print("Perfect for demonstrating:")
    print("   • Risk scoring and prioritization")
    print("   • Compliance tracking and management")
    print("   • Mitigation planning and execution")
    print("   • Admin oversight and notes")
    print("   • Regulation-based organization")

if __name__ == '__main__':
    create_demo_checklist_problems()
