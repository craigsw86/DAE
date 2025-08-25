# Incident Response and Containment

This document details the response and containment procedures for the Incident Response 1 rubric, including network isolation, evidence preservation, and containment playbooks.

---

## 1. Network Isolation Procedures (Parrot OS)

**Network Interface Configuration:**
- Disable network interface:
  ```bash
  sudo ifconfig eth0 down
  ```
- Re-enable interface after containment:
  ```bash
  sudo ifconfig eth0 up
  ```

**Firewall Rules Implementation:**
- Block all inbound/outbound traffic except SSH from admin IP:
  ```bash
  sudo ufw default deny incoming
  sudo ufw default deny outgoing
  sudo ufw allow from 192.168.56.1 to any port 22
  sudo ufw enable
  ```

**VirtualBox Network Segmentation:**
- Move VM to an isolated host-only network in VirtualBox settings.
- Confirm isolation by checking no internet access from Parrot OS.

**Evidence:**
- Screenshot: ifconfig output showing interface down
- Log: `2025-08-20 12:00:00 - Parrot OS network isolated via firewall and VirtualBox.`

---

## 2. Evidence Preservation (Parrot OS Forensic Tools)

**File System Artifacts:**
- Copy suspicious files to evidence directory:
  ```bash
  cp /var/log/auth.log /evidence/auth.log
  cp /home/user/suspicious_file /evidence/
  ```

**Network Traffic Captures:**
- Capture traffic with tcpdump:
  ```bash
  sudo tcpdump -i eth0 -w /evidence/network_capture.pcap
  ```

**Memory Dumps:**
- Acquire memory image:
  ```bash
  sudo dd if=/dev/mem of=/evidence/mem.img bs=1M
  ```

**Evidence:**
- Directory listing of /evidence with timestamps
- Log: `2025-08-20 12:10:00 - Evidence preserved: auth.log, network_capture.pcap, mem.img.`

---

## 3. Containment Playbook

**Host Isolation Steps (VirtualBox):**
1. Pause or power off affected VM.
2. Remove VM from bridged/NAT network; attach to host-only network.
3. Document isolation time and actions taken.

**Network Traffic Blocking:**
- Apply firewall rules as above to block all traffic except admin SSH.

**Service Shutdown Procedures:**
- Stop suspicious or compromised services:
  ```bash
  sudo systemctl stop apache2
  sudo systemctl stop ssh
  ```
- Document all services stopped and reason.

**Evidence:**
- Log: `2025-08-20 12:15:00 - Host isolated, network blocked, services shut down.`
- Screenshot: VirtualBox network settings

---

## 4. Documentation & Evidence

- All actions logged in incident tracking system (see IR Documentation & Reporting)
- Screenshots and logs attached as supporting evidence
- Chain of custody maintained for all preserved artifacts

---

## 5. Summary Table

| Component            | Procedure/Evidence                                 |
|---------------------|----------------------------------------------------|
| Network Isolation   | Interface down, firewall rules, VirtualBox segment  |
| Evidence Preservation | File, network, memory artifacts saved              |
| Containment Playbook| Host isolation, network block, service shutdown     |
| Documentation       | Logs, screenshots, chain of custody                 |

---

**Appendix:**
- Attach screenshots, config files, and log excerpts as supporting evidence.
