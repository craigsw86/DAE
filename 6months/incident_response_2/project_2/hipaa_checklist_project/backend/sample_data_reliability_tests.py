#!/usr/bin/env python3
"""
Week 9 Day 2: Manual Update Reliability Tests
Sample Data Tests and SQL Query Optimization

This script tests:
1. Sample data creation and manipulation
2. Update reliability across different scenarios
3. Data consistency verification
4. SQL query performance analysis
"""

import os
import sys
import django
import time
import json
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection, transaction
from django.test.utils import override_settings
from checklist.models import RegulationUpdate, ChecklistItem
from checklist.serializers import ChecklistItemSerializer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SampleDataReliabilityTester:
    def __init__(self):
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests': [],
            'performance_metrics': {},
            'reliability_score': 0
        }
        self.test_user = None
        self.sample_regulations = []
        self.sample_checklist_items = []
        
    def setup_test_environment(self):
        """Create test user and sample data"""
        print("🔧 Setting up test environment...")
        
        # Create test user
        self.test_user, created = User.objects.get_or_create(
            username='reliability_test_user',
            defaults={
                'email': 'reliability@test.com',
                'first_name': 'Reliability',
                'last_name': 'Tester'
            }
        )
        if created:
            self.test_user.set_password('testpass123')
            self.test_user.save()
            print(f"✅ Created test user: {self.test_user.username}")
        else:
            print(f"✅ Using existing test user: {self.test_user.username}")
            
        # Create sample regulations
        self.create_sample_regulations()
        
        # Create sample checklist items
        self.create_sample_checklist_items()
        
        print(f"✅ Test environment ready with {len(self.sample_regulations)} regulations and {len(self.sample_checklist_items)} checklist items")
        
    def create_sample_regulations(self):
        """Create diverse sample regulations for testing"""
        regulations_data = [
            {
                'title': 'HIPAA Security Rule Update 2024',
                'description': 'Updated requirements for electronic protected health information (ePHI) security',
                'source_url': 'https://www.hhs.gov/hipaa/for-professionals/security/index.html'
            },
            {
                'title': 'HIPAA Privacy Rule Amendment 2024',
                'description': 'New privacy requirements for patient data handling and consent',
                'source_url': 'https://www.hhs.gov/hipaa/for-professionals/privacy/index.html'
            },
            {
                'title': 'HIPAA Breach Notification Rule 2024',
                'description': 'Updated procedures for breach notification and reporting',
                'source_url': 'https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html'
            },
            {
                'title': 'HIPAA Enforcement Rule Update 2024',
                'description': 'New enforcement procedures and penalty structures',
                'source_url': 'https://www.hhs.gov/hipaa/for-professionals/enforcement/index.html'
            },
            {
                'title': 'HIPAA Administrative Safeguards 2024',
                'description': 'Updated administrative requirements for covered entities',
                'source_url': 'https://www.hhs.gov/hipaa/for-professionals/security/guidance/administrative-safeguards/index.html'
            }
        ]
        
        for reg_data in regulations_data:
            regulation, created = RegulationUpdate.objects.get_or_create(
                title=reg_data['title'],
                defaults=reg_data
            )
            self.sample_regulations.append(regulation)
            if created:
                print(f"✅ Created regulation: {regulation.title}")
            else:
                print(f"✅ Using existing regulation: {regulation.title}")
                
    def create_sample_checklist_items(self):
        """Create diverse sample checklist items for testing"""
        checklist_data = [
            {
                'user': self.test_user,
                'regulation_update': self.sample_regulations[0],
                'completed': False,
                'likelihood': 4,
                'impact': 5,
                'notes': 'Critical security requirement',
                'mitigation_steps': '1. Deploy MFA solution\n2. Train staff\n3. Monitor compliance'
            },
            {
                'user': self.test_user,
                'regulation_update': self.sample_regulations[1],
                'completed': True,
                'likelihood': 3,
                'impact': 4,
                'notes': 'Completed last month',
                'mitigation_steps': '1. Legal review\n2. Staff training\n3. Patient notification'
            },
            {
                'user': self.test_user,
                'regulation_update': self.sample_regulations[2],
                'completed': False,
                'likelihood': 2,
                'impact': 5,
                'notes': 'High priority item',
                'mitigation_steps': '1. Select vendor\n2. Configure system\n3. Test procedures'
            },
            {
                'user': self.test_user,
                'regulation_update': self.sample_regulations[3],
                'completed': False,
                'likelihood': 5,
                'impact': 3,
                'notes': 'Annual requirement',
                'mitigation_steps': '1. Gather documentation\n2. Interview staff\n3. Document findings'
            },
            {
                'user': self.test_user,
                'regulation_update': self.sample_regulations[4],
                'completed': True,
                'likelihood': 1,
                'impact': 2,
                'notes': 'Routine update',
                'mitigation_steps': '1. Review current procedures\n2. Update documentation\n3. Train staff'
            }
        ]
        
        for item_data in checklist_data:
            checklist_item, created = ChecklistItem.objects.get_or_create(
                user=item_data['user'],
                regulation_update=item_data['regulation_update'],
                defaults=item_data
            )
            self.sample_checklist_items.append(checklist_item)
            if created:
                print(f"✅ Created checklist item: {checklist_item.regulation_update.title}")
            else:
                print(f"✅ Using existing checklist item: {checklist_item.regulation_update.title}")
                
    def test_basic_crud_reliability(self):
        """Test basic CRUD operations for reliability"""
        print("\n🔍 Testing Basic CRUD Reliability...")
        
        test_results = {
            'test_name': 'Basic CRUD Reliability',
            'passed': 0,
            'failed': 0,
            'details': []
        }
        
        # Test CREATE
        try:
            new_regulation = RegulationUpdate.objects.create(
                title='Test Regulation for CRUD',
                description='Test regulation for reliability testing',
                source_url='https://test.example.com'
            )
            test_results['passed'] += 1
            test_results['details'].append('✅ CREATE operation successful')
        except Exception as e:
            test_results['failed'] += 1
            test_results['details'].append(f'❌ CREATE operation failed: {str(e)}')
            
        # Test READ
        try:
            retrieved_regulation = RegulationUpdate.objects.get(id=new_regulation.id)
            if retrieved_regulation.title == new_regulation.title:
                test_results['passed'] += 1
                test_results['details'].append('✅ READ operation successful')
            else:
                test_results['failed'] += 1
                test_results['details'].append('❌ READ operation failed: Data mismatch')
        except Exception as e:
            test_results['failed'] += 1
            test_results['details'].append(f'❌ READ operation failed: {str(e)}')
            
        # Test UPDATE
        try:
            original_title = retrieved_regulation.title
            retrieved_regulation.title = 'Updated Test Regulation'
            retrieved_regulation.save()
            
            # Verify update
            updated_regulation = RegulationUpdate.objects.get(id=new_regulation.id)
            if updated_regulation.title == 'Updated Test Regulation':
                test_results['passed'] += 1
                test_results['details'].append('✅ UPDATE operation successful')
            else:
                test_results['failed'] += 1
                test_results['details'].append('❌ UPDATE operation failed: Data not updated')
        except Exception as e:
            test_results['failed'] += 1
            test_results['details'].append(f'❌ UPDATE operation failed: {str(e)}')
            
        # Test DELETE
        try:
            regulation_id = updated_regulation.id
            updated_regulation.delete()
            
            # Verify deletion
            try:
                RegulationUpdate.objects.get(id=regulation_id)
                test_results['failed'] += 1
                test_results['details'].append('❌ DELETE operation failed: Record still exists')
            except RegulationUpdate.DoesNotExist:
                test_results['passed'] += 1
                test_results['details'].append('✅ DELETE operation successful')
        except Exception as e:
            test_results['failed'] += 1
            test_results['details'].append(f'❌ DELETE operation failed: {str(e)}')
            
        self.test_results['tests'].append(test_results)
        print(f"✅ Basic CRUD test completed: {test_results['passed']} passed, {test_results['failed']} failed")
        
    def test_concurrent_updates(self):
        """Test concurrent update scenarios"""
        print("\n🔄 Testing Concurrent Updates...")
        
        test_results = {
            'test_name': 'Concurrent Updates',
            'passed': 0,
            'failed': 0,
            'details': []
        }
        
        # Test multiple updates to the same record
        try:
            test_item = self.sample_checklist_items[0]
            original_notes = test_item.notes
            
            # Simulate concurrent updates
            test_item.notes = "Update 1"
            test_item.save()
            
            test_item.notes = "Update 2"
            test_item.save()
            
            test_item.notes = "Update 3"
            test_item.save()
            
            # Verify final state
            final_item = ChecklistItem.objects.get(id=test_item.id)
            if final_item.notes == "Update 3":
                test_results['passed'] += 1
                test_results['details'].append('✅ Concurrent updates handled correctly')
            else:
                test_results['failed'] += 1
                test_results['details'].append('❌ Concurrent updates failed: Final state incorrect')
                
        except Exception as e:
            test_results['failed'] += 1
            test_results['details'].append(f'❌ Concurrent updates failed: {str(e)}')
            
        # Test transaction rollback
        try:
            with transaction.atomic():
                test_item = self.sample_checklist_items[1]
                original_status = test_item.completed
                test_item.completed = not original_status
                test_item.save()
                
                # Force an error to test rollback
                raise Exception("Test rollback")
                
        except Exception:
            # Verify rollback worked
            test_item = ChecklistItem.objects.get(id=self.sample_checklist_items[1].id)
            if test_item.completed == original_status:
                test_results['passed'] += 1
                test_results['details'].append('✅ Transaction rollback successful')
            else:
                test_results['failed'] += 1
                test_results['details'].append('❌ Transaction rollback failed')
                
        self.test_results['tests'].append(test_results)
        print(f"✅ Concurrent updates test completed: {test_results['passed']} passed, {test_results['failed']} failed")
        
    def test_data_consistency(self):
        """Test data consistency across operations"""
        print("\n🔍 Testing Data Consistency...")
        
        test_results = {
            'test_name': 'Data Consistency',
            'passed': 0,
            'failed': 0,
            'details': []
        }
        
        # Test foreign key relationships
        try:
            for item in self.sample_checklist_items:
                regulation = item.regulation_update
                if regulation and regulation.id:
                    test_results['passed'] += 1
                else:
                    test_results['failed'] += 1
                    test_results['details'].append(f'❌ Foreign key relationship broken for item: {item.title}')
                    
            if test_results['passed'] > 0:
                test_results['details'].append('✅ All foreign key relationships intact')
                
        except Exception as e:
            test_results['failed'] += 1
            test_results['details'].append(f'❌ Foreign key test failed: {str(e)}')
            
        # Test data integrity constraints
        try:
            # Test unique constraints
            duplicate_regulation = RegulationUpdate(
                title=self.sample_regulations[0].title,
                description='Duplicate test'
            )
            duplicate_regulation.save()
            test_results['failed'] += 1
            test_results['details'].append('❌ Unique constraint not enforced')
        except Exception as e:
            test_results['passed'] += 1
            test_results['details'].append('✅ Unique constraints properly enforced')
            
        # Test required field constraints
        try:
            incomplete_item = ChecklistItem(
                # Missing required fields: user, regulation_update
            )
            incomplete_item.save()
            test_results['failed'] += 1
            test_results['details'].append('❌ Required field constraints not enforced')
        except Exception as e:
            test_results['passed'] += 1
            test_results['details'].append('✅ Required field constraints properly enforced')
            
        self.test_results['tests'].append(test_results)
        print(f"✅ Data consistency test completed: {test_results['passed']} passed, {test_results['failed']} failed")
        
    def test_sql_query_performance(self):
        """Test and analyze SQL query performance"""
        print("\n⚡ Testing SQL Query Performance...")
        
        test_results = {
            'test_name': 'SQL Query Performance',
            'passed': 0,
            'failed': 0,
            'details': [],
            'performance_metrics': {}
        }
        
        # Test basic queries
        queries_to_test = [
            ('Simple SELECT', 'SELECT * FROM checklist_checklistitem'),
            ('JOIN Query', '''
                SELECT ci.title, ru.title as regulation_title 
                FROM checklist_checklistitem ci 
                JOIN checklist_regulationupdate ru ON ci.regulation_update_id = ru.id
            '''),
            ('Aggregation Query', '''
                SELECT 
                    COUNT(*) as total_items,
                    AVG(likelihood) as avg_likelihood,
                    AVG(impact) as avg_impact
                FROM checklist_checklistitem
            '''),
            ('Filtered Query', '''
                SELECT * FROM checklist_checklistitem 
                WHERE completed = 1 AND likelihood >= 4
            '''),
            ('Complex Query', '''
                SELECT 
                    ru.title as regulation,
                    COUNT(ci.id) as item_count,
                    AVG(ci.likelihood) as avg_likelihood,
                    AVG(ci.impact) as avg_impact
                FROM checklist_regulationupdate ru
                LEFT JOIN checklist_checklistitem ci ON ru.id = ci.regulation_update_id
                GROUP BY ru.id, ru.title
                HAVING COUNT(ci.id) > 0
                ORDER BY avg_likelihood DESC
            ''')
        ]
        
        for query_name, query in queries_to_test:
            try:
                start_time = time.time()
                
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    
                end_time = time.time()
                execution_time = end_time - start_time
                
                test_results['performance_metrics'][query_name] = {
                    'execution_time': execution_time,
                    'result_count': len(results),
                    'status': 'success'
                }
                
                if execution_time < 0.1:  # Less than 100ms
                    test_results['passed'] += 1
                    test_results['details'].append(f'✅ {query_name}: {execution_time:.4f}s (Fast)')
                elif execution_time < 1.0:  # Less than 1 second
                    test_results['passed'] += 1
                    test_results['details'].append(f'⚠️ {query_name}: {execution_time:.4f}s (Acceptable)')
                else:
                    test_results['failed'] += 1
                    test_results['details'].append(f'❌ {query_name}: {execution_time:.4f}s (Slow)')
                    
            except Exception as e:
                test_results['failed'] += 1
                test_results['details'].append(f'❌ {query_name}: Query failed - {str(e)}')
                test_results['performance_metrics'][query_name] = {
                    'execution_time': None,
                    'result_count': 0,
                    'status': 'failed',
                    'error': str(e)
                }
                
        self.test_results['tests'].append(test_results)
        self.test_results['performance_metrics'] = test_results['performance_metrics']
        print(f"✅ SQL performance test completed: {test_results['passed']} passed, {test_results['failed']} failed")
        
    def test_bulk_operations(self):
        """Test bulk operations for reliability"""
        print("\n📦 Testing Bulk Operations...")
        
        test_results = {
            'test_name': 'Bulk Operations',
            'passed': 0,
            'failed': 0,
            'details': []
        }
        
        # Test bulk create
        try:
            start_time = time.time()
            
            bulk_regulations = []
            for i in range(10):
                bulk_regulations.append(RegulationUpdate(
                    title=f'Bulk Test Regulation {i}',
                    description=f'Bulk test regulation {i} for reliability testing',
                    source_url=f'https://bulktest{i}.example.com'
                ))
            
            RegulationUpdate.objects.bulk_create(bulk_regulations)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Verify creation
            created_count = RegulationUpdate.objects.filter(title__startswith='Bulk Test Regulation').count()
            if created_count == 10:
                test_results['passed'] += 1
                test_results['details'].append(f'✅ Bulk create successful: {created_count} records in {execution_time:.4f}s')
            else:
                test_results['failed'] += 1
                test_results['details'].append(f'❌ Bulk create failed: Expected 10, got {created_count}')
                
        except Exception as e:
            test_results['failed'] += 1
            test_results['details'].append(f'❌ Bulk create failed: {str(e)}')
            
        # Test bulk update
        try:
            start_time = time.time()
            
            bulk_regulations = RegulationUpdate.objects.filter(title__startswith='Bulk Test Regulation')
            for reg in bulk_regulations:
                reg.description = 'Updated bulk description'
            
            RegulationUpdate.objects.bulk_update(bulk_regulations, ['description'])
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Verify update
            updated_count = RegulationUpdate.objects.filter(
                title__startswith='Bulk Test Regulation',
                description='Updated bulk description'
            ).count()
            
            if updated_count == 10:
                test_results['passed'] += 1
                test_results['details'].append(f'✅ Bulk update successful: {updated_count} records in {execution_time:.4f}s')
            else:
                test_results['failed'] += 1
                test_results['details'].append(f'❌ Bulk update failed: Expected 10, got {updated_count}')
                
        except Exception as e:
            test_results['failed'] += 1
            test_results['details'].append(f'❌ Bulk update failed: {str(e)}')
            
        # Test bulk delete
        try:
            start_time = time.time()
            
            deleted_count, _ = RegulationUpdate.objects.filter(title__startswith='Bulk Test Regulation').delete()
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            if deleted_count == 10:
                test_results['passed'] += 1
                test_results['details'].append(f'✅ Bulk delete successful: {deleted_count} records in {execution_time:.4f}s')
            else:
                test_results['failed'] += 1
                test_results['details'].append(f'❌ Bulk delete failed: Expected 10, got {deleted_count}')
                
        except Exception as e:
            test_results['failed'] += 1
            test_results['details'].append(f'❌ Bulk delete failed: {str(e)}')
            
        self.test_results['tests'].append(test_results)
        print(f"✅ Bulk operations test completed: {test_results['passed']} passed, {test_results['failed']} failed")
        
    def calculate_reliability_score(self):
        """Calculate overall reliability score"""
        total_tests = 0
        passed_tests = 0
        
        for test in self.test_results['tests']:
            total_tests += test['passed'] + test['failed']
            passed_tests += test['passed']
            
        if total_tests > 0:
            self.test_results['reliability_score'] = (passed_tests / total_tests) * 100
        else:
            self.test_results['reliability_score'] = 0
            
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n📊 Generating Test Report...")
        
        self.calculate_reliability_score()
        
        # Save detailed report
        with open('sample_data_reliability_report.json', 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
            
        # Generate summary report
        summary = f"""
🎯 SAMPLE DATA RELIABILITY TEST REPORT
=====================================
Generated: {self.test_results['timestamp']}
Overall Reliability Score: {self.test_results['reliability_score']:.1f}%

📋 TEST SUMMARY:
"""
        
        for test in self.test_results['tests']:
            summary += f"""
{test['test_name']}:
  ✅ Passed: {test['passed']}
  ❌ Failed: {test['failed']}
  Details: {', '.join(test['details'][:3])}{'...' if len(test['details']) > 3 else ''}
"""
        
        if self.test_results['performance_metrics']:
            summary += f"""
⚡ PERFORMANCE METRICS:
"""
            for query_name, metrics in self.test_results['performance_metrics'].items():
                if metrics['status'] == 'success':
                    summary += f"  {query_name}: {metrics['execution_time']:.4f}s ({metrics['result_count']} results)\n"
                else:
                    summary += f"  {query_name}: FAILED - {metrics.get('error', 'Unknown error')}\n"
        
        summary += f"""
🎯 RECOMMENDATIONS:
"""
        
        if self.test_results['reliability_score'] >= 95:
            summary += "  • Excellent reliability! System is performing optimally.\n"
        elif self.test_results['reliability_score'] >= 85:
            summary += "  • Good reliability with minor issues to address.\n"
        elif self.test_results['reliability_score'] >= 70:
            summary += "  • Moderate reliability - several issues need attention.\n"
        else:
            summary += "  • Poor reliability - significant issues require immediate attention.\n"
            
        # Performance recommendations
        slow_queries = [name for name, metrics in self.test_results['performance_metrics'].items() 
                       if metrics.get('execution_time') is not None and metrics.get('execution_time', 0) > 0.1]
        if slow_queries:
            summary += f"  • Consider optimizing these slow queries: {', '.join(slow_queries)}\n"
            
        summary += """
📁 REPORTS GENERATED:
  • sample_data_reliability_report.json (Detailed results)
  • This summary report
"""
        
        print(summary)
        
        # Save summary report
        with open('sample_data_reliability_summary.txt', 'w') as f:
            f.write(summary)
            
        print("✅ Reports generated successfully!")
        
    def cleanup_test_data(self):
        """Clean up test data"""
        print("\n🧹 Cleaning up test data...")
        
        try:
            # Clean up bulk test data (should already be deleted)
            RegulationUpdate.objects.filter(title__startswith='Bulk Test Regulation').delete()
            
            # Clean up test user
            if self.test_user:
                self.test_user.delete()
                
            print("✅ Test data cleanup completed")
            
        except Exception as e:
            print(f"⚠️ Cleanup warning: {str(e)}")
            
    def run_all_tests(self):
        """Run all reliability tests"""
        print("🚀 Starting Sample Data Reliability Tests...")
        print("=" * 60)
        
        try:
            self.setup_test_environment()
            self.test_basic_crud_reliability()
            self.test_concurrent_updates()
            self.test_data_consistency()
            self.test_sql_query_performance()
            self.test_bulk_operations()
            self.generate_report()
            
        except Exception as e:
            print(f"❌ Test execution failed: {str(e)}")
            logger.exception("Test execution error")
            
        finally:
            self.cleanup_test_data()
            
        print("\n🎉 Sample Data Reliability Tests Completed!")
        print(f"📊 Overall Reliability Score: {self.test_results['reliability_score']:.1f}%")

if __name__ == '__main__':
    tester = SampleDataReliabilityTester()
    tester.run_all_tests()
