# Digital Evidence Management

This document details digital evidence management procedures for the Incident Response 1 rubric, including live data collection, memory analysis, disk acquisition, chain of custody, and event timeline creation.

---

## 1. Live Data Collection (Parrot OS)

**System State Capture:**
- Capture running processes:
  ```bash
  ps aux > /evidence/process_list.txt
  ```
- Capture network connections:
  ```bash
  netstat -anp > /evidence/network_connections.txt
  ```
- Capture open files:
  ```bash
  lsof > /evidence/open_files.txt
  ```

**Evidence:**
- Files saved in /evidence directory with timestamps

---

## 2. Memory Analysis (Volatility)

**Memory Acquisition:**
- Acquire memory image:
  ```bash
  sudo dd if=/dev/mem of=/evidence/mem.img bs=1M
  ```

**Analysis Example:**
- List running processes:
  ```bash
  volatility -f /evidence/mem.img --profile=LinuxParrot_5_10_0_pslist
  ```
- Extract network connections:
  ```bash
  volatility -f /evidence/mem.img --profile=LinuxParrot_5_10_0_netscan
  ```

**Evidence:**
- Volatility output files saved in /evidence

---

## 3. Disk Acquisition (Imaging)

**Disk Imaging:**
- Acquire disk image using dd:
  ```bash
  sudo dd if=/dev/sda of=/evidence/disk.img bs=4M status=progress
  ```
- Verify image integrity:
  ```bash
  sha256sum /evidence/disk.img > /evidence/disk.img.sha256
  ```

**Evidence:**
- disk.img and hash file stored in /evidence

---

## 4. Chain of Custody Documentation

- All evidence files are timestamped, labeled, and stored in a secure, access-controlled directory.
- Chain of custody log maintained:
  ```
  [2025-08-20 13:00:00] Collected process_list.txt by analyst1
  [2025-08-20 13:05:00] Collected mem.img by analyst1
  [2025-08-20 13:10:00] disk.img checked in by sysadmin
  ```
- Access to evidence is logged and restricted to authorized personnel.

---

## 5. Timeline Creation (macOS & Parrot OS Logs)

- Use log2timeline (plaso) to create unified event timeline:
  ```bash
  log2timeline.py /evidence/timeline.plaso /evidence/auth.log /evidence/macOS.log
  psort.py -o l2tcsv -w /evidence/timeline.csv /evidence/timeline.plaso
  ```
- Analyze timeline for sequence of events, correlating macOS and Parrot OS activity.

**Evidence:**
- timeline.csv with annotated events
- Example finding: Unauthorized login attempt on Parrot OS followed by suspicious process on macOS

---

## 6. Summary Table

| Component            | Procedure/Evidence                                 |
|---------------------|----------------------------------------------------|
| Live Data Collection| Process, network, open files captured              |
| Memory Analysis     | Volatility used, output saved                       |
| Disk Acquisition    | Disk image and hash created                         |
| Chain of Custody    | Log maintained, access controlled                   |
| Timeline Creation   | Unified timeline from macOS & Parrot OS logs        |

---

**Appendix:**
- Attach evidence files, chain of custody logs, and timeline CSV as supporting evidence.
