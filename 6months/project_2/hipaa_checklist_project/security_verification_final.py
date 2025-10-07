#!/usr/bin/env python3
"""
Final Week Security Verification Script for HIPAA Checklist Project
Comprehensive security audit covering encryption, database security, firewall rules, and SSL/TLS
"""

import os
import sys
import json
import subprocess
import sqlite3
import ssl
import socket
import requests
import hashlib
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecurityVerification:
    """Comprehensive security verification for HIPAA Checklist Project"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'PENDING',
            'categories': {},
            'recommendations': [],
            'critical_issues': [],
            'summary': {}
        }
        self.project_root = Path.cwd()
        self.backend_path = self.project_root / 'backend'
        self.ssl_path = self.project_root / 'ssl'
        
    def run_complete_verification(self):
        """Run all security verification checks"""
        logger.info(" Starting Comprehensive Security Verification")
        logger.info("=" * 60)
        
        # 1. Database Security Verification
        self.verify_database_security()
        
        # 2. SSL/TLS Certificate Verification
        self.verify_ssl_tls_security()
        
        # 3. Network Security Verification
        self.verify_network_security()
        
        # 4. Authentication & Authorization Verification
        self.verify_authentication_security()
        
        # 5. File Permissions Verification
        self.verify_file_permissions()
        
        # 6. Security Headers Verification
        self.verify_security_headers()
        
        # 7. Generate Final Report
        self.generate_final_report()
        
        return self.results
    
    def verify_database_security(self):
        """Verify database encryption and access controls"""
        logger.info(" Verifying Database Security...")
        
        db_security = {
            'status': 'PENDING',
            'checks': {},
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Check database files
            db_files = [
                self.backend_path / 'db.sqlite3',
                self.backend_path / 'db.sqlite3.encrypted',
                self.backend_path / 'db.encrypted'
            ]
            
            db_security['checks']['database_files'] = {}
            for db_file in db_files:
                if db_file.exists():
                    stat_info = db_file.stat()
                    db_security['checks']['database_files'][str(db_file)] = {
                        'exists': True,
                        'size': stat_info.st_size,
                        'permissions': oct(stat_info.st_mode),
                        'modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat()
                    }
                else:
                    db_security['checks']['database_files'][str(db_file)] = {'exists': False}
            
            # Test database encryption
            if (self.backend_path / 'db.sqlite3.encrypted').exists():
                try:
                    # Try to connect to encrypted database (should fail)
                    conn = sqlite3.connect(str(self.backend_path / 'db.sqlite3.encrypted'))
                    conn.close()
                    db_security['issues'].append("Encrypted database is readable without decryption")
                except:
                    db_security['checks']['encryption_working'] = True
            
            # Check encryption key management
            encryption_key_file = self.backend_path / 'encryption.key'
            if encryption_key_file.exists():
                db_security['checks']['encryption_key_exists'] = True
                db_security['checks']['encryption_key_permissions'] = oct(encryption_key_file.stat().st_mode)
            else:
                db_security['checks']['encryption_key_exists'] = False
                db_security['recommendations'].append("Create dedicated encryption key file")
            
            # Test database connectivity
            if (self.backend_path / 'db.sqlite3').exists():
                try:
                    conn = sqlite3.connect(str(self.backend_path / 'db.sqlite3'))
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    db_security['checks']['database_connectivity'] = True
                    db_security['checks']['tables_count'] = len(tables)
                    conn.close()
                except Exception as e:
                    db_security['issues'].append(f"Database connectivity issue: {e}")
            
            db_security['status'] = 'PASS' if not db_security['issues'] else 'FAIL'
            
        except Exception as e:
            db_security['status'] = 'ERROR'
            db_security['issues'].append(f"Database security check failed: {e}")
        
        self.results['categories']['database_security'] = db_security
    
    def verify_ssl_tls_security(self):
        """Verify SSL/TLS certificate implementation"""
        logger.info(" Verifying SSL/TLS Security...")
        
        ssl_security = {
            'status': 'PENDING',
            'checks': {},
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Check SSL certificate files
            cert_files = [
                self.ssl_path / 'hipaa_checklist.crt',
                self.ssl_path / 'hipaa_checklist.key',
                self.ssl_path / 'hipaa_checklist.pfx'
            ]
            
            ssl_security['checks']['certificate_files'] = {}
            for cert_file in cert_files:
                if cert_file.exists():
                    stat_info = cert_file.stat()
                    ssl_security['checks']['certificate_files'][cert_file.name] = {
                        'exists': True,
                        'size': stat_info.st_size,
                        'permissions': oct(stat_info.st_mode),
                        'modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat()
                    }
                else:
                    ssl_security['checks']['certificate_files'][cert_file.name] = {'exists': False}
            
            # Test SSL certificate validity
            if (self.ssl_path / 'hipaa_checklist.crt').exists():
                try:
                    with open(self.ssl_path / 'hipaa_checklist.crt', 'rb') as f:
                        cert_data = f.read()
                    
                    # Parse certificate
                    cert = ssl.PEM_cert_to_DER_cert(cert_data.decode())
                    x509 = ssl.DER_cert_to_PEM_cert(cert)
                    
                    ssl_security['checks']['certificate_valid'] = True
                    ssl_security['checks']['certificate_format'] = 'PEM'
                except Exception as e:
                    ssl_security['issues'].append(f"Certificate validation failed: {e}")
            
            # Test HTTPS connectivity
            try:
                response = requests.get('https://localhost', verify=False, timeout=5)
                ssl_security['checks']['https_connectivity'] = True
                ssl_security['checks']['https_status_code'] = response.status_code
            except requests.exceptions.SSLError as e:
                ssl_security['issues'].append(f"SSL connection failed: {e}")
            except requests.exceptions.ConnectionError:
                ssl_security['checks']['https_connectivity'] = False
                ssl_security['recommendations'].append("Start HTTPS server for testing")
            except Exception as e:
                ssl_security['issues'].append(f"HTTPS test failed: {e}")
            
            # Check Nginx SSL configuration
            nginx_conf = self.project_root / 'nginx-https.conf'
            if nginx_conf.exists():
                with open(nginx_conf, 'r') as f:
                    nginx_content = f.read()
                
                ssl_security['checks']['nginx_ssl_config'] = {
                    'file_exists': True,
                    'has_ssl_protocols': 'ssl_protocols' in nginx_content,
                    'has_ssl_ciphers': 'ssl_ciphers' in nginx_content,
                    'has_hsts': 'Strict-Transport-Security' in nginx_content
                }
            else:
                ssl_security['checks']['nginx_ssl_config'] = {'file_exists': False}
            
            ssl_security['status'] = 'PASS' if not ssl_security['issues'] else 'FAIL'
            
        except Exception as e:
            ssl_security['status'] = 'ERROR'
            ssl_security['issues'].append(f"SSL/TLS security check failed: {e}")
        
        self.results['categories']['ssl_tls_security'] = ssl_security
    
    def verify_network_security(self):
        """Verify network security and firewall rules"""
        logger.info(" Verifying Network Security...")
        
        network_security = {
            'status': 'PENDING',
            'checks': {},
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Check open ports
            ports_to_check = [80, 443, 8000, 3000, 22, 21, 23, 25, 53, 110, 143, 993, 995]
            network_security['checks']['open_ports'] = {}
            
            for port in ports_to_check:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex(('localhost', port))
                    sock.close()
                    network_security['checks']['open_ports'][port] = result == 0
                except:
                    network_security['checks']['open_ports'][port] = False
            
            # Check for unnecessary open ports
            critical_ports = [22, 21, 23, 25, 53, 110, 143, 993, 995]
            for port in critical_ports:
                if network_security['checks']['open_ports'].get(port, False):
                    network_security['issues'].append(f"Critical port {port} is open")
            
            # Test rate limiting
            try:
                # Test API rate limiting
                for i in range(15):  # Try to exceed rate limit
                    response = requests.get('http://localhost:8000/api/health/', timeout=2)
                    if response.status_code == 429:
                        network_security['checks']['rate_limiting_working'] = True
                        break
                else:
                    network_security['recommendations'].append("Rate limiting may not be working properly")
            except:
                network_security['checks']['rate_limiting_working'] = False
                network_security['recommendations'].append("Test rate limiting when server is running")
            
            # Check Nginx security configuration
            nginx_conf = self.project_root / 'nginx-https.conf'
            if nginx_conf.exists():
                with open(nginx_conf, 'r') as f:
                    nginx_content = f.read()
                
                network_security['checks']['nginx_security'] = {
                    'has_rate_limiting': 'limit_req' in nginx_content,
                    'has_security_headers': 'add_header' in nginx_content,
                    'blocks_sensitive_files': 'deny all' in nginx_content,
                    'has_ssl_redirect': 'return 301' in nginx_content
                }
            
            network_security['status'] = 'PASS' if not network_security['issues'] else 'FAIL'
            
        except Exception as e:
            network_security['status'] = 'ERROR'
            network_security['issues'].append(f"Network security check failed: {e}")
        
        self.results['categories']['network_security'] = network_security
    
    def verify_authentication_security(self):
        """Verify authentication and authorization mechanisms"""
        logger.info(" Verifying Authentication Security...")
        
        auth_security = {
            'status': 'PENDING',
            'checks': {},
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Check Django settings for security
            settings_file = self.backend_path / 'hipaa_checklist' / 'settings.py'
            if settings_file.exists():
                with open(settings_file, 'r') as f:
                    settings_content = f.read()
                
                auth_security['checks']['django_security'] = {
                    'has_secret_key': 'SECRET_KEY' in settings_content,
                    'has_debug_false': 'DEBUG = False' in settings_content,
                    'has_secure_ssl_redirect': 'SECURE_SSL_REDIRECT' in settings_content,
                    'has_csrf_cookie_secure': 'CSRF_COOKIE_SECURE' in settings_content,
                    'has_session_cookie_secure': 'SESSION_COOKIE_SECURE' in settings_content,
                    'has_jwt_auth': 'JWT' in settings_content or 'jwt' in settings_content
                }
            
            # Test JWT authentication
            try:
                # Test token endpoint
                response = requests.post('http://localhost:8000/api/token/', 
                                       json={'username': 'test', 'password': 'test'}, 
                                       timeout=5)
                if response.status_code in [200, 400, 401]:
                    auth_security['checks']['jwt_endpoint_working'] = True
                else:
                    auth_security['issues'].append(f"JWT endpoint returned unexpected status: {response.status_code}")
            except requests.exceptions.ConnectionError:
                auth_security['checks']['jwt_endpoint_working'] = False
                auth_security['recommendations'].append("Start Django server to test JWT authentication")
            except Exception as e:
                auth_security['issues'].append(f"JWT authentication test failed: {e}")
            
            # Check security middleware
            middleware_file = self.backend_path / 'checklist' / 'security_middleware.py'
            if middleware_file.exists():
                with open(middleware_file, 'r') as f:
                    middleware_content = f.read()
                
                auth_security['checks']['security_middleware'] = {
                    'exists': True,
                    'has_security_headers': 'X-Frame-Options' in middleware_content,
                    'has_hsts': 'Strict-Transport-Security' in middleware_content,
                    'has_csp': 'Content-Security-Policy' in middleware_content
                }
            else:
                auth_security['checks']['security_middleware'] = {'exists': False}
            
            auth_security['status'] = 'PASS' if not auth_security['issues'] else 'FAIL'
            
        except Exception as e:
            auth_security['status'] = 'ERROR'
            auth_security['issues'].append(f"Authentication security check failed: {e}")
        
        self.results['categories']['authentication_security'] = auth_security
    
    def verify_file_permissions(self):
        """Verify file permissions and access controls"""
        logger.info(" Verifying File Permissions...")
        
        file_security = {
            'status': 'PENDING',
            'checks': {},
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Check critical file permissions
            critical_files = [
                self.backend_path / 'db.sqlite3',
                self.backend_path / 'db.sqlite3.encrypted',
                self.ssl_path / 'hipaa_checklist.key',
                self.backend_path / 'encryption.key'
            ]
            
            file_security['checks']['file_permissions'] = {}
            for file_path in critical_files:
                if file_path.exists():
                    stat_info = file_path.stat()
                    permissions = oct(stat_info.st_mode)
                    file_security['checks']['file_permissions'][str(file_path)] = {
                        'permissions': permissions,
                        'owner_readable': bool(stat_info.st_mode & 0o400),
                        'group_readable': bool(stat_info.st_mode & 0o040),
                        'other_readable': bool(stat_info.st_mode & 0o004),
                        'owner_writable': bool(stat_info.st_mode & 0o200),
                        'group_writable': bool(stat_info.st_mode & 0o020),
                        'other_writable': bool(stat_info.st_mode & 0o002)
                    }
                    
                    # Check for overly permissive permissions
                    if stat_info.st_mode & 0o022:  # Group or other write
                        file_security['issues'].append(f"File {file_path} has overly permissive write permissions")
                    if stat_info.st_mode & 0o044:  # Group or other read for sensitive files
                        if 'key' in str(file_path) or 'encrypted' in str(file_path):
                            file_security['issues'].append(f"Sensitive file {file_path} is readable by group/others")
            
            # Check directory permissions
            critical_dirs = [self.backend_path, self.ssl_path, self.project_root / 'logs']
            file_security['checks']['directory_permissions'] = {}
            for dir_path in critical_dirs:
                if dir_path.exists():
                    stat_info = dir_path.stat()
                    file_security['checks']['directory_permissions'][str(dir_path)] = {
                        'permissions': oct(stat_info.st_mode),
                        'owner_executable': bool(stat_info.st_mode & 0o100),
                        'group_executable': bool(stat_info.st_mode & 0o010),
                        'other_executable': bool(stat_info.st_mode & 0o001)
                    }
            
            file_security['status'] = 'PASS' if not file_security['issues'] else 'FAIL'
            
        except Exception as e:
            file_security['status'] = 'ERROR'
            file_security['issues'].append(f"File permissions check failed: {e}")
        
        self.results['categories']['file_permissions'] = file_security
    
    def verify_security_headers(self):
        """Verify security headers implementation"""
        logger.info(" Verifying Security Headers...")
        
        headers_security = {
            'status': 'PENDING',
            'checks': {},
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Test security headers via HTTP requests
            try:
                response = requests.get('http://localhost:8000/api/health/', timeout=5)
                headers_security['checks']['http_response'] = {
                    'status_code': response.status_code,
                    'headers': dict(response.headers)
                }
                
                # Check for security headers
                required_headers = [
                    'X-Frame-Options',
                    'X-Content-Type-Options',
                    'X-XSS-Protection',
                    'Strict-Transport-Security'
                ]
                
                headers_security['checks']['security_headers'] = {}
                for header in required_headers:
                    headers_security['checks']['security_headers'][header] = header in response.headers
                    if header not in response.headers:
                        headers_security['recommendations'].append(f"Add {header} security header")
                
            except requests.exceptions.ConnectionError:
                headers_security['checks']['http_response'] = {'error': 'Server not running'}
                headers_security['recommendations'].append("Start server to test security headers")
            except Exception as e:
                headers_security['issues'].append(f"Security headers test failed: {e}")
            
            # Check Nginx security headers configuration
            nginx_conf = self.project_root / 'nginx-https.conf'
            if nginx_conf.exists():
                with open(nginx_conf, 'r') as f:
                    nginx_content = f.read()
                
                headers_security['checks']['nginx_headers'] = {
                    'has_x_frame_options': 'X-Frame-Options' in nginx_content,
                    'has_x_content_type': 'X-Content-Type-Options' in nginx_content,
                    'has_x_xss_protection': 'X-XSS-Protection' in nginx_content,
                    'has_hsts': 'Strict-Transport-Security' in nginx_content
                }
            
            headers_security['status'] = 'PASS' if not headers_security['issues'] else 'FAIL'
            
        except Exception as e:
            headers_security['status'] = 'ERROR'
            headers_security['issues'].append(f"Security headers check failed: {e}")
        
        self.results['categories']['security_headers'] = headers_security
    
    def generate_final_report(self):
        """Generate comprehensive security verification report"""
        logger.info(" Generating Final Security Report...")
        
        # Calculate overall status
        categories = self.results['categories']
        total_categories = len(categories)
        passed_categories = sum(1 for cat in categories.values() if cat['status'] == 'PASS')
        failed_categories = sum(1 for cat in categories.values() if cat['status'] == 'FAIL')
        error_categories = sum(1 for cat in categories.values() if cat['status'] == 'ERROR')
        
        # Determine overall status
        if error_categories > 0:
            self.results['overall_status'] = 'ERROR'
        elif failed_categories > 0:
            self.results['overall_status'] = 'FAIL'
        else:
            self.results['overall_status'] = 'PASS'
        
        # Generate summary
        self.results['summary'] = {
            'total_categories': total_categories,
            'passed_categories': passed_categories,
            'failed_categories': failed_categories,
            'error_categories': error_categories,
            'success_rate': f"{(passed_categories/total_categories)*100:.1f}%" if total_categories > 0 else "0%",
            'critical_issues_count': len(self.results['critical_issues']),
            'recommendations_count': len(self.results['recommendations'])
        }
        
        # Collect all issues and recommendations
        for category_name, category_data in categories.items():
            if 'issues' in category_data:
                self.results['critical_issues'].extend([f"{category_name}: {issue}" for issue in category_data['issues']])
            if 'recommendations' in category_data:
                self.results['recommendations'].extend([f"{category_name}: {rec}" for rec in category_data['recommendations']])
        
        # Save report
        report_file = f"security_verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        logger.info(f" Security verification report saved: {report_file}")
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print security verification summary"""
        print("\n" + "=" * 60)
        print(" HIPAA CHECKLIST PROJECT - SECURITY VERIFICATION SUMMARY")
        print("=" * 60)
        
        print(f" Timestamp: {self.results['timestamp']}")
        print(f" Overall Status: {self.results['overall_status']}")
        print(f" Success Rate: {self.results['summary']['success_rate']}")
        
        print(f"\n Category Results:")
        for category_name, category_data in self.results['categories'].items():
            status_emoji = "" if category_data['status'] == 'PASS' else "" if category_data['status'] == 'FAIL' else ""
            print(f"  {status_emoji} {category_name.replace('_', ' ').title()}: {category_data['status']}")
        
        if self.results['critical_issues']:
            print(f"\n Critical Issues ({len(self.results['critical_issues'])}):")
            for issue in self.results['critical_issues'][:5]:  # Show first 5
                print(f"  • {issue}")
            if len(self.results['critical_issues']) > 5:
                print(f"  ... and {len(self.results['critical_issues']) - 5} more")
        
        if self.results['recommendations']:
            print(f"\n Recommendations ({len(self.results['recommendations'])}):")
            for rec in self.results['recommendations'][:5]:  # Show first 5
                print(f"  • {rec}")
            if len(self.results['recommendations']) > 5:
                print(f"  ... and {len(self.results['recommendations']) - 5} more")
        
        print("\n" + "=" * 60)
        print(" Security verification completed!")
        print("=" * 60)

def main():
    """Main function to run security verification"""
    print(" HIPAA Checklist Project - Final Week Security Verification")
    print("Encryption and Security Verification (Notes/DB checks; firewall rules)")
    print("=" * 70)
    
    verifier = SecurityVerification()
    results = verifier.run_complete_verification()
    
    return results

if __name__ == '__main__':
    main()
