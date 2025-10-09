"""
Real dependency security scanner using npm audit and safety
"""

import os
import json
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
import re


class RealSecurityScanner:
    def __init__(self, project_root):
        self.project_root = Path(project_root).resolve()
        # Handle case where scanner is called from backend directory
        if self.project_root.name == 'backend':
            self.project_root = self.project_root.parent
        self.frontend_dir = self.project_root / 'frontend'
        self.backend_dir = self.project_root / 'backend'
        self.reports_dir = self.project_root / 'reports' / 'detect'
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Debug output (can be removed in production)
        # print(f"DEBUG: Project root resolved to: {self.project_root}")
        # print(f"DEBUG: Frontend dir: {self.frontend_dir}")
        # print(f"DEBUG: Backend dir: {self.backend_dir}")
        # print(f"DEBUG: Frontend exists: {self.frontend_dir.exists()}")
        # print(f"DEBUG: Backend exists: {self.backend_dir.exists()}")
    
    def scan_npm_dependencies(self):
        """Scan npm dependencies using npm audit"""
        print(" Scanning npm dependencies...")
        vulnerabilities = []
        dependencies = []
        
        if not (self.frontend_dir / 'package.json').exists():
            print("    No package.json found in frontend directory")
            return vulnerabilities, dependencies
        
        try:
            # Run npm audit with shell=True on Windows
            result = subprocess.run(
                ['npm', 'audit', '--json'],
                cwd=str(self.frontend_dir),
                capture_output=True,
                text=True,
                timeout=60,
                shell=True
            )
            
            if result.returncode == 0:
                try:
                    audit_data = json.loads(result.stdout)
                    
                    # Parse vulnerabilities
                    if 'vulnerabilities' in audit_data:
                        for vuln_id, vuln_data in audit_data['vulnerabilities'].items():
                            if vuln_data.get('severity') in ['critical', 'high', 'moderate', 'low']:
                                vulnerabilities.append({
                                    'id': vuln_id,
                                    'severity': vuln_data.get('severity', 'unknown').upper(),
                                    'component': f"{vuln_data.get('name', 'unknown')}@{vuln_data.get('range', 'unknown')}",
                                    'description': vuln_data.get('title', 'No description available'),
                                    'cvss_score': self._calculate_cvss_score(vuln_data.get('severity')),
                                    'status': 'open',
                                    'source': 'npm_audit'
                                })
                    
                    print(f"    Found {len(vulnerabilities)} npm vulnerabilities")
                except json.JSONDecodeError as e:
                    print(f"    Could not parse npm audit output: {e}")
                    print(f"    Raw output: {result.stdout[:200]}...")
            else:
                print(f"    npm audit failed (return code {result.returncode}): {result.stderr}")
                if result.stdout:
                    print(f"    stdout: {result.stdout[:200]}...")
            
            # Always parse dependencies from package.json
            try:
                with open(self.frontend_dir / 'package.json', 'r') as f:
                    package_data = json.load(f)
                
                for dep_name, dep_version in package_data.get('dependencies', {}).items():
                    dep_vulns = sum(1 for v in vulnerabilities if dep_name in v['component'])
                    dependencies.append({
                        'name': dep_name,
                        'version': dep_version.replace('^', '').replace('~', ''),
                        'type': 'npm',
                        'vulnerabilities': dep_vulns,
                        'license': 'Unknown'  # Would need to check package.json or node_modules
                    })
                
                print(f"    Found {len(dependencies)} npm dependencies")
            except Exception as e:
                print(f"    Could not parse package.json: {e}")
                
        except subprocess.TimeoutExpired:
            print("    npm audit timed out")
        except Exception as e:
            print(f"    npm audit error: {e}")
        
        return vulnerabilities, dependencies
    
    def scan_pip_dependencies(self):
        """Scan pip dependencies using safety"""
        print(" Scanning pip dependencies...")
        vulnerabilities = []
        dependencies = []
        
        requirements_file = self.backend_dir / 'requirements.txt'
        if not requirements_file.exists():
            print("    No requirements.txt found in backend directory")
            return vulnerabilities, dependencies
        
        try:
            # Install safety if not available
            subprocess.run(['pip', 'install', 'safety'], check=False, capture_output=True)
            
            # Run safety check
            result = subprocess.run(
                ['safety', 'check', '--json', '--file', str(requirements_file)],
                capture_output=True,
                text=True,
                timeout=60,
                shell=True
            )
            
            # Safety returns non-zero for vulnerabilities, but also for other issues
            if result.stdout:
                try:
                    # Try to parse as JSON first
                    safety_data = json.loads(result.stdout)
                    
                    # Parse vulnerabilities
                    for vuln in safety_data:
                        vulnerabilities.append({
                            'id': vuln.get('cve', f"SAFETY-{vuln.get('id', 'unknown')}"),
                            'severity': self._map_safety_severity(vuln.get('severity')),
                            'component': f"{vuln.get('package_name', 'unknown')}=={vuln.get('installed_version', 'unknown')}",
                            'description': vuln.get('advisory', 'No description available'),
                            'cvss_score': self._calculate_cvss_score(vuln.get('severity')),
                            'status': 'open',
                            'source': 'safety'
                        })
                    
                    print(f"    Found {len(vulnerabilities)} pip vulnerabilities")
                except json.JSONDecodeError:
                    # If not JSON, check if it contains vulnerability information
                    if "vulnerability" in result.stdout.lower() or "cve" in result.stdout.lower():
                        print("    Safety found vulnerabilities but output format is not JSON")
                        print("    Consider updating safety or using different output format")
                    else:
                        print("    No pip vulnerabilities found (non-JSON output)")
            elif result.returncode == 0:
                print("    No pip vulnerabilities found")
            else:
                print(f"    Safety check failed (return code {result.returncode}): {result.stderr}")
                if result.stdout:
                    print(f"    stdout: {result.stdout[:200]}...")
            
            # Parse dependencies from requirements.txt
            with open(requirements_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Parse package name and version
                        if '==' in line:
                            name, version = line.split('==', 1)
                        elif '>=' in line:
                            name, version = line.split('>=', 1)
                        else:
                            name = line.split('>')[0].split('<')[0].split('=')[0]
                            version = 'unknown'
                        
                        dep_vulns = sum(1 for v in vulnerabilities if name in v['component'])
                        dependencies.append({
                            'name': name.strip(),
                            'version': version.strip(),
                            'type': 'pip',
                            'vulnerabilities': dep_vulns,
                            'license': 'Unknown'  # Would need to check package metadata
                        })
                        
        except subprocess.TimeoutExpired:
            print("    safety check timed out")
        except Exception as e:
            print(f"    safety check error: {e}")
        
        return vulnerabilities, dependencies
    
    def scan_bandit_security(self):
        """Scan Python code using bandit"""
        print(" Scanning Python code with bandit...")
        vulnerabilities = []
        
        try:
            # Install bandit if not available
            subprocess.run(['pip', 'install', 'bandit'], check=False, capture_output=True)
            
            # Run bandit on backend directory
            result = subprocess.run(
                ['bandit', '-r', str(self.backend_dir), '-f', 'json'],
                capture_output=True,
                text=True,
                timeout=60,
                shell=True
            )
            
            if result.stdout:  # Bandit always produces output
                try:
                    # Extract JSON from output (bandit might have progress text before JSON)
                    output_lines = result.stdout.strip().split('\n')
                    json_start = -1
                    for i, line in enumerate(output_lines):
                        if line.strip().startswith('{'):
                            json_start = i
                            break
                    
                    if json_start >= 0:
                        json_output = '\n'.join(output_lines[json_start:])
                        bandit_data = json.loads(json_output)
                        
                        # Parse bandit results
                        for issue in bandit_data.get('results', []):
                            vulnerabilities.append({
                                'id': f"BANDIT-{issue.get('test_id', 'unknown')}",
                                'severity': issue.get('issue_severity', 'MEDIUM').upper(),
                                'component': f"{issue.get('filename', 'unknown')}:{issue.get('line_number', 'unknown')}",
                                'description': issue.get('issue_text', 'No description available'),
                                'cvss_score': self._calculate_cvss_score(issue.get('issue_severity')),
                                'status': 'open',
                                'source': 'bandit'
                            })
                        
                        print(f"    Found {len(vulnerabilities)} bandit issues")
                    else:
                        print("    No JSON found in bandit output")
                except json.JSONDecodeError as e:
                    print(f"    Could not parse bandit output: {e}")
                    print(f"    Raw output: {result.stdout[:200]}...")
            else:
                print("    No bandit output received")
                
        except subprocess.TimeoutExpired:
            print("    bandit scan timed out")
        except Exception as e:
            print(f"    bandit scan error: {e}")
        
        return vulnerabilities
    
    def run_complete_scan(self):
        """Run complete security scan"""
        print(" Starting complete security scan...")
        print("=" * 50)
        print(f" Project root: {self.project_root}")
        print(f" Frontend dir: {self.frontend_dir}")
        print(f" Backend dir: {self.backend_dir}")
        print(f" Frontend package.json exists: {(self.frontend_dir / 'package.json').exists()}")
        print(f" Backend requirements.txt exists: {(self.backend_dir / 'requirements.txt').exists()}")
        print("=" * 50)
        
        # Scan npm dependencies
        npm_vulns, npm_deps = self.scan_npm_dependencies()
        
        # Scan pip dependencies
        pip_vulns, pip_deps = self.scan_pip_dependencies()
        
        # Scan Python code
        bandit_vulns = self.scan_bandit_security()
        
        # Combine all results
        all_vulnerabilities = npm_vulns + pip_vulns + bandit_vulns
        all_dependencies = npm_deps + pip_deps
        
        # Calculate summary
        summary = self._calculate_summary(all_vulnerabilities, all_dependencies)
        
        # Create report
        report_data = {
            'vulnerabilities': all_vulnerabilities,
            'dependencies': all_dependencies,
            'summary': summary,
            'scan_metadata': {
                'scan_time': datetime.now().isoformat(),
                'scanner_version': '1.0.0',
                'tools_used': ['npm_audit', 'safety', 'bandit']
            }
        }
        
        # Save report
        scan_id = f"real_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        report_file = self.reports_dir / f"{scan_id}_report.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)
        
        # Create summary file
        summary_file = self.reports_dir / f"{scan_id}_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"Real Security Scan Report - {scan_id}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Dependencies: {summary['total_dependencies']}\n")
            f.write(f"Vulnerable Dependencies: {summary['vulnerable_dependencies']}\n")
            f.write(f"Critical Vulnerabilities: {summary['critical_vulnerabilities']}\n")
            f.write(f"High Vulnerabilities: {summary['high_vulnerabilities']}\n")
            f.write(f"Medium Vulnerabilities: {summary['medium_vulnerabilities']}\n")
            f.write(f"Low Vulnerabilities: {summary['low_vulnerabilities']}\n\n")
            f.write("Vulnerabilities Found:\n")
            for vuln in all_vulnerabilities:
                f.write(f"- {vuln['id']}: {vuln['severity']} - {vuln['description']}\n")
        
        print("\n" + "=" * 50)
        print(" SCAN COMPLETE!")
        print("=" * 50)
        print(f" Total Vulnerabilities: {len(all_vulnerabilities)}")
        print(f" Total Dependencies: {len(all_dependencies)}")
        print(f" Critical: {summary['critical_vulnerabilities']}")
        print(f" High: {summary['high_vulnerabilities']}")
        print(f" Medium: {summary['medium_vulnerabilities']}")
        print(f" Low: {summary['low_vulnerabilities']}")
        print(f" Report saved: {report_file}")
        
        return report_data
    
    def _calculate_cvss_score(self, severity):
        """Calculate CVSS score based on severity"""
        severity_map = {
            'critical': 9.0,
            'high': 7.0,
            'medium': 5.0,
            'low': 3.0,
            'info': 1.0
        }
        return severity_map.get(severity.lower(), 5.0)
    
    def _map_safety_severity(self, severity):
        """Map safety severity to standard format"""
        severity_map = {
            'critical': 'CRITICAL',
            'high': 'HIGH',
            'medium': 'MEDIUM',
            'low': 'LOW'
        }
        return severity_map.get(severity.lower(), 'MEDIUM')
    
    def _calculate_summary(self, vulnerabilities, dependencies):
        """Calculate summary statistics"""
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        for vuln in vulnerabilities:
            severity = vuln['severity'].lower()
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        vulnerable_deps = sum(1 for dep in dependencies if dep['vulnerabilities'] > 0)
        
        return {
            'total_dependencies': len(dependencies),
            'vulnerable_dependencies': vulnerable_deps,
            'critical_vulnerabilities': severity_counts['critical'],
            'high_vulnerabilities': severity_counts['high'],
            'medium_vulnerabilities': severity_counts['medium'],
            'low_vulnerabilities': severity_counts['low'],
            'last_scan': datetime.now().isoformat()
        }
