"""
Django management command to run Black Duck Detect security scan
Usage: python manage.py scan_detect
"""

import os
import subprocess
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
from checklist.real_security_scanner import RealSecurityScanner


class Command(BaseCommand):
    help = 'Run Black Duck Detect security scan on the project'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default='../reports/detect',
            help='Output directory for scan results'
        )
        parser.add_argument(
            '--log-level',
            type=str,
            default='TRACE',
            choices=['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR'],
            help='Log level for Detect scan'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting real security scan...')
        )

        try:
            # Set up paths
            project_root = Path(settings.BASE_DIR).parent
            output_dir = Path(options['output_dir'])
            
            # Ensure output directory exists
            output_dir.mkdir(parents=True, exist_ok=True)

            # Create scanner instance
            scanner = RealSecurityScanner(project_root)
            
            # Run the real security scan
            self.stdout.write(' Scanning dependencies for vulnerabilities...')
            report_data = scanner.run_complete_scan()
            
            # Display results
            vulnerabilities = report_data.get('vulnerabilities', [])
            dependencies = report_data.get('dependencies', [])
            summary = report_data.get('summary', {})
            
            self.stdout.write('\n' + '='*50)
            self.stdout.write(self.style.SUCCESS('SCAN COMPLETED SUCCESSFULLY!'))
            self.stdout.write('='*50)
            self.stdout.write(f' Total Dependencies: {summary.get("total_dependencies", 0)}')
            self.stdout.write(f' Vulnerable Dependencies: {summary.get("vulnerable_dependencies", 0)}')
            self.stdout.write(f' Critical Vulnerabilities: {summary.get("critical_vulnerabilities", 0)}')
            self.stdout.write(f' High Vulnerabilities: {summary.get("high_vulnerabilities", 0)}')
            self.stdout.write(f' Medium Vulnerabilities: {summary.get("medium_vulnerabilities", 0)}')
            self.stdout.write(f' Low Vulnerabilities: {summary.get("low_vulnerabilities", 0)}')
            
            if vulnerabilities:
                self.stdout.write('\n VULNERABILITIES FOUND:')
                for vuln in vulnerabilities[:10]:  # Show first 10
                    self.stdout.write(f'  - {vuln["id"]}: {vuln["severity"]} - {vuln["description"][:80]}...')
                if len(vulnerabilities) > 10:
                    self.stdout.write(f'  ... and {len(vulnerabilities) - 10} more')
            
            # Show scan metadata
            scan_metadata = report_data.get('scan_metadata', {})
            if scan_metadata:
                self.stdout.write(f'\n Tools Used: {", ".join(scan_metadata.get("tools_used", []))}')
                self.stdout.write(f' Scan Time: {scan_metadata.get("scan_time", "Unknown")}')
            
            self.stdout.write(
                self.style.SUCCESS('\nReal security scan completed successfully!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error running security scan: {e}')
            )
            import traceback
            self.stdout.write(traceback.format_exc())
