#!/usr/bin/env python3
"""
Simple SQL Query Optimization Test
Tests basic query performance and optimization techniques
"""

import os
import sys
import django
import time
import json
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hipaa_checklist.settings')
django.setup()

from django.db import connection
from checklist.models import RegulationUpdate, ChecklistItem
from django.contrib.auth.models import User

def test_query_performance():
    """Test basic query performance"""
    print("⚡ Testing SQL Query Performance...")
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'queries': [],
        'optimizations': []
    }
    
    # Test 1: Basic queries
    queries = [
        ('All Regulations', lambda: list(RegulationUpdate.objects.all())),
        ('All Checklist Items', lambda: list(ChecklistItem.objects.all())),
        ('Items with Relations', lambda: list(ChecklistItem.objects.select_related('regulation_update', 'user').all())),
        ('High Risk Items', lambda: list(ChecklistItem.objects.filter(likelihood__gte=4, impact__gte=4))),
        ('Completed Items', lambda: list(ChecklistItem.objects.filter(completed=True))),
        ('Items by User', lambda: list(ChecklistItem.objects.filter(user__username='TestUsername'))),
    ]
    
    for name, query_func in queries:
        try:
            start_time = time.time()
            result = query_func()
            end_time = time.time()
            execution_time = end_time - start_time
            
            results['queries'].append({
                'name': name,
                'execution_time': execution_time,
                'result_count': len(result),
                'status': 'success'
            })
            
            print(f"  ✅ {name}: {execution_time:.4f}s ({len(result)} results)")
            
        except Exception as e:
            results['queries'].append({
                'name': name,
                'execution_time': None,
                'result_count': 0,
                'status': 'failed',
                'error': str(e)
            })
            print(f"  ❌ {name}: Failed - {str(e)}")
    
    # Test 2: Optimization techniques
    print("\n🔧 Testing Optimization Techniques...")
    
    # Test select_related optimization
    try:
        # Without optimization
        start_time = time.time()
        items_without_opt = list(ChecklistItem.objects.all())
        for item in items_without_opt:
            _ = item.regulation_update.title
        end_time = time.time()
        without_opt_time = end_time - start_time
        
        # With optimization
        start_time = time.time()
        items_with_opt = list(ChecklistItem.objects.select_related('regulation_update').all())
        for item in items_with_opt:
            _ = item.regulation_update.title
        end_time = time.time()
        with_opt_time = end_time - start_time
        
        improvement = ((without_opt_time - with_opt_time) / without_opt_time) * 100 if without_opt_time > 0 else 0
        
        results['optimizations'].append({
            'technique': 'select_related',
            'before_time': without_opt_time,
            'after_time': with_opt_time,
            'improvement_percent': improvement
        })
        
        print(f"  Without select_related: {without_opt_time:.4f}s")
        print(f"  With select_related: {with_opt_time:.4f}s")
        print(f"  Improvement: {improvement:.1f}%")
        
    except Exception as e:
        print(f"  ❌ select_related test failed: {str(e)}")
    
    # Test 3: Index effectiveness
    print("\n📊 Testing Index Effectiveness...")
    
    index_tests = [
        ('Likelihood Filter', lambda: list(ChecklistItem.objects.filter(likelihood=4))),
        ('Impact Filter', lambda: list(ChecklistItem.objects.filter(impact=5))),
        ('Completion Filter', lambda: list(ChecklistItem.objects.filter(completed=True))),
    ]
    
    for name, query_func in index_tests:
        try:
            start_time = time.time()
            result = query_func()
            end_time = time.time()
            execution_time = end_time - start_time
            
            results['optimizations'].append({
                'technique': f'index_test_{name.lower().replace(" ", "_")}',
                'execution_time': execution_time,
                'result_count': len(result)
            })
            
            print(f"  {name}: {execution_time:.4f}s ({len(result)} results)")
            
        except Exception as e:
            print(f"  ❌ {name}: Failed - {str(e)}")
    
    # Test 4: Raw SQL performance
    print("\n🔍 Testing Raw SQL Performance...")
    
    raw_queries = [
        ('Simple SELECT', 'SELECT COUNT(*) FROM checklist_checklistitem'),
        ('JOIN Query', '''
            SELECT ci.id, ru.title 
            FROM checklist_checklistitem ci 
            JOIN checklist_regulationupdate ru ON ci.regulation_update_id = ru.id
            LIMIT 10
        '''),
        ('Aggregation', '''
            SELECT 
                COUNT(*) as total,
                AVG(likelihood) as avg_likelihood,
                AVG(impact) as avg_impact
            FROM checklist_checklistitem
        '''),
    ]
    
    for name, query in raw_queries:
        try:
            start_time = time.time()
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
            end_time = time.time()
            execution_time = end_time - start_time
            
            results['optimizations'].append({
                'technique': f'raw_sql_{name.lower().replace(" ", "_")}',
                'execution_time': execution_time,
                'result_count': len(result)
            })
            
            print(f"  {name}: {execution_time:.4f}s ({len(result)} results)")
            
        except Exception as e:
            print(f"  ❌ {name}: Failed - {str(e)}")
    
    return results

