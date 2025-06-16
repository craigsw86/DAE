# 🛡 SOC-in-a-Box: 12-Week Capstone Project

**Goal:** Build a self-contained Security Operations Center simulation to learn and demonstrate SOC Analyst skills. This 12-week project provides hands-on experience in log analysis, detection engineering, incident response, and threat hunting.

---

## 📅 Timeline Overview

### ✅ Month 1: Setup & Simulation

**Week 1:**  
- Set up your lab (macOS tools OR virtual machines)  
- Tools: ELK Stack, Zeek, Wireshark, Filebeat/Sysmon, Velociraptor  

**Week 2:**  
- Begin collecting logs from your Mac or VMs  
- Set up filebeat (or Velociraptor) for ingestion into ELK  

**Week 3:**  
- Learn basic packet analysis with Wireshark/Zeek  
- Capture sample network activity  

**Week 4:**  
- Simulate simple attacks (e.g., brute-force, PowerShell abuse)  
- Monitor for corresponding alerts/log entries  

---

### 🧪 Month 2: Detection & Triage

**Week 5:**  
- Write 2–3 detection rules (e.g., failed logins, encoded PowerShell)  
- Visualize and test rules in ELK or your SIEM tool  

**Week 6:**  
- Triage your own alerts  
- Practice reducing false positives and validating threats  

**Week 7:**  
- Simulate another attack (e.g., C2 beacon, file dropper)  
- Investigate using logs + Wireshark  

**Week 8:**  
- Map one complete scenario to MITRE ATT&CK  
- Write a full incident report  

---

### 🧾 Month 3: Reporting & Showcase

**Week 9:**  
- Simulate new alerts and generate evidence  
- Review gaps in your rules or log sources  

**Week 10:**  
- Finalize 2+ incident reports  
- Organize IOC table, alert summary, and response steps  

**Week 11:**  
- Build GitHub repo with:  
  - README  
  - Setup steps  
  - Screenshots  
  - Sample alerts/reports  

**Week 12:**  
- (Optional) Record video walkthrough or write a short PDF case study  
- Submit to portfolio / LinkedIn  

---

## 🛠 Suggested Tools

| Purpose                | Tools (Mac-friendly)                        |
|------------------------|---------------------------------------------|
| SIEM + Dashboard       | ELK Stack (ElasticSearch, Logstash, Kibana) |
| Endpoint Monitoring    | Velociraptor, Filebeat, Sysmon (VMs)        |
| Network Analysis       | Zeek, Wireshark                             |
| Threat Simulation      | Manual scripts, Atomic Red Team (in VM)     |

---

## 📌 Deliverables by Week 12

- ✅ Working log ingestion and SIEM visualization
- ✅ At least 3 simulated threat scenarios
- ✅ 2–3 detailed incident reports
- ✅ GitHub repo or PDF portfolio ready to share

---

_**Start Date:** 2025-06-16_  
_**End Date:** 2025-09-08_

Happy hunting! 🧠🔍
