# IR Training Environment Setup

**HIPAA Checklist Project**  
**Virtual Training Environment Implementation**  
**Date**: September 11, 2025

---

## 1. Virtual Training Environment Architecture

### Network Topology Design

```
                    Internet
                        |
                   [Firewall]
                        |
                   [DMZ Zone]
                        |
                [Internal Network]
                        |
                [Database Network]
```

**Network Segments**:
- **DMZ**: Web servers, load balancers, external-facing services
- **Internal Network**: Application servers, monitoring systems, management tools
- **Database Network**: Database servers, backup systems, sensitive data storage

### Virtual Machine Configuration

#### Windows Server 2019 - Domain Controller
```yaml
Name: DC-01
OS: Windows Server 2019 Standard
RAM: 4GB
CPU: 2 cores
Disk: 100GB
Network: Internal Network
Roles:
  - Active Directory Domain Services
  - DNS Server
  - DHCP Server
  - File Server
```

#### Ubuntu 20.04 - Web Application Server
```yaml
Name: WEB-01
OS: Ubuntu 20.04 LTS
RAM: 4GB
CPU: 2 cores
Disk: 80GB
Network: Internal Network
Services:
  - Apache/Nginx Web Server
  - PHP/Python Application
  - SSL/TLS Termination
  - Load Balancer
```

#### CentOS 8 - Database Server
```yaml
Name: DB-01
OS: CentOS 8 Stream
RAM: 8GB
CPU: 4 cores
Disk: 200GB
Network: Database Network
Services:
  - MySQL/PostgreSQL Database
  - Database Backup Service
  - Encryption Services
  - Audit Logging
```

#### Windows 10 - Workstation
```yaml
Name: WS-01
OS: Windows 10 Professional
RAM: 4GB
CPU: 2 cores
Disk: 100GB
Network: Internal Network
Software:
  - Office 365
  - Web Browser
  - Remote Desktop Client
  - Security Tools
```

#### Kali Linux - Attack Platform
```yaml
Name: KALI-01
OS: Kali Linux 2023.3
RAM: 4GB
CPU: 2 cores
Disk: 100GB
Network: Isolated Network
Tools:
  - Metasploit Framework
  - Nmap Network Scanner
  - Wireshark Packet Analyzer
  - Social Engineering Toolkit
  - Custom Attack Scripts
```

---

## 2. Attack Simulation Tools

### Reconnaissance Tools

#### Network Discovery
```bash
# Nmap Network Scanner
nmap -sS -O -A target_network

# Custom Network Discovery Script
#!/bin/bash
for i in {1..254}; do
    ping -c 1 192.168.1.$i &
done
wait
```

#### Vulnerability Assessment
```bash
# Nessus Vulnerability Scanner
nessus-cli scan --target 192.168.1.0/24

# OpenVAS Vulnerability Scanner
openvas-cli --target 192.168.1.0/24 --scan-type full
```

#### Service Enumeration
```bash
# Service Version Detection
nmap -sV -sC target_ip

# Custom Service Enumeration
#!/bin/bash
for port in {1..65535}; do
    nc -zv target_ip $port 2>&1 | grep succeeded
done
```

### Exploitation Tools

#### Metasploit Framework
```ruby
# Custom Exploit Module
class MetasploitModule < Msf::Exploit::Remote
  Rank = NormalRanking
  
  def initialize(info = {})
    super(update_info(info,
      'Name'           => 'Custom Healthcare App Exploit',
      'Description'    => 'Exploits vulnerability in healthcare application',
      'Author'         => ['Training Team'],
      'License'        => MSF_LICENSE,
      'Platform'       => 'win',
      'Targets'        => [['Windows', {}]],
      'DefaultTarget'  => 0
    ))
  end
  
  def exploit
    # Exploit code here
  end
end
```

#### Social Engineering Toolkit (SET)
```python
# Custom Social Engineering Module
class HealthcarePhishing:
    def __init__(self):
        self.templates = {
            'hipaa_audit': 'HIPAA Compliance Audit Required',
            'password_reset': 'Password Reset Required',
            'system_update': 'System Update Required'
        }
    
    def generate_phishing_email(self, template, target):
        # Generate targeted phishing email
        pass
```

### Persistence Tools

#### Backdoor Installation
```bash
# Custom Backdoor Script
#!/bin/bash
# Install persistent backdoor
cp backdoor.sh /etc/init.d/
chmod +x /etc/init.d/backdoor.sh
update-rc.d backdoor.sh defaults
```

#### Scheduled Task Creation
```powershell
# PowerShell Scheduled Task
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\backdoor.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At 2AM
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "SystemMaintenance"
```

---

## 3. Training Scenario Management System

### Scenario Library Structure

```
scenarios/
 beginner/
    phishing_attack/
    malware_infection/
    unauthorized_access/
 intermediate/
    lateral_movement/
    privilege_escalation/
    data_exfiltration/
 advanced/
    apt_simulation/
    insider_threat/
    supply_chain_attack/
 custom/
     healthcare_specific/
     finance_specific/
     government_specific/
```

### Scenario Configuration Files

