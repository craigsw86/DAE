#!/usr/bin/env python3
"""
Final System Verification Script
HIPAA Checklist Project - 12-Week Completion
"""

import os
import sys
import subprocess
import time
import requests
import json
from pathlib import Path

class SystemVerifier:
    def __init__(self):
        self.project_root = Path.cwd()
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.results = {
            "backend": {"status": "unknown", "details": []},
            "frontend": {"status": "unknown", "details": []},
            "database": {"status": "unknown", "details": []},
            "api": {"status": "unknown", "details": []},
            "overall": {"status": "unknown", "score": 0}
        }
    
    def log(self, message, level="INFO"):
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def check_backend(self):
        """Check Django backend system"""
        self.log("Checking Django backend...")
        
        try:
            # Check if manage.py exists
            manage_py = self.backend_dir / "manage.py"
            if not manage_py.exists():
                self.results["backend"]["details"].append("manage.py not found")
                return False
            
            # Check Django configuration
            os.chdir(self.backend_dir)
            result = subprocess.run(
                ["python", "manage.py", "check"], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                self.results["backend"]["status"] = "PASS"
                self.results["backend"]["details"].append("Django check passed")
                self.log("✅ Backend Django check passed")
            else:
                self.results["backend"]["status"] = "FAIL"
                self.results["backend"]["details"].append(f"Django check failed: {result.stderr}")
                self.log(f"❌ Backend Django check failed: {result.stderr}")
                return False
            
            # Check migrations
            result = subprocess.run(
                ["python", "manage.py", "showmigrations"], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                self.results["backend"]["details"].append("Migrations available")
                self.log("✅ Backend migrations available")
            else:
                self.results["backend"]["details"].append("Migration check failed")
                self.log("⚠️ Backend migration check failed")
            
            return True
            
        except Exception as e:
            self.results["backend"]["status"] = "ERROR"
            self.results["backend"]["details"].append(f"Exception: {str(e)}")
            self.log(f"❌ Backend check error: {str(e)}")
            return False
        finally:
            os.chdir(self.project_root)
    
    def check_frontend(self):
        """Check React frontend system"""
        self.log("Checking React frontend...")
        
        try:
            # Check if package.json exists
            package_json = self.frontend_dir / "package.json"
            if not package_json.exists():
                self.results["frontend"]["details"].append("package.json not found")
                return False
            
            # Check if node_modules exists
            node_modules = self.frontend_dir / "node_modules"
            if not node_modules.exists():
                self.results["frontend"]["details"].append("node_modules not found - run npm install")
                return False
            
            # Check if build directory exists or can be created
            build_dir = self.frontend_dir / "build"
            if not build_dir.exists():
                self.log("⚠️ Frontend build directory not found - will need to run npm run build")
                self.results["frontend"]["details"].append("Build directory not found")
            else:
                self.results["frontend"]["details"].append("Build directory exists")
                self.log("✅ Frontend build directory exists")
            
            # Check package.json for required scripts
            with open(package_json, 'r') as f:
                package_data = json.load(f)
            
            required_scripts = ["start", "build", "test"]
            missing_scripts = [script for script in required_scripts if script not in package_data.get("scripts", {})]
            
            if missing_scripts:
                self.results["frontend"]["details"].append(f"Missing scripts: {missing_scripts}")
                self.log(f"⚠️ Missing frontend scripts: {missing_scripts}")
            else:
                self.results["frontend"]["details"].append("All required scripts present")
                self.log("✅ Frontend scripts available")
            
            self.results["frontend"]["status"] = "PASS"
            return True
            
        except Exception as e:
            self.results["frontend"]["status"] = "ERROR"
            self.results["frontend"]["details"].append(f"Exception: {str(e)}")
            self.log(f"❌ Frontend check error: {str(e)}")
            return False
    
    def check_database(self):
        """Check database system"""
        self.log("Checking database...")
        
        try:
            os.chdir(self.backend_dir)
            
            # Check if database file exists
            db_file = self.backend_dir / "db.sqlite3"
            if db_file.exists():
                self.results["database"]["details"].append("SQLite database file exists")
                self.log("✅ Database file exists")
            else:
                self.results["database"]["details"].append("Database file not found")
                self.log("⚠️ Database file not found")
            
            # Check migrations status
            result = subprocess.run(
                ["python", "manage.py", "showmigrations", "--plan"], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                if "No migrations to apply" in result.stdout:
                    self.results["database"]["status"] = "PASS"
                    self.results["database"]["details"].append("All migrations applied")
                    self.log("✅ Database migrations up to date")
                else:
                    self.results["database"]["status"] = "WARN"
                    self.results["database"]["details"].append("Pending migrations")
                    self.log("⚠️ Database has pending migrations")
            else:
                self.results["database"]["status"] = "FAIL"
                self.results["database"]["details"].append("Migration check failed")
                self.log("❌ Database migration check failed")
            
            return True
            
        except Exception as e:
            self.results["database"]["status"] = "ERROR"
            self.results["database"]["details"].append(f"Exception: {str(e)}")
            self.log(f"❌ Database check error: {str(e)}")
            return False
        finally:
            os.chdir(self.project_root)
    
    def check_api_endpoints(self):
        """Check API endpoints (requires server running)"""
        self.log("Checking API endpoints...")
        
        try:
            # Test basic connectivity
            test_urls = [
                "http://localhost:8000/api/health/",
                "http://localhost:8000/api/info/",
                "http://localhost:8000/admin/"
            ]
            
            working_endpoints = 0
            total_endpoints = len(test_urls)
            
            for url in test_urls:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code in [200, 302]:  # 302 for admin redirect
                        working_endpoints += 1
                        self.results["api"]["details"].append(f"{url} - OK ({response.status_code})")
                        self.log(f"✅ {url} - OK")
                    else:
                        self.results["api"]["details"].append(f"{url} - FAIL ({response.status_code})")
                        self.log(f"❌ {url} - FAIL ({response.status_code})")
                except requests.exceptions.RequestException as e:
                    self.results["api"]["details"].append(f"{url} - ERROR ({str(e)})")
                    self.log(f"❌ {url} - ERROR: {str(e)}")
            
            if working_endpoints == total_endpoints:
                self.results["api"]["status"] = "PASS"
                self.log("✅ All API endpoints working")
            elif working_endpoints > 0:
                self.results["api"]["status"] = "PARTIAL"
                self.log(f"⚠️ {working_endpoints}/{total_endpoints} API endpoints working")
            else:
                self.results["api"]["status"] = "FAIL"
                self.log("❌ No API endpoints working - server may not be running")
            
            return working_endpoints > 0
            
        except Exception as e:
            self.results["api"]["status"] = "ERROR"
            self.results["api"]["details"].append(f"Exception: {str(e)}")
            self.log(f"❌ API check error: {str(e)}")
            return False
    
    def calculate_overall_score(self):
        """Calculate overall system readiness score"""
        scores = {
            "PASS": 100,
            "PARTIAL": 75,
            "WARN": 50,
            "FAIL": 25,
            "ERROR": 0,
            "unknown": 0
        }
        
        total_score = 0
        component_count = 0
        
        for component in ["backend", "frontend", "database", "api"]:
            status = self.results[component]["status"]
            score = scores.get(status, 0)
            total_score += score
            component_count += 1
        
        if component_count > 0:
            overall_score = total_score / component_count
            self.results["overall"]["score"] = round(overall_score, 1)
            
            if overall_score >= 90:
                self.results["overall"]["status"] = "EXCELLENT"
            elif overall_score >= 75:
                self.results["overall"]["status"] = "GOOD"
            elif overall_score >= 50:
                self.results["overall"]["status"] = "FAIR"
            else:
                self.results["overall"]["status"] = "NEEDS_WORK"
    
    def generate_report(self):
        """Generate final verification report"""
        self.log("Generating verification report...")
        
        print("\n" + "="*60)
        print("HIPAA CHECKLIST PROJECT - SYSTEM VERIFICATION REPORT")
        print("="*60)
        print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Project Root: {self.project_root}")
        print()
        
        # Component status
        for component, data in self.results.items():
            if component == "overall":
                continue
                
            status_icon = {
                "PASS": "✅",
                "PARTIAL": "⚠️",
                "WARN": "⚠️", 
                "FAIL": "❌",
                "ERROR": "❌",
                "unknown": "❓"
            }.get(data["status"], "❓")
            
            print(f"{status_icon} {component.upper()}: {data['status']}")
            for detail in data["details"]:
                print(f"   • {detail}")
            print()
        
        # Overall status
        overall_status = self.results["overall"]["status"]
        overall_score = self.results["overall"]["score"]
        
        status_icon = {
            "EXCELLENT": "🎉",
            "GOOD": "✅",
            "FAIR": "⚠️",
            "NEEDS_WORK": "❌"
        }.get(overall_status, "❓")
        
        print(f"{status_icon} OVERALL STATUS: {overall_status} ({overall_score}%)")
        print()
        
        # Recommendations
        print("RECOMMENDATIONS:")
        if overall_score >= 90:
            print("🎉 System is ready for demonstration!")
            print("   • All components are working properly")
            print("   • You can proceed with confidence")
        elif overall_score >= 75:
            print("✅ System is mostly ready for demonstration")
            print("   • Minor issues may need attention")
            print("   • Test the system before presenting")
        elif overall_score >= 50:
            print("⚠️ System needs some work before demonstration")
            print("   • Address the issues identified above")
            print("   • Run the verification again after fixes")
        else:
            print("❌ System needs significant work")
            print("   • Fix the critical issues first")
            print("   • Consider using backup demonstration materials")
        
        print("\n" + "="*60)
        
        return overall_score >= 75
    
    def run_verification(self):
        """Run complete system verification"""
        self.log("Starting HIPAA Checklist Project system verification...")
        print("🔍 Verifying system components for final presentation...")
        print()
        
        # Run all checks
        self.check_backend()
        self.check_frontend()
        self.check_database()
        self.check_api_endpoints()
        
        # Calculate overall score
        self.calculate_overall_score()
        
        # Generate report
        is_ready = self.generate_report()
        
        return is_ready

def main():
    """Main verification function"""
    verifier = SystemVerifier()
    
    print("🚀 HIPAA CHECKLIST PROJECT - FINAL SYSTEM VERIFICATION")
    print("=" * 60)
    print("This script will verify all system components for your final presentation.")
    print()
    
    try:
        is_ready = verifier.run_verification()
        
        if is_ready:
            print("\n🎉 VERIFICATION COMPLETE - SYSTEM READY FOR DEMONSTRATION!")
            print("\nNext steps:")
            print("1. Start Django server: cd backend && python manage.py runserver")
            print("2. Start React app: cd frontend && npm start")
            print("3. Open browser to: http://localhost:3000")
            print("4. Use demo credentials: demo@example.com / demo123")
            print("5. Follow your 30-second demo flow!")
        else:
            print("\n⚠️ VERIFICATION COMPLETE - SYSTEM NEEDS ATTENTION")
            print("\nPlease address the issues above before your presentation.")
            print("Consider using backup demonstration materials if needed.")
        
        return is_ready
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Verification interrupted by user")
        return False
    except Exception as e:
        print(f"\n\n❌ Verification failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
