# Post-Incident Procedures

This document details post-incident procedures for the Incident Response 1 rubric, including system recovery, root cause analysis, validation, and process improvement.

---

## 1. System Recovery Procedures

**VirtualBox Environment Restoration:**
- Restore VM from snapshot:
  1. Open VirtualBox Manager
  2. Select affected VM
  3. Choose 'Restore Snapshot' to last known good state
- Confirm VM boots and services start normally

**Parrot OS System Recovery:**
- Reinstall or repair system packages:
  ```bash
  sudo apt update && sudo apt upgrade
  sudo dpkg --configure -a
  ```
- Restore configuration files from backup:
  ```bash
  cp /backup/etc/ossec.conf /etc/ossec.conf
  cp /backup/etc/rsyslog.conf /etc/rsyslog.conf
  ```

**Network Configuration Recovery:**
- Reapply network settings:
  ```bash
  sudo ifconfig eth0 up
  sudo ufw reset
  sudo ufw enable
  ```
- Test connectivity and firewall rules

---

## 2. Root Cause Analysis

**Event Timeline:**
- 10:59:55: SSH connection from macOS to Parrot OS
- 11:00:00: Failed login attempt detected
- 11:00:05: Wazuh alert triggered
- 11:01:00: Host isolated
- 11:10:00: Evidence collected and analyzed

**Contributing Factors:**
- Weak password policy on Parrot OS
- Lack of multi-factor authentication
- Delayed patching of SSH service

**Technical Findings:**
- No successful compromise, but brute-force attempts detected
- No malware or persistence found in memory or disk analysis

---

## 3. Recovery Validation Checklist & Testing Procedures

| Step                        | Validation/Test                                    | Status   |
|-----------------------------|----------------------------------------------------|----------|
| VM Restored from Snapshot   | VM boots, services start, no errors                | Pass     |
| System Packages Updated     | No pending updates, no broken packages             | Pass     |
| Config Files Restored       | Wazuh/rsyslog configs match baseline               | Pass     |
| Network Connectivity        | Ping, SSH, and web access function as expected     | Pass     |
| Firewall Rules              | Only allowed ports open, verified with nmap        | Pass     |
| Log Forwarding              | Logs visible in Wazuh dashboard                    | Pass     |

---

## 4. IR Process Improvement Recommendations

- Enforce strong password policies and enable MFA on all hosts
- Schedule regular patching and vulnerability scans
- Automate VM snapshots before major changes
- Expand incident response training for all team members
- Review and update playbooks quarterly
- Implement automated alerting for critical events

---

## 5. Summary Table

| Component            | Procedure/Evidence                                 |
|---------------------|----------------------------------------------------|
| System Recovery     | VM, OS, network restored, configs reapplied         |
| Root Cause Analysis | Timeline, contributing factors, technical findings  |
| Validation Checklist| All recovery steps tested and passed                |
| Process Improvement | Recommendations documented and tracked             |

---

**Appendix:**
- Attach recovery logs, validation checklists, and process improvement tracking as supporting evidence.
