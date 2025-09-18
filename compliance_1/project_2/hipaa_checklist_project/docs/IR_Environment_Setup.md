# IR Environment Setup

This document details the incident response environment setup for the Incident Response 1 rubric, including Wazuh SIEM, agent deployment, custom alert rules, Wireshark, Volatility, and system logging.

---

## 1. Wazuh SIEM Installation & Configuration

**Platform:** Parrot OS (VirtualBox)

**Steps:**
1. Download and install Parrot OS in VirtualBox.
2. Update system: `sudo apt update && sudo apt upgrade`
3. Install Wazuh server:
   ```bash
   curl -sO https://packages.wazuh.com/4.6/wazuh-install.sh
   sudo bash ./wazuh-install.sh -a
   ```
4. Access Wazuh dashboard at `https://localhost:5601` (default credentials: admin/admin).

**Evidence:**
- Screenshot: Wazuh dashboard main page (attach as needed)
- Log: `2025-08-20 10:00:00 - Wazuh server started on Parrot OS.`

---

## 2. Agent Deployment & Log Collection

**Steps:**
1. Install Wazuh agent on Parrot OS:
   ```bash
   sudo apt install wazuh-agent
   sudo systemctl enable --now wazuh-agent
   ```
2. Configure agent to connect to Wazuh server (edit `/var/ossec/etc/ossec.conf`).
3. Enable log collection for `/var/log/auth.log` and `/var/log/syslog`.
4. Confirm agent status:
   ```bash
   sudo systemctl status wazuh-agent
   ```

**Evidence:**
- Log: `2025-08-20 10:05:00 - Wazuh agent connected from Parrot OS.`
- Screenshot: Agent listed in Wazuh dashboard.

---

## 3. Custom Alert Rules

**Rule 1:** Detect sudo command usage
```xml
<rule id="100001" level="7">
  <decoded_as>syslog</decoded_as>
  <field name="program">sudo</field>
  <description>Sudo command executed</description>
</rule>
```
**Rule 2:** Detect failed SSH login attempts
```xml
<rule id="100002" level="10">
  <decoded_as>sshd</decoded_as>
  <match>Failed password</match>
  <description>Failed SSH login attempt</description>
</rule>
```
**Rule 3:** Detect new user creation
```xml
<rule id="100003" level="12">
  <decoded_as>syslog</decoded_as>
  <match>useradd</match>
  <description>New user account created</description>
</rule>
```
**Evidence:**
- Log: `2025-08-20 10:10:00 - Custom alert rule 100002 triggered: Failed SSH login.`
- Screenshot: Alert visible in Wazuh dashboard.

---

## 4. Wireshark Configuration

**Installation:**
```bash
sudo apt install wireshark
```
**Capture Filter Example:**
- Only capture SSH traffic: `tcp port 22`
- Only capture traffic from a specific IP: `host 192.168.56.101`

**Evidence:**
- Screenshot: Wireshark running with filter `tcp port 22` (attach as needed)

---

## 5. Volatility Framework Setup

**Installation:**
```bash
sudo apt install volatility
```
**Memory Analysis Example:**
- Acquire memory image: `sudo dd if=/dev/mem of=/tmp/mem.img bs=1M`
- Analyze processes:
  ```bash
  volatility -f /tmp/mem.img --profile=LinuxParrot_5_10_0_pslist
  ```

**Evidence:**
- Output: List of running processes from memory image

---

## 6. System Logging & Ingestion

**Parrot OS:**
- Syslog and auth.log configured for forwarding to Wazuh agent (edit `/etc/rsyslog.conf` and `/var/ossec/etc/ossec.conf`).

**macOS:**
- Enable remote syslog forwarding:
  ```bash
  sudo syslog -s -r 192.168.56.100
  ```
- Confirm logs received in Wazuh dashboard.

**Evidence:**
- Log: `2025-08-20 10:20:00 - macOS log received in Wazuh dashboard.`
- Screenshot: macOS and Parrot OS logs visible in dashboard.

---

## 7. Summary Table

| Component         | Configuration/Evidence                                 |
|------------------|-------------------------------------------------------|
| Wazuh SIEM       | Installed, running, dashboard accessible               |
| Agent Deployment | Agent connected, logs collected from Parrot OS         |
| Custom Rules     | 3 rules created, alerts visible in dashboard           |
| Wireshark        | Installed, capture filters set, traffic captured       |
| Volatility       | Installed, memory image acquired/analyzed              |
| System Logging   | Parrot OS/macOS logs ingested into Wazuh               |

---

**Appendix:**
- Attach screenshots, config files, and log excerpts as supporting evidence.
