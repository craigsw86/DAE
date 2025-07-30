# Security Policy and Governance

## Purpose
To define the security policies and governance structure for the HIPAA Checklist project, ensuring the confidentiality, integrity, and availability of sensitive data.

## Scope
This policy applies to all users, systems, and data associated with the HIPAA Checklist project.

## Policy Development Framework

This document outlines the security policies for the HIPAA Checklist, covering:

### 1. Access Control Policy
- All users must authenticate using unique credentials (username and password).
- Access to sensitive data is restricted based on user roles (e.g., admin, user).
- Multi-factor authentication (MFA) is required for admin accounts.
- Example enforcement:
  - Django permissions restrict access to admin-only data.
  - MFA is enforced using Django Allauth with TOTP.
- Unauthorized access attempts are logged and reviewed weekly.
- Policy reference: NIST CSF PR.AC-1, PR.AC-4

### 2. Data Protection Policy
- All sensitive data is encrypted at rest using field-level encryption (`django-encrypted-model-fields`).
- Data in transit is protected using HTTPS enforced by Nginx and Django settings.
- Regular backups are performed and stored securely offsite.
- Example enforcement:
  - Encryption key is managed via environment variables.
  - Backups are encrypted and stored in AWS S3 with restricted access.
- Policy reference: NIST CSF PR.DS-1, PR.DS-2

### 3. System Use Policy
- Users must not share their credentials.
- System use is monitored and logged using Django auditlog and Wazuh agent.
- Unauthorized use of the system is prohibited and may result in disciplinary action, up to and including termination.
- Example enforcement:
  - Weekly log review by Security Officer.
  - Automated alerts for suspicious activity.
- Policy reference: NIST CSF PR.PT-1, DE.CM-7

## Governance Structure

| Role               | Responsibilities                                      |
|--------------------|------------------------------------------------------|
| Security Officer   | Policy enforcement, periodic review, incident lead   |
| System Admin       | Implements controls, monitors compliance, backups    |
| Compliance Officer | Ensures regulatory alignment, handles notifications  |
| All Users          | Adhere to policies, report violations                |

- Escalation: Policy violations are reported to the Security Officer, who investigates and escalates to management as needed.

## Compliance Requirements

This policy is designed to align with the following security standard:
- **NIST Cybersecurity Framework (NIST CSF)**
  - PR.AC: Access Control
  - PR.DS: Data Security
  - PR.PT: Protective Technology
  - DE.CM: Security Continuous Monitoring

## Policy Implementation

- Policies are communicated to all users during onboarding and via periodic training.
- Access controls are enforced through Django authentication and permissions.
- Data protection is implemented via encrypted fields and HTTPS configuration.
- System use is monitored through application logs, auditlog, and Wazuh agent.
- Compliance is reviewed quarterly by the Security Officer.
- Example:  
  ![Policy training screenshot](screenshots/policy_training.png)
  ![Auditlog review screenshot](screenshots/auditlog_review.png)

## Review and Updates

- This policy is reviewed annually or after any major incident.
- Updates are approved by the Security Officer and communicated to all users.

---

*This document demonstrates the development, governance, compliance, and implementation of security policies for the HIPAA Checklist project, with specific references to NIST CSF controls and real-world enforcement examples.*