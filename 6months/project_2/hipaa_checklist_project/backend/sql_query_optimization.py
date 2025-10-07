#!/usr/bin/env python3
"""
Week 9 Day 2: SQL Query Optimization
Analyze and optimize SQL queries for better performance

This script:
1. Analyzes current query performance
2. Identifies optimization opportunities
3. Tests optimized queries
4. Provides recommendations
"""

import os
import sys
import django
import time
import json
from datetime import datetime
from django.db import connection, models
from django.db.models import Q, Count, Avg, Max, Min
from django.contrib.auth.models import User

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

from checklist.models import RegulationUpdate, ChecklistItem

class SQLQueryOptimizer:
    def __init__(self):
        self.optimization_results = {
            'timestamp': datetime.now().isoformat(),
            'queries_analyzed': [],
            'optimizations_applied': [],
            'performance_improvements': {},
            'recommendations': []
        }
        
    def analyze_current_queries(self):
        """Analyze current query performance"""
        print(" Analyzing Current Query Performance...")
        
        queries_to_analyze = [
            {
                'name': 'All Checklist Items',
                'query': lambda: ChecklistItem.objects.all(),
                'description': 'Basic select all query'
            },
            {
                'name': 'Items by Regulation',
                'query': lambda: ChecklistItem.objects.select_related('regulation_update').all(),
                'description': 'Query with foreign key join'
            },
            {
                'name': 'High Risk Items',
                'query': lambda: ChecklistItem.objects.filter(
                    Q(likelihood__gte=4) | Q(impact__gte=4)
                ),
                'description': 'Filtered query with OR conditions'
            },
            {
                'name': 'Completion Statistics',
                'query': lambda: ChecklistItem.objects.aggregate(
                    total=Count('id'),
                    completed=Count('id', filter=Q(completion_status=True)),
                    avg_likelihood=Avg('likelihood'),
                    avg_impact=Avg('impact')
                ),
                'description': 'Aggregation query with filters'
            },
            {
                'name': 'Regulation Summary',
                'query': lambda: RegulationUpdate.objects.annotate(
                    item_count=Count('checklistitem'),
                    avg_likelihood=Avg('checklistitem__likelihood'),
                    avg_impact=Avg('checklistitem__impact')
                ).filter(item_count__gt=0),
                'description': 'Complex annotation with filtering'
            },
            {
                'name': 'Recent Items',
                'query': lambda: ChecklistItem.objects.filter(
                    created_at__gte=datetime.now().replace(day=1)
                ).order_by('-created_at'),
                'description': 'Date filtered query with ordering'
            }
        ]
        
        for query_info in queries_to_analyze:
            try:
                start_time = time.time()
                result = query_info['query']()
                
                # Force evaluation if it's a QuerySet
                if hasattr(result, '__iter__') and not isinstance(result, dict):
                    list(result)
                    
                end_time = time.time()
                execution_time = end_time - start_time
                
                self.optimization_results['queries_analyzed'].append({
                    'name': query_info['name'],
                    'description': query_info['description'],
                    'execution_time': execution_time,
                    'status': 'success'
                })
                
                print(f" {query_info['name']}: {execution_time:.4f}s")
                
            except Exception as e:
                self.optimization_results['queries_analyzed'].append({
                    'name': query_info['name'],
                    'description': query_info['description'],
                    'execution_time': None,
                    'status': 'failed',
                    'error': str(e)
                })
                print(f" {query_info['name']}: Failed - {str(e)}")
                
    def test_optimization_techniques(self):
        """Test various optimization techniques"""
        print("\n Testing Optimization Techniques...")
        
        # Test 1: select_related vs prefetch_related
        self.test_related_optimization()
        
        # Test 2: Database indexes
        self.test_index_optimization()
        
        # Test 3: Query optimization
        self.test_query_optimization()
        
        # Test 4: Bulk operations
        self.test_bulk_optimization()
        
    def test_related_optimization(self):
        """Test select_related and prefetch_related optimization"""
        print(" Testing Related Object Optimization...")
        
        # Without optimization
        start_time = time.time()
        items_without_opt = list(ChecklistItem.objects.all())
        for item in items_without_opt:
            _ = item.regulation_update.title
        end_time = time.time()
        without_opt_time = end_time - start_time
        
        # With select_related
        start_time = time.time()
        items_with_opt = list(ChecklistItem.objects.select_related('regulation_update').all())
        for item in items_with_opt:
            _ = item.regulation_update.title
        end_time = time.time()
        with_opt_time = end_time - start_time
        
        improvement = ((without_opt_time - with_opt_time) / without_opt_time) * 100 if without_opt_time > 0 else 0
        
        self.optimization_results['optimizations_applied'].append({
            'technique': 'select_related',
            'before_time': without_opt_time,
            'after_time': with_opt_time,
            'improvement_percent': improvement,
            'description': 'Optimized foreign key access'
        })
        
        print(f"  Without select_related: {without_opt_time:.4f}s")
        print(f"  With select_related: {with_opt_time:.4f}s")
        print(f"  Improvement: {improvement:.1f}%")
        
    def test_index_optimization(self):
        """Test database index effectiveness"""
        print(" Testing Database Index Optimization...")
        
        # Test queries that should benefit from indexes
        index_tests = [
            {
                'name': 'Likelihood Filter',
                'query': lambda: ChecklistItem.objects.filter(likelihood=4),
                'indexed_field': 'likelihood'
            },
            {
                'name': 'Impact Filter',
                'query': lambda: ChecklistItem.objects.filter(impact=5),
                'indexed_field': 'impact'
            },
            {
                'name': 'Completion Status Filter',
                'query': lambda: ChecklistItem.objects.filter(completion_status=True),
                'indexed_field': 'completion_status'
            }
        ]
        
        for test in index_tests:
            try:
                start_time = time.time()
                result = list(test['query']())
                end_time = time.time()
                execution_time = end_time - start_time
                
                self.optimization_results['optimizations_applied'].append({
                    'technique': f'index_on_{test["indexed_field"]}',
                    'execution_time': execution_time,
                    'result_count': len(result),
                    'description': f'Query using {test["indexed_field"]} index'
                })
                
                print(f"  {test['name']}: {execution_time:.4f}s ({len(result)} results)")
                
            except Exception as e:
                print(f"   {test['name']}: Failed - {str(e)}")
                
    def test_query_optimization(self):
        """Test query structure optimization"""
        print(" Testing Query Structure Optimization...")
        
        # Test 1: Avoid N+1 queries
        print("  Testing N+1 Query Prevention...")
        
        # N+1 query (bad)
        start_time = time.time()
        regulations = RegulationUpdate.objects.all()
        for reg in regulations:
            items = reg.checklistitem_set.all()
            _ = len(items)
        end_time = time.time()
        n_plus_1_time = end_time - start_time
        
        # Optimized query (good)
        start_time = time.time()
        regulations_opt = RegulationUpdate.objects.prefetch_related('checklistitem_set').all()
        for reg in regulations_opt:
            items = reg.checklistitem_set.all()
            _ = len(items)
        end_time = time.time()
        optimized_time = end_time - start_time
        
        improvement = ((n_plus_1_time - optimized_time) / n_plus_1_time) * 100 if n_plus_1_time > 0 else 0
        
        self.optimization_results['optimizations_applied'].append({
            'technique': 'prefetch_related',
            'before_time': n_plus_1_time,
            'after_time': optimized_time,
            'improvement_percent': improvement,
            'description': 'Prevented N+1 queries with prefetch_related'
        })
        
        print(f"    N+1 query: {n_plus_1_time:.4f}s")
        print(f"    Optimized: {optimized_time:.4f}s")
        print(f"    Improvement: {improvement:.1f}%")
        
        # Test 2: Query complexity
        print("  Testing Query Complexity...")
        
        # Complex query (potentially slow)
        start_time = time.time()
        complex_result = list(ChecklistItem.objects.filter(
            Q(likelihood__gte=3) & Q(impact__gte=3) & Q(completion_status=False)
        ).select_related('regulation_update').order_by('-likelihood', '-impact'))
        end_time = time.time()
        complex_time = end_time - start_time
        
        # Simplified query (potentially faster)
        start_time = time.time()
        simple_result = list(ChecklistItem.objects.filter(
            likelihood__gte=3,
            impact__gte=3,
            completion_status=False
        ).select_related('regulation_update').order_by('-likelihood', '-impact'))
        end_time = time.time()
        simple_time = end_time - start_time
        
        self.optimization_results['optimizations_applied'].append({
            'technique': 'query_simplification',
            'complex_time': complex_time,
            'simple_time': simple_time,
            'description': 'Simplified query structure'
        })
        
        print(f"    Complex query: {complex_time:.4f}s")
        print(f"    Simple query: {simple_time:.4f}s")
        
    def test_bulk_optimization(self):
        """Test bulk operation optimization"""
        print(" Testing Bulk Operation Optimization...")
        
        # Test bulk create
        print("  Testing Bulk Create...")
        
        # Individual creates (slow)
        start_time = time.time()
        for i in range(5):
            RegulationUpdate.objects.create(
                title=f'Bulk Test {i}',
                description=f'Bulk test description {i}',
                source_url=f'https://bulktest{i}.example.com'
            )
        end_time = time.time()
        individual_time = end_time - start_time
        
        # Bulk create (fast)
        start_time = time.time()
        bulk_objects = []
        for i in range(5, 10):
            bulk_objects.append(RegulationUpdate(
                title=f'Bulk Test {i}',
                description=f'Bulk test description {i}',
                source_url=f'https://bulktest{i}.example.com'
            ))
        RegulationUpdate.objects.bulk_create(bulk_objects)
        end_time = time.time()
        bulk_time = end_time - start_time
        
        improvement = ((individual_time - bulk_time) / individual_time) * 100 if individual_time > 0 else 0
        
        self.optimization_results['optimizations_applied'].append({
            'technique': 'bulk_create',
            'before_time': individual_time,
            'after_time': bulk_time,
            'improvement_percent': improvement,
            'description': 'Used bulk_create instead of individual creates'
        })
        
        print(f"    Individual creates: {individual_time:.4f}s")
        print(f"    Bulk create: {bulk_time:.4f}s")
        print(f"    Improvement: {improvement:.1f}%")
        
        # Clean up test data
        RegulationUpdate.objects.filter(title__startswith='Bulk Test').delete()
        
    def generate_optimization_recommendations(self):
        """Generate optimization recommendations"""
        print("\n Generating Optimization Recommendations...")
        
        recommendations = []
        
        # Analyze performance metrics
        slow_queries = [q for q in self.optimization_results['queries_analyzed'] 
                       if q.get('execution_time', 0) > 0.1]
        
        if slow_queries:
            recommendations.append({
                'priority': 'High',
                'category': 'Query Performance',
                'recommendation': f'Optimize {len(slow_queries)} slow queries (>100ms)',
                'details': [q['name'] for q in slow_queries]
            })
            
        # Analyze optimization results
        significant_improvements = [opt for opt in self.optimization_results['optimizations_applied']
                                  if opt.get('improvement_percent', 0) > 20]
        
        if significant_improvements:
            recommendations.append({
                'priority': 'Medium',
                'category': 'Optimization Techniques',
                'recommendation': 'Apply proven optimization techniques',
                'details': [opt['technique'] for opt in significant_improvements]
            })
            
        # General recommendations
        recommendations.extend([
            {
                'priority': 'Medium',
                'category': 'Database Design',
                'recommendation': 'Ensure all foreign keys have proper indexes',
                'details': ['Add indexes on frequently queried fields', 'Consider composite indexes for complex queries']
            },
            {
                'priority': 'Low',
                'category': 'Query Structure',
                'recommendation': 'Use select_related() and prefetch_related() for related objects',
                'details': ['Prevents N+1 queries', 'Reduces database round trips']
            },
            {
                'priority': 'Low',
                'category': 'Bulk Operations',
                'recommendation': 'Use bulk operations for multiple record operations',
                'details': ['bulk_create() for multiple inserts', 'bulk_update() for multiple updates']
            }
        ])
        
        self.optimization_results['recommendations'] = recommendations
        
        for rec in recommendations:
            print(f"  {rec['priority']} Priority - {rec['category']}: {rec['recommendation']}")
            
    def generate_report(self):
        """Generate optimization report"""
        print("\n Generating Optimization Report...")
        
        # Save detailed report
        with open('sql_optimization_report.json', 'w') as f:
            json.dump(self.optimization_results, f, indent=2, default=str)
            
        # Generate summary
        summary = f"""
 SQL QUERY OPTIMIZATION REPORT
===============================
Generated: {self.optimization_results['timestamp']}

 QUERIES ANALYZED: {len(self.optimization_results['queries_analyzed'])}
"""
        
        for query in self.optimization_results['queries_analyzed']:
            if query['status'] == 'success':
                summary += f"   {query['name']}: {query['execution_time']:.4f}s\n"
            else:
                summary += f"   {query['name']}: FAILED\n"
                
        summary += f"""
 OPTIMIZATIONS APPLIED: {len(self.optimization_results['optimizations_applied'])}
"""
        
        for opt in self.optimization_results['optimizations_applied']:
            if 'improvement_percent' in opt:
                summary += f"  {opt['technique']}: {opt['improvement_percent']:.1f}% improvement\n"
            else:
                summary += f"  {opt['technique']}: Applied\n"
                
        summary += f"""
 RECOMMENDATIONS: {len(self.optimization_results['recommendations'])}
"""
        
        for rec in self.optimization_results['recommendations']:
            summary += f"  {rec['priority']} - {rec['category']}: {rec['recommendation']}\n"
            
        summary += """
 REPORTS GENERATED:
  • sql_optimization_report.json (Detailed results)
  • This summary report
"""
        
        print(summary)
        
        # Save summary
        with open('sql_optimization_summary.txt', 'w') as f:
            f.write(summary)
            
        print(" Optimization report generated!")
        
    def run_optimization_analysis(self):
        """Run complete optimization analysis"""
        print(" Starting SQL Query Optimization Analysis...")
        print("=" * 60)
        
        try:
            self.analyze_current_queries()
            self.test_optimization_techniques()
            self.generate_optimization_recommendations()
            self.generate_report()
            
        except Exception as e:
            print(f" Optimization analysis failed: {str(e)}")
            
        print("\n SQL Query Optimization Analysis Completed!")

if __name__ == '__main__':
    optimizer = SQLQueryOptimizer()
    optimizer.run_optimization_analysis()
