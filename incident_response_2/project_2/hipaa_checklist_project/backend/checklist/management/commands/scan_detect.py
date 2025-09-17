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
            self.style.SUCCESS('Starting Black Duck Detect security scan...')
        )

        # Set up Java environment for JDK 11
        # Try multiple possible JDK 11 locations
        possible_java_homes = [
            r'C:\Program Files\Java\jdk-11',  # Current installation
            r'C:\Program Files\OpenJDK\jdk-11',
            r'C:\Program Files\Eclipse Adoptium\jdk-11.0.26.4-hotspot',
            r'C:\Program Files\Temurin\jdk-11.0.26.4-hotspot'
        ]
        
        java_home = None
        for path in possible_java_homes:
            if os.path.exists(path):
                java_home = path
                break
        
        if not java_home:
            self.stdout.write(
                self.style.ERROR('JDK 11 not found in any of the expected locations')
            )
            self.stdout.write(
                self.style.WARNING('Please install JDK 11 using Chocolatey: choco install openjdk11 -y')
            )
            self.stdout.write(
                self.style.WARNING('Or check your JAVA_HOME environment variable')
            )
            return

        # Set environment variables
        os.environ['JAVA_HOME'] = java_home
        os.environ['PATH'] = f"{java_home}\\bin;{os.environ.get('PATH', '')}"

        # Verify Java version
        try:
            result = subprocess.run(['java', '-version'], 
                                  capture_output=True, text=True, check=True)
            self.stdout.write(f'Java version: {result.stderr.splitlines()[0]}')
        except subprocess.CalledProcessError as e:
            self.stdout.write(
                self.style.ERROR(f'Java verification failed: {e}')
            )
            return

        # Set up paths
        project_root = Path(settings.BASE_DIR).parent
        detect_dir = project_root / 'tools' / 'detect'
        output_dir = Path(options['output_dir'])
        
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # Check if detect.ps1 exists
        detect_script = detect_dir / 'detect.ps1'
        if not detect_script.exists():
            self.stdout.write(
                self.style.WARNING('detect.ps1 not found, downloading...')
            )
            try:
                import urllib.request
                urllib.request.urlretrieve(
                    'https://detect.blackduck.com/detect10.ps1',
                    str(detect_script)
                )
                self.stdout.write(
                    self.style.SUCCESS('detect.ps1 downloaded successfully')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to download detect.ps1: {e}')
                )
                return

        # Prepare Detect command
        cmd = [
            'powershell',
            '-ExecutionPolicy', 'Bypass',
            '-File', str(detect_script),
            '--detect.project.name=hipaa_checklist_project',
            f'--detect.source.path={project_root}',
            '--detect.detector.search.depth=3',
            '--detect.python.path=python',
            '--detect.npm.path=npm',
            f'--detect.output.path={output_dir}',
            f'--detect.log.level={options["log_level"]}'
        ]

        self.stdout.write(f'Running command: {" ".join(cmd)}')
        self.stdout.write('This may take 15-20 minutes...')

        try:
            # Run Detect scan
            result = subprocess.run(
                cmd,
                cwd=str(detect_dir),
                capture_output=True,
                text=True,
                timeout=1800  # 30 minute timeout
            )

            # Save output to file
            output_file = detect_dir / 'detect-output.txt'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}")

            if result.returncode == 0:
                self.stdout.write(
                    self.style.SUCCESS('Detect scan completed successfully!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Detect scan completed with warnings (exit code: {result.returncode})')
                )

            # Check for output files
            output_files = list(output_dir.glob('*'))
            if output_files:
                self.stdout.write(f'Scan results saved to: {output_dir}')
                for file in output_files:
                    self.stdout.write(f'  - {file.name}')
            else:
                self.stdout.write(
                    self.style.WARNING('No output files found. Check detect-output.txt for details.')
                )

            # Show last few lines of output
            if result.stdout:
                self.stdout.write('\nLast 10 lines of output:')
                for line in result.stdout.splitlines()[-10:]:
                    self.stdout.write(f'  {line}')

        except subprocess.TimeoutExpired:
            self.stdout.write(
                self.style.ERROR('Detect scan timed out after 30 minutes')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error running Detect scan: {e}')
            )

        self.stdout.write(
            self.style.SUCCESS('Detect scan process completed.')
        )
