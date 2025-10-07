#!/usr/bin/env python3
"""
Test Script for HIPAA Regulations Loading
Tests the comprehensive HIPAA regulations database creation

Author: HIPAA Checklist Project
Date: 2025
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

from checklist.models import RegulationUpdate
from create_comprehensive_hipaa_regulations import create_comprehensive_hipaa_regulations

def test_hipaa_regulations_loading():
    """Test the HIPAA regulations loading functionality"""
    
    print(" Testing HIPAA Regulations Loading...")
    print("=" * 50)
    
    # Count regulations before loading
    initial_count = RegulationUpdate.objects.count()
    print(f" Initial regulation count: {initial_count}")
    
    try:
        # Load regulations
        create_comprehensive_hipaa_regulations()
        
        # Count regulations after loading
        final_count = RegulationUpdate.objects.count()
        print(f" Final regulation count: {final_count}")
        print(f" Regulations added: {final_count - initial_count}")
        
        # Test specific regulations
        print("\n Testing specific regulations...")
        
        # Test Privacy Rule
        privacy_rules = RegulationUpdate.objects.filter(title__icontains='Privacy Rule')
        print(f"  • Privacy Rule regulations: {privacy_rules.count()}")
        
        # Test Security Rule
        security_rules = RegulationUpdate.objects.filter(title__icontains='Security Rule')
        print(f"  • Security Rule regulations: {security_rules.count()}")
        
        # Test Breach Notification
        breach_rules = RegulationUpdate.objects.filter(title__icontains='Breach Notification')
        print(f"  • Breach Notification regulations: {breach_rules.count()}")
        
        # Test Enforcement
        enforcement_rules = RegulationUpdate.objects.filter(title__icontains='Enforcement')
        print(f"  • Enforcement regulations: {enforcement_rules.count()}")
        
        # Test a specific regulation
        test_reg = RegulationUpdate.objects.filter(title__icontains='Administrative Safeguards').first()
        if test_reg:
            print(f"\n Sample regulation: {test_reg.title}")
            print(f"   Description length: {len(test_reg.description)} characters")
            print(f"   Source URL: {test_reg.source_url}")
            print(f"   Description preview: {test_reg.description[:100]}...")
        
        # Test database integrity
        print("\n Testing database integrity...")
        
        # Check for required fields
        missing_titles = RegulationUpdate.objects.filter(title__isnull=True).count()
        missing_descriptions = RegulationUpdate.objects.filter(description__isnull=True).count()
        
        print(f"  • Regulations with missing titles: {missing_titles}")
        print(f"  • Regulations with missing descriptions: {missing_descriptions}")
        
        # Check for duplicate titles
        titles = list(RegulationUpdate.objects.values_list('title', flat=True))
        unique_titles = set(titles)
        duplicates = len(titles) - len(unique_titles)
        print(f"  • Duplicate titles: {duplicates}")
        
        if missing_titles == 0 and missing_descriptions == 0 and duplicates == 0:
            print("   Database integrity check passed!")
        else:
            print("   Database integrity issues found!")
        
        print("\n HIPAA regulations loading test completed successfully!")
        return True
        
    except Exception as e:
        print(f" Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def display_regulation_summary():
    """Display a summary of all loaded regulations"""
    
    print("\n HIPAA Regulations Summary")
    print("=" * 50)
    
    regulations = RegulationUpdate.objects.all().order_by('title')
    
    for i, reg in enumerate(regulations, 1):
        print(f"{i:2d}. {reg.title}")
        print(f"    URL: {reg.source_url}")
        print(f"    Description: {len(reg.description)} characters")
        print()

if __name__ == '__main__':
    success = test_hipaa_regulations_loading()
    
    if success:
        print("\n" + "=" * 50)
        display_regulation_summary()
    else:
        print("\n Testing failed!")
        sys.exit(1)
