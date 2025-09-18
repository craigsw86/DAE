# IR Tabletop Exercise Guide

**HIPAA Checklist Project**  
**Comprehensive Tabletop Exercise Documentation**  
**Date**: September 11, 2025

---

## 1. Tabletop Exercise Overview

### Purpose
Tabletop exercises provide a safe, controlled environment for incident response teams to practice their skills, test procedures, and improve coordination without the risks associated with live drills.

### Objectives
- Test incident response procedures
- Improve team coordination
- Identify process gaps
- Enhance decision-making skills
- Practice communication protocols

---

## 2. Exercise Design Framework

### Scenario Development Process

#### Step 1: Define Learning Objectives
```yaml
Primary Objectives:
  - Test detection and analysis capabilities
  - Practice containment procedures
  - Exercise communication protocols
  - Validate evidence handling

Secondary Objectives:
  - Improve team coordination
  - Enhance decision-making
  - Test crisis management
  - Practice stakeholder communication
```

#### Step 2: Create Realistic Scenarios
```yaml
Scenario Characteristics:
  - Based on real-world threats
  - Relevant to healthcare industry
  - Appropriate difficulty level
  - Clear progression timeline
  - Multiple decision points
```

#### Step 3: Develop Scenario Injects
```yaml
Inject Types:
  - Initial detection alerts
  - Escalation events
  - New information reveals
  - External pressures
  - Resource constraints
  - Time pressures
```

---

## 3. Exercise Scenarios

### Scenario 1: Ransomware Attack with Data Exfiltration

#### Background
A sophisticated ransomware group has targeted your healthcare organization. The attack involves both data encryption and data theft, creating a complex incident requiring coordinated response.

#### Timeline and Injects

**Inject 1: Initial Detection (T+0)**
> "At 2:47 AM, your SIEM alerts show multiple failed login attempts from an unknown IP address (203.45.67.89) targeting your admin accounts. The attempts are coming from a VPN service and appear to be automated."

**Discussion Points**:
- How do you classify this incident?
- What immediate actions do you take?
- Who do you notify first?
- How do you preserve evidence?

**Expected Responses**:
- Classify as potential security incident
- Begin log collection and analysis
- Notify incident response team
- Preserve relevant logs and system state

**Inject 2: Escalation (T+15 minutes)**
> "At 3:02 AM, your monitoring shows successful login to a low-privilege account. The user immediately attempts to access the PHI database but is blocked by access controls. However, they successfully access the file server containing patient documents."

**Discussion Points**:
- How do you respond to this escalation?
- Do you isolate the account or continue monitoring?
- What additional monitoring do you implement?
- How do you communicate with stakeholders?

**Expected Responses**:
- Escalate to security incident
- Implement additional monitoring
- Consider account isolation
- Notify management and legal

**Inject 3: Data Access (T+45 minutes)**
> "At 3:32 AM, logs show the attacker has successfully accessed the PHI database and is querying patient records. The queries are focused on patients with specific medical conditions. Network monitoring shows data being transferred to an external server."

**Discussion Points**:
- How do you contain the breach?
- What immediate actions do you take?
- How do you assess the scope of data access?
- What regulatory notifications are required?

**Expected Responses**:
- Immediate containment actions
- Assess scope of data access
- Begin regulatory notification process
- Coordinate with legal and compliance

**Inject 4: Ransomware Deployment (T+2 hours)**
> "At 4:47 AM, your monitoring systems detect ransomware being deployed across multiple servers. The ransomware is encrypting files and displaying a ransom note demanding payment in cryptocurrency. The attackers claim to have stolen PHI data and threaten to release it publicly."

**Discussion Points**:
- How do you respond to the ransomware?
- Do you pay the ransom?
- How do you handle the data theft threat?
- What communication do you send to patients?

**Expected Responses**:
- Activate crisis management procedures
- Do not pay ransom
- Assess data theft claims
- Prepare patient notification

