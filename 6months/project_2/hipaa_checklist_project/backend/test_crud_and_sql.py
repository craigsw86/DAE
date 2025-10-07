#!/usr/bin/env python
"""
Week 9: API CRUD and SQL Verification Test Script
This script tests all CRUD operations and SQL queries in the Django backend.
"""

import os
import sys
import django
from django.db import connection
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

from checklist.models import RegulationUpdate, ChecklistItem
from checklist.serializers import RegulationUpdateSerializer, ChecklistItemSerializer

class CRUDAndSQLVerificationTest:
    """Comprehensive test class for CRUD operations and SQL verification"""
    
    def __init__(self):
        self.client = APIClient()
        self.test_user = None
        self.test_regulation = None
        self.test_checklist_item = None
        
    def setup_test_data(self):
        """Create test data for testing"""
        print(" Setting up test data...")
        
        # Create test user
        self.test_user, created = User.objects.get_or_create(
            username='testuser_crud',
            defaults={
                'email': 'test@example.com',
                'password': 'testpass123'
            }
        )
        if created:
            self.test_user.set_password('testpass123')
            self.test_user.save()
            print(f" Created test user: {self.test_user.username}")
        else:
            print(f" Using existing test user: {self.test_user.username}")
        
        # Create test regulation
        self.test_regulation, created = RegulationUpdate.objects.get_or_create(
            title='Test HIPAA Regulation',
            defaults={
                'description': 'Test regulation for CRUD testing',
                'source_url': 'https://example.com/test'
            }
        )
        if created:
            print(f" Created test regulation: {self.test_regulation.title}")
        else:
            print(f" Using existing test regulation: {self.test_regulation.title}")
        
        # Create test checklist item
        self.test_checklist_item, created = ChecklistItem.objects.get_or_create(
            user=self.test_user,
            regulation_update=self.test_regulation,
            defaults={
                'completed': False,
                'notes': 'Initial test notes',
                'likelihood': 3,
                'impact': 4
            }
        )
        if created:
            print(f" Created test checklist item")
        else:
            print(f" Using existing test checklist item")
        
        print(" Test data setup complete!\n")
    
    def test_sql_queries(self):
        """Test various SQL queries and verify database operations"""
        print(" Testing SQL Queries and Database Operations...")
        
        # Test 1: Basic SELECT queries
        print("\n Test 1: Basic SELECT Queries")
        with connection.cursor() as cursor:
            # Test user query
            cursor.execute("SELECT id, username, email FROM auth_user WHERE username = %s", [self.test_user.username])
            user_result = cursor.fetchone()
            if user_result:
                print(f" User query successful: {user_result[1]} ({user_result[2]})")
            else:
                print(" User query failed")
            
            # Test regulation query
            cursor.execute("SELECT id, title, description FROM checklist_regulationupdate WHERE title = %s", [self.test_regulation.title])
            reg_result = cursor.fetchone()
            if reg_result:
                print(f" Regulation query successful: {reg_result[1]}")
            else:
                print(" Regulation query failed")
            
            # Test checklist item query with JOIN
            cursor.execute("""
                SELECT ci.id, ci.completed, ci.notes, ru.title 
                FROM checklist_checklistitem ci 
                JOIN checklist_regulationupdate ru ON ci.regulation_update_id = ru.id 
                WHERE ci.user_id = %s
            """, [self.test_user.id])
            items = cursor.fetchall()
            print(f" Checklist items query successful: Found {len(items)} items")
        
        # Test 2: Complex queries with filtering
        print("\n Test 2: Complex Queries with Filtering")
        with connection.cursor() as cursor:
            # Test risk assessment query
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_items,
                    SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed_items,
                    AVG(likelihood) as avg_likelihood,
                    AVG(impact) as avg_impact
                FROM checklist_checklistitem 
                WHERE user_id = %s
            """, [self.test_user.id])
            risk_stats = cursor.fetchone()
            if risk_stats:
                print(f" Risk assessment query successful:")
                print(f"   Total items: {risk_stats[0]}")
                print(f"   Completed: {risk_stats[1]}")
                print(f"   Avg likelihood: {risk_stats[2]:.2f}")
                print(f"   Avg impact: {risk_stats[3]:.2f}")
            else:
                print(" Risk assessment query failed")
        
        # Test 3: Index verification
        print("\n Test 3: Index Verification")
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA index_list(checklist_checklistitem)")
            indexes = cursor.fetchall()
            print(f" Found {len(indexes)} indexes on checklist_checklistitem table")
            
            # Check specific indexes
            expected_indexes = ['user_id', 'regulation_update_id', 'completed', 'last_updated', 'likelihood', 'impact']
            for index in indexes:
                if any(expected in index[1] for expected in expected_indexes):
                    print(f"    Index found: {index[1]}")
        
        print(" SQL query testing complete!\n")
    
    def test_crud_operations(self):
        """Test all CRUD operations through the API"""
        print(" Testing CRUD Operations...")
        
        # Authenticate the client
        self.client.force_authenticate(user=self.test_user)
        
        # Test 1: CREATE operations
        print("\n Test 1: CREATE Operations")
        
        # Create new regulation
        new_reg_data = {
            'title': 'New Test Regulation',
            'description': 'This is a new test regulation for CRUD testing',
            'source_url': 'https://example.com/new-test'
        }
        response = self.client.post('/api/regulations/', new_reg_data, format='json')
        if response.status_code == status.HTTP_201_CREATED:
            new_reg_id = response.data['id']
            print(f" Regulation CREATE successful: ID {new_reg_id}")
        else:
            print(f" Regulation CREATE failed: {response.status_code} - {response.data}")
            new_reg_id = None
        
        # Create new checklist item
        new_item_data = {
            'regulation_update': self.test_regulation.id,
            'completed': False,
            'notes': 'New test checklist item',
            'likelihood': 2,
            'impact': 3,
            'mitigation_steps': 'Test mitigation steps'
        }
        response = self.client.post('/api/checklist/', new_item_data, format='json')
        if response.status_code == status.HTTP_201_CREATED:
            new_item_id = response.data['id']
            print(f" Checklist item CREATE successful: ID {new_item_id}")
        else:
            print(f" Checklist item CREATE failed: {response.status_code} - {response.data}")
            new_item_id = None
        
        # Test 2: READ operations
        print("\n Test 2: READ Operations")
        
        # Read regulations
        response = self.client.get('/api/regulations/')
        if response.status_code == status.HTTP_200_OK:
            print(f" Regulations READ successful: Found {len(response.data)} regulations")
        else:
            print(f" Regulations READ failed: {response.status_code}")
        
        # Read checklist items
        response = self.client.get('/api/checklist/')
        if response.status_code == status.HTTP_200_OK:
            print(f" Checklist items READ successful: Found {len(response.data)} items")
        else:
            print(f" Checklist items READ failed: {response.status_code}")
        
        # Read specific item
        if new_item_id:
            response = self.client.get(f'/api/checklist/{new_item_id}/')
            if response.status_code == status.HTTP_200_OK:
                print(f" Specific item READ successful: {response.data['notes']}")
            else:
                print(f" Specific item READ failed: {response.status_code}")
        
        # Test 3: UPDATE operations
        print("\n Test 3: UPDATE Operations")
        
        # Update checklist item
        if new_item_id:
            update_data = {
                'completed': True,
                'notes': 'Updated test notes',
                'likelihood': 4,
                'impact': 5
            }
            response = self.client.patch(f'/api/checklist/{new_item_id}/', update_data, format='json')
            if response.status_code == status.HTTP_200_OK:
                print(f" Checklist item UPDATE successful: {response.data['notes']}")
            else:
                print(f" Checklist item UPDATE failed: {response.status_code}")
        
        # Update regulation
        if new_reg_id:
            update_data = {
                'description': 'Updated test regulation description'
            }
            response = self.client.patch(f'/api/regulations/{new_reg_id}/', update_data, format='json')
            if response.status_code == status.HTTP_200_OK:
                print(f" Regulation UPDATE successful: {response.data['description']}")
            else:
                print(f" Regulation UPDATE failed: {response.status_code}")
        
        # Test 4: DELETE operations
        print("\n Test 4: DELETE Operations")
        
        # Delete checklist item
        if new_item_id:
            response = self.client.delete(f'/api/checklist/{new_item_id}/')
            if response.status_code == status.HTTP_204_NO_CONTENT:
                print(f" Checklist item DELETE successful")
            else:
                print(f" Checklist item DELETE failed: {response.status_code}")
        
        # Delete regulation
        if new_reg_id:
            response = self.client.delete(f'/api/regulations/{new_reg_id}/')
            if response.status_code == status.HTTP_204_NO_CONTENT:
                print(f" Regulation DELETE successful")
            else:
                print(f" Regulation DELETE failed: {response.status_code}")
        
        print(" CRUD operations testing complete!\n")
    
    def test_additional_api_endpoints(self):
        """Test additional API endpoints"""
        print(" Testing Additional API Endpoints...")
        
        self.client.force_authenticate(user=self.test_user)
        
        # Test compliance report
        print("\n Testing Compliance Report Endpoint")
        response = self.client.get('/api/report/')
        if response.status_code == status.HTTP_200_OK:
            data = response.data
            print(f" Compliance report successful:")
            print(f"   User: {data['user']}")
            print(f"   Total items: {data['total_items']}")
            print(f"   Completion: {data['completion_percentage']}%")
        else:
            print(f" Compliance report failed: {response.status_code}")
        
        # Test user profile
        print("\n Testing User Profile Endpoint")
        response = self.client.get('/api/profile/')
        if response.status_code == status.HTTP_200_OK:
            data = response.data
            print(f" User profile successful: {data['username']} ({data['email']})")
        else:
            print(f" User profile failed: {response.status_code}")
        
        # Test trends report
        print("\n Testing Trends Report Endpoint")
        response = self.client.get('/api/report/trends/')
        if response.status_code == status.HTTP_200_OK:
            print(f" Trends report successful: Found {len(response.data)} trend entries")
        else:
            print(f" Trends report failed: {response.status_code}")
        
        # Test audit log
        print("\n Testing Audit Log Endpoint")
        response = self.client.get(f'/api/auditlog/checklistitem/{self.test_checklist_item.id}/')
        if response.status_code == status.HTTP_200_OK:
            print(f" Audit log successful: Found {len(response.data)} log entries")
        else:
            print(f" Audit log failed: {response.status_code}")
        
        print(" Additional API endpoints testing complete!\n")
    
    def test_sql_performance(self):
        """Test SQL performance with various query patterns"""
        print(" Testing SQL Performance...")
        
        # Test query execution time
        import time
        
        with connection.cursor() as cursor:
            # Test 1: Simple query performance
            start_time = time.time()
            cursor.execute("SELECT COUNT(*) FROM checklist_checklistitem WHERE user_id = %s", [self.test_user.id])
            result = cursor.fetchone()
            simple_query_time = time.time() - start_time
            print(f" Simple query: {simple_query_time:.4f}s - Count: {result[0]}")
            
            # Test 2: Complex JOIN query performance
            start_time = time.time()
            cursor.execute("""
                SELECT ci.id, ci.completed, ci.notes, ru.title, u.username
                FROM checklist_checklistitem ci 
                JOIN checklist_regulationupdate ru ON ci.regulation_update_id = ru.id 
                JOIN auth_user u ON ci.user_id = u.id
                WHERE ci.user_id = %s
                ORDER BY ci.last_updated DESC
            """, [self.test_user.id])
            results = cursor.fetchall()
            complex_query_time = time.time() - start_time
            print(f" Complex JOIN query: {complex_query_time:.4f}s - Results: {len(results)}")
            
            # Test 3: Aggregation query performance
            start_time = time.time()
            cursor.execute("""
                SELECT 
                    completed,
                    COUNT(*) as count,
                    AVG(likelihood) as avg_likelihood,
                    AVG(impact) as avg_impact
                FROM checklist_checklistitem 
                WHERE user_id = %s
                GROUP BY completed
            """, [self.test_user.id])
            results = cursor.fetchall()
            agg_query_time = time.time() - start_time
            print(f" Aggregation query: {agg_query_time:.4f}s - Groups: {len(results)}")
        
        # Performance recommendations
        print("\n Performance Analysis:")
        if simple_query_time > 0.1:
            print("  Simple query is slow - consider adding indexes")
        else:
            print(" Simple query performance is good")
        
        if complex_query_time > 0.2:
            print("  Complex query is slow - consider query optimization")
        else:
            print(" Complex query performance is good")
        
        if agg_query_time > 0.15:
            print("  Aggregation query is slow - consider materialized views")
        else:
            print(" Aggregation query performance is good")
        
        print(" SQL performance testing complete!\n")
    
    def cleanup_test_data(self):
        """Clean up test data"""
        print(" Cleaning up test data...")
        
        # Remove test checklist items
        ChecklistItem.objects.filter(user=self.test_user).delete()
        print(" Removed test checklist items")
        
        # Remove test regulations
        RegulationUpdate.objects.filter(title__startswith='Test').delete()
        print(" Removed test regulations")
        
        # Remove test user
        self.test_user.delete()
        print(" Removed test user")
        
        print(" Cleanup complete!\n")
    
    def run_all_tests(self):
        """Run all tests"""
        print(" Starting Week 9: API CRUD and SQL Verification Tests")
        print("=" * 60)
        
        try:
            self.setup_test_data()
            self.test_sql_queries()
            self.test_crud_operations()
            self.test_additional_api_endpoints()
            self.test_sql_performance()
            
            print(" All tests completed successfully!")
            print("=" * 60)
            
        except Exception as e:
            print(f" Test failed with error: {str(e)}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.cleanup_test_data()

if __name__ == "__main__":
    # Run the tests
    tester = CRUDAndSQLVerificationTest()
    tester.run_all_tests()
