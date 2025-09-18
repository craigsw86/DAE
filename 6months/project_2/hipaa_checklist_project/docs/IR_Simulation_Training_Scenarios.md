# IR Simulation & Training Scenarios

**HIPAA Checklist Project**  
**Incident Response 2 - Training Component**  
**Date**: September 11, 2025

---

## 1. Multi-Stage Attack Scenarios

### Scenario 1: Advanced Persistent Threat (APT) Healthcare Breach

**Objective**: Simulate a sophisticated multi-stage attack targeting PHI data

**Attack Progression**:
1. **Initial Access** (Day 1)
   - Spear phishing email with malicious attachment
   - Social engineering targeting healthcare staff
   - **Decision Point**: How to detect and respond to suspicious emails?

2. **Establishment** (Day 2-3)
   - Malware installation and persistence
   - Credential harvesting
   - **Decision Point**: When to isolate systems vs. continue monitoring?

3. **Lateral Movement** (Day 4-5)
   - Privilege escalation
   - Network reconnaissance
   - **Decision Point**: How to contain without alerting attackers?

4. **Data Exfiltration** (Day 6-7)
   - PHI data collection and staging
   - Exfiltration to external servers
   - **Decision Point**: Immediate containment vs. evidence gathering?

5. **Covering Tracks** (Day 8)
   - Log deletion and obfuscation
   - Persistence mechanisms
   - **Decision Point**: How to preserve evidence while containing?

**Training Objectives**:
- Practice incident detection and classification
- Test communication protocols
- Validate containment procedures
- Exercise evidence collection

---

### Scenario 2: Ransomware Attack with Data Exfiltration

**Objective**: Simulate a ransomware attack with data theft component

**Attack Progression**:
1. **Initial Compromise** (Hour 1)
   - Exploit of unpatched vulnerability
   - **Decision Point**: How quickly can you detect the initial breach?

2. **Reconnaissance** (Hour 2-4)
   - Network mapping and privilege escalation
   - **Decision Point**: When to activate incident response team?

3. **Data Theft** (Hour 5-8)
   - PHI data exfiltration
   - **Decision Point**: How to detect data exfiltration in progress?

4. **Ransomware Deployment** (Hour 9-12)
   - Encryption of critical systems
   - Ransom note delivery
   - **Decision Point**: Immediate containment vs. evidence preservation?

5. **Negotiation Phase** (Hour 13-24)
   - Ransom demands and threats
   - **Decision Point**: How to handle ransom negotiations?

**Training Objectives**:
- Test rapid response capabilities
- Practice crisis communication
- Validate backup and recovery procedures
- Exercise decision-making under pressure

---

### Scenario 3: Insider Threat with Data Exfiltration

**Objective**: Simulate an insider threat scenario

**Attack Progression**:
1. **Suspicious Activity** (Week 1)
   - Unusual access patterns
   - **Decision Point**: How to investigate without alerting the insider?

2. **Data Collection** (Week 2-3)
   - Systematic PHI data gathering
   - **Decision Point**: When to involve HR and legal teams?

3. **Exfiltration Attempt** (Week 4)
   - Attempted data theft
   - **Decision Point**: How to prevent exfiltration while gathering evidence?

4. **Cover-up Attempts** (Week 5)
   - Evidence tampering
   - **Decision Point**: How to preserve evidence for legal proceedings?

**Training Objectives**:
- Practice insider threat detection
- Test legal and HR coordination
- Validate evidence handling procedures
- Exercise sensitive investigation techniques

---

## 2. Tabletop Exercise Documentation

### Exercise Setup

**Participants**:
- Incident Response Lead
- System Administrator
- Compliance Officer
- Communications Manager
- Legal Counsel
- HR Representative

**Duration**: 4 hours
**Format**: Facilitated discussion with scenario injects

### Scenario Injects

#### Inject 1: Initial Detection
> "At 2:47 AM, your SIEM alerts show multiple failed login attempts from an unknown IP address (203.45.67.89) targeting your admin accounts. The attempts are coming from a VPN service and appear to be automated."

**Discussion Points**:
- How do you classify this incident?
- What immediate actions do you take?
- Who do you notify first?
- How do you preserve evidence?

#### Inject 2: Escalation
> "At 3:15 AM, your monitoring shows successful login to a low-privilege account. The user immediately attempts to access the PHI database but is blocked by access controls."

**Discussion Points**:
- How do you respond to this escalation?
- Do you isolate the account or continue monitoring?
- What additional monitoring do you implement?
- How do you communicate with stakeholders?

#### Inject 3: Data Access
> "At 4:30 AM, logs show the attacker has successfully accessed the PHI database and is querying patient records. The queries are focused on patients with specific medical conditions."

**Discussion Points**:
- How do you contain the breach?
- What immediate actions do you take?
- How do you assess the scope of data access?
- What regulatory notifications are required?

#### Inject 4: Data Exfiltration
> "At 5:45 AM, network monitoring shows large amounts of data being transferred to an external server. The transfer appears to be encrypted and is using a legitimate-looking domain."

**Discussion Points**:
- How do you stop the exfiltration?
- What evidence do you collect?
- How do you notify affected patients?
- What legal actions do you take?

### Evaluation Criteria