**Inject 5: Crisis Management (T+4 hours)**
> "At 6:47 AM, local media contacts your organization asking about a potential data breach. The attackers have posted on social media claiming responsibility and threatening to release patient data. Your CEO is demanding immediate answers."

**Discussion Points**:
- How do you handle media inquiries?
- What do you tell the CEO?
- How do you manage the social media threat?
- What legal actions do you take?

**Expected Responses**:
- Activate crisis communication team
- Prepare media response
- Coordinate with legal counsel
- Monitor social media threats

---

### Scenario 2: Insider Threat with Data Exfiltration

#### Background
A disgruntled employee with access to PHI data is suspected of stealing patient information for personal gain. The investigation must be conducted carefully to preserve evidence while protecting patient privacy.

#### Timeline and Injects

**Inject 1: Suspicious Activity (T+0)**
> "Your audit logs show that employee John Smith has been accessing patient records outside of normal business hours and downloading large amounts of data. The activity has been ongoing for several weeks and appears to be increasing in frequency."

**Discussion Points**:
- How do you investigate this activity?
- What evidence do you collect?
- How do you protect patient privacy?
- When do you involve HR and legal?

**Expected Responses**:
- Begin discreet investigation
- Collect audit logs and evidence
- Maintain patient privacy
- Consult with HR and legal

**Inject 2: Evidence Collection (T+30 minutes)**
> "Further investigation reveals that John Smith has been using a personal USB drive to copy patient data. The USB drive was used on multiple workstations and contains thousands of patient records. John has been selling this information to identity thieves."

**Discussion Points**:
- How do you preserve the evidence?
- What legal actions do you take?
- How do you protect affected patients?
- How do you handle the employee?

**Expected Responses**:
- Preserve USB drive and workstations
- Coordinate with law enforcement
- Begin patient notification process
- Suspend employee pending investigation

**Inject 3: Legal Proceedings (T+2 hours)**
> "Law enforcement has arrested John Smith and seized his personal computer. They found evidence of a large-scale identity theft operation involving thousands of patients. The media is beginning to ask questions about the breach."

**Discussion Points**:
- How do you coordinate with law enforcement?
- What do you tell the media?
- How do you notify affected patients?
- What regulatory notifications are required?

**Expected Responses**:
- Coordinate with law enforcement
- Prepare media response
- Notify affected patients
- File regulatory notifications

---

### Scenario 3: Advanced Persistent Threat (APT)

#### Background
A sophisticated nation-state actor has been targeting your healthcare organization for months. The attack involves multiple stages and requires a coordinated response across multiple teams.

#### Timeline and Injects

**Inject 1: Initial Detection (T+0)**
> "Your threat intelligence team has identified indicators of compromise (IOCs) associated with a known APT group. The IOCs suggest that your organization may have been targeted, but no active compromise has been detected yet."

**Discussion Points**:
- How do you investigate the IOCs?
- What additional monitoring do you implement?
- How do you coordinate with threat intelligence?
- What defensive measures do you take?

**Expected Responses**:
- Investigate IOCs thoroughly
- Implement additional monitoring
- Coordinate with threat intelligence
- Enhance defensive measures

**Inject 2: Confirmed Compromise (T+2 hours)**
> "Further investigation confirms that your organization has been compromised. The attackers have been in your network for several weeks and have established persistence through multiple backdoors. They have been collecting sensitive information about your patients and operations."

**Discussion Points**:
- How do you respond to the confirmed compromise?
- How do you assess the scope of the breach?
- What containment measures do you take?
- How do you coordinate with law enforcement?

**Expected Responses**:
- Activate incident response team
- Assess scope of compromise
- Implement containment measures
- Coordinate with law enforcement

**Inject 3: Data Exfiltration (T+6 hours)**
> "Network monitoring shows that the attackers are actively exfiltrating large amounts of PHI data. The exfiltration is happening through encrypted channels and appears to be targeting specific patient populations. The attackers are also attempting to access your research data."

