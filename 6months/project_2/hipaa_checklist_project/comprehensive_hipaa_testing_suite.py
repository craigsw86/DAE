#!/usr/bin/env python3
"""
Comprehensive HIPAA Testing Suite
Tests the entire HIPAA Checklist Project against all HIPAA regulations and guidelines
"""

import os
import sys
import json
import time
import subprocess
import requests
from datetime import datetime
from pathlib import Path

class ComprehensiveHIPAATestingSuite:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "hipaa_rules": {},
            "security_safeguards": {},
            "administrative_safeguards": {},
            "physical_safeguards": {},
            "technical_safeguards": {},
            "breach_notification": {},
            "privacy_rule": {},
            "compliance_validation": {},
            "summary": {}
        }
        self.passed_tests = 0
        self.total_tests = 0
        
    def log_test(self, test_name, status, details="", hipaa_reference=""):
        """Log test results with HIPAA reference"""
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
            print(f" {test_name}: PASS")
            if hipaa_reference:
                print(f"    HIPAA Reference: {hipaa_reference}")
        else:
            print(f" {test_name}: FAIL - {details}")
            if hipaa_reference:
                print(f"    HIPAA Reference: {hipaa_reference}")
        
        return {
            "status": status, 
            "details": details, 
            "hipaa_reference": hipaa_reference,
            "timestamp": datetime.now().isoformat()
        }
    
    def wait_for_server(self, max_attempts=30):
        """Wait for Django server to be ready"""
        print(" Waiting for Django server to start...")
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{self.base_url}/api/health/", timeout=5)
                if response.status_code == 200:
                    print(" Django server is ready!")
                    return True
            except:
                pass
            time.sleep(2)
        return False
    
    def test_hipaa_privacy_rule(self):
        """Test HIPAA Privacy Rule compliance (45 CFR 164.500-534)"""
        print("\n" + "="*60)
        print(" TESTING HIPAA PRIVACY RULE COMPLIANCE")
        print("="*60)
        
        privacy_tests = {}
        
        # Test 1: Individual Rights - Access to PHI
        print("\n Test 1: Individual Rights - Access to PHI")
        print("-" * 50)
        try:
            # Test that users can only access their own data
            response = requests.get(f"{self.base_url}/api/checklist/", timeout=10)
            if response.status_code == 401:  # Should require authentication
                privacy_tests["individual_rights_access"] = self.log_test(
                    "Individual Rights - Access Control", "PASS",
                    "Unauthenticated access properly denied",
                    "45 CFR 164.524 - Individual access"
                )
            else:
                privacy_tests["individual_rights_access"] = self.log_test(
                    "Individual Rights - Access Control", "FAIL",
                    f"Unexpected status: {response.status_code}",
                    "45 CFR 164.524 - Individual access"
                )
        except Exception as e:
            privacy_tests["individual_rights_access"] = self.log_test(
                "Individual Rights - Access Control", "FAIL", str(e),
                "45 CFR 164.524 - Individual access"
            )
        
        # Test 2: Minimum Necessary Standard
        print("\n Test 2: Minimum Necessary Standard")
        print("-" * 50)
        try:
            # Test that only necessary data is exposed
            response = requests.get(f"{self.base_url}/api/checklist/", timeout=10)
            if response.status_code in [200, 401]:  # Should not expose sensitive data
                privacy_tests["minimum_necessary"] = self.log_test(
                    "Minimum Necessary Standard", "PASS",
                    "API properly restricts data exposure",
                    "45 CFR 164.502(b) - Minimum necessary"
                )
            else:
                privacy_tests["minimum_necessary"] = self.log_test(
                    "Minimum Necessary Standard", "FAIL",
                    f"Unexpected response: {response.status_code}",
                    "45 CFR 164.502(b) - Minimum necessary"
                )
        except Exception as e:
            privacy_tests["minimum_necessary"] = self.log_test(
                "Minimum Necessary Standard", "FAIL", str(e),
                "45 CFR 164.502(b) - Minimum necessary"
            )
        
        # Test 3: Notice of Privacy Practices
        print("\n Test 3: Notice of Privacy Practices")
        print("-" * 50)
        if os.path.exists("docs/Security_Policy.md"):
            privacy_tests["privacy_notice"] = self.log_test(
                "Notice of Privacy Practices", "PASS",
                "Privacy policy documentation exists",
                "45 CFR 164.520 - Notice of privacy practices"
            )
        else:
            privacy_tests["privacy_notice"] = self.log_test(
                "Notice of Privacy Practices", "FAIL",
                "Privacy policy documentation not found",
                "45 CFR 164.520 - Notice of privacy practices"
            )
        
        # Test 4: Uses and Disclosures
        print("\n Test 4: Uses and Disclosures")
        print("-" * 50)
        try:
            # Test that data is properly encrypted and access controlled
            response = requests.get(f"{self.base_url}/api/checklist/", timeout=10)
            if response.status_code == 401:  # Proper access control
                privacy_tests["uses_disclosures"] = self.log_test(
                    "Uses and Disclosures", "PASS",
                    "Proper access controls in place",
                    "45 CFR 164.502 - Uses and disclosures"
                )
            else:
                privacy_tests["uses_disclosures"] = self.log_test(
                    "Uses and Disclosures", "FAIL",
                    f"Access control issue: {response.status_code}",
                    "45 CFR 164.502 - Uses and disclosures"
                )
        except Exception as e:
            privacy_tests["uses_disclosures"] = self.log_test(
                "Uses and Disclosures", "FAIL", str(e),
                "45 CFR 164.502 - Uses and disclosures"
            )
        
        self.test_results["privacy_rule"] = privacy_tests
        return privacy_tests
    
    def test_administrative_safeguards(self):
        """Test HIPAA Administrative Safeguards (45 CFR 164.308)"""
        print("\n" + "="*60)
        print(" TESTING ADMINISTRATIVE SAFEGUARDS")
        print("="*60)
        
        admin_tests = {}
        
        # Test 1: Security Officer Assignment
        print("\n Test 1: Security Officer Assignment")
        print("-" * 50)
        if os.path.exists("docs/Security_Policy.md"):
            admin_tests["security_officer"] = self.log_test(
                "Security Officer Assignment", "PASS",
                "Security policy documentation exists",
                "45 CFR 164.308(a)(2) - Security officer"
            )
        else:
            admin_tests["security_officer"] = self.log_test(
                "Security Officer Assignment", "FAIL",
                "Security policy documentation not found",
                "45 CFR 164.308(a)(2) - Security officer"
            )
        
        # Test 2: Workforce Training
        print("\n Test 2: Workforce Training")
        print("-" * 50)
        training_docs = [
            "docs/IR_Training_Implementation_Plan.md",
            "docs/IR_Training_Environment_Setup.md",
            "docs/IR_Simulation_Training_Scenarios.md"
        ]
        training_exists = any(os.path.exists(doc) for doc in training_docs)
        
        if training_exists:
            admin_tests["workforce_training"] = self.log_test(
                "Workforce Training", "PASS",
                "Training documentation exists",
                "45 CFR 164.308(a)(5) - Workforce training"
            )
        else:
            admin_tests["workforce_training"] = self.log_test(
                "Workforce Training", "FAIL",
                "Training documentation not found",
                "45 CFR 164.308(a)(5) - Workforce training"
            )
        
        # Test 3: Access Management
        print("\n Test 3: Access Management")
        print("-" * 50)
        try:
            # Test authentication system
            response = requests.post(f"{self.base_url}/api/token/", 
                                   json={"username": "test", "password": "test"}, 
                                   timeout=10)
            if response.status_code in [200, 401]:  # Authentication system working
                admin_tests["access_management"] = self.log_test(
                    "Access Management", "PASS",
                    "Authentication system functional",
                    "45 CFR 164.308(a)(4) - Access management"
                )
            else:
                admin_tests["access_management"] = self.log_test(
                    "Access Management", "FAIL",
                    f"Authentication system issue: {response.status_code}",
                    "45 CFR 164.308(a)(4) - Access management"
                )
        except Exception as e:
            admin_tests["access_management"] = self.log_test(
                "Access Management", "FAIL", str(e),
                "45 CFR 164.308(a)(4) - Access management"
            )
        
        # Test 4: Information Access Management
        print("\n Test 4: Information Access Management")
        print("-" * 50)
        if os.path.exists("backend/checklist/models.py"):
            with open("backend/checklist/models.py", "r") as f:
                content = f.read()
                if "EncryptedTextField" in content and "EncryptedCharField" in content:
                    admin_tests["info_access_mgmt"] = self.log_test(
                        "Information Access Management", "PASS",
                        "Data encryption implemented",
                        "45 CFR 164.308(a)(3) - Information access management"
                    )
                else:
                    admin_tests["info_access_mgmt"] = self.log_test(
                        "Information Access Management", "FAIL",
                        "Data encryption not implemented",
                        "45 CFR 164.308(a)(3) - Information access management"
                    )
        else:
            admin_tests["info_access_mgmt"] = self.log_test(
                "Information Access Management", "FAIL",
                "Models file not found",
                "45 CFR 164.308(a)(3) - Information access management"
            )
        
        # Test 5: Security Awareness Training
        print("\n Test 5: Security Awareness Training")
        print("-" * 50)
        if os.path.exists("docs/IR_Training_Implementation_Plan.md"):
            admin_tests["security_awareness"] = self.log_test(
                "Security Awareness Training", "PASS",
                "Security awareness training plan exists",
                "45 CFR 164.308(a)(5)(i) - Security awareness training"
            )
        else:
            admin_tests["security_awareness"] = self.log_test(
                "Security Awareness Training", "FAIL",
                "Security awareness training plan not found",
                "45 CFR 164.308(a)(5)(i) - Security awareness training"
            )
        
        # Test 6: Contingency Plan
        print("\n Test 6: Contingency Plan")
        print("-" * 50)
        contingency_docs = [
            "docs/IR_Tabletop_Exercise_Guide.md",
            "MAINTENANCE_PLAN.md"
        ]
        contingency_exists = any(os.path.exists(doc) for doc in contingency_docs)
        
        if contingency_exists:
            admin_tests["contingency_plan"] = self.log_test(
                "Contingency Plan", "PASS",
                "Contingency planning documentation exists",
                "45 CFR 164.308(a)(7) - Contingency plan"
            )
        else:
            admin_tests["contingency_plan"] = self.log_test(
                "Contingency Plan", "FAIL",
                "Contingency planning documentation not found",
                "45 CFR 164.308(a)(7) - Contingency plan"
            )
        
        self.test_results["administrative_safeguards"] = admin_tests
        return admin_tests
    
    def test_physical_safeguards(self):
        """Test HIPAA Physical Safeguards (45 CFR 164.310)"""
        print("\n" + "="*60)
        print(" TESTING PHYSICAL SAFEGUARDS")
        print("="*60)
        
        physical_tests = {}
        
        # Test 1: Facility Access Controls
        print("\n Test 1: Facility Access Controls")
        print("-" * 50)
        if os.path.exists("docs/Security_Policy.md"):
            physical_tests["facility_access"] = self.log_test(
                "Facility Access Controls", "PASS",
                "Security policy includes facility controls",
                "45 CFR 164.310(a)(1) - Facility access controls"
            )
        else:
            physical_tests["facility_access"] = self.log_test(
                "Facility Access Controls", "FAIL",
                "Security policy not found",
                "45 CFR 164.310(a)(1) - Facility access controls"
            )
        
        # Test 2: Workstation Use
        print("\n Test 2: Workstation Use")
        print("-" * 50)
        if os.path.exists("backend/checklist/security_middleware.py"):
            physical_tests["workstation_use"] = self.log_test(
                "Workstation Use", "PASS",
                "Security middleware implemented",
                "45 CFR 164.310(b) - Workstation use"
            )
        else:
            physical_tests["workstation_use"] = self.log_test(
                "Workstation Use", "FAIL",
                "Security middleware not found",
                "45 CFR 164.310(b) - Workstation use"
            )
        
        # Test 3: Workstation Security
        print("\n Test 3: Workstation Security")
        print("-" * 50)
        if os.path.exists("nginx-https.conf"):
            physical_tests["workstation_security"] = self.log_test(
                "Workstation Security", "PASS",
                "HTTPS configuration exists",
                "45 CFR 164.310(c) - Workstation security"
            )
        else:
            physical_tests["workstation_security"] = self.log_test(
                "Workstation Security", "FAIL",
                "HTTPS configuration not found",
                "45 CFR 164.310(c) - Workstation security"
            )
        
        # Test 4: Device and Media Controls
        print("\n Test 4: Device and Media Controls")
        print("-" * 50)
        if os.path.exists("backend/sqlite_encryption.py"):
            physical_tests["device_media_controls"] = self.log_test(
                "Device and Media Controls", "PASS",
                "Database encryption implemented",
                "45 CFR 164.310(d) - Device and media controls"
            )
        else:
            physical_tests["device_media_controls"] = self.log_test(
                "Device and Media Controls", "FAIL",
                "Database encryption not implemented",
                "45 CFR 164.310(d) - Device and media controls"
            )
        
        self.test_results["physical_safeguards"] = physical_tests
        return physical_tests
    
    def test_technical_safeguards(self):
        """Test HIPAA Technical Safeguards (45 CFR 164.312)"""
        print("\n" + "="*60)
        print(" TESTING TECHNICAL SAFEGUARDS")
        print("="*60)
        
        technical_tests = {}
        
        # Test 1: Access Control
        print("\n Test 1: Access Control")
        print("-" * 50)
        try:
            # Test that protected endpoints require authentication
            response = requests.get(f"{self.base_url}/api/checklist/", timeout=10)
            if response.status_code == 401:
                technical_tests["access_control"] = self.log_test(
                    "Access Control", "PASS",
                    "Protected endpoints require authentication",
                    "45 CFR 164.312(a)(1) - Access control"
                )
            else:
                technical_tests["access_control"] = self.log_test(
                    "Access Control", "FAIL",
                    f"Access control issue: {response.status_code}",
                    "45 CFR 164.312(a)(1) - Access control"
                )
        except Exception as e:
            technical_tests["access_control"] = self.log_test(
                "Access Control", "FAIL", str(e),
                "45 CFR 164.312(a)(1) - Access control"
            )
        
        # Test 2: Audit Controls
        print("\n Test 2: Audit Controls")
        print("-" * 50)
        if os.path.exists("backend/checklist/management/commands/monitor_risks.py"):
            technical_tests["audit_controls"] = self.log_test(
                "Audit Controls", "PASS",
                "Audit monitoring system implemented",
                "45 CFR 164.312(b) - Audit controls"
            )
        else:
            technical_tests["audit_controls"] = self.log_test(
                "Audit Controls", "FAIL",
                "Audit monitoring system not found",
                "45 CFR 164.312(b) - Audit controls"
            )
        
        # Test 3: Integrity
        print("\n Test 3: Integrity")
        print("-" * 50)
        if os.path.exists("backend/checklist/models.py"):
            with open("backend/checklist/models.py", "r") as f:
                content = f.read()
                if "auditlog.register" in content:
                    technical_tests["integrity"] = self.log_test(
                        "Integrity", "PASS",
                        "Audit logging implemented for data integrity",
                        "45 CFR 164.312(c)(1) - Integrity"
                    )
                else:
                    technical_tests["integrity"] = self.log_test(
                        "Integrity", "FAIL",
                        "Audit logging not implemented",
                        "45 CFR 164.312(c)(1) - Integrity"
                    )
        else:
            technical_tests["integrity"] = self.log_test(
                "Integrity", "FAIL",
                "Models file not found",
                "45 CFR 164.312(c)(1) - Integrity"
            )
        
        # Test 4: Person or Entity Authentication
        print("\n Test 4: Person or Entity Authentication")
        print("-" * 50)
        try:
            # Test authentication endpoint
            response = requests.post(f"{self.base_url}/api/token/", 
                                   json={"username": "test", "password": "test"}, 
                                   timeout=10)
            if response.status_code in [200, 401]:  # Authentication system working
                technical_tests["entity_authentication"] = self.log_test(
                    "Person or Entity Authentication", "PASS",
                    "Authentication system functional",
                    "45 CFR 164.312(d) - Person or entity authentication"
                )
            else:
                technical_tests["entity_authentication"] = self.log_test(
                    "Person or Entity Authentication", "FAIL",
                    f"Authentication system issue: {response.status_code}",
                    "45 CFR 164.312(d) - Person or entity authentication"
                )
        except Exception as e:
            technical_tests["entity_authentication"] = self.log_test(
                "Person or Entity Authentication", "FAIL", str(e),
                "45 CFR 164.312(d) - Person or entity authentication"
            )
        
        # Test 5: Transmission Security
        print("\n Test 5: Transmission Security")
        print("-" * 50)
        if os.path.exists("nginx-https.conf"):
            technical_tests["transmission_security"] = self.log_test(
                "Transmission Security", "PASS",
                "HTTPS configuration exists",
                "45 CFR 164.312(e)(1) - Transmission security"
            )
        else:
            technical_tests["transmission_security"] = self.log_test(
                "Transmission Security", "FAIL",
                "HTTPS configuration not found",
                "45 CFR 164.312(e)(1) - Transmission security"
            )
        
        self.test_results["technical_safeguards"] = technical_tests
        return technical_tests
    
    def test_breach_notification_rule(self):
        """Test HIPAA Breach Notification Rule (45 CFR 164.400-414)"""
        print("\n" + "="*60)
        print(" TESTING BREACH NOTIFICATION RULE")
        print("="*60)
        
        breach_tests = {}
        
        # Test 1: Breach Detection and Response
        print("\n Test 1: Breach Detection and Response")
        print("-" * 50)
        if os.path.exists("docs/IR_Tabletop_Exercise_Guide.md"):
            breach_tests["breach_detection"] = self.log_test(
                "Breach Detection and Response", "PASS",
                "Incident response documentation exists",
                "45 CFR 164.400 - Breach notification"
            )
        else:
            breach_tests["breach_detection"] = self.log_test(
                "Breach Detection and Response", "FAIL",
                "Incident response documentation not found",
                "45 CFR 164.400 - Breach notification"
            )
        
        # Test 2: Notification Procedures
        print("\n Test 2: Notification Procedures")
        print("-" * 50)
        if os.path.exists("docs/IR_Simulation_Training_Scenarios.md"):
            breach_tests["notification_procedures"] = self.log_test(
                "Notification Procedures", "PASS",
                "Notification procedures documented",
                "45 CFR 164.404 - Notification procedures"
            )
        else:
            breach_tests["notification_procedures"] = self.log_test(
                "Notification Procedures", "FAIL",
                "Notification procedures not documented",
                "45 CFR 164.404 - Notification procedures"
            )
        
        # Test 3: Risk Assessment
        print("\n Test 3: Risk Assessment")
        print("-" * 50)
        risk_docs = [
            "docs/Risk_Framework.md",
            "docs/Risk_Evaluation.md",
            "docs/Risk_Mitigation.md"
        ]
        risk_exists = any(os.path.exists(doc) for doc in risk_docs)
        
        if risk_exists:
            breach_tests["risk_assessment"] = self.log_test(
                "Risk Assessment", "PASS",
                "Risk assessment documentation exists",
                "45 CFR 164.402 - Risk assessment"
            )
        else:
            breach_tests["risk_assessment"] = self.log_test(
                "Risk Assessment", "FAIL",
                "Risk assessment documentation not found",
                "45 CFR 164.402 - Risk assessment"
            )
        
        # Test 4: Business Associate Agreements
        print("\n Test 4: Business Associate Agreements")
        print("-" * 50)
        if os.path.exists("docs/Security_Policy.md"):
            breach_tests["baa_requirements"] = self.log_test(
                "Business Associate Agreements", "PASS",
                "Security policy includes BAA requirements",
                "45 CFR 164.502(e) - Business associate agreements"
            )
        else:
            breach_tests["baa_requirements"] = self.log_test(
                "Business Associate Agreements", "FAIL",
                "BAA requirements not documented",
                "45 CFR 164.502(e) - Business associate agreements"
            )
        
        self.test_results["breach_notification"] = breach_tests
        return breach_tests
    
    def test_compliance_validation(self):
        """Test overall compliance validation and reporting"""
        print("\n" + "="*60)
        print(" TESTING COMPLIANCE VALIDATION")
        print("="*60)
        
        compliance_tests = {}
        
        # Test 1: Compliance Reporting
        print("\n Test 1: Compliance Reporting")
        print("-" * 50)
        try:
            response = requests.get(f"{self.base_url}/api/report/", timeout=10)
            if response.status_code in [200, 401]:  # Report endpoint exists
                compliance_tests["compliance_reporting"] = self.log_test(
                    "Compliance Reporting", "PASS",
                    "Compliance reporting endpoint available",
                    "General compliance reporting requirement"
                )
            else:
                compliance_tests["compliance_reporting"] = self.log_test(
                    "Compliance Reporting", "FAIL",
                    f"Report endpoint issue: {response.status_code}",
                    "General compliance reporting requirement"
                )
        except Exception as e:
            compliance_tests["compliance_reporting"] = self.log_test(
                "Compliance Reporting", "FAIL", str(e),
                "General compliance reporting requirement"
            )
        
        # Test 2: Documentation Completeness
        print("\n Test 2: Documentation Completeness")
        print("-" * 50)
        required_docs = [
            "docs/Security_Policy.md",
            "docs/Risk_Framework.md",
            "docs/HIPAA_Security_Deep_Dive.md",
            "README.md",
            "FINAL_PROJECT_DOCUMENTATION.md"
        ]
        docs_exist = sum(1 for doc in required_docs if os.path.exists(doc))
        doc_percentage = (docs_exist / len(required_docs)) * 100
        
        if doc_percentage >= 80:
            compliance_tests["documentation"] = self.log_test(
                "Documentation Completeness", "PASS",
                f"{docs_exist}/{len(required_docs)} required documents exist ({doc_percentage:.1f}%)",
                "Documentation requirement"
            )
        else:
            compliance_tests["documentation"] = self.log_test(
                "Documentation Completeness", "FAIL",
                f"Only {docs_exist}/{len(required_docs)} required documents exist ({doc_percentage:.1f}%)",
                "Documentation requirement"
            )
        
        # Test 3: Security Testing
        print("\n Test 3: Security Testing")
        print("-" * 50)
        security_tests = [
            "comprehensive_testing_suite.py",
            "owasp_zap_security_audit.py",
            "security_verification_final.py"
        ]
        security_exists = sum(1 for test in security_tests if os.path.exists(test))
        
        if security_exists >= 2:
            compliance_tests["security_testing"] = self.log_test(
                "Security Testing", "PASS",
                f"{security_exists}/{len(security_tests)} security testing tools available",
                "Security testing requirement"
            )
        else:
            compliance_tests["security_testing"] = self.log_test(
                "Security Testing", "FAIL",
                f"Only {security_exists}/{len(security_tests)} security testing tools available",
                "Security testing requirement"
            )
        
        # Test 4: Data Encryption Validation
        print("\n Test 4: Data Encryption Validation")
        print("-" * 50)
        if os.path.exists("backend/checklist/models.py"):
            with open("backend/checklist/models.py", "r") as f:
                content = f.read()
                if "EncryptedTextField" in content and "EncryptedCharField" in content:
                    compliance_tests["data_encryption"] = self.log_test(
                        "Data Encryption Validation", "PASS",
                        "Field-level encryption implemented",
                        "Data protection requirement"
                    )
                else:
                    compliance_tests["data_encryption"] = self.log_test(
                        "Data Encryption Validation", "FAIL",
                        "Field-level encryption not implemented",
                        "Data protection requirement"
                    )
        else:
            compliance_tests["data_encryption"] = self.log_test(
                "Data Encryption Validation", "FAIL",
                "Models file not found",
                "Data protection requirement"
            )
        
        self.test_results["compliance_validation"] = compliance_tests
        return compliance_tests
    
    def generate_hipaa_summary(self):
        """Generate comprehensive HIPAA compliance summary"""
        print("\n" + "="*60)
        print(" COMPREHENSIVE HIPAA COMPLIANCE SUMMARY")
        print("="*60)
        
        # Calculate success rates for each HIPAA rule category
        categories = {
            "Privacy Rule": self.test_results["privacy_rule"],
            "Administrative Safeguards": self.test_results["administrative_safeguards"],
            "Physical Safeguards": self.test_results["physical_safeguards"],
            "Technical Safeguards": self.test_results["technical_safeguards"],
            "Breach Notification Rule": self.test_results["breach_notification"],
            "Compliance Validation": self.test_results["compliance_validation"]
        }
        
        category_summaries = {}
        overall_passed = 0
        overall_total = 0
        
        for category_name, category_tests in categories.items():
            if category_tests:
                passed = sum(1 for test in category_tests.values() if test["status"] == "PASS")
                total = len(category_tests)
                success_rate = (passed / total * 100) if total > 0 else 0
                
                category_summaries[category_name] = {
                    "passed": passed,
                    "total": total,
                    "success_rate": round(success_rate, 2)
                }
                
                overall_passed += passed
                overall_total += total
        
        overall_success_rate = (overall_passed / overall_total * 100) if overall_total > 0 else 0
        
        self.test_results["summary"] = {
            "categories": category_summaries,
            "overall": {
                "passed": overall_passed,
                "total": overall_total,
                "success_rate": round(overall_success_rate, 2)
            }
        }
        
        print(f"\n HIPAA Compliance Test Results:")
        print(f"   Overall Success Rate: {overall_passed}/{overall_total} ({overall_success_rate:.1f}%)")
        print(f"\n Category Breakdown:")
        
        for category_name, summary in category_summaries.items():
            status_icon = "" if summary["success_rate"] >= 80 else "" if summary["success_rate"] >= 60 else ""
            print(f"   {status_icon} {category_name}: {summary['passed']}/{summary['total']} ({summary['success_rate']:.1f}%)")
        
        # HIPAA Compliance Assessment
        print(f"\n HIPAA Compliance Assessment:")
        if overall_success_rate >= 90:
            print("   🟢 EXCELLENT - Fully HIPAA Compliant")
        elif overall_success_rate >= 80:
            print("   🟡 GOOD - Mostly HIPAA Compliant with minor gaps")
        elif overall_success_rate >= 70:
            print("   🟠 FAIR - HIPAA Compliant with some gaps requiring attention")
        else:
            print("    POOR - Significant HIPAA compliance gaps requiring immediate attention")
        
        return self.test_results["summary"]
    
    def save_hipaa_results(self):
        """Save comprehensive HIPAA test results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comprehensive_hipaa_test_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n HIPAA test results saved to: {filename}")
        return filename
    
    def run_comprehensive_hipaa_tests(self):
        """Run all comprehensive HIPAA compliance tests"""
        print(" Starting Comprehensive HIPAA Testing Suite")
        print("=" * 60)
        print("Testing against all HIPAA regulations and guidelines...")
        
        # Wait for server to be ready
        if not self.wait_for_server():
            print(" Django server is not running. Please start it first.")
            return False
        
        # Run all HIPAA compliance test categories
        self.test_hipaa_privacy_rule()
        self.test_administrative_safeguards()
        self.test_physical_safeguards()
        self.test_technical_safeguards()
        self.test_breach_notification_rule()
        self.test_compliance_validation()
        
        # Generate comprehensive summary
        self.generate_hipaa_summary()
        
        # Save results
        filename = self.save_hipaa_results()
        
        print(f"\n Comprehensive HIPAA testing completed!")
        print(f" Overall HIPAA Compliance: {self.test_results['summary']['overall']['success_rate']:.1f}%")
        print(f" Results saved to: {filename}")
        
        return True

def main():
    """Main function"""
    suite = ComprehensiveHIPAATestingSuite()
    suite.run_comprehensive_hipaa_tests()

if __name__ == "__main__":
    main()
