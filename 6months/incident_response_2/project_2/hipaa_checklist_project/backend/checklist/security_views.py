"""
Security-related views for the HIPAA Self-Audit Tool
Includes Black Duck Detect integration and security reporting
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .real_security_scanner import RealSecurityScanner


@api_view(['GET'])
def security_report(request):
    """
    Get security scan report including dependency vulnerabilities
    """
    try:
        # Get the project root directory
        project_root = Path(__file__).parent.parent.parent.parent
        reports_dir = project_root / 'reports' / 'detect'
        
        # Check if reports directory exists
        if not reports_dir.exists():
            return Response({
                'status': 'no_reports',
                'message': 'No security reports found. Run a scan first.',
                'last_scan': None,
                'vulnerabilities': [],
                'dependencies': []
            })
        
        # Look for report files (prioritize real scans over mock data)
        report_files = list(reports_dir.glob('*_report.json'))
        
        if not report_files:
            return Response({
                'status': 'no_reports',
                'message': 'No security reports found. Run a scan first.',
                'last_scan': None,
                'vulnerabilities': [],
                'dependencies': []
            })
        
        # Get the most recent report file
        latest_report = max(report_files, key=os.path.getmtime)
        
        # Parse the report
        try:
            with open(latest_report, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            return Response({
                'status': 'error',
                'message': f'Error parsing report file: {str(e)}',
                'last_scan': None,
                'vulnerabilities': [],
                'dependencies': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'status': 'success',
            'message': 'Security report retrieved successfully',
            'last_scan': datetime.fromtimestamp(os.path.getmtime(latest_report)).isoformat(),
            'report_file': latest_report.name,
            'vulnerabilities': report_data.get('vulnerabilities', []),
            'dependencies': report_data.get('dependencies', []),
            'summary': report_data.get('summary', {}),
            'scan_metadata': report_data.get('scan_metadata', {})
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Error retrieving security report: {str(e)}',
            'last_scan': None,
            'vulnerabilities': [],
            'dependencies': []
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def run_security_scan(request):
    """
    Trigger a new security scan using real dependency scanning tools
    """
    try:
        # Get the project root directory
        project_root = Path(__file__).parent.parent.parent.parent
        
        # Create scanner instance
        scanner = RealSecurityScanner(project_root)
        
        # Run the real security scan
        print("🚀 Starting real security scan...")
        report_data = scanner.run_complete_scan()
        
        # Extract scan ID from the report
        scan_id = report_data.get('scan_metadata', {}).get('scan_time', 'unknown')
        
        return Response({
            'status': 'success',
            'message': 'Real security scan completed successfully',
            'scan_id': scan_id,
            'vulnerabilities_found': len(report_data.get('vulnerabilities', [])),
            'dependencies_scanned': len(report_data.get('dependencies', [])),
            'summary': report_data.get('summary', {})
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Error running security scan: {str(e)}',
            'scan_id': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def create_mock_security_report(report_file):
    """
    Create a mock security report for demonstration purposes
    """
    return {
        'vulnerabilities': [
            {
                'id': 'CVE-2023-1234',
                'severity': 'HIGH',
                'component': 'react@18.2.0',
                'description': 'Cross-site scripting vulnerability in React',
                'cvss_score': 7.5,
                'status': 'open'
            },
            {
                'id': 'CVE-2023-5678',
                'severity': 'MEDIUM',
                'component': 'django@4.2.0',
                'description': 'SQL injection vulnerability in Django ORM',
                'cvss_score': 5.2,
                'status': 'open'
            },
            {
                'id': 'CVE-2023-9012',
                'severity': 'LOW',
                'component': 'requests@2.31.0',
                'description': 'Information disclosure in requests library',
                'cvss_score': 3.1,
                'status': 'open'
            }
        ],
        'dependencies': [
            {
                'name': 'react',
                'version': '18.2.0',
                'type': 'npm',
                'vulnerabilities': 1,
                'license': 'MIT'
            },
            {
                'name': 'django',
                'version': '4.2.0',
                'type': 'pip',
                'vulnerabilities': 1,
                'license': 'BSD-3-Clause'
            },
            {
                'name': 'requests',
                'version': '2.31.0',
                'type': 'pip',
                'vulnerabilities': 1,
                'license': 'Apache-2.0'
            }
        ],
        'summary': {
            'total_dependencies': 3,
            'vulnerable_dependencies': 3,
            'critical_vulnerabilities': 0,
            'high_vulnerabilities': 1,
            'medium_vulnerabilities': 1,
            'low_vulnerabilities': 1,
            'last_scan': datetime.now().isoformat()
        }
    }


def create_mock_scan_result(reports_dir, scan_id):
    """
    Create a mock scan result file for demonstration
    """
    mock_data = create_mock_security_report(None)
    
    # Create a JSON report file
    report_file = reports_dir / f"{scan_id}_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(mock_data, f, indent=2)
    
    # Create a summary file
    summary_file = reports_dir / f"{scan_id}_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"Security Scan Report - {scan_id}\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Dependencies: {mock_data['summary']['total_dependencies']}\n")
        f.write(f"Vulnerable Dependencies: {mock_data['summary']['vulnerable_dependencies']}\n")
        f.write(f"High Vulnerabilities: {mock_data['summary']['high_vulnerabilities']}\n")
        f.write(f"Medium Vulnerabilities: {mock_data['summary']['medium_vulnerabilities']}\n")
        f.write(f"Low Vulnerabilities: {mock_data['summary']['low_vulnerabilities']}\n\n")
        f.write("Vulnerabilities Found:\n")
        for vuln in mock_data['vulnerabilities']:
            f.write(f"- {vuln['id']}: {vuln['severity']} - {vuln['description']}\n")