**Discussion Points**:
- How do you stop the exfiltration?
- What evidence do you collect?
- How do you protect patient data?
- How do you handle the research data threat?

**Expected Responses**:
- Implement network controls
- Collect forensic evidence
- Protect patient data
- Secure research data

**Inject 4: Crisis Management (T+12 hours)**
> "The attackers have released a statement claiming responsibility for the breach and threatening to release patient data publicly. They are demanding a ransom payment and have provided evidence of the stolen data. The media is reporting on the breach."

**Discussion Points**:
- How do you handle the ransom demand?
- What do you tell the media?
- How do you protect patient privacy?
- What legal actions do you take?

**Expected Responses**:
- Do not pay ransom
- Prepare media response
- Protect patient privacy
- Coordinate with legal counsel

---

## 4. Exercise Facilitation

### Facilitator Guidelines

#### Pre-Exercise Preparation
1. **Review Scenario Materials**
   - Read all injects and discussion points
   - Understand learning objectives
   - Prepare evaluation criteria
   - Set up exercise environment

2. **Brief Participants**
   - Explain exercise format
   - Review roles and responsibilities
   - Set expectations for participation
   - Address any questions

3. **Prepare Materials**
   - Print scenario injects
   - Set up evaluation forms
   - Prepare feedback templates
   - Organize reference materials

#### During Exercise
1. **Manage Time**
   - Keep exercise on schedule
   - Allow adequate discussion time
   - Move to next inject when ready
   - Take breaks as needed

2. **Guide Discussion**
   - Ask probing questions
   - Encourage participation
   - Clarify technical points
   - Keep discussion focused

3. **Document Performance**
   - Record key decisions
   - Note response times
   - Track team coordination
   - Document lessons learned

#### Post-Exercise
1. **Conduct Debrief**
   - Review key decisions
   - Discuss lessons learned
   - Identify improvement areas
   - Gather participant feedback

2. **Generate Report**
   - Document performance
   - Identify strengths and weaknesses
   - Recommend improvements
   - Plan follow-up actions

---

## 5. Evaluation Criteria

### Performance Metrics

#### Detection and Analysis
| Criteria | Excellent (4) | Good (3) | Satisfactory (2) | Needs Improvement (1) |
|----------|---------------|----------|------------------|----------------------|
| **Incident Classification** | Accurate, timely | Mostly accurate, minor delays | Basic accuracy, some delays | Poor accuracy, significant delays |
| **Threat Assessment** | Comprehensive, accurate | Good assessment, minor gaps | Basic assessment, some gaps | Poor assessment, significant gaps |
| **Evidence Collection** | Thorough, proper | Good collection, minor issues | Basic collection, some issues | Poor collection, significant issues |

#### Response Coordination
| Criteria | Excellent (4) | Good (3) | Satisfactory (2) | Needs Improvement (1) |
|----------|---------------|----------|------------------|----------------------|
| **Team Coordination** | Seamless, effective | Good coordination, minor issues | Basic coordination, some issues | Poor coordination, significant issues |
| **Communication** | Clear, timely, appropriate | Good communication, minor gaps | Basic communication, some gaps | Poor communication, significant gaps |
| **Decision Making** | Sound, timely | Good decisions, minor delays | Basic decisions, some delays | Poor decisions, significant delays |

#### Crisis Management
| Criteria | Excellent (4) | Good (3) | Satisfactory (2) | Needs Improvement (1) |
|----------|---------------|----------|------------------|----------------------|
| **Stakeholder Communication** | Professional, timely | Good communication, minor issues | Basic communication, some issues | Poor communication, significant issues |
| **Media Management** | Effective, coordinated | Good management, minor gaps | Basic management, some gaps | Poor management, significant gaps |
| **Regulatory Compliance** | Complete, timely | Good compliance, minor delays | Basic compliance, some delays | Poor compliance, significant delays |