#### Basic Scenario Template
```yaml
name: "Phishing Attack Simulation"
difficulty: "beginner"
duration: "2 hours"
participants: 4
objectives:
  - Detect phishing attempt
  - Contain compromised account
  - Preserve evidence
  - Notify stakeholders
injects:
  - time: "00:00"
    type: "email"
    content: "Suspicious email received"
  - time: "00:15"
    type: "system"
    content: "Account compromise detected"
  - time: "00:30"
    type: "network"
    content: "Data exfiltration attempt"
evaluation_criteria:
  - detection_time: "< 5 minutes"
  - containment_time: "< 15 minutes"
  - evidence_preservation: "100%"
  - communication: "timely and accurate"
```

#### Advanced Scenario Template
```yaml
name: "APT Healthcare Breach"
difficulty: "advanced"
duration: "8 hours"
participants: 8
objectives:
  - Detect multi-stage attack
  - Coordinate response team
  - Preserve forensic evidence
  - Manage crisis communication
  - Coordinate with law enforcement
injects:
  - time: "00:00"
    type: "reconnaissance"
    content: "Network scanning detected"
  - time: "01:00"
    type: "exploitation"
    content: "Vulnerability exploited"
  - time: "02:00"
    type: "lateral_movement"
    content: "Lateral movement detected"
  - time: "04:00"
    type: "data_exfiltration"
    content: "PHI data being exfiltrated"
  - time: "06:00"
    type: "crisis"
    content: "Media inquiry received"
evaluation_criteria:
  - detection_time: "< 30 minutes"
  - containment_time: "< 2 hours"
  - evidence_preservation: "100%"
  - communication: "professional and timely"
  - coordination: "effective team coordination"
```

---

## 4. Performance Monitoring and Analytics

### Real-time Monitoring Dashboard

#### System Health Monitoring
```python
# System Health Monitor
import psutil
import time
import json

class SystemMonitor:
    def __init__(self):
        self.metrics = {}
    
    def collect_metrics(self):
        self.metrics = {
            'timestamp': time.time(),
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'network_io': psutil.net_io_counters()._asdict()
        }
        return self.metrics
    
    def save_metrics(self):
        with open('system_metrics.json', 'a') as f:
            json.dump(self.metrics, f)
            f.write('\n')
```

#### Team Performance Tracking
```python
# Team Performance Tracker
class TeamPerformanceTracker:
    def __init__(self):
        self.performance_data = {}
    
    def track_action(self, team_member, action, timestamp, success):
        if team_member not in self.performance_data:
            self.performance_data[team_member] = []
        
        self.performance_data[team_member].append({
            'action': action,
            'timestamp': timestamp,
            'success': success,
            'response_time': self.calculate_response_time(action)
        })
    
    def calculate_response_time(self, action):
        # Calculate response time based on action type
        pass
    
    def generate_report(self):
        # Generate performance report
        pass
```

### Analytics and Reporting

#### Performance Metrics
```python
# Performance Analytics
class PerformanceAnalytics:
    def __init__(self):
        self.metrics = {}
    
    def calculate_metrics(self, performance_data):
        self.metrics = {
            'average_response_time': self.calculate_avg_response_time(performance_data),
            'success_rate': self.calculate_success_rate(performance_data),
            'team_coordination_score': self.calculate_coordination_score(performance_data),
            'evidence_handling_score': self.calculate_evidence_score(performance_data)
        }
        return self.metrics
    
    def generate_improvement_recommendations(self):
        recommendations = []
        if self.metrics['average_response_time'] > 300:  # 5 minutes
            recommendations.append("Improve response time through better training")
        if self.metrics['success_rate'] < 0.8:  # 80%
            recommendations.append("Focus on decision-making skills")
        return recommendations
```

---

## 5. Implementation Checklist

### Environment Setup
- [ ] Deploy virtual machines
- [ ] Configure network topology
- [ ] Install attack simulation tools
- [ ] Set up monitoring systems
- [ ] Test all components

### Scenario Development
- [ ] Create beginner scenarios
- [ ] Create intermediate scenarios
- [ ] Create advanced scenarios
- [ ] Create custom scenarios
- [ ] Test all scenarios

### Training Program
- [ ] Train instructors
- [ ] Develop evaluation criteria
- [ ] Create assessment tools
- [ ] Set up progress tracking
- [ ] Launch training program

### Maintenance
- [ ] Regular scenario updates
- [ ] Performance monitoring
- [ ] Continuous improvement
- [ ] Documentation updates
- [ ] Team feedback collection

---

## 6. Success Metrics

### Training Effectiveness
- **Response Time**: Target 25% improvement
- **Decision Accuracy**: Target 90% correct decisions
- **Team Coordination**: Target 95% effective communication
- **Evidence Handling**: Target 100% proper procedures

### Skill Development
- **Individual Competency**: Regular assessments
- **Team Performance**: Quarterly evaluations
- **Certification Rates**: Annual tracking
- **Knowledge Retention**: Ongoing testing

### Operational Impact
- **Incident Response Time**: Measurable reduction
- **Decision Quality**: Improved outcomes
- **Team Coordination**: Enhanced effectiveness
- **Evidence Handling**: Better preservation

---

*This virtual training environment provides a comprehensive platform for incident response training while maintaining safety and effectiveness.*
