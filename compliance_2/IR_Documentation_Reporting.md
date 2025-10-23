# IR Documentation & Reporting

This document details incident response documentation and reporting for the Incident Response 1 rubric, including playbooks, tracking, reporting, and tool documentation.

---

## 1. Incident Response Playbook

**Purpose:** Step-by-step guide for responding to common incidents on Parrot OS.

**Example: Unauthorized Access Playbook**
1. Detect unauthorized access via Wazuh alert or log review.
2. Isolate affected host (disable network interface, apply firewall rules).
3. Collect evidence (logs, memory, disk image).
4. Analyze logs and correlate with other hosts.
5. Notify incident response lead and compliance officer.
6. Document all actions and findings.

**Tool-Specific Commands:**
- Network isolation: `sudo ifconfig eth0 down`
- Log collection: `cp /var/log/auth.log /evidence/`
- Memory dump: `sudo dd if=/dev/mem of=/evidence/mem.img bs=1M`
- Disk imaging: `sudo dd if=/dev/sda of=/evidence/disk.img bs=4M`

**Evidence Collection Steps:**
- Timestamp and label all files
- Store in /evidence directory
- Update chain of custody log

---

## 2. Incident Tracking System

**Tracking Template:**
| Incident ID | Date/Time           | Type              | Status    | Actions Taken                | Timeline Ref |
|-------------|---------------------|-------------------|-----------|------------------------------|--------------|
| IR-2025-001 | 2025-08-20 11:00:00 | Unauthorized Login| Closed    | Host isolated, evidence collected, report filed | T-001        |

**Details Documented:**
- Incident description
- Response actions
- Evidence collected
- Timeline of events
- Resolution and lessons learned

---

## 3. Complete Incident Report (Sample)

**Incident Report: IR-2025-001**
- **Date/Time:** 2025-08-20 11:00:00
- **Type:** Unauthorized Login Attempt
- **Detection:** Wazuh alert for failed SSH login on Parrot OS
- **Analysis:** Correlated with macOS logs, confirmed no successful compromise
- **Containment:** Network interface disabled, firewall rules applied
- **Evidence:** Collected logs, memory image, network capture
- **Timeline:**
  - 10:59:55: SSH connection from macOS
  - 11:00:00: Failed login on Parrot OS
  - 11:00:05: Wazuh alert triggered
  - 11:01:00: Host isolated
- **Resolution:** No compromise, host returned to service after review
- **Lessons Learned:** Strengthen password policy, enable MFA

---

## 4. IR Tools & Procedures Documentation (Parrot OS)

| Tool         | Purpose                        | Example Command/Usage                |
|--------------|-------------------------------|--------------------------------------|
| Wazuh Agent  | Log collection, alerting       | `sudo systemctl status wazuh-agent`  |
| Wireshark    | Network traffic capture        | `sudo wireshark` (GUI), `tcp port 22`|
| Volatility   | Memory analysis                | `volatility -f mem.img --profile=...`|
| tcpdump      | Network capture (CLI)          | `sudo tcpdump -i eth0 -w capture.pcap`|
| dd           | Disk/memory imaging            | `sudo dd if=/dev/sda of=disk.img`    |
| rsyslog      | Log forwarding                 | `/etc/rsyslog.conf`                  |

**Usage Explanations:**
- Each tool is documented with installation, configuration, and example usage.
- Procedures for evidence collection, analysis, and reporting are standardized and reviewed quarterly.

---

## 5. Summary Table

| Component            | Documentation/Evidence                                 |
|---------------------|--------------------------------------------------------|
| Playbook            | Step-by-step, tool commands, evidence steps             |
| Tracking System     | Template, incident details, timeline                    |
| Incident Report     | Complete sample, standard format                        |
| Tool Documentation  | Table, usage explanations, procedures                   |

---

**Appendix:**
- Attach playbook templates, tracking logs, and full incident reports as supporting evidence.