| Criteria | Excellent (4) | Good (3) | Satisfactory (2) | Needs Improvement (1) |
|----------|---------------|----------|------------------|----------------------|
| **Detection & Analysis** | Rapid, accurate classification | Good classification, minor delays | Basic classification, some delays | Poor classification, significant delays |
| **Response Coordination** | Seamless team coordination | Good coordination, minor issues | Basic coordination, some confusion | Poor coordination, significant confusion |
| **Communication** | Clear, timely, appropriate | Good communication, minor gaps | Basic communication, some issues | Poor communication, significant gaps |
| **Decision Making** | Sound, timely decisions | Good decisions, minor delays | Basic decisions, some poor choices | Poor decisions, significant issues |
| **Evidence Handling** | Proper collection and preservation | Good handling, minor issues | Basic handling, some problems | Poor handling, significant problems |

---

## 3. Live Drill Procedures

### Pre-Drill Safety Measures

**System Isolation**:
- All drills conducted in isolated test environment
- No production systems affected
- Backup systems verified before drill
- Rollback procedures tested and ready

**Scope Boundaries**:
- **Green Zone**: Test environment only
- **Yellow Zone**: Staging environment (with approval)
- **Red Zone**: Production systems (prohibited)

**Safety Protocols**:
- Emergency stop procedures documented
- Incident commander has authority to halt drill
- Real-time monitoring of system health
- Immediate escalation for any production impact

### Drill Execution Procedures

#### Phase 1: Preparation (30 minutes)
1. **Environment Setup**
   - Deploy test systems
   - Configure monitoring
   - Brief all participants
   - Verify safety measures

2. **Team Assembly**
   - Confirm all team members present
   - Test communication channels
   - Verify access to tools and systems
   - Review roles and responsibilities

#### Phase 2: Execution (2-4 hours)
1. **Scenario Deployment**
   - Inject initial incident
   - Monitor team response
   - Document actions taken
   - Track decision points

2. **Real-time Monitoring**
   - System health monitoring
   - Team performance tracking
   - Safety protocol compliance
   - Evidence collection

#### Phase 3: Recovery (30 minutes)
1. **System Restoration**
   - Restore test environment
   - Verify system integrity
   - Document any issues
   - Clean up test data

2. **Team Debrief**
   - Immediate feedback session
   - Identify lessons learned
   - Document improvement areas
   - Schedule follow-up actions

### Post-Drill Analysis

**Performance Metrics**:
- Response time to initial detection
- Time to containment
- Communication effectiveness
- Decision quality
- Evidence handling

**Improvement Recommendations**:
- Process improvements
- Training needs
- Tool enhancements
- Procedure updates

---

## 4. Virtual Training Environment

### Environment Architecture

**Network Topology**:
```
Internet
    |
[Firewall]
    |
[DMZ]
    |
[Internal Network]
    |
[Database Network]
```

**Virtual Machines**:
- **Windows Server 2019**: Domain controller and file server
- **Ubuntu 20.04**: Web application server
- **CentOS 8**: Database server
- **Windows 10**: Workstation for testing
- **Kali Linux**: Attack simulation platform

### Attack Simulation Tools

**Reconnaissance**:
- Nmap for network scanning
- Nessus for vulnerability assessment
- Custom scripts for service enumeration

**Exploitation**:
- Metasploit for exploit delivery
- Custom payloads for specific scenarios
- Social engineering toolkit (SET)

**Persistence**:
- Backdoor installation
- Scheduled task creation
- Service installation

**Lateral Movement**:
- Credential harvesting
- Pass-the-hash attacks
- Remote service exploitation

### Training Scenario Management

**Scenario Library**:
- Pre-built attack scenarios
- Customizable parameters
- Difficulty levels (Beginner, Intermediate, Advanced)
- Industry-specific scenarios (Healthcare, Finance, etc.)

**Progress Tracking**:
- Individual performance metrics
- Team coordination scores
- Skill development tracking
- Certification progress

**Assessment Tools**:
- Automated scoring systems
- Real-time feedback
- Performance analytics
- Improvement recommendations

---

## 5. Training Implementation Plan

### Phase 1: Environment Setup (Week 1-2)
- Deploy virtual training environment
- Configure attack simulation tools
- Create initial scenario library
- Train instructors and facilitators

### Phase 2: Pilot Program (Week 3-4)
- Conduct pilot tabletop exercise
- Test live drill procedures
- Gather feedback and refine processes
- Update documentation

### Phase 3: Full Implementation (Week 5-8)
- Launch comprehensive training program
- Conduct regular exercises
- Track performance metrics
- Continuous improvement

### Phase 4: Maintenance (Ongoing)
- Monthly tabletop exercises
- Quarterly live drills
- Annual scenario updates
- Continuous skill development

---

## 6. Success Metrics

**Training Effectiveness**:
- Response time improvement: Target 25% reduction
- Decision accuracy: Target 90% correct decisions
- Team coordination: Target 95% effective communication
- Evidence handling: Target 100% proper procedures

**Skill Development**:
- Individual competency assessments
- Team performance evaluations
- Certification achievement rates
- Knowledge retention testing

**Operational Impact**:
- Reduced incident response time
- Improved decision quality
- Enhanced team coordination
- Better evidence handling

---

*This comprehensive training program ensures your incident response team is prepared for real-world scenarios while maintaining safety and effectiveness.*
