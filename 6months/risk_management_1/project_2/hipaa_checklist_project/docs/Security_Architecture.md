# Security Architecture and Advanced Defense Strategies

## Overview
This document outlines the security architecture for the HIPAA Checklist project, highlighting layered defenses, audit logging, encryption, and incident response.

## Architecture Diagram
```mermaid
graph TD;
  User["User (Browser/React)"] -->|HTTPS/JWT| DjangoAPI["Django API (Backend)"]
  DjangoAPI -->|Encrypted Fields| DB[(Database)]
  DjangoAPI -->|Audit Log| Auditlog["Audit Log"]
  DjangoAPI -->|Logs| Wazuh["Wazuh Agent"]
  DjangoAPI -->|Reverse Proxy| Nginx[Nginx (HTTPS)]
  Nginx -->|Firewall| Internet
```

## Security Layers Summary
| Layer         | Control/Technology                | Purpose                                    |
|--------------|-----------------------------------|--------------------------------------------|
| Network      | Nginx, Firewall                   | HTTPS, restrict ports, reverse proxy       |
| Application  | Django, JWT, Permissions          | Auth, access control, audit logging        |
| Data         | Encrypted Model Fields            | Encrypt sensitive data at rest             |
| Monitoring   | Wazuh, django-auditlog            | Log review, alerting, incident response    |

## Zero Trust Architecture
- **Backend (Django) Authentication:** All sensitive API endpoints require JWT authentication.
- **Frontend (React) Route Protection:** React checks for a valid JWT before rendering protected routes.
- **Unauthorized access attempts** are logged and result in a 401 error.

## Defense in Depth
- **Network Layer:**
  - Nginx reverse proxy enforces HTTPS.
  - Firewall restricts to ports 80/443.
- **Application Layer:**
  - Django settings enforce security (e.g., `SECURE_SSL_REDIRECT`, `CSRF_COOKIE_SECURE`).
  - Only authenticated users can access sensitive endpoints.
- **Data Layer:**
  - Sensitive fields use `django-encrypted-model-fields`.
  - Encryption key is stored securely in environment variables.

## Supply Chain Security
- Dependencies are checked monthly using `pip-audit` and `npm audit`.
- Vulnerabilities are remediated promptly.

## Advanced Security Model: Bell-LaPadula
- Enforces data confidentiality by restricting information flow based on security levels.
- Example: Only superusers or compliance admins can change regulations in Django admin.

## Incident Response & Log Review
- All system and security events are logged using django-auditlog and Wazuh agent.
- Incident response follows the documented playbooks (see `Security_Playbooks.md`).
- Example log review:
  - Weekly review by Security Officer.
  - Automated alerts for suspicious activity.

## Best Practices
- Use strong, unique passwords and enable MFA for admin accounts.
- Regularly review audit logs and system alerts.
- Keep all dependencies up to date.
- Enforce least privilege for all users and services.

## References
- [Security_Policy.md](Security_Policy.md)
- [Security_Playbooks.md](Security_Playbooks.md)
- [Incident_Response_Plan.md](Incident_Response_Plan.md)
- [API.md](API.md)

---
*This document demonstrates the application of advanced cybersecurity defense strategies in the HIPAA Checklist project, with specific technical controls, configuration examples, and references to logs and monitoring outputs.*