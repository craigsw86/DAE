# Incident Detection and Analysis

This document details the detection and analysis of security incidents for the Incident Response 1 rubric, including log analysis, incident investigation, classification, and findings.

---

## 1. Log Analysis Methodology

- Centralized log collection using Wazuh SIEM from both Parrot OS and macOS hosts.
- Automated alerting for suspicious events (e.g., failed logins, privilege escalation, new user creation).
- Manual review of logs in Wazuh dashboard for correlation and context.
- Use of timeline analysis to reconstruct events.

---

## 2. Parrot OS and macOS Log Analysis (Wazuh)

**Parrot OS:**
- Monitored `/var/log/auth.log` and `/var/log/syslog` for authentication and system events.
- Example alert: `2025-08-20 11:00:00 - Failed SSH login detected from 192.168.56.102`.

**macOS:**
- Monitored system.log and auth.log via remote syslog forwarding.
- Example alert: `2025-08-20 11:01:00 - Unusual login detected from Parrot OS IP`.

**Evidence:**
- Screenshot: Wazuh dashboard showing both Parrot OS and macOS logs (attach as needed).

---

## 3. Suspicious Login Investigation

**Incident:** Suspicious login attempt detected on Parrot OS.

**Steps:**
1. Wazuh alert triggered for failed SSH login on Parrot OS.
2. Correlated with macOS logs showing outbound SSH connection at the same timestamp.
3. Created event timeline:
   - 10:59:55: SSH connection initiated from macOS (192.168.56.101) to Parrot OS (192.168.56.102)
   - 11:00:00: Failed login attempt on Parrot OS
   - 11:00:05: Alert generated in Wazuh
4. Validated alert by reviewing both host logs and confirming no successful login.

**Evidence:**
- Log excerpts from both systems
- Timeline diagram (attach as needed)

---

## 4. Incident Classification (Severity Matrix)

| Incident Type         | Severity   | Description                                 |
|----------------------|------------|---------------------------------------------|
| Failed SSH Login     | Medium     | Multiple failed attempts, no compromise     |
| New User Creation    | High       | Unauthorized account added                  |
| Sudo Command Abuse   | Critical   | Privilege escalation, potential compromise  |

**Classification based on taught severity matrix (impact, likelihood, business risk).**

---

## 5. Findings and Security Implications

- Multiple failed SSH logins indicate possible brute-force attempt; no successful compromise detected.
- Unauthorized user creation would allow persistent access; immediate remediation required.
- Sudo command abuse could lead to full system compromise; triggers critical alert and incident response.

**Security Implications:**
- Need for strong password policies and multi-factor authentication.
- Continuous monitoring and alerting are essential for early detection.
- Incident response procedures must be followed for high/critical events.

---

## 6. Summary Table

| Component                | Evidence/Status                                 |
|-------------------------|-------------------------------------------------|
| Log Analysis            | Wazuh dashboard, log correlation, timeline      |
| Suspicious Login        | Investigated, timeline created, alert validated |
| Incident Classification | 3 incidents classified with severity matrix     |
| Findings                | Documented, security implications addressed     |

---

**Appendix:**
- Attach log excerpts, screenshots, and timeline diagrams as supporting evidence.
