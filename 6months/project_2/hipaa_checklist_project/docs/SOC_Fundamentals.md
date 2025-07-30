SOC_Fundamentals.md
Security Operations Center (SOC) Fundamentals
Purpose
To outline the structure, roles, monitoring practices, and incident response fundamentals of a Security Operations Center (SOC) as applied to the HIPAA Checklist project.
1. SOC Overview
A Security Operations Center (SOC) is a centralized unit that deals with security issues on an organizational and technical level. The SOC is responsible for monitoring, detecting, responding to, and mitigating security threats in real time.
2. SOC Roles and Responsibilities
Role	Responsibilities
SOC Analyst	Monitors security dashboards, investigates alerts, performs initial triage
Incident Responder	Takes action on confirmed incidents, contains threats, coordinates with IT
SOC Manager	Oversees SOC operations, manages staff, ensures incident response procedures
3. Monitoring Fundamentals
Tools Used:
Wazuh agent for log and file integrity monitoring
Django auditlog for application-level monitoring
Monitored Activities:
Authentication Events:
Login attempts (success/failure), password changes
Example log:
File Integrity Monitoring:
Changes to critical system or application files
Example log:
4. Alert Management
Alert 1: Multiple failed login attempts detected by Wazuh
Investigation: Analyst reviews logs, identifies brute-force attempt
Resolution: Source IP blocked at firewall
Evidence:
!Wazuh alert screenshot
Alert 2: Unauthorized modification of a sensitive file
Investigation: Analyst confirms unauthorized change
Resolution: File restored from backup, user access reviewed
Evidence:
!File integrity alert screenshot
5. Threat Detection Example
Threat Identified: Suspicious outbound network connection from application server
Detection: Wazuh network monitoring flagged the connection
Response: Incident responder investigated, found malware attempting data exfiltration. Malware removed, system patched.
Log Example:
6. SOC Reporting and Continuous Improvement
All incidents and alerts are documented in the SOC incident tracking system.
Weekly and monthly reports are generated for management review.
Lessons learned from incidents are used to update playbooks and improve monitoring rules.
This document demonstrates SOC fundamentals, including roles, monitoring, alert management, and threat detection, as applied in the HIPAA Checklist project. Screenshots and log excerpts should be attached for each real incident.