def generate_optimization_report(results):
    """Generate optimization report"""
    print("\n📊 Generating Optimization Report...")
    
    # Calculate performance metrics
    successful_queries = [q for q in results['queries'] if q['status'] == 'success']
    avg_query_time = sum(q['execution_time'] for q in successful_queries) / len(successful_queries) if successful_queries else 0
    
    slow_queries = [q for q in successful_queries if q['execution_time'] > 0.1]
    
    # Generate recommendations
    recommendations = []
    
    if slow_queries:
        recommendations.append(f"Optimize {len(slow_queries)} slow queries (>100ms)")
    
    if avg_query_time > 0.05:
        recommendations.append("Consider adding more database indexes")
    
    # Check for optimization improvements
    significant_improvements = [opt for opt in results['optimizations'] 
                              if opt.get('improvement_percent', 0) > 20]
    
    if significant_improvements:
        recommendations.append("Apply proven optimization techniques")
    
    # Generate report
    report = f"""
🎯 SQL QUERY OPTIMIZATION REPORT
===============================
Generated: {results['timestamp']}

📊 PERFORMANCE SUMMARY:
  • Total Queries Tested: {len(results['queries'])}
  • Successful Queries: {len(successful_queries)}
  • Average Query Time: {avg_query_time:.4f}s
  • Slow Queries (>100ms): {len(slow_queries)}

⚡ OPTIMIZATION RESULTS:
"""
    
    for opt in results['optimizations']:
        if 'improvement_percent' in opt:
            report += f"  • {opt['technique']}: {opt['improvement_percent']:.1f}% improvement\n"
        else:
            report += f"  • {opt['technique']}: {opt.get('execution_time', 0):.4f}s\n"
    
    report += f"""
💡 RECOMMENDATIONS:
"""
    
    for rec in recommendations:
        report += f"  • {rec}\n"
    
    if not recommendations:
        report += "  • Excellent performance! No optimizations needed.\n"
    
    report += """
📁 REPORTS GENERATED:
  • sql_optimization_simple_report.json
  • This summary report
"""
    
    print(report)
    
    # Save reports
    with open('sql_optimization_simple_report.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    with open('sql_optimization_simple_summary.txt', 'w') as f:
        f.write(report)
    
    print("✅ Optimization report generated!")

def main():
    """Main function"""
    print("🚀 Starting Simple SQL Query Optimization Test...")
    print("=" * 60)
    
    try:
        results = test_query_performance()
        generate_optimization_report(results)
        
    except Exception as e:
        print(f"❌ Optimization test failed: {str(e)}")
    
    print("\n🎉 Simple SQL Query Optimization Test Completed!")

if __name__ == '__main__':
    main()
