# Security Playbooks

## Purpose
To provide step-by-step, actionable guides for responding to common security incidents in the HIPAA Checklist project.

## Scope
These playbooks apply to all staff involved in incident response and system administration.

---

## Playbook 1: Data Breach

**Objective:** Contain and remediate a data breach involving PHI/PII.

| Step | Action | Responsible | Evidence/Tool |
|------|--------|-------------|--------------|
| 1 | Detect breach via monitoring tool (e.g., Wazuh alert, Django auditlog) | SOC Analyst | ![Wazuh alert screenshot](screenshots/wazuh_alert.png) |
| 2 | Contain affected systems (disable accounts, block IPs) | System Admin | `sudo ufw deny from <ip>` |
| 3 | Collect and preserve logs, screenshots, and other evidence | System Admin | Archive logs, screenshots |
| 4 | Notify Compliance Officer and begin IRP steps | SOC Analyst | Email notification |
| 5 | Notify affected users and authorities as required | Compliance Officer | Notification template |

**Log Example:**
```
[2024-06-01 12:34:56] Wazuh alert: Data exfiltration detected from 192.168.1.100
```

---

## Playbook 2: Ransomware Attack

**Objective:** Isolate, eradicate, and recover from a ransomware infection.

| Step | Action | Responsible | Evidence/Tool |
|------|--------|-------------|--------------|
| 1 | Isolate infected machines from the network | System Admin | Disconnect network cable, disable Wi-Fi |
| 2 | Do NOT pay ransom; preserve evidence | All | Archive ransom note, affected files |
| 3 | Restore from clean backups | System Admin | Backup logs, restoration logs |
| 4 | Notify Compliance Officer and authorities | System Admin | Email notification |
| 5 | Review and update backup and patching policies | Security Officer | Updated policy document |

**Log Example:**
```
[2024-06-01 13:00:00] Ransomware detected on server-2. Machine isolated.
```

---

## Playbook 3: Unauthorized Access

**Objective:** Contain and remediate unauthorized access to the system.

| Step | Action | Responsible | Evidence/Tool |
|------|--------|-------------|--------------|
| 1 | Disable compromised accounts immediately | System Admin | Django admin, user management logs |
| 2 | Review access logs for scope of breach | SOC Analyst | Auditlog, Wazuh logs |
| 3 | Change all relevant passwords and keys | System Admin | Password change logs |
| 4 | Notify Compliance Officer and affected users | SOC Analyst | Email notification |
| 5 | Conduct post-incident review and update access controls | Security Officer | Updated access control policy |

**Log Example:**
```
[2024-06-01 14:10:00] Unauthorized login detected for user 'bob'.
```

---

*Each playbook references the Incident Response Plan and includes evidence collection, notification, and post-incident review steps. Screenshots and log excerpts should be attached for each real incident.*