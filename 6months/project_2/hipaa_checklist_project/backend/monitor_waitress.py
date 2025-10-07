#!/usr/bin/env python3
"""
Waitress Server Monitoring Script
Monitors performance, memory usage, and security metrics
"""

import psutil
import time
import sqlite3
import json
from datetime import datetime
from pathlib import Path

class WaitressMonitor:
    def __init__(self):
        self.db_path = Path('db.sqlite3')
        self.log_file = Path('waitress_monitor.log')
        
    def get_system_metrics(self):
        """Get system performance metrics"""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'memory_available': psutil.virtual_memory().available,
            'disk_usage': psutil.disk_usage('/').percent,
            'load_average': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None,
        }
    
    def get_database_metrics(self):
        """Get database performance metrics"""
        if not self.db_path.exists():
            return {'error': 'Database not found'}
        
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Get database size
            db_size = self.db_path.stat().st_size
            
            # Get table counts
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            table_counts = {}
            for table in tables:
                table_name = table[0]
                if not table_name.startswith('sqlite_'):
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    table_counts[table_name] = count
            
            # Get database info
            cursor.execute("PRAGMA page_count")
            page_count = cursor.fetchone()[0]
            
            cursor.execute("PRAGMA page_size")
            page_size = cursor.fetchone()[0]
            
            cursor.execute("PRAGMA journal_mode")
            journal_mode = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'db_size_bytes': db_size,
                'db_size_mb': round(db_size / (1024 * 1024), 2),
                'page_count': page_count,
                'page_size': page_size,
                'journal_mode': journal_mode,
                'table_counts': table_counts,
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_security_metrics(self):
        """Get security-related metrics"""
        security_metrics = {
            'db_permissions': oct(self.db_path.stat().st_mode) if self.db_path.exists() else None,
            'db_encrypted': False,  # Would need to check encryption status
            'log_files_exist': self.log_file.exists(),
        }
        
        # Check for recent security events in logs
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    lines = f.readlines()
                    recent_lines = lines[-50:] if len(lines) > 50 else lines
                    
                security_events = [line for line in recent_lines if 'security' in line.lower() or 'error' in line.lower()]
                security_metrics['recent_security_events'] = len(security_events)
            except:
                security_metrics['recent_security_events'] = 0
        
        return security_metrics
    
    def log_metrics(self, metrics):
        """Log metrics to file"""
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(metrics) + '\n')
        except Exception as e:
            print(f"Failed to log metrics: {e}")
    
    def print_metrics(self, metrics):
        """Print metrics in a readable format"""
        print(f"\n Waitress Server Metrics - {metrics['timestamp']}")
        print("=" * 50)
        
        # System metrics
        sys_metrics = metrics['system']
        print(f"  CPU Usage: {sys_metrics['cpu_percent']:.1f}%")
        print(f" Memory Usage: {sys_metrics['memory_percent']:.1f}% ({sys_metrics['memory_available']:,} bytes available)")
        print(f" Disk Usage: {sys_metrics['disk_usage']:.1f}%")
        
        # Database metrics
        db_metrics = metrics['database']
        if 'error' not in db_metrics:
            print(f"  Database Size: {db_metrics['db_size_mb']} MB")
            print(f" Pages: {db_metrics['page_count']:,} (size: {db_metrics['page_size']} bytes)")
            print(f" Journal Mode: {db_metrics['journal_mode']}")
            print(" Table Counts:")
            for table, count in db_metrics['table_counts'].items():
                print(f"   {table}: {count:,} records")
        else:
            print(f" Database Error: {db_metrics['error']}")
        
        # Security metrics
        sec_metrics = metrics['security']
        print(f" Database Permissions: {sec_metrics['db_permissions']}")
        print(f" Database Encrypted: {sec_metrics['db_encrypted']}")
        print(f" Log Files: {'' if sec_metrics['log_files_exist'] else ''}")
        print(f"  Recent Security Events: {sec_metrics['recent_security_events']}")
    
    def monitor_loop(self, interval=30):
        """Main monitoring loop"""
        print(" Starting Waitress Server Monitoring...")
        print(f" Monitoring interval: {interval} seconds")
        print("Press Ctrl+C to stop monitoring\n")
        
        try:
            while True:
                metrics = {
                    'system': self.get_system_metrics(),
                    'database': self.get_database_metrics(),
                    'security': self.get_security_metrics(),
                }
                
                self.print_metrics(metrics)
                self.log_metrics(metrics)
                
                print(f"\n⏰ Next check in {interval} seconds...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n Monitoring stopped by user")
        except Exception as e:
            print(f"\n Monitoring error: {e}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor Waitress Server Performance')
    parser.add_argument('--interval', type=int, default=30, help='Monitoring interval in seconds')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    
    args = parser.parse_args()
    
    monitor = WaitressMonitor()
    
    if args.once:
        metrics = {
            'system': monitor.get_system_metrics(),
            'database': monitor.get_database_metrics(),
            'security': monitor.get_security_metrics(),
        }
        monitor.print_metrics(metrics)
    else:
        monitor.monitor_loop(args.interval)

if __name__ == '__main__':
    main()