---

## 6. Exercise Materials

### Participant Handouts

#### Incident Response Checklist
```markdown
# Incident Response Checklist

## Initial Response
- [ ] Classify incident severity
- [ ] Notify incident response team
- [ ] Preserve evidence
- [ ] Document initial findings

## Containment
- [ ] Isolate affected systems
- [ ] Block malicious traffic
- [ ] Disable compromised accounts
- [ ] Implement additional monitoring

## Investigation
- [ ] Collect forensic evidence
- [ ] Analyze attack vectors
- [ ] Assess scope of compromise
- [ ] Document findings

## Recovery
- [ ] Remove threats
- [ ] Restore systems
- [ ] Verify security
- [ ] Monitor for reinfection

## Communication
- [ ] Notify stakeholders
- [ ] Prepare media response
- [ ] File regulatory notifications
- [ ] Update procedures
```

#### Decision Matrix
```markdown
# Decision Matrix

## Incident Classification
- **Critical**: Immediate threat to patient safety
- **High**: Significant data breach or system compromise
- **Medium**: Limited impact, contained threat
- **Low**: Minor incident, no significant impact

## Response Actions
- **Immediate**: Take action within 15 minutes
- **Urgent**: Take action within 1 hour
- **Important**: Take action within 4 hours
- **Routine**: Take action within 24 hours

## Communication Requirements
- **CEO**: Critical and High incidents
- **Legal**: All incidents involving data breach
- **Compliance**: All incidents involving PHI
- **Media**: Public-facing incidents
```

### Reference Materials

#### Contact Information
```markdown
# Emergency Contacts

## Internal Team
- Incident Response Lead: (555) 123-4567
- Security Team: (555) 123-4568
- Legal Counsel: (555) 123-4569
- Compliance Officer: (555) 123-4570

## External Resources
- Law Enforcement: 911
- FBI Cyber Division: (555) 123-4571
- HHS OCR: (555) 123-4572
- Cyber Insurance: (555) 123-4573
```

#### Regulatory Requirements
```markdown
# Regulatory Notification Requirements

## HIPAA Breach Notification
- **Timeline**: Within 60 days of discovery
- **Recipients**: Affected individuals, HHS, media (if >500 affected)
- **Content**: Description of breach, steps taken, contact information

## State Notification Requirements
- **Timeline**: Varies by state (typically 30-90 days)
- **Recipients**: State attorney general, affected individuals
- **Content**: Similar to HIPAA requirements

## Law Enforcement Notification
- **Timeline**: Immediately upon discovery
- **Recipients**: Local law enforcement, FBI
- **Content**: Incident details, evidence, impact assessment
```

---

## 7. Exercise Outcomes

### Expected Learning Outcomes

#### Technical Skills
- Improved incident detection capabilities
- Enhanced forensic analysis skills
- Better evidence handling procedures
- Improved containment techniques

#### Soft Skills
- Enhanced team coordination
- Better communication skills
- Improved decision-making
- Stronger crisis management

#### Process Improvements
- Identified procedure gaps
- Enhanced documentation
- Improved training needs
- Better resource allocation

### Follow-up Actions

#### Immediate Actions (Within 1 Week)
- [ ] Conduct exercise debrief
- [ ] Document lessons learned
- [ ] Identify improvement areas
- [ ] Update procedures as needed

#### Short-term Actions (Within 1 Month)
- [ ] Implement procedure improvements
- [ ] Conduct additional training
- [ ] Update documentation
- [ ] Test new procedures

#### Long-term Actions (Within 3 Months)
- [ ] Plan next exercise
- [ ] Evaluate training effectiveness
- [ ] Update training materials
- [ ] Share lessons learned

---

*This comprehensive tabletop exercise guide provides a structured approach to testing and improving incident response capabilities while maintaining a safe learning environment.*
