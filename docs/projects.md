---
title: "Projects"
permalink: /projects/
layout: single
---

<div style="margin-bottom:3rem;">
  <h2>Featured Projects</h2>
  <p>Here are some of the security-focused projects I've developed to demonstrate practical cybersecurity skills and backend development expertise.</p>
</div>

## 🔐 Patient File Management

<div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; margin:1rem 0; border-left:4px solid #007bff;">
  <p><strong>Tech Stack:</strong> Python, SQLite, TKinter</p>
  <p><strong>Duration:</strong> 3 months | <strong>Status:</strong> Completed</p>
</div>

Built a reminder app to let medical workers know when it was safe to delete old files, in compliance with HIPAA laws for the State of Connecticut. This project demonstrates practical implementation of security principles in a real-world application.



---

## 🚨 HIPAA Checklist

<div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; margin:1rem 0; border-left:4px solid #28a745;">
  <p><strong>Tech Stack:</strong> Python, Django, JavaScript, React, JSON, HTML, CSS, Gunicorn, Axios, MUI, Emotion</p>
  <p><strong>Duration:</strong> 2 months | <strong>Status:</strong> In Development</p>
</div>

Developing a project for **Governance, Risk, and Compliance (GRC)**.

**Key Features:**
- **Secure Authentication**: JWT-based login, Django admin, and permissions.
- **Checklist Management**: Add, edit, and track compliance checklist items.
- **Real-Time Notes**: Edit notes for each item instantly in both React and Django.
- **Risk Dashboard**: Visual KPIs, alert banners, and drill-down for risk details.
- **Automated Monitoring & Alerts**: Management command for risk scanning, on-screen and email alerts for high/overdue risks.
- **Audit Logging**: All changes tracked for compliance and review.
- **Field-Level Encryption**: Sensitive data encrypted at rest.
- **Responsive Design**: Works seamlessly on mobile, tablet, and desktop.
- **Accessibility**: Keyboard navigation, ARIA labels, and tooltips for all interactive elements.
- **Comprehensive Documentation**: Risk analysis, BIA, scoring models, stakeholder approval, and user guides.

**Key Components:**
- **Django Backend**: User authentication; RESTful API; Encrypted model fields for sensitive data; Audit logging for all changes; Checklist item and regulation models; Management commands for automated risk monitoring and alerting.
- **Reach Frontend**: Secure login with JWT; Dashboard with checklist table; Real-time notes editing; Toggle completion status; KPI cards and risk alert banners; Drill-down dialogs for risk details; Responsible design for mobile, tablet, and desktop.
- **Django Templates**: Checklist form and item display for server-rendered pages; Notes editing and highlighting; Success/error messages and accessibility features.
- **Documentation**: Risk management docs; User/admin guides and changelogs; Markdown and Word files for executive/academic review.

---

## 🔍 API Security Scanner

<div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; margin:1rem 0; border-left:4px solid #dc3545;">
  <p><strong>Tech Stack:</strong> Go, REST APIs, JSON, Docker</p>
  <p><strong>Duration:</strong> 6 weeks | <strong>Status:</strong> Completed</p>
</div>

Created a specialized security scanner for **REST API endpoints** that identifies common vulnerabilities and misconfigurations in web applications.

**Scanning Capabilities:**
- 🔐 **Authentication Bypass**: Testing for auth vulnerabilities
- 💉 **Injection Attacks**: SQL, NoSQL, and command injection detection
- 🔓 **Authorization Flaws**: IDOR and privilege escalation checks
- 📝 **Input Validation**: Boundary testing and fuzzing
- 🛡️ **Security Headers**: Missing security controls identification

**Features:**
- Comprehensive reporting with remediation guidance
- Integration with CI/CD pipelines
- Custom rule engine for organization-specific checks
- Export results in multiple formats (JSON, PDF, HTML)

---

<div style="text-align:center; margin-top:3rem; padding:2rem; background:#f8f9fa; border-radius:8px;">
  <h3>Want to Learn More?</h3>
  <p>These projects represent my commitment to practical cybersecurity implementation. Each project includes detailed documentation, security considerations, and lessons learned.</p>
  <p><a href="/contact/" style="background:#007bff; color:white; padding:0.5rem 1rem; text-decoration:none; border-radius:4px;">Get in Touch</a></p>
  
  <div style="margin-top:2rem;">
    <img src="{{ '/assets/img/dae-logo.jpg' | relative_url }}" alt="DAE Logo" style="height:40px; opacity:0.7;">
  </div>
</div>
