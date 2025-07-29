# Incident Response Plan (IRP)

## Purpose
This document outlines the steps to take in the event of a security incident affecting the HIPAA Checklist Web Application.

## Incident Types
- Data breach (PHI/PII exposure)
- Unauthorized access
- Ransomware or malware infection
- Service outage or DoS attack
- Insider threat

## Response Steps
1. **Detection & Reporting**
   - Identify and report the incident to the security team.
   - Log all relevant details (time, affected systems, users, etc.).
2. **Containment**
   - Isolate affected systems (e.g., take server offline).
   - Change passwords/keys if needed.
3. **Eradication**
   - Remove malware or unauthorized access.
   - Patch vulnerabilities.
4. **Recovery**
   - Restore from backups if needed.
   - Monitor for further suspicious activity.
5. **Notification**
   - Notify affected users and regulatory bodies (if PHI/PII is involved).
6. **Post-Incident Review**
   - Document lessons learned and update policies.

## Roles & Responsibilities
- **Incident Response Lead:** Coordinates all response activities.
- **System Admin:** Performs technical containment and recovery.
- **Compliance Officer:** Handles regulatory notifications.
- **Communications:** Manages user and public communications.

## Incident Response Framework
1. **Preparation**: Establish policies, train staff, and set up monitoring.
2. **Identification**: Detect and report incidents.
3. **Containment**: Isolate affected systems to prevent spread.
4. **Eradication**: Remove the cause of the incident (e.g., malware).
5. **Recovery**: Restore systems and resume normal operations.

## Digital Forensics
- **Forensic Tool Used:** log2timeline (or Windows Event Viewer, Linux auditd, etc.)
- **Example:** Collected and analyzed system logs from the server to determine the timeline of a suspected breach.

## Evidence Collection
- **Log Files:** Downloaded and archived Django server logs.
- **Screenshots:** Captured screenshots of suspicious admin panel activity.
- **Chain of Custody:** Each piece of evidence was timestamped, labeled, and stored in a secure, access-controlled folder. Access was logged and only authorized personnel could retrieve evidence.

## Incident Triage and Prioritization
| Incident Type         | Severity   | Business Impact         |
|-----------------------|------------|------------------------|
| Data Breach           | High       | Regulatory, reputation |
| Ransomware Infection  | Critical   | Service outage, loss   |
| Unauthorized Access   | Medium     | Data integrity         |

## Post-Incident Analysis
- **Summary:**  
  After a simulated unauthorized access incident, logs were reviewed and the account was disabled. No data was exfiltrated.
- **Lessons Learned:**  
  1. Multi-factor authentication should be enabled for all admin accounts.
  2. Regular log reviews help detect suspicious activity early.

## Contact Information
- Security Team: security@example.com
- Compliance Officer: compliance@example.com
- IT Support: support@example.com