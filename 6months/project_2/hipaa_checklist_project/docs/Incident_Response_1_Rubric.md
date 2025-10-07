# Incident Response 1 – Project Rubric

This rubric outlines the requirements for incident response environment setup, detection, containment, evidence management, documentation, and post-incident procedures. Each criterion must be met at an advanced level for full credit.

---

## Grading Scale
- **1:** Complete
- **0:** Incomplete

---

## Criteria

### 1. IR Environment Setup
- Demonstrate successful installation and configuration of Wazuh SIEM platform on Parrot OS (VirtualBox)
- Evidence of basic agent deployment and log collection from Parrot OS
- Creation of 3 custom alert rules for security events
- Wireshark configuration on Parrot OS with proper capture filters
- Volatility framework setup in Parrot OS with memory analysis configuration
- System logging for both Parrot OS and macOS, with evidence of successful ingestion into Wazuh dashboard
- All configurations must include documentation and evidence of functionality

| Criterion | Complete (1) | Incomplete (0) |
|-----------|:-----------:|:--------------:|
| IR Environment Setup |          |            |

---

### 2. Incident Detection and Analysis
- Analysis of both Parrot OS and macOS logs using Wazuh
- Documented analysis methodology and findings
- Detailed investigation of 1 suspicious login attempt, showing log correlation, event timeline, and alert validation
- Classification of 3 distinct security incidents using severity matrix
- Clear documentation of methodologies and security implications

| Criterion | Complete (1) | Incomplete (0) |
|-----------|:-----------:|:--------------:|
| Incident Detection and Analysis |          |            |

---

### 3. Incident Response and Containment
- Demonstrate network isolation procedures in Parrot OS (interface config, firewall rules, VirtualBox segmentation)
- Evidence preservation using Parrot OS forensic tools (file system, network, memory)
- Containment playbook with host isolation, network blocking, and service shutdown steps
- Documentation and evidence of all implementations

| Criterion | Complete (1) | Incomplete (0) |
|-----------|:-----------:|:--------------:|
| Incident Response and Containment |          |            |

---

### 4. Digital Evidence Management
- Live data collection from Parrot OS (system state, processes, network connections)
- Memory analysis using Volatility in Parrot OS
- Disk acquisition using Parrot OS imaging tools
- Chain of custody documentation for all evidence
- Timeline creation with macOS and Parrot OS logs and event analysis

| Criterion | Complete (1) | Incomplete (0) |
|-----------|:-----------:|:--------------:|
| Digital Evidence Management |          |            |

---

### 5. IR Documentation & Reporting
- Incident response playbook with response procedures, tool-specific commands, and evidence collection steps
- Incident tracking system documenting incident details, response actions, and event timeline
- Complete incident report for 1 security event (standard format)
- Documentation of all IR tools and procedures in Parrot OS with clear usage explanations

| Criterion | Complete (1) | Incomplete (0) |
|-----------|:-----------:|:--------------:|
| IR Documentation & Reporting |          |            |

---

### 6. Post-Incident Procedures
- System recovery procedures for VirtualBox, Parrot OS, and network configuration
- Root cause analysis with event timeline, contributing factors, and technical findings
- Recovery validation checklist and testing procedures
- IR process improvement recommendations based on lessons learned

| Criterion | Complete (1) | Incomplete (0) |
|-----------|:-----------:|:--------------:|
| Post-Incident Procedures |          |            |

---

**Instructions:**
- For each criterion, check the appropriate box () when the requirement is fully met and evidence is documented.
- Attach supporting evidence and documentation as appendices or in referenced project files.
